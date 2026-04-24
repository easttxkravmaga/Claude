# ETKM CSS Token System
## File 2 of 4 — etkm-web-production skill series

**Version:** 1.0
**Built:** 2026-04-24
**Research basis:** Gemini Deep Research — HTML/CSS Production Standards 2026
**Brand basis:** etkm-brand-kit v3.1
**Applies to:** All HTML/CSS production for ETKM — WordPress page sections,
               landing pages, email templates, lead magnet PDFs
**Next file:** COMPONENT-LIBRARY.md (built against this token system)

---

## SYSTEM LAW — READ BEFORE WRITING ANY CSS

These rules have no exceptions. They apply to every line of CSS
Claude writes for ETKM across every output type.

1. **Never write a raw hex value in CSS.** Use a token. Always.
   — Wrong: `color: #CC0000;`
   — Right: `color: var(--color-brand-red);`

2. **Never write an arbitrary pixel value.** Use a spacing token.
   — Wrong: `padding: 80px 0;`
   — Right: `padding: var(--section-padding-y) 0;`

3. **Never write a raw font-size.** Use a type scale token or clamp().
   — Wrong: `font-size: 42px;`
   — Right: `font-size: var(--text-4xl);`

4. **Never use `#FF0000`.** It is permanently retired. ETKM red is
   `#CC0000` only, accessed via `var(--color-brand-red)`.

5. **All red buttons and red backgrounds require:**
   `color: #fff !important;` — this is a hard rule from etkm-brand-kit.

6. **Never use gradients.** The ETKM design system prohibits them.

7. **Images are grayscale sitewide:**
   `filter: grayscale(100%);` applies to all `<img>` elements globally.

8. **No colors outside the ETKM 5-color palette.**
   The palette is: `#000000`, `#FFFFFF`, `#CC0000`, `#575757`, `#BBBBBB`.
   No blues, greens, yellows, or any other colors exist in this system.

---

## TIER 1 — PRIMITIVE TOKENS
### Raw values. Never referenced in component CSS directly.
### Only Tier 2 semantic tokens consume primitives.

```css
:root {

  /* ─── COLOR PRIMITIVES ─────────────────────────────────────────── */
  --primitive-black:       #000000;
  --primitive-white:       #FFFFFF;
  --primitive-red:         #CC0000;
  --primitive-gray:        #575757;
  --primitive-gray-light:  #BBBBBB;
  --primitive-gray-50:     #F9FAFB;
  --primitive-gray-100:    #F4F5F7;
  --primitive-gray-200:    #E5E7EB;

  /* ─── TYPOGRAPHY PRIMITIVES ────────────────────────────────────── */
  --primitive-font-headline: 'Montserrat', system-ui, sans-serif;
  --primitive-font-body:     'Inter', system-ui, sans-serif;
  --primitive-font-mono:     ui-monospace, SFMono-Regular, 'Courier New', monospace;

  --primitive-weight-regular:   400;
  --primitive-weight-medium:    500;
  --primitive-weight-semibold:  600;
  --primitive-weight-bold:      700;
  --primitive-weight-black:     900;

  /* ─── TYPE SCALE (Perfect Fourth — 1.333 ratio, 16px base) ─────── */
  --primitive-text-xs:   0.75rem;
  --primitive-text-sm:   0.875rem;
  --primitive-text-base: 1rem;
  --primitive-text-lg:   1.333rem;
  --primitive-text-xl:   1.777rem;
  --primitive-text-2xl:  2.369rem;
  --primitive-text-3xl:  3.157rem;
  --primitive-text-4xl:  4.209rem;
  --primitive-text-5xl:  5.610rem;
  --primitive-text-6xl:  7.478rem;

  /* ─── SPACING PRIMITIVES (8px base) ────────────────────────────── */
  --primitive-space-1:    0.5rem;
  --primitive-space-2:    1rem;
  --primitive-space-3:    1.5rem;
  --primitive-space-4:    2rem;
  --primitive-space-6:    3rem;
  --primitive-space-8:    4rem;
  --primitive-space-12:   6rem;
  --primitive-space-16:   8rem;
  --primitive-space-20:  10rem;

  /* ─── LAYOUT PRIMITIVES ────────────────────────────────────────── */
  --primitive-container-sm:   640px;
  --primitive-container-md:   768px;
  --primitive-container-lg:  1024px;
  --primitive-container-xl:  1280px;
  --primitive-container-2xl: 1536px;

  /* ─── EFFECT PRIMITIVES ────────────────────────────────────────── */
  --primitive-radius-none:  0;
  --primitive-radius-sm:    0.25rem;
  --primitive-radius-md:    0.5rem;
  --primitive-radius-lg:    1rem;
  --primitive-radius-full:  9999px;

  --primitive-shadow-sm:  0 1px 2px 0 rgba(0,0,0,0.05);
  --primitive-shadow-md:  0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
  --primitive-shadow-lg:  0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
  --primitive-shadow-xl:  0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);

  --primitive-transition-fast:   100ms;
  --primitive-transition-base:   200ms;
  --primitive-transition-slow:   300ms;
  --primitive-transition-slower: 500ms;
}
```

