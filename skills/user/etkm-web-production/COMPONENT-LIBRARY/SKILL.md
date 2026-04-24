# ETKM Component Library
## File 3 of 4 — etkm-web-production skill series

**Version:** 1.0
**Built:** 2026-04-24
**Depends on:** CSS-SYSTEM.md v1.0
**Applies to:** All HTML/CSS production for ETKM

---

## COMPONENT SYSTEM LAW

1. Every component CSS value references a token. No raw hex,
   no arbitrary px, no hardcoded rem values outside the scale.
2. Every component uses BEM naming. Elements flat to block.
   Modifiers always accompany base class.
3. Every component is mobile-first. Base CSS = mobile.
   min-width queries add desktop behavior.
   Single→multi-column at 768px minimum.
4. Every component uses semantic HTML.
   No <main>, global <header>, global <footer> in injected partials.
   H1 owned by WordPress. Injected HTML starts at H2.
5. Interactive elements are native HTML only.
   Buttons = <button type="button">. Never <div onclick>.
6. All images: width + height attributes, alt attribute,
   filter: grayscale(100%) applied globally via CSS-SYSTEM.md.

---

## 1. PRIMARY CTA BUTTON

Usage: Primary conversion action. One per section. Red bg, white text.
Text: verb + outcome. Never "Click Here" or "Submit".

```html
<button type="button" class="btn btn--primary">
  Start Your Free Trial
</button>

<a href="#trial" class="btn btn--primary">
  Start Your Free Trial
</a>
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-1);
  padding-block: var(--btn-padding-y);
  padding-inline: var(--btn-padding-x);
  font-family: var(--btn-font-family);
  font-size: var(--btn-font-size);
  font-weight: var(--btn-font-weight);
  line-height: 1;
  letter-spacing: var(--btn-letter-spacing);
  text-transform: uppercase;
  text-decoration: none;
  border-width: 2px;
  border-style: solid;
  border-radius: var(--btn-radius);
  cursor: pointer;
  white-space: nowrap;
  transition:
    background-color var(--transition-base) var(--ease-out),
    border-color var(--transition-base) var(--ease-out),
    color var(--transition-base) var(--ease-out),
    transform var(--transition-fast) var(--ease-out);
  min-height: 44px;
  min-width: 44px;
}

.btn--primary {
  background-color: var(--btn-bg);
  color: var(--btn-color);
  border-color: var(--btn-border);
}

.btn--primary:hover {
  background-color: var(--btn-bg-hover);
  border-color: var(--btn-border-hover);
  color: #fff !important;
  transform: translateY(-1px);
}

.btn--primary:active { transform: translateY(0); }

.btn--primary:focus-visible {
  outline: 2px solid var(--color-interactive-focus);
  outline-offset: 3px;
}
```

---

## 2. SECONDARY CTA BUTTON

Usage: Paired with primary. Lower-commitment action. Outlined red.

```html
<button type="button" class="btn btn--secondary">See How It Works</button>
<button type="button" class="btn btn--ghost">Learn More</button>
```

```css
.btn--secondary {
  background-color: transparent;
  color: var(--color-brand-red);
  border-color: var(--color-brand-red);
}

.btn--secondary:hover {
  background-color: var(--color-brand-red);
  color: #fff;
  transform: translateY(-1px);
}

.btn--ghost {
  background-color: transparent;
  color: var(--color-text-inverse);
  border-color: var(--color-brand-white);
}

.btn--ghost:hover {
  background-color: var(--color-brand-white);
  color: var(--color-brand-black);
  transform: translateY(-1px);
}
```

---

## 3. FULL-WIDTH HERO SECTION

Usage: First section on landing pages. One per page. H2 headline.
LCP image: HTML img with fetchpriority="high". Never CSS background.
min-height: 100svh (svh not vh — solves mobile browser chrome).

