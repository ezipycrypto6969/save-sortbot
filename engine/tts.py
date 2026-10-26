"""Kokoro-82M (ONNX) speech from phonemes. Model files come from the kokoro-onnx GitHub release (Apache-2.0)."""
import json, os, subprocess
import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
MODELS = os.path.join(ROOT, "models")
REL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
FILES = {"kokoro.onnx": "kokoro-v1.0.onnx", "voices.bin": "voices-v1.0.bin"}
SR = 24000

# Kokoro's phoneme vocabulary (from the model config; 114 symbols)
VOCAB = json.load(open(os.path.join(os.path.dirname(__file__), "vocab.json")))
_sess = None; _voices = None


def ensure_models():
    os.makedirs(MODELS, exist_ok=True)
    for local, remote in FILES.items():
        p = os.path.join(MODELS, local)
        if not os.path.exists(p) or os.path.getsize(p) < 1_000_000:
            subprocess.run(["curl", "-sSL", "--fail", "-o", p, REL + remote], check=True)


def _load():
    global _sess, _voices
    if _sess is None:
        import onnxruntime as ort
        ensure_models()
        _sess = ort.InferenceSession(os.path.join(MODELS, "kokoro.onnx"), providers=["CPUExecutionProvider"])
        _voices = np.load(os.path.join(MODELS, "voices.bin"))
    return _sess, _voices


def speak(phonemes, voice="af_heart", speed=1.1):
    sess, voices = _load()
    names = {i.name: i for i in sess.get_inputs()}
    tok_name = "input_ids" if "input_ids" in names else "tokens"
    toks = [VOCAB[c] for c in phonemes if c in VOCAB][:510]
    # a voice can be a blend, e.g. "am_onyx*0.6+am_puck*0.4"
    style = 0
    for part in voice.split("+"):
        name, _, w = part.partition("*")
        style = style + voices[name.strip()][len(toks) - 1] * (float(w) if w else 1.0)
    spd_int = "int" in names["speed"].type
    feeds = {tok_name: np.array([[0, *toks, 0]], dtype=np.int64),
             "style": np.asarray(style, dtype=np.float32).reshape(1, -1),
             "speed": np.array([int(round(speed)) if spd_int else speed], dtype=np.int32 if spd_int else np.float32)}
    audio = sess.run(None, feeds)[0].squeeze().astype(np.float32)
    idx = np.where(np.abs(audio) > 0.01)[0]
    if len(idx): audio = audio[max(0, idx[0] - 600): idx[-1] + 2400]
    return audio


def pitch(audio, semitones):
    """Shift pitch without changing speed (ffmpeg rubberband). Positive = higher, a bit cartoony."""
    if not semitones: return audio
    import subprocess
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-af", f"rubberband=pitch={2 ** (semitones / 12):.5f}", "-f", "f32le", "-"],
                       input=audio.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()
