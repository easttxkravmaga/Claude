---
name: etkm-web-production
version: 1.0
updated: 2026-04-24
description: >
  Load this skill for ANY HTML/CSS production task for ETKM.
  Triggers: building WordPress page sections, landing pages, email
  templates, lead magnet PDFs, HFCM injections, site header/footer,
  form builds, or any HTML/CSS code that will be installed on the
  ETKM site or sent to students. This is the governing standard.
  Do NOT write ETKM HTML/CSS without this skill loaded.
  Companion files: CSS-SYSTEM.md (tokens), COMPONENT-LIBRARY.md
  (components), OUTPUT-STANDARDS.md (per-type rules).
---

# ETKM Web Production — Governing Build Protocol

**Version:** 1.0
**Last Updated:** 2026-04-24

---

## SECTION 1 — BEFORE WRITING A SINGLE LINE OF CODE

### Step 1 — Classify the output type

```
What am I building?
│
├── Code injected into WordPress via HFCM or Additional CSS
│   → OUTPUT TYPE: WordPress Page Section
│
├── A full standalone conversion page
│   → OUTPUT TYPE: Landing Page
│
├── HTML email for Pipedrive sequences or broadcast
│   → OUTPUT TYPE: Email Template
│   CRITICAL: Email CSS rules CONTRADICT web CSS rules.
│   Never mix the two.
│
└── PDF rendered via HTML → Playwright
    → OUTPUT TYPE: Lead Magnet PDF
    CRITICAL: PDF CSS differs from web CSS.
```

### Step 2 — Map components before writing code

Name every component from COMPONENT-LIBRARY.md the page needs.
Build the component list first. Never start with code.

### Step 3 — Load the token system

Every CSS value comes from CSS-SYSTEM.md.
Never write raw hex, arbitrary px, or hardcoded color.

### Step 4 — Write structure before style

HTML skeleton first. Semantic elements. Correct headings. ARIA.
Verify structure before writing any CSS.

### Step 5 — Write CSS mobile-first

Base styles = mobile. min-width queries add desktop behavior.
Single → multi-column at 768px minimum.

### Step 6 — Run QC before handoff

Every output runs Section 5 QC checklist before delivery.

---

## SECTION 2 — HTML PRODUCTION STANDARDS

### 2.1 WordPress Injection Rules

NEVER duplicate — WordPress/GeneratePress owns these:
- `<html>`, `<head>`, `<body>`
- `<main>`
- Global `<header role="banner">`
- Global `<footer role="contentinfo">`
- `<h1>` — WordPress page title owns H1

**Every injected HTML partial starts at `<h2>`.**

### 2.2 Semantic Element Decision Tree

```
Is content independently distributable/syndicatable?
  YES → <article>

Is content tangentially related, removable without
breaking primary narrative?
  YES → <aside>

Does content group thematically related information
requiring a heading?
  YES → <section aria-labelledby="heading-id">

Purely for layout/styling/CSS wrapper?
  YES → <div>

NEVER use <section> as a div.
NEVER use <div> for thematically grouped content.
```

### 2.3 Heading Hierarchy

```
H1 — WordPress owns this. Never write it.
H2 — First heading in every injected section
H3 — Within an H2 section
H4 — Rare. Only when genuinely needed.

Never skip levels. H2 → H4 is wrong.
Every <section> must have an <h2>.
Use CSS for visual size — never choose heading level for size.
```

### 2.4 Accessibility (WCAG 2.1 AA)

Required on every build:

```html
<!-- Skip nav — first focusable element in DOM -->
<a href="#main-content" class="skip-nav">Skip to main content</a>

<!-- Section with landmark -->
<section aria-labelledby="section-id">
  <h2 id="section-id">Section Title</h2>
</section>

<!-- Images -->
<img src="..." alt="Description" width="800" height="600">
<img src="..." alt="" width="400" height="300"> <!-- decorative -->

<!-- Icon buttons -->
<button type="button" aria-label="Close menu">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Current page -->
<a href="/programs" aria-current="page">Programs</a>
```

