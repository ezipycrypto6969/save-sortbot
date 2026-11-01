"""Per-platform text for the same reel. Each platform rewards different things:

- Instagram: sends (people DMing the reel to a friend) are the strongest reach signal for non-followers,
  so the caption ends with one easy "send this to..." line, unless the reel already asks for a comment.
- YouTube Shorts: viewers find Shorts through search and titles, so the description opens with a plain
  searchable line, then the link to the site, then the caption, with a few hashtags.
- TikTok: TikTok search reads captions, so the caption leads with the hook plus a keyword line, asks a
  question to pull comments, and keeps to 3-5 hashtags.

A queue item can override any of these with "ig_caption", "yt_description" or "tiktok_caption".
"""
import re

TAG_RE = re.compile(r"#[\w]+")


def _split(caption):
    """(body without trailing hashtag lines, list of hashtags in order)."""
    tags = TAG_RE.findall(caption)
    lines = caption.rstrip().split("\n")
    while lines and (not lines[-1].strip() or all(w.startswith("#") for w in lines[-1].split())):
        lines.pop()
    return "\n".join(lines).rstrip(), list(dict.fromkeys(tags))


def _asks_comment(text):
    return bool(re.search(r"\bcomment\b|\bguess\b|👇|\?\s*$", text, re.I))


def ig_caption(spec):
    if spec.get("ig_caption"): return spec["ig_caption"][:2200]
    body, tags = _split(spec["caption"])
    if not _asks_comment(body) and "send this" not in body.lower():
        body += "\n\nSend this to the friend with 500 saved reels 📩"
    return (body + ("\n\n" + " ".join(tags[:8]) if tags else ""))[:2200]


def yt_description(spec, site=""):
    if spec.get("yt_description"): d = spec["yt_description"]
    else:
        body, tags = _split(spec["caption"])
        body = re.sub(r"(l)ink in bio", lambda m: m.group(1) + ("ink below" if site else "ink on our channel"), body, flags=re.I)
        lead = "How to sort and actually use your Instagram saved reels, free with SaveSort."
        d = lead + (f"\nSort yours: {site}" if site else "") + "\n\n" + body
        d += "\n\n" + " ".join((["#Shorts"] + [t for t in tags if t.lower() != "#shorts"])[:4])
    return d.replace("<", "").replace(">", "")[:4900]


def tiktok_caption(spec):
    if spec.get("tiktok_caption"): return spec["tiktok_caption"][:2200]
    body, tags = _split(spec["caption"])
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    hook = paras[0] if paras else ""
    rest = paras[1] if len(paras) > 1 else ""
    text = hook + ("\n\n" + rest if rest and len(hook) + len(rest) < 400 else "")
    # TikTok bio links need a business account or 1,000 followers, so name the site instead
    text = re.sub(r"\blink in bio\b", "savesortai.com", text, flags=re.I)
    text += "\n\nHow to organise your Instagram saved reels, free at savesortai.com"
    if not _asks_comment(text): text += "\nHow many saved reels have you got? 👇"
    base = ["#savedreels", "#instagramtips", "#productivity"]
    hashtags = list(dict.fromkeys(base + tags))[:5]
    return (text + "\n\n" + " ".join(hashtags))[:2200]
