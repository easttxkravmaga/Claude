---
name: etkm-webpage-build
description: >
  The locked production standard for building any ETKM HTML page — homepage, landing
  page, service page, event page, Fight Back ETX page, or any page that will be
  deployed to etxkravmaga.com, fightbacketx.com, or etkmstudent.com via WordPress
  Raw HTML block. Load this skill before writing a single line of HTML for ETKM.
  Covers hero spec, image treatment, section patterns, font loading, responsive
  breakpoints, and WordPress deployment rules — all derived from the March 2026
  site rebuild (19 pages). This is the parent standard that etkm-event-page,
  etkm-pdf-pipeline, and etkm-webform-build all reference. Trigger phrases:
  "build a page", "HTML page", "landing page", "rebuild this page", "add a section",
  "WordPress page", "same layout as", "site page", "homepage", "service page",
  "Fight Back ETX page", or any request to produce a self-contained HTML file for
  ETKM web deployment. Always load etkm-brand-kit alongside this skill.
---

# ETKM Webpage Build Standard

**Version:** 1.0
**Last Updated:** 2026-03-28
**Derived from:** March 2026 etxkravmaga.com rebuild (19 pages)

---

## Core Rules — Non-Negotiable

1. Every page is **self-contained HTML** — all CSS inline in `<style>`, no external
   CSS files, no separate JS files, Google Fonts loaded via `<link>` in `<head>`.
2. Deployed via **WordPress Raw HTML block** — never as a theme template.
3. Background: `#000000` body, `#111111` surface cards. Never gray, never gradient.
4. Text: white on dark sections, black on white sections. No exceptions.
5. Accent: `#CC0000` only. One element per section maximum.
6. Fonts: Montserrat (headlines, 900 default) + Inter (body). Both from Google Fonts CDN.
7. **No emojis. Ever.**
8. **No split-layout heroes.** Heroes are always full-bleed with overlaid text.
9. All images: grayscale filter applied (see Section 3).
10. Mobile-first responsive — every section has a breakpoint at 768px.

---

## 1. Page Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[PAGE TITLE] — East Texas Krav Maga</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* All CSS goes here — no external stylesheets */
  </style>
</head>
<body>
  <!-- nav -->
  <!-- hero -->
  <!-- sections -->
  <!-- footer -->
</body>
</html>
```

---

## 2. Hero Section — Locked Spec

### Rules
- Always full-bleed (100vw, min-height 80vh or 100vh for homepage)
- Background image with `brightness(0.42) grayscale(100%)` filter — no other values
- No split-layout. Image behind, text over.
- Eyebrow line: small caps, letter-spaced, `#CC0000` or white — one word or short phrase
- H1: Montserrat 900, white, 56–72px desktop / 36–48px mobile
- Subhead: Inter 400 or 500, white, 18–22px, max-width 600px
- CTA button: `background: #CC0000`, white text, no border-radius or minimal (4px)

### Hero HTML Pattern

```html
<section class="hero" style="
  position: relative;
  min-height: 85vh;
  display: flex;
  align-items: center;
  background: #000;
  overflow: hidden;
">
  <div class="hero-bg" style="
    position: absolute;
    inset: 0;
    background-image: url('[IMAGE URL]');
    background-size: cover;
    background-position: center right;
    filter: brightness(0.42) grayscale(100%);
    z-index: 0;
  "></div>
  <div class="hero-content" style="
    position: relative;
    z-index: 1;
    padding: 80px 5%;
    max-width: 720px;
  ">
    <p class="eyebrow" style="
      font-family: 'Montserrat', sans-serif;
      font-weight: 700;
      font-size: 12px;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: #CC0000;
      margin-bottom: 16px;
    ">[EYEBROW TEXT]</p>
    <h1 style="
      font-family: 'Montserrat', sans-serif;
      font-weight: 900;
      font-size: clamp(38px, 6vw, 72px);
      line-height: 1.05;
      color: #fff;
      margin: 0 0 24px 0;
    ">[HEADLINE]</h1>
    <p style="
      font-family: 'Inter', sans-serif;
      font-size: 18px;
      line-height: 1.6;
      color: rgba(255,255,255,0.85);
      max-width: 560px;
      margin-bottom: 36px;
    ">[SUBHEADLINE]</p>
    <a href="[CTA URL]" style="
      display: inline-block;
      background: #CC0000;
      color: #fff;
      font-family: 'Montserrat', sans-serif;
      font-weight: 700;
      font-size: 14px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 16px 36px;
      text-decoration: none;
      border-radius: 4px;
    ">[CTA TEXT]</a>
  </div>
</section>
```