Rules:
- `:focus-visible` for focus rings — never `:focus` alone
- All interactive elements minimum 44×44px
- tabindex: only 0 or -1. Never positive integers.
- aria-hidden: never on elements with focusable children
- aria-live="polite" on form error containers
- aria-expanded on toggle buttons
- aria-controls pointing to controlled element

### 2.5 Form Standards

Every field requires:
```html
<label for="input-id">Label Text</label>
<input type="text" id="input-id" name="field"
  autocomplete="given-name" required>
```

Required autocomplete values:
- given-name, family-name, name
- email, tel
- street-address, postal-code

Native HTML5 validation before JavaScript:
- required, type="email", minlength, maxlength, pattern

Submit: `<button type="submit">` — never `<input type="submit">`
method="POST" for all lead capture. method="GET" for search only.

### 2.6 Image Standards

```html
<!-- Standard image -->
<img src="image.jpg" alt="Description"
  width="800" height="600"
  loading="lazy" decoding="async">

<!-- LCP hero image — different rules -->
<img src="hero.jpg" alt=""
  width="1920" height="1080"
  fetchpriority="high" decoding="async">
```

Critical rules:
- loading="lazy" NEVER on above-fold/hero images (kills LCP)
- fetchpriority="high" on the single LCP image only
- width and height ALWAYS — prevents CLS
- Hero images: <img> tag — NEVER CSS background-image
- grayscale(100%) applied globally via CSS-SYSTEM.md
- class="no-grayscale" for logos and icons only

---

## SECTION 3 — CSS PRODUCTION STANDARDS

### 3.1 The Token Law (No Exceptions)

```
NEVER in component CSS:
  ✗ Any hex color (#CC0000, #000, #fff)
  ✗ Any raw px font-size (42px, 16px)
  ✗ Any arbitrary spacing (80px, 24px, 1.5rem)
  ✗ Any hardcoded font-family string
  ✗ #FF0000 — permanently retired

ALWAYS instead:
  ✓ var(--color-brand-red)       not #CC0000
  ✓ var(--text-4xl)              not 4.209rem
  ✓ var(--space-4)               not 2rem
  ✓ var(--font-family-headline)  not 'Montserrat'

ONLY legitimate raw color:
  color: #fff !important  on red buttons/backgrounds
  This is a brand rule, not a token bypass.
```

### 3.2 BEM Naming

```
Block:    .hero
Element:  .hero__title      (double underscore)
Modifier: .hero--dark       (double dash)

✓ Elements FLAT to block: .hero__title
✗ Double nesting: .hero__content__title  (WRONG)

✓ Modifier WITH base: class="hero hero--dark"
✗ Modifier alone:     class="hero--dark"  (WRONG)
```

### 3.3 WordPress Cascade

Loading order:
```
GeneratePress base
  → Child theme
    → Additional CSS (Customizer)
      → HFCM wp_head   ← Your CSS
        → HFCM wp_footer
```

Override GP without !important — match specificity:
```css
#content .my-component h2 { ... }

/* Or use @layer */
@layer components { .hero { ... } }
```

Full-width breakout (CSS Grid method — always use this):
```css
.entry-content {
  display: grid;
  grid-template-columns:
    minmax(var(--space-4), 1fr)
    minmax(auto, var(--container-xl))
    minmax(var(--space-4), 1fr);
}
.entry-content > * { grid-column: 2; }
.entry-content > .full-bleed { grid-column: 1 / -1; }
```

### 3.4 Mobile-First Breakpoints

```css
/* Base: mobile 320px — no query */
@media (min-width: 480px)  { /* large phone */ }
@media (min-width: 768px)  { /* tablet — column changes here */ }
@media (min-width: 1024px) { /* laptop */ }
@media (min-width: 1280px) { /* desktop */ }
@media (min-width: 1536px) { /* wide */ }
```

Always min-width. Never max-width.

### 3.5 Critical CSS Gotchas

```css
/* Flex overflow fix — always pair these */
.flex-child {
  flex: 1;       /* = flex: 1 1 0, not flex: 1 1 auto */
  min-width: 0;  /* REQUIRED — prevents text overflow */
}

/* Card grid — auto-fit not auto-fill */
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));

/* Viewport height — svh not vh */
.hero {
  min-height: 100vh;    /* fallback */
  min-height: 100svh;   /* correct — excludes browser chrome */
}
```