---

## TIER 2 — SEMANTIC TOKENS

```css
:root {

  /* ─── BACKGROUNDS ───────────────────────────────────────────────── */
  --color-bg-page:     var(--primitive-white);
  --color-bg-surface:  var(--primitive-white);
  --color-bg-subtle:   var(--primitive-gray-50);
  --color-bg-dark:     var(--primitive-black);
  --color-bg-muted:    var(--primitive-gray-100);

  /* ─── TEXT ──────────────────────────────────────────────────────── */
  --color-text-primary:   var(--primitive-black);
  --color-text-secondary: var(--primitive-gray);
  --color-text-muted:     var(--primitive-gray-light);
  --color-text-inverse:   var(--primitive-white);

  /* ─── BRAND ─────────────────────────────────────────────────────── */
  --color-brand-red:   var(--primitive-red);
  --color-brand-black: var(--primitive-black);
  --color-brand-white: var(--primitive-white);
  --color-brand-gray:  var(--primitive-gray);

  /* ─── BORDERS ───────────────────────────────────────────────────── */
  --color-border-default: var(--primitive-gray-200);
  --color-border-strong:  var(--primitive-gray-light);
  --color-border-dark:    var(--primitive-black);

  /* ─── INTERACTIVE (RED ONLY — ETKM SYSTEM) ─────────────────────── */
  --color-interactive-default: var(--primitive-red);
  --color-interactive-hover:   #A30000;
  --color-interactive-active:  #8A0000;
  --color-interactive-focus:   var(--primitive-red);

  /* ─── FEEDBACK ──────────────────────────────────────────────────── */
  --color-feedback-success: #16A34A;
  --color-feedback-error:   #DC2626;

  /* ─── TYPOGRAPHY ────────────────────────────────────────────────── */
  --font-family-headline: var(--primitive-font-headline);
  --font-family-body:     var(--primitive-font-body);
  --font-family-mono:     var(--primitive-font-mono);

  --font-weight-regular:  var(--primitive-weight-regular);
  --font-weight-medium:   var(--primitive-weight-medium);
  --font-weight-semibold: var(--primitive-weight-semibold);
  --font-weight-bold:     var(--primitive-weight-bold);
  --font-weight-black:    var(--primitive-weight-black);

  --text-xs:   var(--primitive-text-xs);
  --text-sm:   var(--primitive-text-sm);
  --text-base: var(--primitive-text-base);
  --text-lg:   var(--primitive-text-lg);
  --text-xl:   var(--primitive-text-xl);
  --text-2xl:  var(--primitive-text-2xl);
  --text-3xl:  var(--primitive-text-3xl);
  --text-4xl:  var(--primitive-text-4xl);
  --text-5xl:  var(--primitive-text-5xl);
  --text-6xl:  var(--primitive-text-6xl);

  --line-height-tight:   1.2;
  --line-height-base:    1.5;
  --line-height-relaxed: 1.75;

  --letter-spacing-tight:   -0.025em;
  --letter-spacing-base:     0;
  --letter-spacing-wide:     0.025em;
  --letter-spacing-wider:    0.05em;
  --letter-spacing-widest:   0.1em;

  --measure-base:   65ch;
  --measure-narrow: 45ch;
  --measure-wide:   80ch;

  /* ─── SPACING ───────────────────────────────────────────────────── */
  --section-padding-y: var(--primitive-space-12);
  --section-padding-x: var(--primitive-space-4);
  --component-gap:     var(--primitive-space-6);
  --element-gap:       var(--primitive-space-2);
  --content-gap:       var(--primitive-space-4);

  --space-1:  var(--primitive-space-1);
  --space-2:  var(--primitive-space-2);
  --space-3:  var(--primitive-space-3);
  --space-4:  var(--primitive-space-4);
  --space-6:  var(--primitive-space-6);
  --space-8:  var(--primitive-space-8);
  --space-12: var(--primitive-space-12);
  --space-16: var(--primitive-space-16);

  /* ─── LAYOUT ────────────────────────────────────────────────────── */
  --container-sm:   var(--primitive-container-sm);
  --container-md:   var(--primitive-container-md);
  --container-lg:   var(--primitive-container-lg);
  --container-xl:   var(--primitive-container-xl);
  --container-2xl:  var(--primitive-container-2xl);
  --container-base: var(--primitive-container-xl);

  --grid-cols-2: repeat(2, 1fr);
  --grid-cols-3: repeat(3, 1fr);
  --grid-cols-4: repeat(4, 1fr);

  /* ─── EFFECTS ───────────────────────────────────────────────────── */
  --radius-none:  var(--primitive-radius-none);
  --radius-sm:    var(--primitive-radius-sm);
  --radius-md:    var(--primitive-radius-md);
  --radius-lg:    var(--primitive-radius-lg);
  --radius-full:  var(--primitive-radius-full);

  --shadow-sm:  var(--primitive-shadow-sm);
  --shadow-md:  var(--primitive-shadow-md);
  --shadow-lg:  var(--primitive-shadow-lg);
  --shadow-xl:  var(--primitive-shadow-xl);

  --transition-fast:   var(--primitive-transition-fast);
  --transition-base:   var(--primitive-transition-base);
  --transition-slow:   var(--primitive-transition-slow);

  --ease-out:    cubic-bezier(0, 0, 0.2, 1);
  --ease-in:     cubic-bezier(0.4, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* ─── GENERATEPRESS VARIABLE MAPPING ────────────────────────────── */
  --contrast:   var(--color-text-primary);
  --contrast-2: var(--color-text-secondary);
  --contrast-3: var(--color-text-muted);
  --base:       var(--color-bg-page);
  --base-2:     var(--color-bg-subtle);
  --base-3:     var(--color-bg-muted);
  --accent:     var(--color-brand-red);
}
```

