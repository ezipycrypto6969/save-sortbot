"""English text -> Kokoro phonemes using Misaki's pronunciation dictionaries (no espeak needed).
Unknown words raise UnknownWords so the script writer can rephrase them."""
import json, os, re, urllib.request

DATA = os.path.join(os.path.dirname(__file__), "..", "models")
BASE = "https://raw.githubusercontent.com/hexgrad/misaki/main/misaki/data/"


class UnknownWords(Exception):
    pass


def _lex():
    os.makedirs(DATA, exist_ok=True)
    out = {}
    for name in ("us_silver.json", "us_gold.json"):  # gold overrides silver
        p = os.path.join(DATA, name)
        if not os.path.exists(p):
            urllib.request.urlretrieve(BASE + name, p)
        out.update(json.load(open(p)))
    custom = os.path.join(DATA, "custom.json")  # brand names and slang; extend when a word is unknown
    if os.path.exists(custom):
        out.update(json.load(open(custom)))
    return out


LEX = None
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + num_words(n % 100))
    for div, word in ((10**9, "billion"), (10**6, "million"), (1000, "thousand")):
        if n >= div:
            return num_words(n // div) + " " + word + ("" if n % div == 0 else (" and " if n % div < 100 else " ") + num_words(n % div))


def normalise(text):
    t = text.replace("—", ", ").replace("–", " to ").replace("…", ".").replace("’", "'").replace("“", "").replace("”", "").replace('"', "")
    def money(m):
        whole, cents, k = m.group(2).replace(",", ""), m.group(3), m.group(4)
        words = num_words(whole) + (" thousand" if k else "") + " dollars"
        if cents and int(cents): words += " " + num_words(cents)
        return " " + words + " "
    t = re.sub(r"(A?\$)\s?(\d[\d,]*)(?:\.(\d\d))?(k\b)?", money, t)
    t = re.sub(r"(\d+)\s*%", lambda m: m.group(1) + " percent", t)
    t = re.sub(r"(\d+)k\b", lambda m: m.group(1) + " thousand", t, flags=re.I)
    t = re.sub(r"(\d+|dollars)\s*/(day|mo|month|week|yr|year)\b",lambda m: m.group(1) + " a " + {"mo": "month", "yr": "year"}.get(m.group(2), m.group(2)), t)
    t = re.sub(r"\d{1,3}(,\d{3})+", lambda m: m.group(0).replace(",", ""), t)
    t = re.sub(r"(\d+)\.(\d+)", lambda m: num_words(m.group(1)) + " point " + " ".join(ONES[int(c)] for c in m.group(2)), t)
    t = re.sub(r"\d+", lambda m: num_words(m.group(0)), t)
    t = t.replace("&", " and ").replace("+", " plus ").replace("/", " ").replace("-", " ")
    return re.sub(r"\s+", " ", t).strip()


def _word(w):
    cands = [w, w.lower(), w.capitalize()]
    for c in cands:
        if c in LEX:
            v = LEX[c]
            return v["DEFAULT"] if isinstance(v, dict) else v
    lw = w.lower()
    if lw.endswith("'s") and _word_opt(lw[:-2]): return _word_opt(lw[:-2]) + "z"
    if lw.endswith("s") and _word_opt(lw[:-1]):
        base = _word_opt(lw[:-1]); return base + ("s" if base[-1] in "ptkfθ" else "z")
    # simple morphology: -ed, -ing, -ly, -er on known stems
    def stems(s, cut):
        base = s[:-cut]
        return [base, base + "e", base[:-1] if len(base) > 2 and base[-1] == base[-2] else None, base[:-1] + "y" if base.endswith("i") else None]
    if lw.endswith("ed") and len(lw) > 4:
        for st in stems(lw, 2):
            p = st and _word_opt(st)
            if p:
                last = p.rstrip("ˈˌ")[-1]
                return p + ("ɪd" if last in "td" else "t" if last in "pkfsʃʧθ" else "d")
    if lw.endswith("ing") and len(lw) > 5:
        for st in stems(lw, 3):
            p = st and _word_opt(st)
            if p: return p + "ɪŋ"
    if lw.endswith("ly") and len(lw) > 4:
        p = _word_opt(lw[:-2]) or _word_opt(lw[:-3] + "le")
        if p: return p + "li"
    if w.isupper() and 1 < len(w) <= 5:  # acronym: spell letters
        parts = [_word_opt(ch) for ch in w]
        if all(parts): return "".join(p.replace("ˈ", "ˌ") for p in parts[:-1]) + parts[-1]
    return None


def _word_opt(w):
    try: return _word(w)
    except Exception: return None


def phonemize(text):
    global LEX
    if LEX is None: LEX = _lex()
    t = normalise(text)
    out, unknown = [], []
    for tok in re.findall(r"[A-Za-z']+|[,.!?;:]", t):
        if tok in ",.!?;:":
            if out: out[-1] += tok
            continue
        if tok.lower() == "a": out.append("ɐ"); continue
        p = _word(tok.strip("'"))
        if p is None: unknown.append(tok); continue
        out.append(p)
    if unknown: raise UnknownWords(", ".join(sorted(set(unknown))))
    s = " ".join(out)
    return s if s[-1] in ".!?" else s + "."


if __name__ == "__main__":
    import sys
    print(phonemize(" ".join(sys.argv[1:])))
