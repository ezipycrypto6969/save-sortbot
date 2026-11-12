---
name: SaveSort
description: Sorts your saved Instagram reels by topic, in your browser. White, lit, glass, orange to act.
colors:
  paper: "#FFFFFF"
  tint: "#F4F6FC"
  sunk: "#ECEFF8"
  ink: "#0D1233"
  muted: "#565C78"
  line: "#DADDE9"
  ember: "#FF6B1A"
  ember-hot: "#FF8A3D"
  ember-deep: "#F05A06"
  ember-text: "#C23D06"
  ember-soft: "#FFE8DA"
  sorty-blue: "#4C5CFF"
  sorty-blue-soft: "#ECEEFF"
  night: "#0B1030"
  night-2: "#141A45"
  night-muted: "#A9B0D6"
  do-it: "#0B7A53"
  watch-it: "#4C5CFF"
  skip-it: "#C2261C"
  locked: "#855600"
typography:
  display:
    fontFamily: "Bricolage Grotesque, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(40px, 6.2vw, 76px)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Bricolage Grotesque, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(30px, 4.2vw, 48px)"
    fontWeight: 700
    lineHeight: 1.04
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Bricolage Grotesque, ui-sans-serif, system-ui, sans-serif"
    fontSize: "21px"
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Figtree, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Figtree, ui-sans-serif, system-ui, sans-serif"
    fontSize: "12.5px"
    fontWeight: 750
    lineHeight: 1
    letterSpacing: "0.01em"
rounded:
  s: "10px"
  m: "16px"
  l: "26px"
  xl: "32px"
  pill: "999px"
spacing:
  gutter: "20px"
  container: "1160px"
  band: "clamp(64px, 9vw, 120px)"
components:
  button-primary:
    backgroundColor: "{colors.ember}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "15px 22px"
    height: "48px"
  button-ghost:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "15px 22px"
    height: "48px"
  label-do-it:
    backgroundColor: "{colors.do-it}"
    textColor: "{colors.paper}"
    rounded: "7px"
    padding: "5px 10px"
  label-watch-it:
    backgroundColor: "{colors.watch-it}"
    textColor: "{colors.paper}"
    rounded: "7px"
    padding: "5px 10px"
  label-skip-it:
    backgroundColor: "{colors.skip-it}"
    textColor: "{colors.paper}"
    rounded: "7px"
    padding: "5px 10px"
  label-locked:
    backgroundColor: "{colors.locked}"
    textColor: "{colors.paper}"
    rounded: "7px"
    padding: "5px 10px"
  chip-filter:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "8px 14px"
    height: "44px"
  chip-filter-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
  card-panel:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.xl}"
    padding: "clamp(24px, 3vw, 34px)"
---

# Design System: SaveSort

## Overview

**Creative North Star: "Sorted Under Glass"**

The visitor's Saved tab is a mess; SaveSort hands it back laid out clean on a lit glass desk. The page is white and calm. Warm orange light pools behind the content and on the one thing to press. Frosted-glass panels float a little above the page, and one tilted 3D shot of the sorted report sits in the hero as the product's proof. The light SaveSort blue, the colour of Sorty's head, shows up only as small glints: labels, links, icons, an underline.

Depth is **lifted, not loud**. Glass, glow and layered shadow go on the key objects (the hero product shot, the sorter, the pricing cards, the closing band). Reading areas (blog posts, legal pages, FAQ answers) stay plain white with dark ink so nothing gets in the way of the words. Motion is tasteful and always optional: things settle into place, Sorty bobs and blinks, numbers count up once. All of it switches off for reduced motion.

It should read like a funded software company's site: confident type, generous space, real product UI as the hero image, and no invented proof. The incumbent site (Nov 2026) is the starting point; this file records it and the owner's binding rules.