---

## 3. Image Rules

- **All sitewide images: `filter: grayscale(100%)`** applied via CSS on the element
- Format: square 1080×1080px preferred for section images
- Position: **action/subject on the right side** of the frame when using side-by-side layouts
- Hero background images: `background-position: center right` to favor right-side subject
- Never apply color tints, overlays, or brand color filters — the grayscale + brightness filter IS the treatment

```css
/* Standard image treatment */
img.etkm-img {
  filter: grayscale(100%);
  object-fit: cover;
}

/* Background image treatment (hero, full-bleed sections) */
.etkm-bg {
  filter: brightness(0.42) grayscale(100%);
}
```

---

## 4. Section Patterns

### 4A — Split Content (Text + Image)

Use for: service descriptions, about sections, feature callouts.

```html
<section style="background: #000; padding: 80px 5%;">
  <div style="
    max-width: 1100px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;
  ">
    <div>
      <p style="font-family:'Montserrat';font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:#CC0000;margin-bottom:12px;">[EYEBROW]</p>
      <h2 style="font-family:'Montserrat';font-weight:900;font-size:clamp(28px,4vw,48px);color:#fff;line-height:1.1;margin-bottom:20px;">[HEADING]</h2>
      <p style="font-family:'Inter';font-size:16px;line-height:1.7;color:rgba(255,255,255,0.8);margin-bottom:28px;">[BODY]</p>
      <a href="[URL]" style="display:inline-block;background:#CC0000;color:#fff;font-family:'Montserrat';font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;padding:14px 30px;text-decoration:none;">[CTA]</a>
    </div>
    <div>
      <img src="[IMG URL]" alt="[ALT]" style="width:100%;display:block;filter:grayscale(100%);">
    </div>
  </div>
</section>
```

**Responsive rule:** At 768px, `grid-template-columns: 1fr`. Image stacks below text.

### 4B — Card Grid

Use for: membership tiers, benefits, program offerings.

```html
<section style="background: #111; padding: 80px 5%;">
  <div style="max-width:1100px;margin:0 auto;">
    <h2 style="font-family:'Montserrat';font-weight:900;font-size:clamp(28px,4vw,44px);color:#fff;text-align:center;margin-bottom:48px;">[HEADING]</h2>
    <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:24px;">
      <!-- Card -->
      <div style="background:#000;padding:36px 28px;border-top:3px solid #CC0000;">
        <h3 style="font-family:'Montserrat';font-weight:900;font-size:22px;color:#fff;margin-bottom:12px;">[CARD TITLE]</h3>
        <p style="font-family:'Inter';font-size:15px;line-height:1.7;color:rgba(255,255,255,0.75);">[CARD BODY]</p>
      </div>
    </div>
  </div>
</section>
```

**Responsive rule:** 3 → 2 → 1 columns at 900px → 600px.

### 4C — Testimonial Block

```html
<section style="background:#000;padding:80px 5%;border-top:1px solid #222;">
  <div style="max-width:800px;margin:0 auto;text-align:center;">
    <p style="font-family:'Montserrat';font-weight:300;font-size:clamp(20px,3vw,30px);color:#fff;line-height:1.5;margin-bottom:24px;">"[QUOTE TEXT]"</p>
    <p style="font-family:'Inter';font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#CC0000;">— [NAME], [DESCRIPTOR]</p>
  </div>
</section>
```

### 4D — CTA Banner

Use at page bottom before footer.

```html
<section style="background:#CC0000;padding:72px 5%;text-align:center;">
  <h2 style="font-family:'Montserrat';font-weight:900;font-size:clamp(28px,4vw,48px);color:#fff;margin-bottom:20px;">[HEADLINE]</h2>
  <p style="font-family:'Inter';font-size:17px;color:rgba(255,255,255,0.9);max-width:560px;margin:0 auto 32px;">[SUBTEXT]</p>
  <a href="[URL]" style="display:inline-block;background:#000;color:#fff;font-family:'Montserrat';font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;padding:16px 36px;text-decoration:none;">[CTA]</a>
</section>
```

### 4E — Stats / Numbers Bar

```html
<section style="background:#111;padding:60px 5%;border-top:1px solid #222;border-bottom:1px solid #222;">
  <div style="max-width:1000px;margin:0 auto;display:flex;justify-content:space-around;flex-wrap:wrap;gap:32px;text-align:center;">
    <div>
      <p style="font-family:'Montserrat';font-weight:900;font-size:52px;color:#CC0000;margin-bottom:8px;">[NUMBER]</p>
      <p style="font-family:'Inter';font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:rgba(255,255,255,0.6);">[LABEL]</p>
    </div>
  </div>
</section>
```

