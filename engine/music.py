"""Original synthesised music bed + sound effects, timed to a reel's cuts. No samples, no licensing issues."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000


def make(dur, cuts, hits, ticks, end_at, seed=7, root=55.0, mode="sfx", events=None):
    """mode: "full" = beat + bass + melody + effects; "sfx" = effects only (whooshes, hits, ticks); "none" = silence.
    events: optional [(t, kind)] so each moment gets a fitting, varied effect (see SFX_KINDS below)."""
    rng = np.random.default_rng(seed)
    N = int(SR * dur)
    L = np.zeros(N); R = np.zeros(N)

    def add(sig, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= N or i < 0: return
        j = min(N, i + len(sig)); s = sig[: j - i] * gain
        L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))

    def env(n, a=0.002, d=0.2):
        t = np.arange(n) / SR
        return np.minimum(1, t / a) * np.exp(-t / d)

    def kick():
        n = int(0.45 * SR); t = np.arange(n) / SR
        ph = 2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 28)) / SR
        return np.sin(ph) * env(n, 0.001, 0.16) * 1.1 + np.tanh(np.sin(ph) * 3) * env(n, 0.001, 0.04) * 0.25

    def hat(open_=False):
        n = int((0.18 if open_ else 0.05) * SR)
        return sosfilt(butter(4, 7000, 'hp', fs=SR, output='sos'), rng.standard_normal(n)) * env(n, 0.001, 0.06 if open_ else 0.015)

    def clap():
        n = int(0.25 * SR)
        x = sosfilt(butter(2, [900, 3500], 'bp', fs=SR, output='sos'), rng.standard_normal(n)); e = np.zeros(n)
        for k, off in enumerate([0, 0.011, 0.022]):
            i = int(off * SR); e[i:] += env(n - i, 0.001, 0.012 if k < 2 else 0.09)
        return x * e * 1.4

    def bass(f, length):
        n = int(length * SR); t = np.arange(n) / SR
        return np.tanh((np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t)) * 1.6) * env(n, 0.005, length * 0.6) * 0.55

    def whoosh(length=0.4):
        n = int(length * SR); x = rng.standard_normal(n); out = np.zeros(n)
        for b in range(0, n, 512):
            fc = 300 + 7000 * (b / n) ** 2
            out[b:b + 512] = sosfilt(butter(2, [max(80, fc * .6), min(SR / 2 - 100, fc * 1.4)], 'bp', fs=SR, output='sos'), x[b:b + 512])
        return out * np.linspace(0, 1, n) ** 2 * 0.9

    def impact():
        n = int(1.2 * SR); t = np.arange(n) / SR
        body = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t * 12)) / SR) * env(n, 0.001, 0.45)
        noise = sosfilt(butter(2, 2500, 'lp', fs=SR, output='sos'), rng.standard_normal(n)) * env(n, 0.001, 0.08)
        return np.tanh((body * 1.3 + noise * 0.6) * 1.5) * 0.9

    def tick(f=2600):
        n = int(0.04 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * f * t) * env(n, 0.0005, 0.008) * 0.5

    def pluck(f, length=0.5):
        n = int(length * SR); t = np.arange(n) / SR
        return sum(np.sin(2 * np.pi * f * h * t) / h for h in (1, 2, 3, 4)) * env(n, 0.003, 0.18) * 0.25

    beat = 0.5
    if mode == "full":
        first_cut = cuts[1] if len(cuts) > 1 else 2.0
        for k in range(int(dur / beat) + 1):
            tb = k * beat
            if end_at - 0.3 <= tb < end_at: continue
            if tb < first_cut:
                if k % 2 == 0: add(kick(), tb, 0.8)
            else:
                add(kick(), tb, 1.0)
                if k % 2 == 1: add(clap(), tb, 0.5, 0.05)
                if k % 4 == 3: add(hat(True), tb + beat / 2, 0.22, 0.4)
            add(hat(), tb + beat / 2, 0.32, -0.3)
        notes = [root, root * 1.189, root * 0.891, root, root * 1.335, root * 1.189]
        for b in range(int(dur / 2) + 1):
            tb = b * 2.0
            if tb < first_cut - 0.01: continue
            for q in range(4):
                add(bass(notes[b % len(notes)], beat * 0.9), tb + q * beat, 0.85 if q == 0 else 0.55)
        scale = [440, 523.25, 587.33, 659.25, 783.99]
        k = 0; tb = first_cut
        while tb < end_at - 0.3:
            add(pluck(scale[(k * 3) % 5]), tb, 0.45 if k % 2 == 0 else 0.25, 0.25 if k % 2 else -0.25); k += 1; tb += beat / 2
    if mode == "none":
        return np.zeros((N, 2))
    if events is None:
        for c in cuts[1:]: add(whoosh(), c - 0.4, 0.5)
        for h in hits: add(impact(), h, 0.9)
        for i, tt in enumerate(ticks): add(tick(1800 + 120 * (i % 8)) * 2, tt, 0.7)
        add(whoosh(1.0), end_at - 1.0, 0.45)
        add(impact(), end_at, 1.0); add(pluck(659.25, 1.2), end_at, 0.6); add(pluck(987.77, 1.2), end_at + 0.05, 0.5)
    else:
        lib = _library(rng, env, whoosh, impact, tick, pluck)
        last = {}
        def pick(kind):
            opts = lib[kind]
            if len(opts) == 1: return opts[0]
            choices = [k for k in range(len(opts)) if k != last.get(kind)]
            k = int(rng.choice(choices)); last[kind] = k
            return opts[k]
        for c in cuts[1:]:
            fn, lead, g = pick("cut"); add(fn(), c - lead, g, float(rng.uniform(-0.3, 0.3)))
        for tt, kind in events:
            if kind not in lib: kind = "hit"
            fn, lead, g = pick(kind); add(fn(), tt - lead, g, float(rng.uniform(-0.15, 0.15)))
        for i, tt in enumerate(ticks): add(tick(1800 + 120 * (i % 8)) * 2, tt, 0.6)
        fn, lead, g = pick("riser"); add(fn(), end_at - lead, g)
        fn, lead, g = pick("end"); add(fn(), end_at, g)
    mix = np.stack([L, R], 1)
    fade = int(0.35 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    mix = np.tanh(mix * 0.9)
    return mix / (np.max(np.abs(mix)) + 1e-9) * (0.89 if mode == "full" else 0.6)  # effects sit quieter under the voice


def _library(rng, env, whoosh, impact, tick, pluck):
    """Synthesised effects grouped by moment. Each entry: (make_fn, seconds_before_the_moment, gain)."""
    def n_(sec): return int(sec * SR)
    def t_(sec): return np.arange(n_(sec)) / SR
    def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], 'bp', fs=SR, output='sos'), x)
    def lp(x, f): return sosfilt(butter(2, f, 'lp', fs=SR, output='sos'), x)
    def hp(x, f): return sosfilt(butter(2, f, 'hp', fs=SR, output='sos'), x)
    def sweep(f0, f1, sec, curve=1.0):
        t = t_(sec); f = f0 + (f1 - f0) * (t / sec) ** curve
        return np.sin(2 * np.pi * np.cumsum(f) / SR)
    def saw(f, sec):
        t = t_(sec); ph = np.cumsum(np.broadcast_to(f, t.shape)) / SR
        return 2 * (ph % 1) - 1

    # --- transitions between scenes ---
    def swish_down(sec=0.35):
        n = n_(sec); x = rng.standard_normal(n); out = np.zeros(n)
        for b in range(0, n, 512):
            fc = 6000 - 5200 * (b / n) ** 0.7
            out[b:b + 512] = bp(x[b:b + 512], max(100, fc * .6), min(SR / 2 - 100, fc * 1.4))
        return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5 * 0.9
    def swipe(): return hp(rng.standard_normal(n_(0.16)), 2500) * np.sin(np.pi * np.linspace(0, 1, n_(0.16))) * 0.7
    def zipper():
        n = n_(0.28); x = bp(rng.standard_normal(n), 1500, 6000)
        am = (np.sin(2 * np.pi * np.cumsum(np.linspace(40, 110, n)) / SR) > 0.2).astype(float)
        return x * am * np.linspace(0.3, 1, n) * 0.8
    def pageflip():
        n = n_(0.22); x = bp(rng.standard_normal(n), 800, 5000)
        return x * (env(n, 0.002, 0.03) + 0.6 * np.roll(env(n, 0.002, 0.05), n_(0.07))) * 0.8
    def reverse_swell():
        n = n_(0.5); x = lp(rng.standard_normal(n), 5000)
        return x * np.linspace(0, 1, n) ** 3 * 0.9
    def pop_cut():
        return sweep(250, 900, 0.08) * env(n_(0.08), 0.001, 0.03) * 0.6

    # --- moments ---
    def stamp():
        n = n_(0.5); t = t_(0.5)
        thud = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-t * 40)) / SR) * env(n, 0.001, 0.09)
        slap = bp(rng.standard_normal(n), 400, 3000) * env(n, 0.0005, 0.025)
        return np.tanh((thud * 1.4 + slap * 1.2) * 1.3) * 0.9
    def gavel():
        n = n_(0.4); t = t_(0.4)
        knock = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((420, 1), (1130, .5), (2150, .25))) * env(n, 0.0005, 0.05)
        return np.tanh(knock * 2) * 0.8 + stamp()[:n] * 0.5
    def buzzer():
        x = np.sign(np.sin(2 * np.pi * 110 * t_(0.45))) * 0.5 + np.sign(np.sin(2 * np.pi * 116 * t_(0.45))) * 0.5
        return lp(x, 1800) * env(n_(0.45), 0.005, 0.5) * 0.45
    def bass_drop():
        return np.tanh(sweep(140, 32, 0.9, 0.5) * 2) * env(n_(0.9), 0.002, 0.5) * 0.9
    def plop():
        b = sweep(300, 1100, 0.12, 0.6) * env(n_(0.12), 0.001, 0.05)
        return np.concatenate([b, np.zeros(n_(0.05))]) * 0.8
    def bubble(): return sweep(500, 1600, 0.07) * env(n_(0.07), 0.001, 0.025) * 0.6
    def click(): return hp(rng.standard_normal(n_(0.02)), 3000) * env(n_(0.02), 0.0003, 0.004) * 1.2
    def tock(): return np.sin(2 * np.pi * 950 * t_(0.08)) * env(n_(0.08), 0.0005, 0.018) * 0.8
    def bell(f=1320, sec=1.0):
        t = t_(sec); n = n_(sec)
        return sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t * d) for r, a, d in ((1, 1, 3), (2.76, .4, 6), (5.4, .2, 10))) * np.minimum(1, t / 0.001) * 0.45
    def chime_up():
        out = np.zeros(n_(1.1))
        for k, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
            p = pluck(f, 0.7); i = n_(0.07 * k); out[i:i + len(p)] += p[: len(out) - i] * 1.6
        return out
    def register():
        cha = bp(rng.standard_normal(n_(0.18)), 2000, 8000) * env(n_(0.18), 0.002, 0.05) * 0.6
        b = bell(2093, 0.9); b[:len(cha)] += cha
        return b
    def boing():
        t = t_(0.7); f = 180 + 120 * np.exp(-t * 4) * np.sin(2 * np.pi * 14 * t)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n_(0.7), 0.003, 0.3) * 0.6
    def scratch():
        t = t_(0.35); f = 900 + 700 * np.sin(2 * np.pi * 3 * t)
        x = bp(rng.standard_normal(n_(0.35)), 300, 4000) * (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR / 10))
        return x * np.sin(np.pi * np.linspace(0, 1, n_(0.35))) * 0.8
    def sad_trombone():
        out = []
        for f, sec in ((392, .28), (370, .28), (349, .28), (330, .8)):
            t = t_(sec); vib = 1 + (0.02 * np.sin(2 * np.pi * 6 * t) if sec > .5 else 0)
            out.append(lp(saw(f / 2 * vib, sec), 1400) * env(n_(sec), 0.02, sec * 0.7))
        return np.concatenate(out) * 0.35
    def hmm():
        t = t_(0.6); f = 150 * (1 + 0.15 * t)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t)) * env(n_(0.6), 0.03, 0.4) * 0.5
    def sparkle():
        out = np.zeros(n_(0.6))
        for k in range(6):
            p = bell(float(rng.choice([2093, 2349, 2637, 3136])), 0.4) * 0.5; i = n_(0.05 * k); out[i:i + len(p)] += p[: len(out) - i]
        return out
    def flick_run():  # thumb flicking through reels
        out = np.zeros(n_(0.9))
        for k in range(5):
            s_ = swipe() * (0.9 - k * 0.12); i = n_(0.17 * k); out[i:i + len(s_)] += s_[: len(out) - i]
        return out
    def riser(sec=1.0):
        return (sweep(200, 1400, sec, 2) * 0.3 + lp(rng.standard_normal(n_(sec)), 6000) * 0.5) * np.linspace(0, 1, n_(sec)) ** 2 * 0.8
    def end_chord(freqs):
        def f():
            out = impact() * 0.8; 
            for k, fr in enumerate(freqs):
                p = pluck(fr, 1.2); i = n_(0.04 * k); out[i:i + len(p)] += p[: len(out) - i] * 2
            return out
        return f

    return {
        "cut": [(whoosh, 0.4, 0.5), (swish_down, 0.3, 0.5), (swipe, 0.12, 0.6), (zipper, 0.25, 0.4),
                (pageflip, 0.1, 0.55), (reverse_swell, 0.5, 0.4), (pop_cut, 0.03, 0.5)],
        "stamp": [(stamp, 0, 1.0), (gavel, 0, 0.9), (buzzer, 0, 0.8)],
        "hook": [(bass_drop, 0, 0.9), (impact, 0, 0.9)],
        "count": [(impact, 0, 0.85), (bass_drop, 0, 0.8), (gavel, 0, 0.7)],
        "drop": [(plop, 0, 0.9), (bubble, 0, 0.9)],
        "tap": [(click, 0, 0.9), (tock, 0, 0.7), (bubble, 0, 0.5)],
        "item": [(tock, 0, 0.6), (click, 0, 0.7), (pop_cut, 0, 0.5)],
        "payoff": [(chime_up, 0, 0.7), (register, 0, 0.7), (sparkle, 0, 0.6)],
        "statend": [(bell, 0, 0.6), (register, 0, 0.6)],
        "mood:shocked": [(boing, 0, 0.55), (scratch, 0, 0.5)],
        "mood:sad": [(sad_trombone, 0, 0.55)],
        "mood:smug": [(bell, 0, 0.4), (sparkle, 0, 0.45)],
        "mood:suspicious": [(hmm, 0, 0.55)],
        "scroll": [(flick_run, 0, 0.6)],
        "hit": [(impact, 0, 0.9), (stamp, 0, 0.8)],
        "riser": [(lambda: whoosh(1.0), 1.0, 0.45), (riser, 1.0, 0.45)],
        "end": [(end_chord((659.25, 987.77)), 0, 1.0), (end_chord((523.25, 659.25, 783.99)), 0, 1.0),
                (end_chord((587.33, 739.99, 880.0)), 0, 1.0)],
    }
