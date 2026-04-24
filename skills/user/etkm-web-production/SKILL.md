---
name: etkm-web-production
version: 1.0
updated: 2026-04-24
description: >
  Load this skill for ANY task that produces HTML or CSS for ETKM.
  Triggers: building WordPress page sections, landing pages, lead
  magnets, email templates, HFCM injection code, or any web deliverable.
  This skill governs the build protocol. Load CSS-SYSTEM.md for token
  reference. Load COMPONENT-LIBRARY.md for component HTML/CSS patterns.
  All four files work together — never load one without the others.
---

# ETKM Web Production — Governing Build Protocol

**Version:** 1.0
**Built:** 2026-04-24
**Research basis:** Gemini Deep Research — HTML/CSS Production Standards 2026
**Depends on:**
  - etkm-web-production/CSS-SYSTEM (all token values)
  - etkm-web-production/COMPONENT-LIBRARY (all component patterns)
  - etkm-web-production/OUTPUT-STANDARDS (output-type specific rules)

---

## PROTOCOL LAW — NON-NEGOTIABLE RULES

### Brand Rules (from etkm-brand-kit v3.1)
- Red is #CC0000 only — accessed via var(--color-brand-red)
- #FF0000 is permanently retired — never write it
- Red buttons and red backgrounds: color: #fff !important always
- No gradients anywhere in the system
- No colors outside: #000000, #FFFFFF, #CC0000, #575757, #BBBBBB
- Images: filter: grayscale(100%) sitewide — applied in CSS-SYSTEM
- Headlines: Montserrat 900 — var(--font-family-headline)
- Body: Inter 400 — var(--font-family-body)
- Swiss layout: asymmetric, high contrast, left-aligned default
- Centered text: hero headlines and step numbers only

### CSS Rules
- Never write a raw hex value — always use a token
- Never write an arbitrary px value — always use a spacing token
- Never write a raw font-size — use type scale token or clamp()
- All CSS is mobile-first: base = mobile, min-width adds desktop
- Single to multi-column transitions: minimum 768px breakpoint
- Never use positive tabindex integers
- Only animate transform and opacity (GPU-composited)
- Never animate width, height, margin, padding, top, left

### HTML Rules
- WordPress owns H1 — injected HTML starts at H2
- Never inject main, global header, global footer (GP owns these)
- section requires aria-labelledby pointing to heading ID
- Every img requires: width, height, alt attributes
- Interactive elements must be native: button, a, input
- Never use div onclick or span onclick
- LCP image: fetchpriority="high" — never loading="lazy"
- All below-fold images: loading="lazy"

---

## STEP 1 — CLASSIFY THE OUTPUT TYPE

Before writing a single line of code, identify which output type.

WordPress Page Section:
- Code installed into WordPress via HFCM or Additional CSS
- Must integrate with GeneratePress DOM
- Rules: OUTPUT-STANDARDS § WordPress/HFCM

Landing Page:
- Standalone conversion page (trial signup, program, event, lead magnet)
- StoryBrand sequence, CTA in hero + plan + final section
- Rules: OUTPUT-STANDARDS § Landing Pages

Email Template:
- HTML email for Pipedrive sequences or campaigns
- NO Grid, NO Flexbox, table layout, MSO conditionals, inline CSS
- Rules: OUTPUT-STANDARDS § Email Templates

Lead Magnet PDF:
- PDF rendered via HTML to Playwright
- printBackground:true, Base64 fonts, print-color-adjust:exact
- Rules: OUTPUT-STANDARDS § Lead Magnet PDF

---

## STEP 2 — MAP COMPONENTS BEFORE CODING

Never start writing HTML cold. Map structure first.

1. List every section the output needs
2. Match each to COMPONENT-LIBRARY
3. Sections without match: define using token system + BEM first
4. Note StoryBrand sequence for landing pages
5. Only after map is complete: begin writing HTML

Landing page StoryBrand sequence:
1. Site Navigation (Component 12)
2. Hero Section (Component 3 or 4)
3. Stakes/Problem Band (dark section)
4. Guide Introduction (Component 6)
5. Three-Step Plan (Component 5 — REQUIRED)
6. CTA Band (Component 8 — after plan)
7. Testimonials (Component 9)
8. Final CTA Band (Component 8 — repeat)
9. Lead Capture Form (Component 11 — optional)
10. Page Footer (Component 13)

---

## STEP 3 — BUILD SEQUENCE

1. HTML SKELETON FIRST
   Semantic HTML structure completely
   BEM class names applied
   H2 starts heading hierarchy (not H1)
   NO CSS yet