---

## TIER 3 — COMPONENT TOKENS

```css
.btn {
  --btn-font-family:    var(--font-family-headline);
  --btn-font-weight:    var(--font-weight-black);
  --btn-font-size:      var(--text-base);
  --btn-letter-spacing: var(--letter-spacing-wide);
  --btn-padding-y:      var(--space-2);
  --btn-padding-x:      var(--space-4);
  --btn-radius:         var(--radius-sm);
  --btn-transition:     var(--transition-base);
}

.btn--primary {
  --btn-bg:           var(--color-brand-red);
  --btn-color:        #fff;
  --btn-border:       var(--color-brand-red);
  --btn-bg-hover:     var(--color-interactive-hover);
  --btn-border-hover: var(--color-interactive-hover);
}

.btn--secondary {
  --btn-bg:          transparent;
  --btn-color:       var(--color-brand-red);
  --btn-border:      var(--color-brand-red);
  --btn-bg-hover:    var(--color-brand-red);
  --btn-color-hover: #fff;
}

.btn--ghost {
  --btn-bg:          transparent;
  --btn-color:       var(--color-text-inverse);
  --btn-border:      var(--color-brand-white);
  --btn-bg-hover:    var(--color-brand-white);
  --btn-color-hover: var(--color-brand-black);
}

.card {
  --card-bg:           var(--color-bg-surface);
  --card-border:       var(--color-border-default);
  --card-radius:       var(--radius-md);
  --card-shadow:       var(--shadow-sm);
  --card-shadow-hover: var(--shadow-md);
  --card-padding:      var(--space-4);
  --card-gap:          var(--space-2);
}

.form {
  --form-gap:                var(--space-4);
  --form-label-size:         var(--text-sm);
  --form-label-weight:       var(--font-weight-semibold);
  --form-label-color:        var(--color-text-primary);
  --form-input-bg:           var(--color-bg-muted);
  --form-input-border:       var(--color-border-default);
  --form-input-border-focus: var(--color-interactive-focus);
  --form-input-radius:       var(--radius-sm);
  --form-input-padding:      var(--space-2) var(--space-3);
  --form-input-size:         var(--text-base);
  --form-input-color:        var(--color-text-primary);
}

.section--dark {
  --section-bg:         var(--color-bg-dark);
  --section-text:       var(--color-text-inverse);
  --section-text-muted: var(--color-brand-gray);
}

.section--light {
  --section-bg:         var(--color-bg-page);
  --section-text:       var(--color-text-primary);
  --section-text-muted: var(--color-text-secondary);
}

.section--subtle {
  --section-bg:         var(--color-bg-subtle);
  --section-text:       var(--color-text-primary);
  --section-text-muted: var(--color-text-secondary);
}

.nav {
  --nav-bg:            var(--color-bg-dark);
  --nav-text:          var(--color-text-inverse);
  --nav-text-hover:    var(--color-brand-red);
  --nav-height:        4rem;
  --nav-height-mobile: 3.5rem;
  --nav-z-index:       100;
}

.hero {
  --hero-min-height:    100svh;
  --hero-overlay-color: rgba(0,0,0,0.6);
  --hero-text:          var(--color-text-inverse);
  --hero-subtext:       rgba(255,255,255,0.85);
}

.testimonial {
  --testimonial-bg:          var(--color-bg-surface);
  --testimonial-border:      var(--color-border-default);
  --testimonial-accent:      var(--color-brand-red);
  --testimonial-quote-size:  var(--text-lg);
  --testimonial-name-weight: var(--font-weight-bold);
}
```