```html
<section class="hero" aria-labelledby="hero-title">
  <img
    src="hero-bg.jpg"
    alt=""
    class="hero__bg"
    width="1920"
    height="1080"
    fetchpriority="high"
    decoding="async">
  <div class="hero__overlay" aria-hidden="true"></div>
  <div class="hero__content container">
    <p class="hero__eyebrow">East Texas Krav Maga</p>
    <h2 id="hero-title" class="hero__title">
      Real Self-Defense.<br>
      <span class="hero__title-accent">Real Confidence.</span>
    </h2>
    <p class="hero__desc">
      Practical protection skills for East Texans — no experience required.
    </p>
    <div class="hero__actions">
      <a href="#trial" class="btn btn--primary">Start Your Free Trial</a>
      <a href="#how-it-works" class="btn btn--ghost">See How It Works</a>
    </div>
  </div>
</section>
```

```css
.hero {
  position: relative;
  display: grid;
  place-items: center;
  min-height: var(--hero-min-height);
  padding-block: var(--space-16);
  overflow: hidden;
  background-color: var(--color-bg-dark);
}

.hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

.hero__overlay {
  position: absolute;
  inset: 0;
  background-color: var(--hero-overlay-color);
  z-index: 1;
}

.hero__content {
  position: relative;
  z-index: 2;
  text-align: left;
  max-width: var(--container-lg);
}

.hero__eyebrow {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-widest);
  text-transform: uppercase;
  color: var(--color-brand-red);
  margin-bottom: var(--space-2);
  max-width: none;
}

.hero__title {
  font-size: clamp(var(--text-3xl), 2.3394rem + 4.088vw, var(--text-5xl));
  color: var(--hero-text);
  margin-bottom: var(--space-4);
  text-wrap: balance;
}

.hero__title-accent {
  color: var(--color-brand-red);
  display: block;
}

.hero__desc {
  font-size: clamp(var(--text-base), 0.9168rem + 0.416vw, var(--text-lg));
  color: var(--hero-subtext);
  margin-bottom: var(--space-6);
  max-width: var(--measure-narrow);
}

.hero__actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  align-items: flex-start;
}

@media (min-width: 480px) {
  .hero__actions {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
```

---

## 4. SPLIT HERO SECTION

Usage: When image needs equal visual weight with copy.
Text left, image right (desktop). Stacked on mobile.

```html
<section class="hero-split" aria-labelledby="hero-split-title">
  <div class="hero-split__content container">
    <div class="hero-split__text">
      <p class="hero-split__eyebrow">Fight Back ETX</p>
      <h2 id="hero-split-title" class="hero-split__title">
        Self-Defense for Women in East Texas
      </h2>
      <p class="hero-split__desc">
        Practical Krav Maga techniques in a supportive environment.
        No experience needed.
      </p>
      <a href="#trial" class="btn btn--primary">Attend a Free Trial</a>
    </div>
    <div class="hero-split__media">
      <img
        src="fight-back-etx.jpg"
        alt="Women practicing self-defense techniques in class"
        class="hero-split__img"
        width="800"
        height="600"
        fetchpriority="high">
    </div>
  </div>
</section>
```

```css
.hero-split {
  background-color: var(--color-bg-page);
  padding-block: var(--section-padding-y);
}

.hero-split__content {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--component-gap);
  align-items: center;
}

@media (min-width: 768px) {
  .hero-split__content {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-12);
  }
}

.hero-split__text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-4);
}

.hero-split__eyebrow {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-widest);
  text-transform: uppercase;
  color: var(--color-brand-red);
  max-width: none;
}

.hero-split__title {
  font-size: clamp(var(--text-2xl), 1.65rem + 3.35vw, var(--text-4xl));
  color: var(--color-text-primary);
  text-wrap: balance;
}

.hero-split__img { width: 100%; height: auto; }
```

---

## 5. THREE-STEP PLAN SECTION

Usage: StoryBrand core section. Always exactly 3 steps. Required on
every landing page. ETKM steps:
1. Attend a Free Trial Lesson
2. Get Your Personalized Training Blueprint
3. Become a Confident, Capable Protector
Step numbers: red circle, white text.

