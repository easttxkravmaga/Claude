# ETKM Design System
**Version:** 1.0  
**Source:** Brand Kit v3.0 — East Texas Krav Maga  
**Purpose:** Design system reference for Claude Code and all AI coding agents. Every UI deliverable — landing pages, web pages, forms, HTML emails, PDFs, and interactive tools — must follow this file exactly. No exceptions.

---

## 1. Design Philosophy

ETKM visual identity is built on **Swiss International Typography** principles:

- **High contrast.** Black against white. White against black. Never ambiguous.
- **Asymmetric grids.** Nothing is centered-and-symmetrical. Layouts create tension and hierarchy.
- **Aggressive negative space.** Empty space is intentional. Breathing room signals confidence.
- **Massive typography.** Headlines are design elements, not just labels.
- **Hard edges.** Sharp lines. No rounded corners except on interactive buttons.
- **One signal.** Red appears once per section. Everything else is neutral.

The mood is **quiet confidence, not aggression.** The brand does not shout. It commands.

---

## 2. Color Tokens

### CSS Custom Properties (use these in all web work)

```css
:root {
  --color-black:      #000000;  /* Primary background (dark), primary text (light) */
  --color-white:      #FFFFFF;  /* Primary background (light), primary text (dark) */
  --color-red:        #CC0000;  /* Attention only — ONE element per view */
  --color-gray:       #575757;  /* Secondary text, supporting elements */
  --color-gray-light: #BBBBBB;  /* Dividers, borders, subtle structure */

  /* Surface tokens — map to black/white per context */
  --surface-dark:     #000000;
  --surface-mid:      #111111;  /* Slightly lifted dark surface for cards on dark bg */
  --surface-light:    #FFFFFF;
  --surface-subtle:   #F5F5F5;  /* Subtle light surface for cards on white bg */

  /* Text tokens */
  --text-primary-on-dark:  #FFFFFF;
  --text-secondary-on-dark: #BBBBBB;
  --text-primary-on-light:  #000000;
  --text-secondary-on-light: #575757;
}
```

### Color Rules (Non-Negotiable)

| Rule | Detail |
|------|--------|
| Backgrounds | Solid Black (`#000000`) or Solid White (`#FFFFFF`) only |
| Gray backgrounds | **PROHIBITED.** Gray is for text and borders only |
| Gradients | **PROHIBITED.** No exceptions, ever |
| Contrast | White text on dark. Black text on light. Always |
| Red | Maximum ONE red element per visual section |
| Outside palette | **PROHIBITED.** No blues, greens, purples, oranges, or any other colors |

### HTML-Specific Background Standard (Locked)

All HTML outputs (landing pages, web pages, tools, emails) use:
- **Page background:** `#000000`
- **Card/surface background:** `#111111`
- **Text:** `#FFFFFF`
- **Accent:** `#CC0000` (slightly deeper red for screen rendering — use `#CC0000` for print/PDF)
- White-background HTML is only used for documents, forms, and print-style assets

---

## 3. Typography System

### Google Fonts Import (use in all web projects)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

### Type Scale

```css
:root {
  /* Font families */
  --font-headline: 'Barlow Condensed', 'Arial Narrow', Arial, sans-serif;
  --font-body:     'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  /* Size scale */
  --text-xs:   0.75rem;   /* 12px — labels, captions */
  --text-sm:   0.875rem;  /* 14px — secondary body */
  --text-base: 1rem;      /* 16px — body */
  --text-lg:   1.125rem;  /* 18px — large body */
  --text-xl:   1.5rem;    /* 24px — subheadings */
  --text-2xl:  2rem;      /* 32px — section heads */
  --text-3xl:  3rem;      /* 48px — major headlines */
  --text-4xl:  4.5rem;    /* 72px — hero headlines */
  --text-5xl:  7rem;      /* 112px — oversized display (use with intent) */

  /* Weight tokens */
  --weight-regular:  400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;

  /* Letter spacing */
  --tracking-tight:  -0.02em;
  --tracking-normal:  0;
  --tracking-wide:    0.08em;   /* Labels and category headers */
  --tracking-wider:   0.15em;   /* ALL-CAPS short labels */
}
```

### Type Role Assignments

