"""Original synthesised music bed + sound effects, timed to a reel's cuts. No samples, no licensing issues."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000


def make(dur, cuts, hits, ticks, end_at, seed=7, root=55.0):
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
    for c in cuts[1:]: add(whoosh(), c - 0.4, 0.5)
    for h in hits: add(impact(), h, 0.9)
    for i, tt in enumerate(ticks): add(tick(1800 + 120 * (i % 8)) * 2, tt, 0.7)
    add(whoosh(1.0), end_at - 1.0, 0.45)
    add(impact(), end_at, 1.0); add(pluck(659.25, 1.2), end_at, 0.6); add(pluck(987.77, 1.2), end_at + 0.05, 0.5)
    mix = np.stack([L, R], 1)
    fade = int(0.35 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    mix = np.tanh(mix * 0.9)
    return mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