```html
<section class="plan" aria-labelledby="plan-title">
  <div class="container">
    <div class="plan__header">
      <h2 id="plan-title" class="plan__title">How It Works</h2>
      <p class="plan__intro">Three simple steps to real confidence.</p>
    </div>
    <div class="plan__grid">
      <article class="plan-step">
        <div class="plan-step__number" aria-hidden="true">1</div>
        <h3 class="plan-step__title">Attend a Free Trial Lesson</h3>
        <p class="plan-step__desc">
          Come in with zero experience. See what Krav Maga feels like
          firsthand — no commitment, no pressure.
        </p>
      </article>
      <article class="plan-step">
        <div class="plan-step__number" aria-hidden="true">2</div>
        <h3 class="plan-step__title">Get Your Personalized Training Blueprint</h3>
        <p class="plan-step__desc">
          We assess where you are and map out exactly what you need.
        </p>
      </article>
      <article class="plan-step">
        <div class="plan-step__number" aria-hidden="true">3</div>
        <h3 class="plan-step__title">Become a Confident, Capable Protector</h3>
        <p class="plan-step__desc">
          Train with a proven system used by everyday people to protect
          themselves and the people they love.
        </p>
      </article>
    </div>
    <div class="plan__cta">
      <a href="#trial" class="btn btn--primary">Start with a Free Trial</a>
    </div>
  </div>
</section>
```

```css
.plan {
  padding-block: var(--section-padding-y);
  background-color: var(--color-bg-subtle);
}

.plan__header {
  text-align: center;
  max-width: var(--container-md);
  margin-inline: auto;
  margin-bottom: var(--space-12);
}

.plan__title {
  font-size: clamp(var(--text-2xl), 1.65rem + 3.35vw, var(--text-4xl));
  color: var(--color-text-primary);
  margin-bottom: var(--space-3);
}

.plan__intro {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  max-width: var(--measure-narrow);
  margin-inline: auto;
}

.plan__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--component-gap);
}

@media (min-width: 768px) {
  .plan__grid { grid-template-columns: repeat(3, 1fr); }
}

.plan-step {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--element-gap);
  padding: var(--space-6);
  background-color: var(--color-bg-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.plan-step__number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  background-color: var(--color-brand-red);
  color: #fff;
  border-radius: var(--radius-full);
  font-family: var(--font-family-headline);
  font-weight: var(--font-weight-black);
  font-size: var(--text-xl);
  line-height: 1;
  flex-shrink: 0;
}

.plan-step__title {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-black);
  color: var(--color-text-primary);
}

.plan-step__desc {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.plan__cta {
  display: flex;
  justify-content: center;
  margin-top: var(--space-12);
}
```

---

## 6. TWO-COLUMN FEATURE SECTION

Usage: Program details, instructor story, benefit elaboration.
Text-left default. Add .feature--reverse for text-right.

```html
<section class="feature" aria-labelledby="feature-title-1">
  <div class="container">
    <div class="feature__grid">
      <div class="feature__text">
        <p class="feature__eyebrow">Why Krav Maga</p>
        <h2 id="feature-title-1" class="feature__title">
          Practical Skills That Work in the Real World
        </h2>
        <p class="feature__desc">
          Krav Maga was developed for real situations — not tournaments.
        </p>
        <ul class="feature__list">
          <li class="feature__list-item">No experience required</li>
          <li class="feature__list-item">Works regardless of size or strength</li>
          <li class="feature__list-item">Builds confidence from day one</li>
        </ul>
        <a href="#trial" class="btn btn--primary">Attend a Free Trial</a>
      </div>
      <div class="feature__media">
        <img
          src="krav-maga-training.jpg"
          alt="Student practicing Krav Maga with instructor"
          class="feature__img"
          width="600"
          height="500"
          loading="lazy">
      </div>
    </div>
  </div>
</section>
```

```css
.feature {
  padding-block: var(--section-padding-y);
  background-color: var(--color-bg-page);
}

.feature__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--component-gap);
  align-items: center;
}

@media (min-width: 768px) {
  .feature__grid {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-12);
  }

  .feature--reverse .feature__grid { direction: rtl; }
  .feature--reverse .feature__grid > * { direction: ltr; }
}

.feature__text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-4);
}

.feature__eyebrow {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-widest);
  text-transform: uppercase;
  color: var(--color-brand-red);
  max-width: none;
}

.feature__title {
  font-size: clamp(var(--text-xl), 1.25rem + 2vw, var(--text-3xl));
  color: var(--color-text-primary);
  text-wrap: balance;
}

.feature__list { list-style: none; display: flex; flex-direction: column; gap: var(--space-2); }

.feature__list-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-base);
}

.feature__list-item::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: var(--color-brand-red);
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.feature__img { width: 100%; height: auto; }
```