**Key Characteristics:**
- White page; orange (#FF6B1A family) is the only action colour.
- Sorty blue (#4C5CFF) in small parts only, never a full-bleed band.
- Glass and soft shadow on key objects; plain white for reading.
- One tilted product shot of the real sorted report in the hero.
- Responsive layout at 390, 768 and 1440 px. No device mockup pictures.
- Self-hosted fonts, no third-party requests.

## Colors

A white, lightly cool page, warmed by one ember orange, with a small cool blue accent and a deep navy for the rare dark panel.

### Primary
- **Ember Orange** (#FF6B1A, gradient from #FF8A3D to #F05A06): primary buttons, step numbers, the ticker strip, the closing band's light, focus of attention. Text on it is always Ink (6.4:1), never white (2.85:1 fails).
- **Ember Text** (#C23D06): orange when it has to be text on white, such as kickers and the headline accent gradient's darkest stop (5.3:1).
- **Ember Soft** (#FFE8DA): hover wash for the drop zone and upsell panel.

### Secondary
- **Sorty Blue** (#4C5CFF): the mascot's head, the logo ribbon, links, the headline underline, the Watch it label, small icons. 4.9:1 on white, so it's fine for text on Paper, but not for small text on Sorty Blue Soft (4.26:1).
- **Sorty Blue Soft** (#ECEEFF): selected topic row background.

### Tertiary
- **Night** (#0B1030) and **Night 2** (#141A45): the only dark surfaces: the Pro plan card, the privacy band, the end-of-post box. Lit from the corners with orange and blue light. Muted text on night is #A9B0D6 (8.7:1).

### Neutral
- **Paper** (#FFFFFF): page and panel background.
- **Tint** (#F4F6FC): inset boxes, the sorter band, path hints.
- **Sunk** (#ECEFF8): pressed or recessed surfaces, code.
- **Ink** (#0D1233): all body text and headings.
- **Muted Ink** (#565C78): secondary text (6.6:1 on white).
- **Hairline** (#DADDE9): dividers and borders when a border is needed at all.

### Label colours
- **Do it** #0B7A53, **Watch it** #4C5CFF, **Skip it** #C2261C, **Locked** #855600, each with white text (5.3 to 6.3:1). Label names are fixed by the owner.

### Named Rules
**The One Action Colour Rule.** Orange means "press this" or "look here first". Never use it for decoration that competes with the primary button in the same viewport.

**The Glint Rule.** Sorty Blue never fills a section or a large card. If a blue area is bigger than a label or a button, it's wrong.

**The Ink-on-Ember Rule.** Text on orange is Ink. White text sits only on Ember Text (#C23D06) or darker.

## Typography

**Display Font:** Bricolage Grotesque (fallback ui-sans-serif, system-ui), self-hosted variable 200–800.
**Body Font:** Figtree (fallback system-ui, Segoe UI), self-hosted variable 300–900, with italic.

**Character:** A slightly quirky grotesque for confident, tightly tracked headlines, paired with a friendly, clear sans for reading. Big and direct, never shouty.

### Hierarchy
- **Display** (700, clamp(40px, 6.2vw, 76px), 0.98): the hero headline only. The first line ("You saved 156 reels.") is a muted 500-weight lead-in at 0.58em.
- **Headline** (700, clamp(30px, 4.2vw, 48px), 1.04): section headings.
- **Title** (650, 21px, 1.2): card and step titles.
- **Body** (400, 17px, 1.55; prose 18.5px, 1.7, max 68ch): all reading text. Never below 16px for paragraphs on phones.
- **Label** (750, 12.5px, +0.01em): the four label tags. The smallest text on the site; 12px is the floor.

### Named Rules
**The Balanced Headline Rule.** Every heading uses `text-wrap: balance` and negative tracking; no orphaned single words at 390 px.

## Layout

A centred container of 1160px with 20px side gutters (safe-area aware). Sections are bands with clamp(64px, 9vw, 120px) vertical padding. The hero is a two-column grid (copy left, tilted product shot right) that stacks to one column under 940px, copy first. Grids collapse to one column at 760 to 900px. Every page is checked at 390, 768 and 1440 px: no sideways scroll, no overlap, tap targets at least 44px on phones.

The site is a responsive web layout. It never shows pictures of phones or laptops to imply responsiveness.

## Elevation & Depth

A hybrid of soft layered shadow, frosted glass and coloured light. Shadows are ambient (several soft layers, low opacity), not hard drop shadows. Glass (`backdrop-filter: blur`) sits only on things that float over something: the nav, the hero chips, ghost buttons, the privacy list. Behind the hero, a large warm orange bloom and a smaller blue one, plus a faint dot grid, give the "lit stage".

### Shadow Vocabulary
- **Depth** (`0 1px 1px rgba(13,18,51,.04), 0 8px 16px -8px rgba(13,18,51,.10), 0 30px 60px -24px rgba(13,18,51,.20)`): resting panels and cards.
- **Depth Hi** (`0 1px 1px rgba(13,18,51,.04), 0 18px 36px -14px rgba(13,18,51,.18), 0 60px 110px -40px rgba(232,80,10,.32)`): the hero product shot, the Pro card, hovered cards. The warm tail is the orange light.
- **Ember Glow** (`0 12px 26px -10px rgba(240,90,6,.75)` plus inner highlight): primary buttons only.

### Named Rules
**The Lifted Not Loud Rule.** Glass and glow on key objects only. Reading text sits on plain Paper.

**The One Tilt Rule.** Only the hero product shot is tilted in 3D. Everything else sits flat and level.

## Shapes

Generously rounded, soft corners: 10px on small insets, 16px on rows, 26 to 32px on panels and cards, full pills on every button, chip and the floating nav. Labels are small 7px-cornered tags with an icon. Borders are hairlines at low opacity; depth carries the structure, not outlines.

## Components

### Buttons
- **Shape:** full pill (999px), at least 48px tall, 44px minimum on phones (small nav button included).
- **Primary:** glossy Ember gradient (#FF8A3D → #FF6B1A → #F05A06), Ink text, 700 weight, inner top highlight, Ember Glow shadow. Hover lifts 2px and lightens.
- **Ghost:** frosted Paper glass, Ink text, faint ink border; hover darkens the border.
- **Light (on dark or orange panels):** white with Ember Text text.
- **Focus:** 3px Sorty Blue outline, 3px offset, on every interactive element.

### Labels (Do it / Watch it / Skip it / Locked)
- **Style:** solid label colour, white text, a small masked icon (tick, play, cross, lock), slight bottom shadow. In the hero board they tilt -2°.

### Chips and tabs
- **Style:** Paper pill, hairline border, Ink text, 650 weight.
- **Selected:** Ink fill, Paper text, small shadow. `aria-pressed` / `aria-selected` drive the state.

### Cards / Containers
- **Corner Style:** 32px.
- **Background:** Paper, or glass over the lit areas.
- **Shadow Strategy:** Depth at rest, Depth Hi on hover (blog cards also rise 4px).
- **Internal Padding:** clamp(22px, 3vw, 34px).

### Navigation
- A floating frosted-glass pill, sticky at the top, 62px tall, logo left, links in Muted Ink (Ink when current), orange primary button right. Under 860px the links fold into a menu button.

### Hero product shot (signature)
- The real sorted report as live HTML (not an image): "Saved, 156 reels, sorted", four lanes with label, count and example captions, footnote stating where the numbers come from. Tilted (rotateY -13°, rotateX 7°), follows the pointer slightly on desktop, flattens under 940px. Two glass stat chips float at different depths; Sorty peeks over the corner.

### Sorty
- The blue bookmark mascot (inline SVG). Bobs, waves and blinks; peeks over the hero shot; sits in the closing band and on About and 404.

## Do's and Don'ts

### Do:
- **Do** keep the page white and let orange carry every primary action.
- **Do** use Sorty Blue only for labels, links, icons and small glints.
- **Do** use only the real numbers: 156 saves, 30 Do it, 65 Watch it, 10 Skip it, 22 Locked.
- **Do** keep reading surfaces plain: Paper background, Ink text, 16px minimum.
- **Do** check every page at 390, 768 and 1440 px, and keep tap targets at 44px or more on phones.
- **Do** wrap every animation in a reduced-motion opt-out.

### Don't:
- **Don't** put white text on Ember Orange (#FF6B1A); it fails contrast.
- **Don't** fill sections with Sorty Blue or use blue as a second action colour.
- **Don't** add device-frame mockups, stock photos, fake logos, testimonials, ratings or user counts.
- **Don't** tilt anything except the hero product shot.
- **Don't** load fonts, scripts or images from another domain.
- **Don't** rename the page hooks the reel capture script uses (`#try`, `#drop`, `#file`, `#report`, `#r-stats .rstat`, `#r-topics .bar`, `.chip[data-l]`, `.nav`).