2. VERIFY STRUCTURE
   Heading hierarchy correct?
   Every section has aria-labelledby?
   Every interactive element native HTML?
   Every image has width, height, alt?
   NO to any: fix before proceeding

3. TOKEN-BASED CSS
   Reference CSS-SYSTEM for every value
   Mobile styles first — no media query
   min-width queries scale up
   No raw values — tokens only

4. RESPONSIVE BEHAVIOR
   Single column at 375px — nothing overflows
   768px breakpoint for multi-column
   All interactive elements 44x44px minimum

5. INTERACTIVE STATES
   hover: transform + color transitions only
   focus-visible: 2px outline, 3px offset
   active: transform back to baseline
   disabled: muted colors, cursor not-allowed

6. RUN QC CHECKLIST
   Every item passes before handoff

---

## STEP 4 — WORDPRESS/HFCM INJECTION RULES

HFCM hook locations:

wp_head — CSS style blocks, font preloads
generate_before_header — site-wide announcement bars
generate_after_header — secondary nav, breadcrumbs
wp_body_open — tag managers, chat widgets
generate_before_content — page-specific hero sections
generate_after_content — CTAs, related content
generate_before_footer — pre-footer CTA bands
wp_footer — scripts with defer, analytics

CSS injection rules:
- Component CSS: style block in wp_head, scoped to wrapper class
- Global CSS: WordPress Additional CSS (Customizer)
- Never link rel="stylesheet" via HFCM — use style blocks
- Always scope to component wrapper:
  .etkm-hero { } and .etkm-hero .hero__title { }
  NEVER bare h2 { } — bleeds into theme

Script rules:
- DOM-dependent scripts: wp_footer with defer
- Analytics: wp_head or wp_body_open with async
- Never block rendering with synchronous scripts in wp_head

GeneratePress integration:
- Container: .container — override via #page .container
- Content wrapper: .entry-content — reset margins for components
- Full-width breakout CSS Grid method:

.entry-content--breakout {
  display: grid;
  grid-template-columns:
    minmax(var(--space-4), 1fr)
    minmax(auto, var(--container-xl))
    minmax(var(--space-4), 1fr);
}
.entry-content--breakout > * { grid-column: 2; }
.entry-content--breakout > .full-bleed { grid-column: 1 / -1; }

Specificity override without !important:
#content .etkm-component { }

---

## STEP 5 — PRE-SHIP QC CHECKLIST

All items binary: PASS or FAIL. One FAIL = blocked delivery.

UNIVERSAL (all output types):
[ ] No H1 in injected HTML — starts at H2
[ ] No raw hex in CSS — grep # returns zero (except comments)
[ ] No #FF0000 anywhere — grep confirms
[ ] No gradients — grep gradient returns zero
[ ] .btn--primary has color: #fff
[ ] Every img has width, height, alt
[ ] No div onclick — native elements only
[ ] All interactive elements show focus-visible outline
[ ] All clickable elements 44x44px minimum
[ ] Layout correct at 375px — no horizontal overflow
[ ] No Tier 1 primitive tokens in component CSS

WORDPRESS PAGE SECTION:
[ ] No main, global header, global footer injected
[ ] Every section has aria-labelledby
[ ] All CSS scoped to component wrapper class
[ ] Scripts in wp_footer with defer
[ ] No unscoped bare element selectors
[ ] Hero image: img with fetchpriority="high" not CSS background

LANDING PAGE:
[ ] StoryBrand sequence: Hero, Stakes, Guide, Plan, CTA Band, Testimonials, Final CTA
[ ] Plan section has exactly 3 steps
[ ] Primary CTA in Hero + after Plan + Final CTA (minimum 3 placements)
[ ] Headline + CTA visible at 375px without scrolling
[ ] All multi-column layouts single column below 768px
[ ] Form inputs and body text 16px minimum (prevents iOS zoom)
[ ] Hero image: img with fetchpriority="high"

EMAIL TEMPLATE:
[ ] DOCTYPE is XHTML 1.0 Transitional
[ ] Zero display: grid declarations
[ ] Zero display: flex declarations
[ ] Structure uses table elements
[ ] MSO conditional tables present
[ ] All layout/spacing/typography inlined
[ ] All img use absolute https:// URLs
[ ] All img have display: block
[ ] Bulletproof VML button for Outlook
[ ] Email container max-width 600px
[ ] Hidden preheader text present
[ ] Dark mode @media (prefers-color-scheme: dark) present
[ ] Web fonts have system font fallback stack

