---
name: etkm-html-standards
version: 1.0
locked: 2026-03-25
description: >
  The production standard for ALL ETKM web-facing HTML output. Load this skill
  whenever building any HTML file that carries the ETKM name — journey maps,
  landing pages, etxkravmaga.com pages, etkmstudent.com pages, student guides,
  instructor guides, event pages, WordPress blocks, or any HTML deliverable.
  This skill defines fonts, colors, image/video treatment, component patterns,
  and the QC chain. Always load alongside etkm-brand-kit. Always run
  etkm-deliverable-qc before present_files.
trigger: >
  Trigger phrases: "build an HTML page", "build a landing page", "create a web page",
  "WordPress block", "HTML for the site", "student guide HTML", "instructor guide",
  "event page", "journey map", "build an ETKM page", "HTML template",
  "update the site", "add a page", or any request to produce an HTML file for ETKM.
companion_skills:
  always_load:
    - etkm-brand-kit     # Visual identity reference — load first
    - etkm-deliverable-qc # QC gate — run before every delivery
  template:
    - etkm-html-master-template.html  # The bones — start every project from this file
---

# ETKM HTML Standards
## Every ETKM HTML page starts from the same bones. These bones never change.

---

## The Production Chain

```
1. Load etkm-brand-kit          ← visual identity
2. Load etkm-html-standards     ← this skill
3. Open etkm-html-master-template.html  ← start here, not from scratch
4. Build                        ← replace placeholder content, delete unused components
5. Run etkm-deliverable-qc      ← Gate 4 (brand) + Gate 6 (functional) minimum
6. present_files                ← only after QC passes
```

Never start an ETKM HTML file from a blank page. The template already has the
correct fonts, variables, reset, and base components. Starting from scratch
is how fonts end up wrong and backgrounds end up white.

---

## Rule 1 — Black Background. Always.

```css
body {
  background: #000000;  /* LOCKED. Never change. */
  color: #FFFFFF;
}
```

- Body is `#000000` — always
- Surface cards, panels, elevated elements — `#111111`
- Hover states — `#161616`
- Borders — `#222222` structural, `#2a2a2a` subtle
- **There is no white background variant for HTML deliverables.**
- If a designer or requester asks for a light version — the answer is no.
  Light backgrounds exist only in PDFs and DOCX. Never HTML.

---

## Rule 2 — Fonts. Always Both. Always Google Fonts.

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

| Role | Font | Weight |
|------|------|--------|
| Display / Hero headline | Montserrat | 900 Black |
| H1 | Montserrat | 900 Black |
| H2 | Montserrat | 900 Black |
| H3 | Montserrat | 700 Bold |
| Kicker / label | Montserrat | 700 Bold, uppercase, letter-spacing |
| Body copy | Inter | 400 Regular |
| Supporting body | Inter | 500 Medium |
| Captions, data | Inter | 500 Medium, uppercase, letter-spacing |

**Never** use system fonts, Arial, Helvetica, or any substitute on HTML deliverables.
**Never** load fonts from any source other than Google Fonts CDN.
The `@import` must be in `<head>` — not inline, not deferred.

---

## Rule 3 — Red. One element per section. Never decorative.

- Hex: `#CC0000`
- Use for: CTA buttons, kicker labels, one headline word, one accent rule, one phase dot
- Maximum: one red element per visible section
- Red is never used for: full backgrounds, multiple elements, borders on all four sides, decorative patterns
- When red appears, everything else must be neutral (black, white, gray)

---

## Rule 4 — Images. Always B&W. Red accent as overlay.

### The CSS rule — apply to every image

```css
.img-bw {
  filter: grayscale(100%);
}
```

This is the single CSS declaration that enforces B&W across all images.
Apply it as a class on every `<img>` tag. Never bake grayscale into the
source file — CSS filter is applied at render time, keeping assets flexible.

### Image sizes by usage

| Usage | Aspect Ratio | Min Source Width | CSS class |
|-------|-------------|-----------------|-----------|
| Full-width hero | 16:9 or 21:9 | 1440px | `.hero-image` |
| Half-split | 3:2 | 800px | `.split-img-side img` |
| Thumbnail grid | 16:9 | 600px | `.thumb-item img` |
| Inline / editorial | 4:3 or 3:2 | 400px | `.img-bw` |
| Card image | 16:9 | 600px | `.card-image img` |
| Background section | 16:9 or wider | 1600px | `.bg-image-section` |
| Email header | 600×280px fixed | 600px | n/a |