---

## 7. THREE-COLUMN BENEFIT GRID

Usage: 3 or 6 benefits. Icon + title + 1-2 sentence desc.
Dark variant: add .benefit-grid--dark.

```html
<section class="benefit-grid" aria-labelledby="benefits-title">
  <div class="container">
    <h2 id="benefits-title" class="benefit-grid__title">Why Train at ETKM</h2>
    <div class="benefit-grid__items">
      <div class="benefit-grid__item">
        <div class="benefit-grid__icon" aria-hidden="true">⚡</div>
        <h3 class="benefit-grid__item-title">Fast Results</h3>
        <p class="benefit-grid__item-desc">Usable skills from your very first class.</p>
      </div>
      <div class="benefit-grid__item">
        <div class="benefit-grid__icon" aria-hidden="true">🎯</div>
        <h3 class="benefit-grid__item-title">Proven System</h3>
        <p class="benefit-grid__item-desc">Same methods used by military worldwide — adapted for everyday people.</p>
      </div>
      <div class="benefit-grid__item">
        <div class="benefit-grid__icon" aria-hidden="true">🛡️</div>
        <h3 class="benefit-grid__item-title">Real Confidence</h3>
        <p class="benefit-grid__item-desc">A mindset shift that changes how you carry yourself every day.</p>
      </div>
    </div>
  </div>
</section>
```

```css
.benefit-grid {
  padding-block: var(--section-padding-y);
  background-color: var(--color-bg-page);
}

.benefit-grid__title {
  font-size: clamp(var(--text-2xl), 1.65rem + 3.35vw, var(--text-4xl));
  text-align: center;
  margin-bottom: var(--space-12);
}

.benefit-grid__items {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--component-gap);
}

@media (min-width: 768px) {
  .benefit-grid__items { grid-template-columns: repeat(3, 1fr); }
}

.benefit-grid__item {
  display: flex;
  flex-direction: column;
  gap: var(--element-gap);
  padding: var(--space-6);
  background-color: var(--color-bg-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.benefit-grid__icon { font-size: var(--text-2xl); line-height: 1; }
.benefit-grid__item-title { font-size: var(--text-xl); font-weight: var(--font-weight-black); }
.benefit-grid__item-desc { font-size: var(--text-base); color: var(--color-text-secondary); }
```

---

## 8. FULL-WIDTH CTA BAND

Usage: Conversion checkpoint between content sections.
Dark background. One CTA only. Short headline + one sentence.

```html
<section class="cta-band" aria-labelledby="cta-band-title">
  <div class="container">
    <div class="cta-band__content">
      <div>
        <h2 id="cta-band-title" class="cta-band__title">
          Ready to Train More and Fear Less?
        </h2>
        <p class="cta-band__desc">
          Your first class is free. No experience, no commitment.
        </p>
      </div>
      <a href="#trial" class="btn btn--primary cta-band__btn">
        Claim Your Free Trial
      </a>
    </div>
  </div>
</section>
```

```css
.cta-band {
  padding-block: var(--space-16);
  background-color: var(--color-bg-dark);
}

.cta-band__content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-6);
}

@media (min-width: 768px) {
  .cta-band__content {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .cta-band__btn { flex-shrink: 0; }
}

.cta-band__title {
  font-size: clamp(var(--text-xl), 1.25rem + 2vw, var(--text-3xl));
  color: var(--color-text-inverse);
  margin-bottom: var(--space-2);
  text-wrap: balance;
}

.cta-band__desc {
  font-size: var(--text-base);
  color: rgba(255,255,255,0.8);
  max-width: var(--measure-base);
}
```

---

## 9. TESTIMONIAL BLOCK

Usage: After plan section. Minimum 1, prefer 3. Real student words.
Include: quote, name, context. Red left border accent.

```html
<section class="testimonials" aria-labelledby="testimonials-title">
  <div class="container">
    <h2 id="testimonials-title" class="testimonials__title">What Our Students Say</h2>
    <div class="testimonials__grid">
      <blockquote class="testimonial">
        <div class="testimonial__quote-mark" aria-hidden="true">"</div>
        <p class="testimonial__text">
          I came in thinking I couldn't do this. Three months later
          I feel confident walking to my car at night. That's real.
        </p>
        <footer class="testimonial__footer">
          <cite class="testimonial__name">Sarah M.</cite>
          <span class="testimonial__context">Fight Back ETX Student</span>
        </footer>
      </blockquote>
    </div>
  </div>
</section>
```