LEAD MAGNET PDF:
[ ] @page size declared (8.5in 11in or 210mm 297mm)
[ ] Playwright config has printBackground: true
[ ] -webkit-print-color-adjust: exact !important present
[ ] print-color-adjust: exact !important present
[ ] Fonts embedded as Base64 data URIs
[ ] All images use https:// or data: URIs
[ ] Major content blocks have break-inside: avoid
[ ] orphans: 3; widows: 3; on paragraphs
[ ] All colored sections have explicit background-color

---

## STEP 6 — COMMON FAILURES REFERENCE

Failure | Prevention | QC Check
H1 injected | Always start at H2 | Grep h1
Raw hex in CSS | Tokens only | Grep # in CSS
#FF0000 used | Token system | Grep FF0000
Missing image dimensions | Template w+h | Check every img
CSS background hero kills LCP | HTML img + fetchpriority | Inspect hero
Flexbox in email | Table-only | Grep flex in email CSS
Gradient in design | Prohibited | Grep gradient
Arbitrary px spacing | Spacing token system | Grep px values
Positive tabindex | Never use positive | Grep tabindex=[1-9]
div onclick | Native button only | Inspect interactive
Missing focus styles | focus-visible in global CSS | Tab through page
Touch target under 44px | min-height: 44px on all interactive | DevTools
No aria-labelledby | Required on every section | Check sections
flex:1 overflow | min-width: 0 on flex children | Inspect flex
Missing autocomplete | Required on all user data inputs | Check inputs
PDF backgrounds missing | print-color-adjust: exact | Render test PDF
Fonts to Times New Roman | Base64 embed fonts for PDF | Visual check
lazy on LCP image | fetchpriority="high" on hero | Check hero img
Double BEM nesting | .block__element only never __element__ | Review class names
!important abuse | Utility overrides only | Review !important

---

## DECISION TREES

section vs div vs article:
Content independently distributable? YES: article
Groups thematic info AND needs heading? YES: section aria-labelledby
Layout wrapper only? YES: div

CSS Grid vs Flexbox:
Layout defines sizes (equal columns)? Grid
Content defines sizes (items flow)? Flexbox
Navigation or button group? Flexbox
Multi-column page layout? Grid

button vs anchor:
Navigates to URL? YES: a href="..."
Performs action (submit, toggle)? YES: button type="button"
CTA styled as button that navigates? a href class="btn btn--primary"

LCP image:
Above the fold? fetchpriority="high", HTML img, never CSS background
Below the fold? loading="lazy"

Where does injected CSS go:
Global to entire site? WordPress Additional CSS
Component-specific? style block in HFCM wp_head, scoped to wrapper
One specific page only? HFCM conditional targeting page ID, body.page-id-X

---

## SKILL LOAD ORDER

For any ETKM web production task, load in this order:

1. etkm-web-production (this file — build protocol)
2. etkm-web-production/CSS-SYSTEM (token reference)
3. etkm-web-production/COMPONENT-LIBRARY (component patterns)
4. etkm-web-production/OUTPUT-STANDARDS (output-type rules)
5. etkm-brand-foundation (messaging and voice)
6. etkm-brand-kit (visual standards)
7. etkm-deliverable-qc (final QC before handoff)

---

## FILE RELATIONSHIP MAP

CSS-SYSTEM:
  Defines all tokens
  Governs all CSS values
  Consumed by all other files

COMPONENT-LIBRARY:
  13 ETKM components with HTML + token CSS
  Instantiated by build protocol
  Consumed by OUTPUT-STANDARDS per output type

OUTPUT-STANDARDS:
  WordPress/HFCM specific rules
  Landing page StoryBrand sequence
  Email template isolated CSS ruleset
  Lead magnet PDF Playwright and print CSS

etkm-web-production (this file):
  Governs the build process
  References all other files
  Contains QC checklist
  Contains decision trees

---

## QUARTERLY MAINTENANCE

Next review: 2026-07-24

[ ] Verify GeneratePress CSS variables still match (GP updates)
[ ] Check HFCM hook names against current WordPress version
[ ] Verify email CSS support matrix is current (Gmail and Outlook change)
[ ] Confirm Playwright PDF API options unchanged
[ ] Update component library for new ETKM sections
[ ] Check browser support: container queries, :has(), CSS nesting (all 96%+ as of 2026)
[ ] Update updated date and version number

Version rules:
Patch: QC item change (1.0 to 1.1)
Minor: New component or output type (1.0 to 1.1)
Major: Protocol change affecting all builds (1.0 to 2.0)