### 3.6 Animation Rules

```
Only animate (GPU-composited):
  ✓ transform  ✓ opacity

Never animate (triggers layout):
  ✗ width  ✗ height  ✗ margin  ✗ padding  ✗ top/left

Durations:
  100ms — micro-interactions
  200ms — state changes (hover, focus)
  300ms — UI transitions
```

---

## SECTION 4 — WORDPRESS/HFCM DEPLOYMENT

### 4.1 Injection Locations

| Location | Hook | Use For |
|---|---|---|
| `<head>` | wp_head | CSS, font preloads |
| Before header | generate_before_header | Announcement bars |
| After header | generate_after_header | Hero sections |
| Before content | generate_before_content | Page banners |
| After content | generate_after_content | CTA sections |
| Before footer | generate_before_footer | Newsletter signups |
| `</body>` | wp_footer | JavaScript, analytics |

### 4.2 Script Loading

```html
<!-- defer: after HTML parsed, in order — use for component JS -->
<script defer src="component.js"></script>

<!-- async: immediately on download — ONLY for analytics -->
<script async src="analytics.js"></script>
```

### 4.3 WordPress Body Classes for CSS Targeting

```css
.page-id-42 .hero { ... }           /* specific page */
.home .hero { min-height: 100svh; } /* front page */
.logged-in .admin-notice { ... }    /* logged-in users */
```

---

## SECTION 5 — PRE-SHIP QC CHECKLIST

Binary: Pass ✅ or Fail ❌. One ❌ blocks delivery.

### Universal (All Types)

```
STRUCTURE
[ ] No <h1> in injected HTML
[ ] Heading levels sequential, no skipped ranks
[ ] Every <section> has aria-labelledby
[ ] No <main>/global <header>/global <footer> injected
[ ] Every <img> has alt attribute
[ ] Every <img> has width and height attributes

ACCESSIBILITY
[ ] All interactive elements are native HTML
[ ] No <div onclick> or <span onclick>
[ ] All interactive elements minimum 44px touch target
[ ] :focus-visible on all interactive elements
[ ] No positive tabindex integers
[ ] aria-hidden never on elements with focusable children
[ ] Every form input has explicit <label for="id">
[ ] Every form input has autocomplete attribute

CSS
[ ] Zero raw hex values in CSS
[ ] Zero arbitrary pixel values
[ ] All colors use var(--color-*) tokens
[ ] All spacing uses var(--space-*) or semantic tokens
[ ] All font-sizes use var(--text-*) or clamp()
[ ] No #FF0000 anywhere
[ ] Animations only on transform and opacity

MOBILE
[ ] Renders correctly at 375px viewport
[ ] No horizontal scroll
[ ] Touch targets minimum 44×44px
[ ] Body text minimum 16px
[ ] Multi-column stacks to single below 768px
[ ] 100svh used for full-height elements

BRAND
[ ] Only ETKM 5 colors (#000, #FFF, #CC0000, #575757, #BBBBBB)
[ ] No gradients
[ ] Red buttons have color: #fff !important
[ ] Images have grayscale(100%) (or no-grayscale for logos)
[ ] Montserrat for H1-H3, Inter for body
```

### WordPress Page Section

```
[ ] CSS scoped to component wrapper (no theme bleed)
[ ] Full-bleed uses CSS Grid method (not negative margins)
[ ] GeneratePress variable mapping present
[ ] Correct HFCM injection location
[ ] JS uses defer in wp_footer
[ ] CSS in wp_head <style> block (not inline style attributes)
```

### Landing Page

```
[ ] Hero is <img fetchpriority="high"> not CSS background
[ ] Hero img has width and height attributes
[ ] StoryBrand sequence: Hero→Stakes→Guide→Plan→CTA→Proof→CTA
[ ] Three-step plan has exactly 3 steps
[ ] ETKM steps verbatim (see Section 7)
[ ] Primary CTA in: hero, after plan, final section
[ ] Single column below 768px
[ ] Above fold 375px: headline + subhead + CTA visible
[ ] Skip nav is first focusable element
```