```css
.testimonials {
  padding-block: var(--section-padding-y);
  background-color: var(--color-bg-subtle);
}

.testimonials__title {
  font-size: clamp(var(--text-2xl), 1.65rem + 3.35vw, var(--text-4xl));
  text-align: center;
  margin-bottom: var(--space-12);
}

.testimonials__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--component-gap);
}

@media (min-width: 768px) {
  .testimonials__grid { grid-template-columns: repeat(3, 1fr); }
}

.testimonial {
  position: relative;
  padding: var(--space-6) var(--space-6) var(--space-6) var(--space-8);
  background-color: var(--color-bg-surface);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--color-brand-red);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.testimonial__quote-mark {
  font-family: var(--font-family-headline);
  font-size: var(--text-6xl);
  font-weight: var(--font-weight-black);
  color: var(--color-brand-red);
  line-height: 1;
  position: absolute;
  top: var(--space-2);
  left: var(--space-4);
  opacity: 0.3;
  user-select: none;
}

.testimonial__text {
  font-size: var(--text-lg);
  font-style: italic;
  color: var(--color-text-primary);
  line-height: var(--line-height-relaxed);
  max-width: none;
}

.testimonial__footer { display: flex; flex-direction: column; gap: 0.25rem; margin-top: auto; }
.testimonial__name { font-style: normal; font-weight: var(--font-weight-bold); font-size: var(--text-base); }
.testimonial__context { font-size: var(--text-sm); color: var(--color-text-secondary); }
```

---

## 10. PROGRAM CARD

Usage: Program listing pages. Red accent bar top. Full-card clickable.
Max 6 per grid. Footer always at bottom via flex column.

```html
<div class="program-grid">
  <article class="program-card">
    <div class="program-card__accent" aria-hidden="true"></div>
    <div class="program-card__body">
      <h3 class="program-card__title">Fight Back ETX</h3>
      <p class="program-card__desc">
        Self-defense designed specifically for women.
      </p>
      <ul class="program-card__details">
        <li>Open to all fitness levels</li>
        <li>No experience required</li>
      </ul>
    </div>
    <div class="program-card__footer">
      <a href="/fight-back-etx" class="btn btn--primary program-card__cta">Learn More</a>
    </div>
  </article>
</div>
```

```css
.program-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--component-gap);
}

@media (min-width: 768px) { .program-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .program-grid { grid-template-columns: repeat(3, 1fr); } }

.program-card {
  display: flex;
  flex-direction: column;
  background-color: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  overflow: hidden;
  transition:
    box-shadow var(--transition-base) var(--ease-out),
    transform var(--transition-base) var(--ease-out);
}

.program-card:hover {
  box-shadow: var(--card-shadow-hover);
  transform: translateY(-2px);
}

.program-card__accent { height: 4px; background-color: var(--color-brand-red); flex-shrink: 0; }

.program-card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--card-padding);
}

.program-card__title { font-size: var(--text-xl); font-weight: var(--font-weight-black); }
.program-card__desc { font-size: var(--text-base); color: var(--color-text-secondary); }

.program-card__details { list-style: none; display: flex; flex-direction: column; gap: var(--space-1); }

.program-card__details li {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.program-card__details li::before {
  content: '';
  width: 6px;
  height: 6px;
  background-color: var(--color-brand-red);
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.program-card__footer { padding: var(--space-4); padding-top: 0; }
.program-card__cta { width: 100%; justify-content: center; }
```

---

## 11. LEAD CAPTURE FORM

Usage: Free trial signups, lead magnet downloads, event registration.
Every input: explicit label (for/id), autocomplete, native validation.
CTA text: specific action, never "Submit".
Font-size 16px minimum on inputs — prevents iOS auto-zoom.

