# Marketing tools (from the open-source Instagram agent skill)

Copied from [postzen-dev/instagram-agent-skill](https://github.com/postzen-dev/instagram-agent-skill) (MIT licence, see `LICENSE`). Plain Python, no installs.

| Tool | Use |
| --- | --- |
| `hooks.json` | 26 hook formulas, each with a template, example, on-screen version, what it's best for and **its trap**. The hook writer (#23) starts from these. |
| `hookscore.py` | Scores opening lines on 5 checks (short enough to say in under 3 s, concrete, stakes, payload first, aimed at the viewer). `python3 team/tools/hookscore.py hooks.txt` (one per line) or `--hook "..."`. |
| `beats.py` | Times a script at speaking pace: `python3 team/tools/beats.py script.txt --target 35`. |
| `caption.py` | Lints a caption, including what shows before "… more" (first 125 characters): `python3 team/tools/caption.py caption.txt --keywords "saved reels,instagram saves"`. |

**How far to trust the hook score** (its author's own test): it separates real hooks from bad ones well, but barely tells a creator's hits from their misses. Use it as a floor that catches weak, slow or vague openings, never as a prediction of views. Real retention numbers in `stats/` always win.
