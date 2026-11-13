# Sorty animation: cheaper, better, more viral (research, 13 Nov 2026)

We keep the whole Sorty idea (`content/sorty.md`, `content/animated.md`). This is how to make the same episodes for less money, at better quality, with Claude doing the work instead of clicking through websites.

## The short version
1. **Connect Artlist to Claude Code directly** (official Artlist MCP). It uses the credits we already pay for, with no browser clicking.
2. **Stop using Seedance 2.5 for every clip.** It's about 500 Artlist credits per second at 720p. Use it for one hero shot at most, and cheaper models for the rest.
3. **Edit in code, not CapCut** (Remotion plus its official Claude Code skills). Cuts, zooms, shakes, stamps, captions, SFX and beat-sync all happen automatically, for free.
4. **Make Sorty's voice and SFX separately** (ElevenLabs). The voice is identical every episode, and the clips don't pay for built-in voice.
5. **Design for sends.** That's what Instagram weights most for reaching new people.

Result: about **2,000–3,500 Artlist credits per episode instead of about 8,700**, edited by Claude.

## Episode 1 cost: now vs new way
| | Now | New way |
|---|---|---|
| Video clips | 3 × Seedance 2.5, 5 s, built-in voice = 7,500 | 1 hero Seedance 2.5 clip (3 s, about 1,500) + 2 clips on a cheaper model (about 175–600 each) |
| Still frames | ~9 × 130 = 1,170 | Same, about 1,170 |
| Voice | Built into the clips | ElevenLabs, one fixed Sorty voice |
| Edit | CapCut by hand | Remotion, rendered by Claude |
| **Total** | **about 8,700 credits** | **about 2,000–3,500 credits** |

Check the model picker before each run, because rates change.

## Cheaper (ranked by savings)
1. Cheaper video models for non-hero shots: in Artlist, Seedance 2.5 at 720p is about 500 credits a second, while cheaper models start at about 35–40 credits a second (MiniMax, Seedance 1.0 Fast at 480p).
2. Shorter clips: 3 s, not 5 s (shots are only 1.5–2 s on screen).
3. Draft at 480p or on Fast/Mini, and finish only the keeper at 720p. Budget for 2–3 tries per usable shot.
4. Stills plus code camera moves (push-in, shake, whip pan) instead of video wherever Sorty doesn't need to move.
5. Built-in voice off. Use ElevenLabs lines over reaction shots, and lip-sync only 1–2 talking close-ups.
6. Reuse the outro, sets and a Sorty reaction sheet across episodes.
7. Outside Artlist, if we outgrow it: Kling 3.0 is about US$0.08–0.17 a second at 720p and Seedance 2.0 Fast about US$0.24 a second via fal.ai and similar APIs.

## Better
- Lock Sorty's look with the same reference image and the same written description every time. Add "no cape" except for superhero specials.
- Sorty reaction sheet: 8–10 stills made once (happy, shocked, smug, sad, suspicious, screaming, sunglasses, sweatband) and reused as start frames.
- One ElevenLabs voice ID for Sorty. Built-in video-model audio often still sounds robotic.
- ElevenLabs sound effects (0.5–5 s) and music, all original.
- Remotion puts cuts on the music's beat map (episode 1 hits: 6.2, 13.6, 21.0, 28.4 and 36.0 s) and renders 1080×1920.

## Connectors and skills for Claude Code
| Tool | What it does | Cost | Official | Do it? |
|---|---|---|---|---|
| Artlist MCP `https://mcp.artlist.io/mcp` | Images and videos on our Artlist account, saved to the library, 100+ models | Existing credits. Charged when the request is sent, and it can't be cancelled | Yes (beta) | **First** |
| Remotion + Agent Skills (`npx remotion skills add`) | Build and render the edit in code | Free for individuals and small teams | Yes | **Second** |
| ElevenLabs MCP | Voice lines, SFX, music | Free tier, then paid | Yes | **Third** |
| fal.ai MCP `https://mcp.fal.ai/mcp` | 1,000+ models pay-per-use (cheapest Kling/Seedance) | Pay per generation | Yes | Later |
| Higgsfield MCP `https://mcp.higgsfield.ai/mcp` | Video, characters, voice | Separate plan from US$49/month. MCP always spends credits | Yes | Skip for now |

## Going viral
- Instagram's top signals are watch time, likes per reach and sends per reach, with sends counting more for non-followers (Mosseri). Every episode needs a "send this to the mate who…" moment.
- Mobile viewers decide in about 1.7 s, so the hook goes on frame one.
- Instagram rewards originality and punishes reposts. Our all-original episodes are on the right side of this.
- A recurring character drives growth: Duolingo's TikTok reportedly grew from about 50k to 10.7M on one character. A cartoon also avoids the "is it real?" backlash.
- Series beat one-offs, so judge results by the whole series.
- Risk: TikTok flags "unoriginal", mass-produced AI (generic voices, templates). Our defences are a consistent personality, a custom voice, real SaveSort proof and nothing copied.
- Use TikTok's AI-generated toggle plus our caption label. A label is disclosure, not a penalty.

## First 3 things to set up
1. Connect the Artlist MCP to Claude Code and test one Sorty still (130 credits).
2. Add a Remotion project at `episodes/` with the official skills, and build the episode template (beat map, cut list, stamps, captions, outro).
3. ElevenLabs free tier: design the Sorty voice once, save the voice ID in `content/sorty.md`, and make episode 1's lines and SFX.

Episode 1 target: under 3,500 credits and no manual editing.

## Sources
Artlist help center, Artlist MCP (Aug–Oct 2026) · cchound.com, Artlist credits test runs (7 Nov 2026) · Higgsfield MCP help and pricing (Oct 2026) · fal.ai Seedance 2.0/2.5 pricing and MCP docs · EvoLink and fal Kling 3.0 pricing (2026) · Remotion Agent Skills docs, Tella guide (Aug 2026) · ElevenLabs official MCP · Buffer, Sprout Social, eClincher on Mosseri's ranking signals (2025–26) · Fanpage Karma, AI vs human influencers (Oct 2026) · TIME on Granny Spills · Lab Marcel mascot lip-sync guide.