```html
<section class="form-section" aria-labelledby="form-title">
  <div class="container container--narrow">
    <div class="form-section__header">
      <h2 id="form-title" class="form-section__title">
        Claim Your Free Trial Class
      </h2>
      <p class="form-section__desc">
        No experience needed. No commitment required.
      </p>
    </div>
    <form action="/free-trial" method="POST" class="form" novalidate>
      <div class="form__row">
        <div class="form__field">
          <label for="first-name" class="form__label">First Name</label>
          <input type="text" id="first-name" name="first_name"
            class="form__input" autocomplete="given-name"
            required placeholder="Your first name">
        </div>
        <div class="form__field">
          <label for="email" class="form__label">Email Address</label>
          <input type="email" id="email" name="email"
            class="form__input" autocomplete="email"
            required placeholder="your@email.com">
        </div>
      </div>
      <button type="submit" class="btn btn--primary form__submit">
        Start My Free Trial
      </button>
      <p class="form__privacy">No spam. We'll only contact you about your trial class.</p>
    </form>
  </div>
</section>
```

```css
.form-section { padding-block: var(--section-padding-y); }

.form-section__header { text-align: center; margin-bottom: var(--space-8); }
.form-section__title { font-size: clamp(var(--text-2xl), 1.65rem + 3.35vw, var(--text-4xl)); margin-bottom: var(--space-3); }
.form-section__desc { font-size: var(--text-lg); color: var(--color-text-secondary); max-width: var(--measure-narrow); margin-inline: auto; }

.form { display: flex; flex-direction: column; gap: var(--form-gap); }

.form__row { display: grid; grid-template-columns: 1fr; gap: var(--form-gap); }
@media (min-width: 480px) { .form__row { grid-template-columns: 1fr 1fr; } }

.form__field { display: flex; flex-direction: column; gap: var(--space-1); }

.form__label {
  font-size: var(--form-label-size);
  font-weight: var(--form-label-weight);
  color: var(--form-label-color);
}

.form__input {
  width: 100%;
  padding: var(--form-input-padding);
  background-color: var(--form-input-bg);
  border: 1px solid var(--form-input-border);
  border-radius: var(--form-input-radius);
  font-family: var(--font-family-body);
  font-size: var(--form-input-size);
  color: var(--form-input-color);
  min-height: 44px;
  transition: border-color var(--transition-base) var(--ease-out);
  appearance: none;
}

.form__input:focus-visible {
  outline: 2px solid var(--form-input-border-focus);
  outline-offset: 1px;
  border-color: var(--form-input-border-focus);
}

.form__submit { width: 100%; justify-content: center; padding-block: var(--space-3); }
.form__privacy { font-size: var(--text-sm); color: var(--color-text-muted); text-align: center; max-width: none; }
```

---

## 12. SITE NAVIGATION

Usage: HFCM injection. Dark bg, white text, red CTA.
Skip nav first. Logo: no-grayscale class.
Mobile hamburger → drawer. Desktop: horizontal links.

```html
<a href="#main-content" class="skip-nav">Skip to main content</a>

<header class="site-nav" role="banner">
  <div class="site-nav__container container">
    <a href="/" class="site-nav__logo" aria-label="East Texas Krav Maga home">
      <img src="/wp-content/uploads/etkm-logo.png" alt="East Texas Krav Maga"
        class="site-nav__logo-img no-grayscale" width="160" height="48" loading="eager">
    </a>
    <nav class="site-nav__links" aria-label="Main navigation">
      <ul class="site-nav__list" role="list">
        <li><a href="/programs" class="site-nav__link">Programs</a></li>
        <li><a href="/about" class="site-nav__link">About</a></li>
        <li><a href="/schedule" class="site-nav__link">Schedule</a></li>
        <li><a href="/blog" class="site-nav__link">Blog</a></li>
      </ul>
    </nav>
    <div class="site-nav__actions">
      <a href="/free-trial" class="btn btn--primary site-nav__cta">Free Trial</a>
      <button type="button" class="site-nav__toggle"
        aria-controls="mobile-menu" aria-expanded="false"
        aria-label="Open navigation menu">
        <span class="site-nav__hamburger" aria-hidden="true"></span>
      </button>
    </div>
  </div>
  <div class="site-nav__mobile" id="mobile-menu" aria-hidden="true"
    role="dialog" aria-label="Navigation menu">
    <nav aria-label="Mobile navigation">
      <ul class="site-nav__mobile-list" role="list">
        <li><a href="/programs" class="site-nav__mobile-link">Programs</a></li>
        <li><a href="/about" class="site-nav__mobile-link">About</a></li>
        <li><a href="/schedule" class="site-nav__mobile-link">Schedule</a></li>
        <li><a href="/blog" class="site-nav__mobile-link">Blog</a></li>
        <li><a href="/free-trial" class="btn btn--primary site-nav__mobile-cta">Claim Free Trial</a></li>
      </ul>
    </nav>
  </div>
</header>
```

