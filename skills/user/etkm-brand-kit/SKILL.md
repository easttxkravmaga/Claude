---
name: etkm-brand-kit
version: 3.1
updated: 2026-03-29
description: >
  Use this skill whenever producing any visual output for ETKM — HTML pages, PDFs,
  presentations, forms, social media image briefs, React artifacts, SVGs, flyers,
  email templates, landing pages, or any design deliverable. Also trigger for Canva
  image briefs, branded documents, app UIs, visual aide tools, or any file where
  colors, typography, layout, or visual styling decisions are being made for ETKM.
  Trigger phrases: "make it on-brand", "ETKM brand", "brand colors", "brand kit",
  "visual style", "design for ETKM", "branded", "Swiss layout", "red accent",
  "black and white design". If the output will be seen by students, prospects, or
  the public and carries the ETKM name, use this skill. Non-negotiable for all
  final-revision and production-ready visual work.
---

# ETKM Brand Kit

**Version:** 3.1
**Last Updated:** 2026-03-29
**Changes from V3.0:** #FF0000 → #CC0000 sitewide. Added Section 8 (Cinematic Visual Doctrine core rules). Added changelog.

---

## 1. Color Palette (Non-Negotiable)

| Color | Hex | Role |
|-------|-----|------|
| Black | #000000 | Primary background, primary text |
| White | #FFFFFF | Primary background, primary text |
| Red | #CC0000 | Attention only — one element per view |
| Gray | #575757 | Supporting elements, secondary text |
| Lite Gray | #BBBBBB | Dividers, borders, subtle structure |

### Color Rules

- Backgrounds: Solid Black or Solid White only. Never gray backgrounds.
- Gradients: Prohibited. No exceptions.
- Contrast: White text on dark backgrounds. Black text on light backgrounds.
- No other colors exist in the ETKM system. If a design needs color
  beyond this palette, the design is wrong.

---

## 2. Red Usage (Attention Only)

Red is a weapon, not decoration. It draws the eye to exactly one thing.

- Use for: One word, one short phrase, one command, one warning, one decision point.
- Do NOT use for: Paragraphs, backgrounds, multiple elements, decorative bars, borders on multiple sides.
- Principle: When red appears, all other elements must be neutral (black, white, gray).
- Maximum: One red element per visual section. If you are tempted to add a second, remove the first or choose which matters more.

### Proven Red Applications

| Context | Red Usage |
|---------|-----------|
| PDFs and documents | Single attention phrase (e.g., "Train Hard.") |
| HTML pages and forms | CTA button background, single accent line |
| Email templates | Red top bar, red CTA button |
| Social media image briefs | One accent element per image |
| Curriculum sheets | Single red accent line below header |
| Visual aide tools | Available in palette but applied sparingly |

---

## 3. Typography System

### Primary Type Stack

| Role | Font | Weight |
|------|------|--------|
| Headlines (Title, H1, H2) | Montserrat | Light (300) through Black (900) — default Black 900 for maximum impact |
| Body Text (Paragraphs, H3, H4) | Inter | Regular or Medium |
| Form headlines and labels | Montserrat | Bold (700) or SemiBold (600) |
| Data labels, captions, small text | Inter | Medium, uppercase with letter-spacing |

### Typography Rules

- Never stretch, distort, or embellish typography.
- Uppercase with wide letter-spacing for labels and category headers.
- Headlines can be massive — Swiss International style embraces oversized type.
- Body text stays clean and readable. No decorative fonts anywhere.

### Web and App Fallbacks

Montserrat and Inter are both Google Fonts — load both via Google Fonts CDN in all HTML, React, and web deployments. No fallback needed for headlines; Montserrat is the universal standard across all deliverable types.
- Headlines: Montserrat (Google Fonts) — always available, no fallback required
- Body: Inter (Google Fonts)
- Never fall back to serif fonts or decorative alternatives

---

## 4. Visual Style and Geometry

### Layout Doctrine: Swiss International