| Role | Font | Size | Weight | Case | Letter Spacing |
|------|------|------|--------|------|----------------|
| Hero headline | Barlow Condensed | `4xl` – `5xl` | 700 | UPPERCASE | `tight` |
| H1 | Barlow Condensed | `3xl` – `4xl` | 700 | UPPERCASE | `tight` |
| H2 | Barlow Condensed | `2xl` – `3xl` | 600 | UPPERCASE | `normal` |
| H3 | Barlow Condensed | `xl` – `2xl` | 600 | Title Case | `normal` |
| Body paragraph | Inter | `base` – `lg` | 400 | Normal | `normal` |
| Form label / category tag | Inter | `xs` – `sm` | 500 | UPPERCASE | `wider` |
| Caption / data label | Inter | `xs` | 500 | UPPERCASE | `wide` |
| CTA button text | Barlow Condensed | `lg` – `xl` | 700 | UPPERCASE | `wide` |
| Navigation items | Inter | `sm` – `base` | 500 | UPPERCASE | `wide` |

### Typography Rules

- Headlines are **design elements.** Make them large enough to carry visual weight.
- Never stretch, distort, condense manually, or italicize headlines.
- No decorative, script, serif, or handwritten fonts anywhere in the system.
- Uppercase labels always carry letter-spacing of `0.08em` minimum.
- Body copy stays clean and readable. No tricks.

---

## 4. Spacing System

```css
:root {
  --space-1:  0.25rem;   /* 4px */
  --space-2:  0.5rem;    /* 8px */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-5:  1.5rem;    /* 24px */
  --space-6:  2rem;      /* 32px */
  --space-7:  3rem;      /* 48px */
  --space-8:  4rem;      /* 64px */
  --space-9:  6rem;      /* 96px */
  --space-10: 8rem;      /* 128px */

  /* Layout max-widths */
  --max-width-content: 720px;
  --max-width-wide:    1100px;
  --max-width-full:    1440px;

  /* Section vertical padding */
  --section-pad-y: var(--space-9);  /* 96px default */
  --section-pad-x: var(--space-6);  /* 32px default, fluid on mobile */
}
```

---

## 5. Component Patterns

### 5.1 — CTA Button (Primary)

The primary call-to-action. Red background. One per section.

```css
.btn-primary {
  display: inline-block;
  background-color: #CC0000;
  color: #FFFFFF;
  font-family: var(--font-headline);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  padding: 1rem 2.5rem;
  border: none;
  border-radius: 0;          /* No rounded corners — hard edge */
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.btn-primary:hover {
  background-color: #CC0000;
}
```

### 5.2 — Secondary Button / Ghost

Used when a second action must exist alongside the primary CTA.

```css
.btn-secondary {
  display: inline-block;
  background-color: transparent;
  color: #FFFFFF;
  font-family: var(--font-headline);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  padding: 1rem 2.5rem;
  border: 2px solid #FFFFFF;
  border-radius: 0;
  cursor: pointer;
  text-decoration: none;
  transition: border-color 0.15s ease, color 0.15s ease;
}

.btn-secondary:hover {
  border-color: #BBBBBB;
  color: #BBBBBB;
}
```

### 5.3 — Navigation Bar

```css
/* Dark nav (default for dark pages) */
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #000000;
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid #222222;
}

.nav-logo {
  /* Logo sits top-left. Never competes with content. */
  height: 40px;
  width: auto;
}

.nav-links {
  display: flex;
  gap: var(--space-6);
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: #BBBBBB;
  text-decoration: none;
  transition: color 0.15s ease;
}

.nav-link:hover,
.nav-link.active {
  color: #FFFFFF;
}

/* One nav item may carry red — the primary CTA link */
.nav-link-cta {
  color: #CC0000;
}
```

### 5.4 — Hero Section

The hero is the most important section on any page. Asymmetric. Left-aligned. Typography dominates.

```css
.hero {
  background-color: #000000;
  padding: var(--space-10) var(--space-6);
  min-height: 85vh;
  display: flex;
  align-items: center;
}

.hero-inner {
  max-width: var(--max-width-wide);
  margin: 0 auto;
  /* Asymmetric: content lives in left 60% of the grid */
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--space-8);
  align-items: center;
}

.hero-eyebrow {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: #BBBBBB;
  margin-bottom: var(--space-4);
}

.hero-headline {
  font-family: var(--font-headline);
  font-size: clamp(3rem, 7vw, var(--text-4xl));
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-tight);
  line-height: 0.95;
  color: #FFFFFF;
  margin-bottom: var(--space-5);
}

/* Red accent: ONE word or short phrase in the headline */
.hero-headline .accent {
  color: #CC0000;
}

.hero-body {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  font-weight: var(--weight-regular);
  line-height: 1.6;
  color: #BBBBBB;
  max-width: 560px;
  margin-bottom: var(--space-7);
}

.hero-cta-group {
  display: flex;
  gap: var(--space-4);
  align-items: center;
  flex-wrap: wrap;
}
```