---

## 5. Responsive Breakpoints

All pages must include a `<style>` block with at minimum:

```css
@media (max-width: 768px) {
  /* Grid: switch all multi-column grids to 1fr */
  /* Hero: reduce H1 to 36-42px, reduce padding */
  /* Cards: stack vertically */
  /* Nav: collapse to hamburger or stacked links */
}

@media (max-width: 480px) {
  /* Further reduction for small phones */
  /* CTA buttons: full width */
}
```

Use `clamp()` for fluid font sizes wherever possible — reduces the number of breakpoint overrides needed.

---

## 6. Key URLs and Constants

| Item | Value |
|------|-------|
| Free Trial Calendly | `https://calendly.com/easttxkravmaga-fud9/free-trial-lesson` |
| Web3Forms endpoint | `https://api.web3forms.com/submit` |
| Web3Forms access key | `8365e17b-3dd5-481d-ba48-465042f70e3d` |
| Primary domain | `https://etxkravmaga.com` |
| Fight Back ETX | `https://fightbacketx.com` |
| Student portal | `https://etkmstudent.com` |
| Phone | `(903) 590-0085` |

---

## 7. WordPress Deployment Rules

- Every page is deployed as a **single Raw HTML block** inside a blank WordPress page
- No page builder columns or rows around the block — the HTML manages its own layout
- Set WordPress page template to: **Full Width** or **Blank Canvas** (theme-dependent)
- To override WordPress theme font injection:
  ```css
  /* Use !important to beat theme stylesheets */
  h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; }
  p, li, span { font-family: 'Inter', sans-serif !important; }
  body { background: #000 !important; }
  ```
- Never rely on the theme to provide fonts or colors — always declare them inline
- Test on live WordPress before delivery — Raw HTML blocks can collapse empty lines
  in ways that affect layout

---

## 8. Navigation Pattern

ETKM nav is consistent across all pages. Use the approved pattern:

- Background: `#000` always
- Logo: left-aligned, ETKM mark
- Links: Inter 500, white, letter-spaced, uppercase
- CTA link: `#CC0000` background button on right end
- Mobile: links collapse, show hamburger or stacked menu
- Nav sticks to top on scroll (`position: sticky; top: 0; z-index: 999`)

---

## 9. Footer Pattern

- Background: `#000`
- Top border: `1px solid #222`
- Three columns: Logo + tagline / Nav links / Contact + social
- Bottom bar: `©` line, Inter 400, small, `rgba(255,255,255,0.4)`

---

## 10. QC Gates — Run Before Delivery

### Gate 1 — Brand Compliance
- [ ] Background is `#000` or `#111` — no other colors as backgrounds
- [ ] Red is `#CC0000` — not `#CC0000`, not any other value
- [ ] Fonts loaded: Montserrat + Inter from Google Fonts CDN
- [ ] No emojis anywhere in the HTML
- [ ] No prohibited words (mastery, dominate, destroy, killer, beast, crush, elite, warrior)
- [ ] Red used maximum once per visual section

### Gate 2 — HTML Structure
- [ ] All tags balanced and closed
- [ ] No broken image `src` attributes (no placeholder text left in)
- [ ] All images have `filter: grayscale(100%)` applied
- [ ] Hero background has `filter: brightness(0.42) grayscale(100%)`
- [ ] No inline `style=""` left blank or broken

### Gate 3 — Link Validation
- [ ] All `href` values are real URLs or `#anchor` links
- [ ] Calendly link is exactly: `https://calendly.com/easttxkravmaga-fud9/free-trial-lesson`
- [ ] No `href="#"` placeholders left in production output
- [ ] Phone link format: `href="tel:+19035900085"`

### Gate 4 — Responsive
- [ ] `@media (max-width: 768px)` block present and covers all grid layouts
- [ ] No fixed widths that overflow on mobile (no `width: 1100px` without max-width)
- [ ] Hero text readable at 375px viewport width
- [ ] CTA buttons are full-width or appropriately sized on mobile

---

## 11. What This Skill Does NOT Cover

- PDF generation → use `etkm-pdf-pipeline`
- Form logic and Web3Forms config → use `etkm-webform-build`
- Social media graphics → use `etkm-social-graphics`
- Event page-specific layout patterns → use `etkm-event-page`
- Copy voice, tone, prohibited words → use `etkm-brand-foundation`