- High contrast between elements
- Asymmetric grids — not centered, not symmetrical
- Aggressive use of negative space
- Massive typography as a design element, not just text
- Clean geometric shapes — no rounded corners unless functional (buttons)
- Hard edges, sharp lines, defined boundaries

### Layout Patterns (Proven in Production)

| Pattern | When to Use |
|---------|-------------|
| Bold Black Foundation | Default for high-impact pieces — black background, white type, red accent |
| Clean White Canvas | Documents, forms, instructional content — white background, black type |
| Split Screen | Before/after comparisons, two-concept layouts |
| Red Accent Block | Single red bar or block draws attention to one element |
| Minimalist Text-Only | Quotes, slogans, PEACE framework posts |
| Structured Grid | Multi-section content, dashboards, comparison tables |
| Asymmetric Bold | Hero sections, landing pages, cinematic image briefs |

### Specific Layout Standards

- PDF documents: Clean White Canvas base, black header bar, single red accent line
- HTML forms: Black/white/red palette, tile-style inputs, animated step transitions
- Email templates: Red top bar, black footer, Swiss grid, red CTA buttons
- Social image briefs: Black or white background only, one red accent per image, no gradients
- Curriculum sheets: All-white background, black font, black header bar, red accent line
- Visual aide tools: White workspace, brand palette in controls, transparent PNG export

---

## 5. Logo and Identity

- ETKM circle logo is the primary mark
- No star in the logo (removed per Nathan's direction)
- Logo can be embedded as base64 for self-contained HTML/PDF deployments
- Logo placement: top-left or centered in headers, never competing with content

---

## 6. Image and Photography Direction

For AI-generated image briefs and Canva designs:

- Cinematic, not stock photo
- Desaturated or monochromatic base with red as the single color accent
- Subjects positioned with intentional sightlines and spatial awareness
- Back-turned or profile subjects preferred over direct-to-camera poses
- Environmental storytelling — the setting communicates the message
- No martial arts action shots unless specifically requested
- The mood is quiet confidence, not aggression

---

## 7. What This Kit Prohibits

- Gradients of any kind
- Colors outside the 5-color palette
- Multiple red elements in a single view
- Rounded, playful, or whimsical design elements
- Stock photo aesthetic
- Centered-and-symmetrical layouts (Swiss style is asymmetric)
- Decorative fonts or script typography
- Drop shadows (unless subtle and functional in layered UI)
- Borders on all four sides of an element (use one or two sides maximum)

---

## 8. Cinematic Visual Doctrine — Core Rules

When creating AI image prompts, Canva image briefs, or any visual content direction for ETKM, these core rules apply. For the full cinematic doctrine (sightline zones, scene intent categories, platform presets, AR overlay details), load the etkm-cinematic-doctrine project instruction file.

**HUD Overlay:** Red (#CC0000) only. Reduced opacity (30-50%) or thin wireframe lines. Applied to behavioral anomalies in the scene — never to the subject themselves, neutral bystanders, or environmental elements that are not threats.

**Sightline Composition:** Primary sightline crosses at least 60% of the frame. Environmental elements do not block the primary sightline. If subject is seated, wall behind or corner advantage — never center-of-room with back exposed.

**Subject Positioning:** Subject is the observer, not the observed. Camera behind or beside the subject (3/4 rear or profile view). The viewer sees what the subject sees. Witness angle (face visible) is reserved for identity reveal moments only.

**Color in Scene:** B&W grayscale environment. Red HUD overlays are the only color. This matches the sitewide brand rule: black, white, gray, red (#CC0000) only.

**Tone:** Quiet confidence, not aggression. Preparedness, not paranoia. The subject reads the environment — they do not dominate it.

---

## CHANGELOG

- V3.1 — 2026-03-29 — #FF0000 → #CC0000 sitewide. Added Section 8 (Cinematic Visual Doctrine core rules absorbed from etkm-cinematic-doctrine). Added changelog.
- V3.0 — 2026-03-09 — Full restructure with Swiss layout system, image handling rules, and prohibited elements.