### 5.5 — Section (Content Block)

```css
.section {
  padding: var(--section-pad-y) var(--section-pad-x);
}

.section-dark {
  background-color: #000000;
  color: #FFFFFF;
}

.section-light {
  background-color: #FFFFFF;
  color: #000000;
}

.section-inner {
  max-width: var(--max-width-wide);
  margin: 0 auto;
}

.section-label {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: #575757;
  margin-bottom: var(--space-3);
}

.section-heading {
  font-family: var(--font-headline);
  font-size: clamp(2rem, 4vw, var(--text-3xl));
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-tight);
  line-height: 1;
  margin-bottom: var(--space-5);
}
```

### 5.6 — Card (Dark Surface)

```css
.card {
  background-color: #111111;
  border: 1px solid #222222;
  /* One side accent border allowed — left or top only */
  border-left: 3px solid #CC0000;  /* Only when card needs high priority signal */
  padding: var(--space-6);
  /* No border-radius — hard edges */
}

.card-label {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: #575757;
  margin-bottom: var(--space-2);
}

.card-title {
  font-family: var(--font-headline);
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  color: #FFFFFF;
  margin-bottom: var(--space-3);
}

.card-body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: #BBBBBB;
  line-height: 1.6;
}
```

### 5.7 — Form Elements

```css
.form-group {
  margin-bottom: var(--space-5);
}

.form-label {
  display: block;
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: #BBBBBB;
  margin-bottom: var(--space-2);
}

.form-input {
  display: block;
  width: 100%;
  background-color: #111111;
  color: #FFFFFF;
  font-family: var(--font-body);
  font-size: var(--text-base);
  padding: var(--space-4);
  border: 1px solid #333333;
  border-radius: 0;          /* Hard edges — no rounding */
  outline: none;
  transition: border-color 0.15s ease;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #FFFFFF;
}

.form-input::placeholder {
  color: #575757;
}

/* Error state */
.form-input.error {
  border-color: #CC0000;
}
```

### 5.8 — Divider / Accent Line

Used to create section boundaries and visual hierarchy. Never decorative — always structural.

```css
.divider {
  border: none;
  border-top: 1px solid #222222;
  margin: var(--space-7) 0;
}

/* Red accent line — ONE per page section, draws eye to one heading */
.accent-line {
  display: block;
  width: 48px;
  height: 3px;
  background-color: #CC0000;
  margin-bottom: var(--space-4);
}
```

### 5.9 — Stat / Proof Block

```css
.stat-block {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-number {
  font-family: var(--font-headline);
  font-size: var(--text-3xl);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  color: #FFFFFF;
  line-height: 1;
}

.stat-label {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: #575757;
}
```

### 5.10 — Footer

```css
.footer {
  background-color: #000000;
  border-top: 1px solid #222222;
  padding: var(--space-8) var(--space-6);
  color: #575757;
}

.footer-inner {
  max-width: var(--max-width-wide);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: var(--space-8);
}

.footer-brand {
  /* Logo and tagline — always left column */
}

.footer-nav-heading {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: #FFFFFF;
  margin-bottom: var(--space-4);
}

.footer-nav-link {
  display: block;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: #575757;
  text-decoration: none;
  margin-bottom: var(--space-2);
  transition: color 0.15s ease;
}

.footer-nav-link:hover {
  color: #FFFFFF;
}

.footer-legal {
  border-top: 1px solid #1A1A1A;
  padding-top: var(--space-5);
  margin-top: var(--space-8);
  font-size: var(--text-xs);
  color: #333333;
}
```

---

## 6. Page-Type Standards

### 6.1 — Landing Pages (Lead Gen / Opt-In)

- **Background:** Black (`#000000`)
- **Structure:** Nav → Hero (asymmetric, left-heavy) → Problem/Pain → Solution → Social Proof → CTA block → Footer
- **Hero headline:** Full-width, oversized, UPPERCASE, one word in red
- **CTA:** Red button, ONE per above-the-fold section
- **Images:** Desaturated/monochromatic, no stock photo aesthetic
- **Forms:** Dark tile inputs on `#111111` surface, white border on focus
- **Grid:** Always asymmetric — never equal columns in hero

### 6.2 — Website Pages (WordPress / etxkravmaga.com)