### Dark overlay — required when text sits over an image

```css
/* Standard dark overlay — use on all hero and bg images with text */
.hero-image::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.58);
  z-index: 1;
}
```

- Light subject, dark bg: `rgba(0,0,0,0.45)` — lighter overlay
- Dark subject, busy bg: `rgba(0,0,0,0.65)` — heavier overlay
- Default when unsure: `rgba(0,0,0,0.55)`

### Red accent options — three approaches (use one per image, never combined)

**Option A — Red left stripe** (most common, matches section dividers)
```css
.img-stripe::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4px;
  background: #CC0000;
  z-index: 1;
}
```

**Option B — Red tint overlay** (cinematic, subtle)
```css
.hero-image-red::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(204,0,0,0.12);
  z-index: 2;
}
```

**Option C — Red text foreground** (headline in red over dark image)
```html
<h1 class="t-display">Train Hard.<br><span class="t-red">Go Home Safe.</span></h1>
```

### Image source for ETKM
- Primary: etxkravmaga.com WordPress media library
- All training photos, group shots, Nathan on the mat — all appropriate
- Apply B&W at render time via CSS — no need to pre-process assets
- No stock photography. No posed non-ETKM imagery.

---

## Rule 5 — Videos. Always B&W. Always youtube-nocookie.com.

### YouTube embed — responsive 16:9

```html
<div class="video-embed">
  <iframe
    src="https://www.youtube-nocookie.com/embed/VIDEO_ID?rel=0&modestbranding=1"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>
```

```css
.video-embed {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;   /* 16:9 ratio */
  height: 0;
  overflow: hidden;
  filter: grayscale(100%);  /* B&W */
}

.video-embed iframe {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}
```

**Always use `youtube-nocookie.com`** — not `youtube.com`. Reduces tracking.
**Always include `?rel=0`** — prevents related video suggestions from other channels.
**Always include `&modestbranding=1`** — reduces YouTube branding in player.

### Video source for ETKM
- Primary channel: youtube.com/@easttxkravmaga
- Get VIDEO_ID from the URL: `youtube.com/watch?v=VIDEO_ID`
- YouTube thumbnail URL pattern: `https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg`

### Background video — autoplay, muted, B&W

```html
<div class="hero-video-wrap">
  <video autoplay muted loop playsinline>
    <source src="training-footage.mp4" type="video/mp4">
  </video>
  <div class="hero-video-content">
    <!-- content here, above the video layer -->
  </div>
</div>
```

```css
.hero-video-wrap video {
  filter: grayscale(100%);  /* B&W */
  position: absolute;
  inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}
```

- `autoplay muted loop playsinline` — all four attributes required for mobile
- YouTube videos **cannot** be used as background video — embed only
- Use actual `.mp4` files for background video

### Video thumbnail with play button

```html
<div class="video-thumb" data-src="https://www.youtube.com/watch?v=VIDEO_ID">
  <img src="https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg"
       alt="Description" class="img-bw">
  <div class="video-play">▶</div>
</div>
```

- Thumbnail is pulled directly from YouTube (`maxresdefault.jpg`)
- B&W via `.img-bw` class on the `<img>` tag
- Red play button is the sole red accent on the component
- Click opens YouTube link in new tab (see JS in template)

---

## Component Library — Quick Reference

All components are in `etkm-html-master-template.html`. Copy the block, swap content.