### Email Template

```
[ ] DOCTYPE: XHTML 1.0 Transitional
[ ] Max-width 600px on container
[ ] Layout: HTML tables only (no Grid, no Flexbox)
[ ] MSO conditional comments around table layout
[ ] Critical CSS inlined on elements
[ ] CTA: bulletproof VML table technique
[ ] All images: absolute https:// URLs
[ ] All images: display: block
[ ] Preheader text present and visually hidden
[ ] Dark mode meta tags present
[ ] No position: absolute/relative
[ ] No external <link> stylesheets
```

### Lead Magnet PDF

```
[ ] @page rule specifies size (8.5in 11in or 210mm 297mm)
[ ] Playwright printBackground: true
[ ] -webkit-print-color-adjust: exact !important present
[ ] print-color-adjust: exact !important present (BOTH required)
[ ] All image URLs absolute https://
[ ] Fonts loaded via CDN or Base64 embedded
[ ] break-inside: avoid on logical containers
[ ] orphans: 3 and widows: 3 on paragraphs
[ ] Playwright margin in API payload, not CSS body
```

---

## SECTION 6 — AI FAILURE PREVENTION REFERENCE

| Failure | Prevention Rule | QC Check |
|---|---|---|
| Raw hex in CSS | Token law — no hex ever | Grep `#[0-9A-Fa-f]` in CSS |
| `#FF0000` used | Token enforces `#CC0000` | Grep `FF0000` |
| Multiple H1s | Injected HTML starts at H2 | Count H1 elements |
| Divitis | Semantic decision tree | Check section/article use |
| Missing alt | alt required on every img | Check all img tags |
| No width/height | CLS rule — both always | Check all img tags |
| Lazy on hero | Hero = fetchpriority="high" | Check first img |
| CSS background hero | img tag rule — LCP | Check hero section |
| flex:1 overflow | Always pair with min-width:0 | Inspect flex children |
| auto-fill confusion | auto-fit for card grids | Check repeat() |
| Gradient added | Prohibited — brand-kit | Grep `gradient` |
| Wrong viewport unit | 100svh with 100vh fallback | Check min-height |
| Positive tabindex | 0 or -1 only | Grep `tabindex="[1-9]` |
| aria-hidden on button | Never on focusable elements | Check aria-hidden |
| No autocomplete | Required on user data fields | Check all inputs |
| No label | for/id explicit association | Check label pairs |
| BEM double nesting | Elements flat to block | Check `__.*__` |
| Email uses Flexbox | Tables only in email | Grep `flex` in email |
| PDF background stripped | printBackground: true | Check API payload |
| PDF print-color missing | Both prefixes required | Check print CSS |
| Arbitrary z-index | Max z-index: 100 | Reject z-index > 100 |

---

## SECTION 7 — ETKM BRAND CONSTANTS

Colors (5 only):
```
#000000  Black   — backgrounds, text
#FFFFFF  White   — backgrounds, text
#CC0000  Red     — CTAs, accents (one per section max)
#575757  Gray    — supporting, secondary text
#BBBBBB  LtGray  — dividers, borders
```
Never: #FF0000 (retired). Never: gradients. Never: other colors.

Typography:
```
H1-H3:    Montserrat 900
Body/H4+: Inter 400
Load:     Google Fonts CDN with preconnect
```

Images: grayscale(100%) sitewide. Logos: no-grayscale class.
Buttons (red): color: #fff !important always.
Layout: Swiss International — asymmetric, left-aligned default.

Tagline (exact — never rewrite): "Train More...Fear Less."

Three steps (exact — never rewrite):
1. Attend a Free Trial Lesson
2. Get Your Personalized Training Blueprint
3. Become a Confident, Capable Protector

---

## SECTION 8 — QUARTERLY MAINTENANCE

Next review: 2026-07-24

- [ ] Verify skill files consistent with current etkm-global.css
- [ ] Check new CSS features at 96%+ browser support
- [ ] Review GeneratePress updates for DOM changes
- [ ] Update tokens if brand palette changes
- [ ] Add new components to COMPONENT-LIBRARY.md
- [ ] Update QC checklist if new failure modes found