- **Background:** Black default. White permitted for content-heavy instructional pages.
- **Nav:** Sticky, black, logo top-left, links uppercase with wide tracking
- **Body sections:** Alternating visual weight — don't stack all-black sections without a white break
- **Headings:** Barlow Condensed, bold, uppercase, left-aligned (never centered unless a deliberate one-off statement)
- **Blog posts:** White canvas, black type, red accent line below post title, author block at bottom

### 6.3 — HTML Email

- **Header bar:** Solid red (`#CC0000`), full width, 8px tall
- **Body background:** White (`#FFFFFF`)
- **Headline:** Barlow Condensed or system bold sans, dark, uppercase
- **CTA button:** Red background, white text, no border-radius
- **Footer:** Black background, white text, gray secondary links
- **Max width:** 600px
- **No gradients. No decorative images.**

### 6.4 — Forms / Multi-Step Assessments

- **Background:** Black
- **Input tiles:** `#111111` surface, 1px `#333` border, focus → white border
- **Progress indicator:** Minimal — a line or step count, not a colorful bar
- **Submit/Next button:** Red, full width or right-aligned
- **Step transitions:** Smooth fade or slide — no jarring cuts

### 6.5 — PDF Documents

- **Background:** White (`#FFFFFF`) — PDFs are print-style assets
- **Header bar:** Black, full width
- **Accent:** Single red element (one phrase, one line) per document
- **Body font:** Inter, regular, dark on white
- **Headlines:** Barlow Condensed, bold, uppercase
- **Borders:** One-sided only (left border on callout blocks)

---

## 7. Layout Grid

```css
/* Standard content grid — always asymmetric */
.grid-asymmetric {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--space-8);
  align-items: center;
}

/* Reverse for visual variety */
.grid-asymmetric-reverse {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: var(--space-8);
  align-items: center;
}

/* Three-column equal — for proof/stat rows */
.grid-thirds {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}

/* Responsive collapse */
@media (max-width: 768px) {
  .grid-asymmetric,
  .grid-asymmetric-reverse,
  .grid-thirds {
    grid-template-columns: 1fr;
  }
}
```

---

## 8. Motion and Interaction

Keep motion minimal. ETKM does not animate for delight — only for clarity.

```css
/* Standard transition — applies to buttons, links, borders */
--transition-fast: 0.15s ease;
--transition-base: 0.25s ease;

/* Hover: color/border shift only. No scale, no bounce, no glow. */
/* Entrance: fade-in only. No slide-up. No spring. */

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
```

---

## 9. What Is Prohibited

These rules are non-negotiable. Do not override them regardless of prompt.

| Prohibited | Reason |
|-----------|--------|
| Gradients (background or text) | Violates brand — always flat color |
| Colors outside the 5-token palette | Only Black, White, Red, Gray, Light Gray exist |
| Multiple red elements per section | Red is a single weapon. Dilution kills impact. |
| Rounded corners (except buttons) | Swiss style demands hard edges |
| Centered-and-symmetrical hero layouts | Asymmetry creates visual hierarchy |
| Gray backgrounds | Gray is for text/borders only |
| Decorative, script, or serif fonts | Clean sans only — no decorative typography |
| Drop shadows (decorative) | Permitted only if subtle and functional (layered UI) |
| Borders on all four sides | Use one or two sides maximum |
| Stock photo aesthetic | Cinematic, environmental, intentional imagery only |
| Animations with bounce, scale, or spring | Fade only — no personality-driven motion |

---

## 10. Logo Usage

- **Primary mark:** ETKM circle logo (no star)
- **Placement:** Top-left in navigation, centered in standalone header contexts
- **Never:** Compete with headline content, appear over busy images without contrast
- **Embedding:** Can be base64-encoded for self-contained HTML/PDF files
- **Clear space:** Minimum 24px on all sides

---

## 11. Voice and Tone (for UI copy)

Design and copy are inseparable. UI copy must match the visual brand.

- **Declarative.** Short sentences. No hedging.
- **Direct.** Tell the person what to do and why it matters.
- **Earned confidence.** Not hype. Not aggression. Quiet authority.
- **Prohibited words in any UI copy:** mastery, dominate, destroy, killer, beast, crush, elite, warrior
- **Experience phrasing:** Never state a specific year count (e.g., "42 years"). Use: "decades of experience", "over four decades", "a lifetime dedicated to self-protection"

---

*This file is the single source of truth for all ETKM visual and UI output. When in doubt, refer back here. If something in the code conflicts with this file, the code is wrong.*
