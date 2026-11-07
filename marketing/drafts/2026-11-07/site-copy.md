# Site copy fixes for savesortai.com (draft: the owner decides and makes the change)

Why: every reel says 156 saved / 30 worth doing / 65 need the video / 10 be careful / 22 gated guides (the real report screenshots). The main page says something else, and it promises Pro features that aren't launched. People who click through from a reel see numbers that don't match what they just heard. From D6 (Copy), D9 (Quality), D10 (Product marketing). Line numbers are for `site/public/index.html` as of 7 Nov.

## Numbers (owner rule: never more than 156; never numbers that differ from the screenshots)
- H1 (~line 323): "You saved 312 reels. Here are the 21 worth doing." → "156 saved reels. Only 30 worth doing. What's in yours?"
- Phone mock (~338) and JS flip text (~649–650): "312 posts" → "156 posts"; "21 worth doing" → "30 worth doing"; "312 saved · 0 opened" → "156 saved · 0 opened".
- Proof strip (~361–365): "156 reels saved in a year / 24 / 61 captions too vague / 7 hype" → "156 saved reels / 30 worth doing / 65 need the video / 10 be careful / 22 gated guides". ("in a year" isn't in the real data, so it comes out.)
- Check when done: searching the file for `312`, `>24<`, `>61<` and `>7<` finds nothing.

## Pro promises (Pro isn't launched)
- Lede (~324): "…flags the scams and hype, and turns the useful ones into step-by-step plans with the real tools, costs and catches." → "SaveSort reads your Instagram saves, sorts them by topic and flags which are worth doing, which need the video, which to be careful with and which hide the steps behind a comment. Free, in your browser, nothing uploaded."
- Feature "Step-by-step plans…" (~492) → remove, or retitle "Step-by-step plans (Pro, coming soon)".
- Feature "Gated guides, unlocked … We find the tool or method they're hinting at." → "Gated guides, flagged. 'Comment GUIDE for the doc' posts are marked, so you know before you comment."
- "Comment GUIDE" card: "SaveSort finds the tools and steps for you." → "SaveSort flags them as gated guides, so you know the steps aren't in the reel."
- How it works, Step 3: "Pro: a full breakdown for each useful reel, plus a fresh report every month." → delete.
- "Filter, search…": there is no search box in the code. Drop "search" or add one.
- **Owner decision:** the "Get Pro · A$1.99 a week" button links to a live Stripe checkout (~530, ~621). If Pro isn't ready, set `CONFIG.link` to `""` (the button then reads "Checkout opening shortly"). Prices elsewhere in the content are in USD (owner rule); decide whether the site should match.

## Other fixes
- Timing contradiction: "Three steps. About ten minutes, mostly waiting on Instagram." vs "usually within a few hours" → "Three steps. Most of it is waiting for Instagram's email."
- Sample report (`SAMPLE` array): it contains real handles and near-verbatim captions (D9 #85). Paraphrase them and remove the handles.
- Page `<title>`: "SaveSort" → "SaveSort: sort your saved Instagram reels by topic (free)" (D7 #62).

## Instagram bio (max 150 characters) and link
"Saved 156 reels. Only 30 worth doing. Sort yours free: by topic, worth doing or be careful. In your browser, nothing uploaded ↓"
Link: `savesortai.com/#try` (opens the drop zone and the "Load the sample report" button in one tap).