---

## GLOBAL CSS FOUNDATION

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  max-width: 100%;
  overflow-x: hidden;
}

html { scroll-behavior: smooth; }

body {
  font-family: var(--font-family-body);
  font-size: var(--text-base);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-base);
  color: var(--color-text-primary);
  background-color: var(--color-bg-page);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

h1, h2, h3 {
  font-family: var(--font-family-headline);
  font-weight: var(--font-weight-black);
  line-height: var(--line-height-tight);
  letter-spacing: var(--letter-spacing-tight);
  color: inherit;
}

h4, h5, h6 {
  font-family: var(--font-family-body);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: inherit;
}

h1 { font-size: clamp(var(--text-3xl), 5vw, var(--text-5xl)); }
h2 { font-size: clamp(var(--text-2xl), 4vw, var(--text-4xl)); }
h3 { font-size: clamp(var(--text-xl),  3vw, var(--text-3xl)); }
h4 { font-size: var(--text-xl); }
h5 { font-size: var(--text-lg); }
h6 { font-size: var(--text-base); }

p {
  font-size: var(--text-base);
  line-height: var(--line-height-base);
  max-width: var(--measure-base);
}

img, video {
  max-width: 100%;
  height: auto;
  display: block;
  filter: grayscale(100%);
}

img.no-grayscale, .logo img, .icon img { filter: none; }

