# Sorty episodes (animated reels, edited in code)

Animated Sorty episodes are edited here with [Remotion](https://www.remotion.dev) instead of CapCut. The script is a JSON file, and the render is a finished 1080×1920 MP4 with every cut on the music's beat, camera moves, Sorty's lines as captions, stamps, sound effects, music and the end card.

Rules: `content/sorty.md` (character), `content/animated.md` (scriptwriter rules), `content/research/animation-2026-11.md` (costs and tools). Remotion is free for individuals and companies of up to 3 people.

## Make an episode
1. **Script:** copy `ep01.json` to `epNN.json`. Each shot has `start`/`end` (seconds), `camera` (`push`, `crash`, `shake`, `whip`, `pan`, `tilt`, `wobble`, `none`), `line` (Sorty's words; `*word*` = yellow highlight), `sfx`, and optional `card`, `stamp` (`do`, `watch`, `skip`, `locked`), `stampAt` and `big` (joke text). Put the biggest jokes on the music `hits`.
2. **Pictures:** put frames and clips in `public/epNN/` and set each shot's `src` (for example `"ep01/frames/06.png"` or `"ep01/clips/B.mp4"`). A shot with no `src` renders as a storyboard card, so the episode can be previewed before anything is paid for.
3. **Voice:** put Sorty's line for each shot at `public/epNN/voice/NN.mp3` and set `voice`. Without one, the captions still run.
4. **Music:** `public/epNN/music.mp3` (original or properly licensed only). It drops to `duck` volume under every line.
5. **Render:** `npm install` once, then `npm run render -- epNN` writes `out/epNN.mp4`. `npm run studio` opens a live preview.

## Paid parts (show the owner the frames before any clips)
- Frames: Artlist (Nano Banana, about 130 credits each, 9:16). Always pass both Sorty reference pictures (full body + face) and keep him exactly identical, mask and cape included (`content/sorty.md`).
- Clips: at most 3 per episode (`content/animated.md` rule 12). Use Seedance 2.5 for one 3 s hero shot at most, and a cheaper model for the rest.
- Sound effects are free and ours: `public/sfx/` is generated from `engine/music.py` by `python3 tools/sfx_pack.py`. Names are `<kind>-1..3.wav` (cut, stamp, hook, drop, tap, payoff, scroll, hit, irony, riser, end, mood-shocked, mood-sad, mood-smug, mood-suspicious).

## Claude Code skills
The official Remotion agent skills are in `.claude/skills/remotion-*` (installed with `npx skills add remotion-dev/skills`).

## Episode 1 v2 (`ep01b`): real motion
- `tools/build_ep01b.py` builds `ep01b.json` from a beat list; the timing follows the voice lines, so re-recording a line re-times the edit. It also writes our own music bed (`engine/music.py`).
- New shot fields: `from` (seconds into a clip), `tint` (`cool` problem / `warm` / `red` / `gold` win), `kind: "title"` (`text` + `sub`), `kind: "screen"` with `screen: {src, y0, y1}` (a real SaveSort screenshot scrolled inside a phone), `tag`, `cardLabel`.
- Top-level `voices` (captions are built from these, one word at a time, `*word*` = yellow), `sfxAt`, `musicMute` and `aiTag`.
- Clips: download the episode's videos from the Artlist folder "Sorty episodes" into `public/ep01b/clips/raw_a.mp4 … raw_h.mp4` (not in git; too big).
- Render: `node render.mjs ep01b`.
