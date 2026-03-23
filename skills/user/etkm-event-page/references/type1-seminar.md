# TYPE 1 — Seminar / Workshop Template Reference

**Locked reference page:** [etxkravmaga.com/fight-back-etx/womens-self-defense-seminar-in-tyler-tx/](http://etxkravmaga.com/fight-back-etx/womens-self-defense-seminar-in-tyler-tx/)

Use this file when building any TYPE 1 seminar or workshop page. The WSD (Women's Self Defense) page is the locked standard. All new seminar pages use this as the structural template.

---

## Fixed 10-Section Order (Non-Negotiable)

Do not add, remove, or reorder sections.

| # | Section | Notes |
|---|---------|-------|
| 1 | Top Bar | Red background, event name + "Spots Are Limited" |
| 2 | Hero | Full-bleed B&W background image, headline, event bar |
| 3 | Registration | Ecwid widget + price + 3-cell meta — JUST UNDER FOLD |
| 4 | Who This Is For | 6-card audience grid |
| 5 | Insight Block | Red left-border quote, core training truth |
| 6 | Seminar Content | 2×2 level/module cards with ghost numbers |
| 7 | Testimonial | Pull quote (omit if none available) |
| 8 | Location | Venue address + ETKM contact |
| 9 | Final CTA | Headline + button that scrolls to `#register` |
| 10 | Footer | ETKM address/phone/URL |

---

## What Changes vs. What Never Changes

| Element | Changes Per Event? |
|---------|-------------------|
| Wording (headlines, copy, level descriptions, who-grid) | YES |
| Hero background image (always B&W embedded base64) | YES |
| Ecwid embed code + price | YES |
| CSS architecture | NO |
| Section structure and order | NO |
| Spacing and layout | NO |
| Scroll animations | NO |
| WordPress deploy rules | NO |
| Wrapper ID convention | NO (follow naming table) |

---

## Image Processing Specs

### Hero Background Image
- Convert to Black & White (grayscale)
- Apply dark overlay gradient for text readability
- **Gradient:** `linear-gradient(to right, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0.30) 100%)`
- **Image opacity:** 1.0 (full), gradient handles the darkening
- Resize to 1400px wide max
- Save as JPEG quality 80
- Embed as base64: `data:image/jpeg;base64,...`

### Python Pattern
```python
from PIL import Image
import base64, io

img = Image.open('hero.jpg')
bw = img.convert('L').resize((1400, int(img.height*1400/img.width)), Image.LANCZOS)
buf = io.BytesIO()
bw.save(buf, 'JPEG', quality=80)
b64 = base64.b64encode(buf.getvalue()).decode()
```

---

## Hero Headline Two-Line Rule

The hero headline MUST span exactly two lines. Use a `<br>` tag to force the break at the natural rhythm point.

**Pattern:**
```html
<h1 class="hero-hed fd">
  [First Line of Headline]<br>
  [Second Line of Headline]
</h1>
```

**Examples:**
- "Fight Back ETX<br>Women's Self-Defense Seminar"
- "College Ready<br>Personal Safety Seminar"
- "Youth Self-Defense<br>Workshop"

Never let the headline wrap naturally — always control the break.

---

## Wrapper ID Convention

| Event | Wrapper ID |
|-------|-----------|
| Women's Self Defense | `etkm-wsd` |
| Youth Self Defense | `etkm-youth-sd` |
| College Ready | `etkm-college` |
| Intro to Krav | `etkm-intro-km` |
| New events | `etkm-[event-slug]` |

---

## TYPE 1 Component Reference

### Section 1 — Top Bar
```css
#W .topbar { background:#CC0000; padding:10px 0; text-align:center; font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:14px; letter-spacing:.12em; text-transform:uppercase; color:#fff; }
```
```html
<div class="topbar">
  [EVENT NAME] — [DATE] — Tyler, Texas — <strong>Spots Are Limited</strong>
</div>
```

---

### Section 2 — Hero with Background Image
Full-bleed B&W background image with dark gradient overlay.

```css
#W .hero {
  position:relative; min-height:520px; display:flex; align-items:center;
  background:#000; overflow:hidden;
}
#W .hero-bg {
  position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
  object-position:center top; filter:grayscale(100%) contrast(1.05);
  opacity:1.0;
}
#W .hero-overlay {
  position:absolute; inset:0;
  background:linear-gradient(to right, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0.30) 100%);
}
#W .hero-inner { position:relative; z-index:2; padding:80px 28px; max-width:700px; }
#W .hero-hed {
  font-family:'Barlow Condensed',sans-serif; font-weight:900; font-size:clamp(48px,7vw,88px);
  line-height:.95; letter-spacing:-.01em; color:#fff; text-transform:uppercase; margin:0 0 24px;
}
#W .hero-sub {
  font-family:'Inter',sans-serif; font-size:16px; font-weight:400; color:#BBBBBB;
  line-height:1.6; margin:0 0 32px; max-width:520px;
}
#W .hero-bar {
  display:flex; gap:32px; flex-wrap:wrap; margin-bottom:36px;
}
#W .hero-bar-item { display:flex; flex-direction:column; }
#W .hero-bar-label { font-family:'Inter',sans-serif; font-size:10px; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:#575757; }
#W .hero-bar-value { font-family:'Barlow Condensed',sans-serif; font-size:22px; font-weight:700; color:#fff; letter-spacing:.02em; }
```

```html
<section class="hero">
  <img class="hero-bg" src="data:image/jpeg;base64,[BASE64]" alt="[EVENT NAME]">
  <div class="hero-overlay"></div>
  <div class="hero-inner cp">
    <div class="eyebrow fd">East Texas Krav Maga — [CITY, STATE]</div>
    <h1 class="hero-hed fd">
      [LINE ONE]<br>[LINE TWO]
    </h1>
    <p class="hero-sub fd">[1–2 sentence hook about what attendees will learn/gain]</p>
    <div class="hero-bar fd">
      <div class="hero-bar-item"><span class="hero-bar-label">Date</span><span class="hero-bar-value">[DATE]</span></div>
      <div class="hero-bar-item"><span class="hero-bar-label">Time</span><span class="hero-bar-value">[TIME]</span></div>
      <div class="hero-bar-item"><span class="hero-bar-label">Location</span><span class="hero-bar-value">[VENUE SHORT]</span></div>
      <div class="hero-bar-item"><span class="hero-bar-label">Investment</span><span class="hero-bar-value">$[PRICE]</span></div>
    </div>
    <a href="#register" class="btn-p fd">Register Now</a>
  </div>
</section>
```

---

### Section 3 — Registration Block (Ecwid Pattern)

**Rule:** This section MUST have `id="register"`. The Ecwid widget embeds here. The final CTA button scrolls to this section — it NEVER re-embeds Ecwid.

```css
#W .reg-section { background:#111; padding:60px 0; }
#W .reg-block { max-width:680px; margin:0 auto; padding:0 28px; }
#W .reg-price { font-family:'Barlow Condensed',sans-serif; font-size:52px; font-weight:900; color:#fff; letter-spacing:-.01em; margin:0 0 4px; }
#W .reg-price-sub { font-family:'Inter',sans-serif; font-size:13px; color:#575757; margin:0 0 28px; }
#W .reg-meta { display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:#1e1e1e; margin-bottom:32px; }
#W .reg-meta-cell { background:#111; padding:16px; }
#W .reg-meta-label { font-size:9px; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:#575757; font-family:'Inter',sans-serif; }
#W .reg-meta-value { font-size:15px; font-weight:600; color:#fff; font-family:'Inter',sans-serif; margin-top:4px; }
```

```html
<section class="reg-section" id="register">
  <div class="reg-block">
    <div class="eyebrow fd">Registration</div>
    <div class="rule fd"></div>
    <div class="reg-price fd">$[PRICE]</div>
    <div class="reg-price-sub fd">per person — [any included items, e.g., "includes workbook"]</div>
    <div class="reg-meta fd">
      <div class="reg-meta-cell">
        <div class="reg-meta-label">Date</div>
        <div class="reg-meta-value">[DATE]</div>
      </div>
      <div class="reg-meta-cell">
        <div class="reg-meta-label">Time</div>
        <div class="reg-meta-value">[TIME]</div>
      </div>
      <div class="reg-meta-cell">
        <div class="reg-meta-label">Location</div>
        <div class="reg-meta-value">[VENUE SHORT]</div>
      </div>
    </div>
    <!-- Ecwid embed — replace with live embed code -->
    <div class="fd" id="my-store-[ECWID_STORE_ID]"></div>
    <script data-cfasync="false" type="text/javascript" src="https://app.ecwid.com/script.js?[ECWID_STORE_ID]&data_platform=code" charset="utf-8"></script>
    <script type="text/javascript">
      xProductBrowser("categoriesPerRow=3","views=grid(20,3) list(60) table(60)","categoryView=grid","searchView=list","id=my-store-[ECWID_STORE_ID]");
    </script>
  </div>
</section>
```

---

### Section 4 — Who This Is For (6-Card Grid)
```css
#W .who-section { background:#000; padding:80px 0; }
#W .who-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:#111; margin-top:40px; }
#W .who-card { background:#000; padding:28px 24px; }
#W .who-icon { font-size:22px; margin-bottom:12px; }
#W .who-title { font-family:'Barlow Condensed',sans-serif; font-size:18px; font-weight:700; color:#fff; text-transform:uppercase; letter-spacing:.04em; margin-bottom:8px; }
#W .who-desc { font-family:'Inter',sans-serif; font-size:13px; color:#BBBBBB; line-height:1.6; }
```

```html
<section class="who-section">
  <div class="cp">
    <div class="eyebrow fd">Who This Is For</div>
    <div class="rule fd"></div>
    <h2 class="fd" style="font-family:'Barlow Condensed',sans-serif;font-size:clamp(32px,5vw,52px);font-weight:900;color:#fff;text-transform:uppercase;margin:0 0 8px;">[Section Headline]</h2>
    <div class="who-grid fd">
      <!-- Repeat 6 times -->
      <div class="who-card">
        <div class="who-icon">[EMOJI or leave blank]</div>
        <div class="who-title">[Audience Type]</div>
        <div class="who-desc">[1–2 sentence description]</div>
      </div>
    </div>
  </div>
</section>
```

---

### Section 5 — Insight Block (Red Left-Border Quote)
```css
#W .insight-section { background:#111; padding:80px 0; }
#W .insight-block { max-width:760px; margin:0 auto; padding:0 28px; border-left:4px solid #CC0000; padding-left:40px; }
#W .insight-quote { font-family:'Barlow Condensed',sans-serif; font-size:clamp(28px,4vw,44px); font-weight:700; color:#fff; line-height:1.15; margin:0 0 20px; }
#W .insight-body { font-family:'Inter',sans-serif; font-size:15px; color:#BBBBBB; line-height:1.7; }
```

```html
<section class="insight-section">
  <div class="cp">
    <div class="insight-block fd">
      <p class="insight-quote">"[Core training truth — 1–2 sentences, punchy]"</p>
      <p class="insight-body">[Supporting paragraph — what this means for the attendee]</p>
    </div>
  </div>
</section>
```

---

### Section 6 — Seminar Content (2×2 Levels Grid with Ghost Numbers)
```css
#W .content-section { background:#000; padding:80px 0; }
#W .levels-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1px; background:#111; margin-top:40px; }
#W .level-card { background:#000; padding:36px 32px; position:relative; overflow:hidden; }
#W .level-ghost { position:absolute; top:-10px; right:16px; font-family:'Barlow Condensed',sans-serif; font-size:120px; font-weight:900; color:#111; line-height:1; pointer-events:none; user-select:none; }
#W .level-eyebrow { font-family:'Inter',sans-serif; font-size:10px; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:#CC0000; margin-bottom:10px; }
#W .level-title { font-family:'Barlow Condensed',sans-serif; font-size:26px; font-weight:800; color:#fff; text-transform:uppercase; letter-spacing:.03em; margin-bottom:14px; }
#W .level-list { list-style:none; padding:0; margin:0; }
#W .level-list li { font-family:'Inter',sans-serif; font-size:13px; color:#BBBBBB; line-height:1.6; padding:5px 0; border-bottom:1px solid #1a1a1a; }
#W .level-list li:last-child { border-bottom:none; }
#W .level-list li::before { content:'→ '; color:#CC0000; font-weight:700; }
```

```html
<section class="content-section">
  <div class="cp">
    <div class="eyebrow fd">What You'll Train</div>
    <div class="rule fd"></div>
    <h2 class="fd" style="font-family:'Barlow Condensed',sans-serif;font-size:clamp(32px,5vw,52px);font-weight:900;color:#fff;text-transform:uppercase;margin:0 0 8px;">[Section Headline]</h2>
    <div class="levels-grid">
      <!-- Repeat 4 times (2×2 grid) -->
      <div class="level-card fd">
        <div class="level-ghost">[1]</div>
        <div class="level-eyebrow">Module [N]</div>
        <div class="level-title">[Module Title]</div>
        <ul class="level-list">
          <li>[Topic 1]</li>
          <li>[Topic 2]</li>
          <li>[Topic 3]</li>
        </ul>
      </div>
    </div>
  </div>
</section>
```

---

### Section 7 — Testimonial Block (Pull Quote)

Omit this section entirely if no testimonial is available.

```css
#W .testimonial-section { background:#111; padding:80px 0; }
#W .testimonial-block { max-width:680px; margin:0 auto; padding:0 28px; text-align:center; }
#W .testimonial-mark { font-family:'Barlow Condensed',sans-serif; font-size:80px; color:#CC0000; line-height:.6; margin-bottom:16px; }
#W .testimonial-quote { font-family:'Barlow Condensed',sans-serif; font-size:clamp(22px,3vw,34px); font-weight:700; color:#fff; line-height:1.2; margin:0 0 20px; font-style:italic; }
#W .testimonial-attr { font-family:'Inter',sans-serif; font-size:12px; font-weight:600; letter-spacing:.12em; text-transform:uppercase; color:#575757; }
```

```html
<section class="testimonial-section">
  <div class="cp">
    <div class="testimonial-block fd">
      <div class="testimonial-mark">"</div>
      <p class="testimonial-quote">[Testimonial text]</p>
      <div class="testimonial-attr">— [Name], [Title/Descriptor]</div>
    </div>
  </div>
</section>
```

---

### Section 8 — Location
```css
#W .location-section { background:#000; padding:80px 0; border-top:1px solid #111; }
#W .location-grid { display:grid; grid-template-columns:1fr 1fr; gap:60px; margin-top:40px; }
#W .location-label { font-family:'Inter',sans-serif; font-size:10px; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:#575757; margin-bottom:8px; }
#W .location-value { font-family:'Barlow Condensed',sans-serif; font-size:22px; font-weight:700; color:#fff; line-height:1.3; }
#W .location-sub { font-family:'Inter',sans-serif; font-size:13px; color:#BBBBBB; margin-top:6px; line-height:1.6; }
```

```html
<section class="location-section">
  <div class="cp">
    <div class="eyebrow fd">Location & Details</div>
    <div class="rule fd"></div>
    <div class="location-grid">
      <div class="fd">
        <div class="location-label">Venue</div>
        <div class="location-value">[VENUE NAME]</div>
        <div class="location-sub">[ADDRESS LINE 1]<br>[CITY, STATE ZIP]</div>
      </div>
      <div class="fd">
        <div class="location-label">Questions?</div>
        <div class="location-value">East Texas Krav Maga</div>
        <div class="location-sub">
          [PHONE]<br>
          <a href="mailto:[EMAIL]" style="color:#BBBBBB;">[EMAIL]</a><br>
          <a href="https://etxkravmaga.com" target="_blank" style="color:#BBBBBB;">etxkravmaga.com</a>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

### Section 9 — Final CTA Button Pattern

**Critical Rule:** The final CTA button MUST use `href="#register"` to scroll back to the registration block. It NEVER re-embeds the Ecwid widget. This is non-negotiable.

```css
#W .fcta-section { background:#111; padding:80px 0; text-align:center; }
#W .fcta-hed { font-family:'Barlow Condensed',sans-serif; font-size:clamp(36px,5vw,60px); font-weight:900; color:#fff; text-transform:uppercase; line-height:1; margin:0 0 16px; }
#W .fcta-sub { font-family:'Inter',sans-serif; font-size:15px; color:#BBBBBB; margin:0 0 36px; }
#W .fcta-main { background:#CC0000; color:#fff; font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:18px; letter-spacing:.12em; text-transform:uppercase; text-decoration:none; padding:20px 52px; display:inline-block; transition:background .2s; }
#W .fcta-main:hover { background:#aa0000; }
```

```html
<section class="fcta-section">
  <div class="cp">
    <h2 class="fcta-hed fd">[CTA Headline]</h2>
    <p class="fcta-sub fd">[One-line urgency statement]</p>
    <!-- MUST scroll to #register — NEVER re-embed Ecwid here -->
    <a href="#register" class="fcta-main fd">Register Now — $[PRICE]</a>
  </div>
</section>
```

---

### Section 10 — Footer
```css
#W .footer { background:#000; border-top:1px solid #111; padding:40px 0; text-align:center; }
#W .footer-name { font-family:'Barlow Condensed',sans-serif; font-size:18px; font-weight:800; color:#fff; text-transform:uppercase; letter-spacing:.08em; margin-bottom:8px; }
#W .footer-info { font-family:'Inter',sans-serif; font-size:12px; color:#575757; line-height:1.8; }
#W .footer-info a { color:#575757; text-decoration:none; }
#W .footer-info a:hover { color:#BBBBBB; }
```

```html
<footer class="footer">
  <div class="cp">
    <div class="footer-name">East Texas Krav Maga</div>
    <div class="footer-info">
      [ADDRESS] · Tyler, TX [ZIP]<br>
      [PHONE] · <a href="mailto:[EMAIL]">[EMAIL]</a><br>
      <a href="https://etxkravmaga.com" target="_blank">etxkravmaga.com</a>
    </div>
  </div>
</footer>
```

---

## Checkout System: Ecwid

TYPE 1 pages use Ecwid, not Stripe. The Ecwid widget embeds in Section 3 (Registration). The final CTA (Section 9) scrolls to `#register` — it does NOT re-embed Ecwid.

**Ecwid embed pattern:**
```html
<div id="my-store-[STORE_ID]"></div>
<script data-cfasync="false" type="text/javascript"
  src="https://app.ecwid.com/script.js?[STORE_ID]&data_platform=code" charset="utf-8">
</script>
<script type="text/javascript">
  xProductBrowser(
    "categoriesPerRow=3",
    "views=grid(20,3) list(60) table(60)",
    "categoryView=grid",
    "searchView=list",
    "id=my-store-[STORE_ID]"
  );
</script>
```

---

## Responsive Rules (860px Breakpoint)

```css
@media(max-width:860px){
  #W .who-grid { grid-template-columns:1fr 1fr; }
  #W .levels-grid { grid-template-columns:1fr; }
  #W .location-grid { grid-template-columns:1fr; gap:32px; }
  #W .hero-hed { font-size:clamp(38px,10vw,60px); }
  #W .reg-meta { grid-template-columns:1fr; }
}
@media(max-width:540px){
  #W .who-grid { grid-template-columns:1fr; }
}
```

---

## Fade Animation (TYPE 1 — use wrapper ID)

```css
#W .fd { opacity:0; transform:translateY(22px); transition:opacity .6s ease,transform .6s ease; }
#W .fd.vis { opacity:1; transform:none; }
```

```javascript
(function(){
  var els = document.querySelectorAll('#[WRAPPER-ID] .fd');
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('vis'); obs.unobserve(e.target); } });
  },{threshold:0.08,rootMargin:'0px 0px -30px 0px'});
  els.forEach(function(el){ obs.observe(el); });
})();
```

---

## TYPE 1 QC Checklist

- [ ] Section order matches the fixed 10-section structure exactly
- [ ] Hero headline spans exactly two lines (controlled `<br>`)
- [ ] Hero background image is B&W and embedded as base64
- [ ] Registration section has `id="register"`
- [ ] Ecwid embed code is live (not placeholder)
- [ ] Final CTA button uses `href="#register"` — not a re-embedded Ecwid widget
- [ ] All CSS scoped to unique wrapper ID
- [ ] WP override block present in CSS
- [ ] Red used max once per visible section
- [ ] Responsive breakpoint at 860px present
- [ ] `target="_blank"` on all external links
- [ ] No placeholder text remaining
- [ ] Google Fonts link included