a {
  color: var(--color-brand-red);
  text-decoration: underline;
  transition: color var(--transition-base) var(--ease-out);
}

a:hover { color: var(--color-interactive-hover); }

:focus-visible {
  outline: 2px solid var(--color-interactive-focus);
  outline-offset: 3px;
}

:focus:not(:focus-visible) { outline: none; }

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.skip-nav {
  position: absolute;
  top: -100%;
  left: var(--space-2);
  z-index: 9999;
  padding: var(--space-2) var(--space-4);
  background: var(--color-brand-red);
  color: #fff !important;
  font-family: var(--font-family-headline);
  font-weight: var(--font-weight-black);
  text-decoration: none;
  transition: top var(--transition-fast);
}

.skip-nav:focus { top: var(--space-2); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

.container {
  width: 100%;
  max-width: var(--container-base);
  margin-inline: auto;
  padding-inline: var(--section-padding-x);
}

.container--narrow { max-width: var(--container-md); }
.container--wide   { max-width: var(--container-2xl); }

.entry-content--breakout {
  display: grid;
  grid-template-columns:
    minmax(var(--space-4), 1fr)
    minmax(auto, var(--container-xl))
    minmax(var(--space-4), 1fr);
}

.entry-content--breakout > * { grid-column: 2; }
.entry-content--breakout > .full-bleed { grid-column: 1 / -1; }

[class*="btn--primary"],
[class*="--red"] { color: #fff !important; }
```

---

## GOOGLE FONTS LOADING

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## MOBILE-FIRST BREAKPOINTS

```
xs:   320px  (no query — default styles)
sm:   480px  @media (min-width: 480px)
md:   768px  @media (min-width: 768px)  ← single→multi-column transition
lg:  1024px  @media (min-width: 1024px)
xl:  1280px  @media (min-width: 1280px)
2xl: 1536px  @media (min-width: 1536px)
```

Always min-width. Never max-width. Mobile-first is non-negotiable.

---

## FLUID TYPOGRAPHY

```css
/* Hero headline: ~51px → ~90px across 320px → 1280px */
.hero__title {
  font-size: clamp(var(--text-3xl), 2.3394rem + 4.088vw, var(--text-5xl));
}

/* Section heading: ~38px → ~67px */
.section__title {
  font-size: clamp(var(--text-2xl), 1.65rem + 3.35vw, var(--text-4xl));
}

/* Body subtle fluid: 16px → 18px */
.prose {
  font-size: clamp(var(--text-base), 0.9168rem + 0.416vw, 1.125rem);
}
```

---

## TOKEN DECISION TREE

```
Color value?      → var(--color-[role]) — NEVER a hex code
Font-size?        → var(--text-N) or clamp() with tokens
Spacing?          → var(--section-padding-y/x) or var(--space-N)
Border-radius?    → var(--radius-sm) default — Swiss = sharp
Shadow?           → var(--shadow-sm) cards, var(--shadow-lg) modals
Transition?       → var(--transition-base) default
```

---

## ANIMATION RULES

Only animate `transform` and `opacity`. GPU-composited only.
Never animate width, height, margin, padding, top, left.

```css
.btn {
  transition:
    background-color var(--transition-base) var(--ease-out),
    border-color var(--transition-base) var(--ease-out),
    color var(--transition-base) var(--ease-out),
    transform var(--transition-fast) var(--ease-out);
}

.btn:hover  { transform: translateY(-1px); }
.btn:active { transform: translateY(0); }
```