```css
.site-nav {
  position: sticky;
  top: 0;
  z-index: var(--nav-z-index);
  background-color: var(--nav-bg);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.site-nav__container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--nav-height-mobile);
}

@media (min-width: 1024px) { .site-nav__container { height: var(--nav-height); } }

.site-nav__logo-img { height: 2.5rem; width: auto; }

.site-nav__links { display: none; }
@media (min-width: 1024px) { .site-nav__links { display: block; } }

.site-nav__list { display: flex; align-items: center; gap: var(--space-6); list-style: none; }

.site-nav__link {
  font-family: var(--font-family-headline);
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-wide);
  text-transform: uppercase;
  color: var(--nav-text);
  text-decoration: none;
  transition: color var(--transition-base) var(--ease-out);
}

.site-nav__link:hover, .site-nav__link[aria-current="page"] { color: var(--nav-text-hover); }

.site-nav__actions { display: flex; align-items: center; gap: var(--space-3); }

.site-nav__cta { display: none; }
@media (min-width: 768px) { .site-nav__cta { display: inline-flex; } }

.site-nav__toggle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 44px;
  height: 44px;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1);
}

@media (min-width: 1024px) { .site-nav__toggle { display: none; } }

.site-nav__hamburger,
.site-nav__hamburger::before,
.site-nav__hamburger::after {
  display: block;
  width: 24px;
  height: 2px;
  background-color: var(--color-text-inverse);
  transition: transform var(--transition-base) var(--ease-in-out);
}

.site-nav__hamburger { position: relative; }
.site-nav__hamburger::before, .site-nav__hamburger::after { content: ''; position: absolute; }
.site-nav__hamburger::before { top: -7px; }
.site-nav__hamburger::after { top: 7px; }

.site-nav__mobile {
  display: none;
  position: fixed;
  inset: 0;
  top: var(--nav-height-mobile);
  background-color: var(--color-bg-dark);
  z-index: calc(var(--nav-z-index) - 1);
  padding: var(--space-8);
  overflow-y: auto;
}

.site-nav__mobile[aria-hidden="false"] { display: block; }

.site-nav__mobile-list { list-style: none; display: flex; flex-direction: column; gap: var(--space-4); }

.site-nav__mobile-link {
  font-family: var(--font-family-headline);
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-black);
  color: var(--color-text-inverse);
  text-decoration: none;
  display: block;
  padding-block: var(--space-2);
}

.site-nav__mobile-link:hover { color: var(--color-brand-red); }
.site-nav__mobile-cta { width: 100%; justify-content: center; margin-top: var(--space-4); }
```

---

## 13. PAGE FOOTER

Usage: HFCM injection. Dark bg. 3-col desktop, 1-col mobile.
Tagline: "Train More...Fear Less." Red. Auto year via JS.