| Component | CSS Class | When to Use |
|-----------|-----------|-------------|
| Hero text only | `.hero-text` | No imagery available or pure text-focus pages |
| Hero background image | `.hero-image` | Primary landing pages, section headers |
| Hero background video | `.hero-video-wrap` | High-impact home pages, event pages |
| Split image/content | `.split-image` | About sections, feature callouts |
| Background image section | `.bg-image-section` | Mid-page atmosphere blocks |
| Thumbnail grid 3-up | `.thumb-grid` | Gallery, class photos, technique shots |
| Thumbnail grid 4-up | `.thumb-grid-4` | Larger galleries |
| YouTube embed | `.video-embed` | Tutorial videos, technique breakdowns |
| Video thumbnails | `.video-thumb` | Video library pages, resource pages |
| Dark concept panel | `.panel-dark` | Key principle, most important idea on page |
| Quote block | `.quote-block` | Expert citations, Nathan quotes |
| Pull quote | `.pull-quote` | Large display quote, mid-content emphasis |
| Stat callout | `.stat-block` | Data points, quick facts |
| Three-box row | `.three-box` | Comparison, before/after, three pillars |
| Item list | `.item-list` | Numbered steps, curriculum points |
| Full-width accent strip | `.accent-strip` | Chapter breaks, section transitions |
| Primary CTA button | `.btn-primary` | Main action — red filled |
| Secondary button | `.btn-secondary` | Alternative action — outline |
| PDF download button | `.btn-pdf` | PDF download — red filled, ↓ prefix |
| Text link | `.link-arrow` | Inline links, navigation |
| Card | `.card` | Resource links, article previews |
| Contact form | `.form-input` | All form fields |
| Navigation | `.nav` | Top nav — sticky |
| Footer | `.footer` | Every page |

---

## Page Shell Options

Three layouts are pre-built in the template:

**Full-page (Journey Map / Landing Page)**
- No max-width constraint on hero
- `container` class (max-width: 1200px) for content sections
- Suited for: journey maps, landing pages, event pages

**Content page (Guides / Articles)**
- `container` + `container-narrow` alternating
- `container-narrow` max-width 760px for long-form reading
- Suited for: student guides, instructor guides, blog posts, curriculum pages

**Narrow-column (Focused reading)**
- `container-narrow` throughout (max-width: 760px)
- Maximum reading comfort for text-heavy content
- Suited for: individual articles, reference pages, policy pages

---

## WordPress Deployment

When deploying to etxkravmaga.com or etkmstudent.com:

1. Copy the HTML content between `<body>` and `</body>`
2. Include the Google Fonts `<link>` tag in the page `<head>` (or add via WordPress Customizer → Additional CSS if fonts already loaded site-wide)
3. Paste CSS into a `<style>` block within the WordPress block, or add to the child theme's stylesheet
4. Use a **Raw HTML block** in the WordPress editor — never Gutenberg blocks
5. Test on mobile before marking complete

**The CSS variables must be present.** If deploying to a page that already
has the ETKM master CSS loaded site-wide, the variables don't need to be
repeated — just reference them. If deploying standalone, include the full
`:root {}` block.

---

## QC Checklist — Run Before Every Delivery

Minimum checks for all HTML deliverables (reference `etkm-deliverable-qc` Gate 4 and Gate 6 for full detail):

- [ ] Body background is `#000000` — not white, not gray, not any other color
- [ ] Google Fonts CDN `<link>` is in `<head>` and loading
- [ ] All headlines render in Montserrat (thick, rounded strokes) — not system sans-serif
- [ ] All body text renders in Inter — not system sans-serif
- [ ] Every image has `filter: grayscale(100%)` applied via `.img-bw` or container filter
- [ ] No image is in full color (unless an intentional red-accent-only exception, approved)
- [ ] No video embeds use `youtube.com` — must be `youtube-nocookie.com`
- [ ] Red appears no more than once per visible section
- [ ] All CTA buttons use `.btn-primary` (red) or `.btn-secondary` (outline) — no custom colors
- [ ] Page renders correctly on mobile (375px width minimum)
- [ ] All links have correct URLs (etxkravmaga.com not easttxkravmaga.com)
- [ ] Phone number correct where present: 903-590-0085
- [ ] No placeholder text, [INSERT], or template variables visible

---

## What This Skill Prohibits

- White or gray backgrounds on any ETKM HTML deliverable
- Fonts other than Montserrat and Inter
- Colored images (full color or partial color without red accent treatment)
- YouTube embeds via `youtube.com` (must use `youtube-nocookie.com`)
- Multiple red elements in a single section
- Gradients
- Rounded corners except on buttons
- Centered-symmetrical layouts (Swiss = asymmetric)
- Starting from a blank file instead of the master template

---

*Version 1.0 — Locked 2026-03-25*
*Covers: bones, fonts, colors, image/video standards, component library, page shells, WordPress deployment, QC*
*Maintained by: Nathan Lundstrom / East Texas Krav Maga*