```html
<footer class="site-footer" role="contentinfo">
  <div class="site-footer__main container">
    <div class="site-footer__brand">
      <img src="/wp-content/uploads/etkm-logo-white.png" alt="East Texas Krav Maga"
        class="site-footer__logo no-grayscale" width="160" height="48" loading="lazy">
      <p class="site-footer__tagline">Train More...Fear Less.</p>
      <p class="site-footer__location">Tyler, TX</p>
    </div>
    <nav class="site-footer__nav" aria-label="Programs">
      <h3 class="site-footer__nav-title">Programs</h3>
      <ul class="site-footer__nav-list" role="list">
        <li><a href="/programs/krav-maga" class="site-footer__link">Krav Maga</a></li>
        <li><a href="/programs/fight-back-etx" class="site-footer__link">Fight Back ETX</a></li>
        <li><a href="/programs/armed-citizen" class="site-footer__link">Armed Citizen Tactics</a></li>
        <li><a href="/programs/youth" class="site-footer__link">Youth Program</a></li>
      </ul>
    </nav>
    <nav class="site-footer__nav" aria-label="Company">
      <h3 class="site-footer__nav-title">Company</h3>
      <ul class="site-footer__nav-list" role="list">
        <li><a href="/about" class="site-footer__link">About Nathan</a></li>
        <li><a href="/schedule" class="site-footer__link">Class Schedule</a></li>
        <li><a href="/blog" class="site-footer__link">Blog</a></li>
        <li><a href="/contact" class="site-footer__link">Contact</a></li>
      </ul>
    </nav>
  </div>
  <div class="site-footer__bottom container">
    <p class="site-footer__copyright">
      &copy; <span id="footer-year"></span> East Texas Krav Maga. All rights reserved.
    </p>
    <div class="site-footer__legal">
      <a href="/privacy-policy" class="site-footer__legal-link">Privacy Policy</a>
      <a href="/terms" class="site-footer__legal-link">Terms</a>
    </div>
  </div>
</footer>
<script>
  document.getElementById('footer-year').textContent = new Date().getFullYear();
</script>
```

```css
.site-footer { background-color: var(--color-bg-dark); color: var(--color-text-inverse); padding-top: var(--space-16); }

.site-footer__main {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-8);
  padding-bottom: var(--space-12);
}

@media (min-width: 768px) { .site-footer__main { grid-template-columns: 2fr 1fr 1fr; gap: var(--space-12); } }

.site-footer__brand { display: flex; flex-direction: column; gap: var(--space-3); }

.site-footer__tagline {
  font-family: var(--font-family-headline);
  font-size: var(--text-lg);
  font-weight: var(--font-weight-black);
  letter-spacing: var(--letter-spacing-wide);
  color: var(--color-brand-red);
  max-width: none;
}

.site-footer__location { font-size: var(--text-sm); color: rgba(255,255,255,0.6); max-width: none; }

.site-footer__nav-title {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-widest);
  text-transform: uppercase;
  color: rgba(255,255,255,0.5);
  margin-bottom: var(--space-3);
}

.site-footer__nav-list { list-style: none; display: flex; flex-direction: column; gap: var(--space-2); }

.site-footer__link {
  font-size: var(--text-base);
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  transition: color var(--transition-base) var(--ease-out);
}

.site-footer__link:hover { color: var(--color-brand-red); }

.site-footer__bottom {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding-block: var(--space-6);
  border-top: 1px solid rgba(255,255,255,0.1);
}

@media (min-width: 768px) { .site-footer__bottom { flex-direction: row; justify-content: space-between; align-items: center; } }

.site-footer__copyright { font-size: var(--text-sm); color: rgba(255,255,255,0.5); max-width: none; }
.site-footer__legal { display: flex; gap: var(--space-4); }
.site-footer__legal-link { font-size: var(--text-sm); color: rgba(255,255,255,0.5); text-decoration: none; transition: color var(--transition-base) var(--ease-out); }
.site-footer__legal-link:hover { color: var(--color-text-inverse); }
```

---

## COMPONENT USAGE MATRIX

| Component | WP Page | Landing | Email | PDF |
|---|---|---|---|---|
| Primary CTA Button | ✅ | ✅ | ✅ bulletproof | ✅ |
| Secondary CTA Button | ✅ | ✅ | ❌ | ✅ |
| Full-Width Hero | ✅ | ✅ first | ❌ | ❌ |
| Split Hero | ✅ | ✅ | ❌ | ❌ |
| Three-Step Plan | ✅ | ✅ required | Simplified | ✅ |
| Two-Column Feature | ✅ | ✅ | ❌ | ✅ |
| Three-Column Benefit Grid | ✅ | ✅ | ❌ | ✅ |
| Full-Width CTA Band | ✅ | ✅ 2-3× | ❌ | ❌ |
| Testimonial Block | ✅ | ✅ | Simplified | ✅ |
| Program Card | ✅ | ❌ | ❌ | ❌ |
| Lead Capture Form | ✅ | ✅ | Via Pipedrive | ❌ |
| Site Navigation | HFCM | ✅ | ❌ | ❌ |
| Page Footer | HFCM | ✅ | Simplified | ❌ |
