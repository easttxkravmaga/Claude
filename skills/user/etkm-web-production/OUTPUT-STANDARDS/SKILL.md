# ETKM Output Standards
## File 5 of 4 — etkm-web-production skill series

**Version:** 1.0
**Built:** 2026-04-24
**Depends on:** SKILL.md, CSS-SYSTEM.md, COMPONENT-LIBRARY.md

---

## CRITICAL ISOLATION WARNING

```
Web CSS:   CSS Grid ✅  Flexbox ✅  var() ✅  External CSS ✅
Email CSS: CSS Grid ❌  Flexbox ❌  var() ❌  External CSS ❌
           Tables ✅  Inline CSS ✅  max-width: 600px ✅
PDF CSS:   CSS Grid ✅  Flexbox ✅  var() ✅
           BUT: print-color-adjust required
           AND: Playwright printBackground: true required
           AND: Absolute image URLs required
```

NEVER mix email CSS with web CSS.
NEVER mix PDF print rules with standard web rules.

---

## OUTPUT TYPE 1 — WORDPRESS PAGE SECTIONS

### HFCM Hook Selection

| Content Type | Hook |
|---|---|
| CSS styles | `wp_head` |
| Site header | `generate_before_header` |
| Hero section | `generate_after_header` |
| Page intro | `generate_before_content` |
| CTA section | `generate_after_content` |
| Newsletter | `generate_before_footer` |
| JavaScript | `wp_footer` |

### Code Block Structure

```html
<style>
@layer components {
  .my-section {
    background-color: var(--color-bg-dark);
    padding-block: var(--section-padding-y);
  }
  .my-section h2 {
    font-size: clamp(var(--text-3xl),
      2.3394rem + 4.088vw, var(--text-5xl));
    color: var(--color-text-inverse);
  }
}
</style>

<section class="my-section full-bleed" aria-labelledby="section-id">
  <div class="container">
    <h2 id="section-id">Section Title</h2>
  </div>
</section>
```

### GeneratePress Integration

```css
/* Variable mapping in Additional CSS */
:root {
  --contrast:   var(--color-text-primary);
  --contrast-2: var(--color-text-secondary);
  --contrast-3: var(--color-text-muted);
  --base:       var(--color-bg-page);
  --base-2:     var(--color-bg-subtle);
  --base-3:     var(--color-bg-muted);
  --accent:     var(--color-brand-red);
}

/* Full-bleed breakout */
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

### CSS Scoping

```css
/* WRONG — bleeds into theme */
.hero { background: black; }
h2 { font-size: 3rem; }

/* CORRECT — scoped to component */
.my-hero-section { background-color: var(--color-bg-dark); }
.my-hero-section h2 {
  font-size: clamp(var(--text-3xl), 2.3394rem + 4.088vw,
    var(--text-5xl));
}
```

### .entry-content Reset

```css
.my-component p,
.my-component ul,
.my-component ol { margin-bottom: 0; }
```

---

## OUTPUT TYPE 2 — LANDING PAGES

### StoryBrand Section Sequence

```
1. HERO (required)
   Component #3 or #4 | fetchpriority="high" on hero img

2. STAKES (recommended)
   Cost of inaction | Dark bg | No CTA | 2-4 sentences max

3. GUIDE INTRODUCTION (recommended)
   Authority + empathy | Social proof signals

4. THREE-STEP PLAN (required)
   Component #5 | Exactly 3 steps | ETKM steps verbatim:
     1. Attend a Free Trial Lesson
     2. Get Your Personalized Training Blueprint
     3. Become a Confident, Capable Protector
   Primary CTA immediately follows

5. EXPLANATORY CTA (required)
   Component #8 | Expands offering | Repeats primary CTA

6. SOCIAL PROOF (recommended)
   Component #9 | Minimum 1 testimonial | Real student words

7. FINAL CTA (required)
   Component #8 or #11 | Last conversion opportunity
```

### CTA Placement

```
Hero:          ✅ Required
Stakes:        ❌ No CTA
Guide:         ❌ No CTA
Plan:          ✅ Required (immediately after steps)
Explanatory:   ✅ Required
Social Proof:  ❌ No CTA
Final CTA:     ✅ Required
```

### Above-Fold Requirements

Mobile (375×667): brand + H2 headline + subhead + primary CTA
Desktop (1280×800): all of above + hero image optional

### Mobile Rules

```
Single column below 768px — enforced
Body text minimum 16px — prevents iOS auto-zoom
Touch targets minimum 44×44px
Sticky CTA: position fixed bottom — high mobile conversion
```

### Performance

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">
```

Core Web Vitals:
- LCP < 2.5s: hero = `<img>` not CSS background
- CLS < 0.1: all images need width/height
- INP < 200ms: no layout property animations

---

## OUTPUT TYPE 3 — EMAIL TEMPLATES

### Email HTML Boilerplate

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
  xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <!--[if mso]>
  <xml><o:OfficeDocumentSettings>
    <o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch>
  </o:OfficeDocumentSettings></xml>
  <![endif]-->
  <style type="text/css">
    body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; }

    @media only screen and (max-width: 600px) {
      .email-container { width: 100% !important; }
      .mobile-full { width: 100% !important; display: block !important; }
      .mobile-padding { padding: 16px !important; }
    }

    @media (prefers-color-scheme: dark) {
      .email-bg { background-color: #121212 !important; }
      .email-body { background-color: #1e1e1e !important; }
      .email-text { color: #ffffff !important; }
    }
  </style>
</head>
<body style="margin:0; padding:0; background-color:#f4f5f7;" class="email-bg">

  <!-- Preheader — shown in inbox preview, visually hidden -->
  <div style="display:none; max-height:0; overflow:hidden;
    font-size:1px; line-height:1px; color:#f4f5f7; mso-hide:all;">
    Preview text here — 90 characters max.
    &#847; &zwnj; &nbsp; &#847; &zwnj; &nbsp;
  </div>

  <table role="presentation" cellspacing="0" cellpadding="0"
    border="0" width="100%" style="background-color:#f4f5f7;">
    <tr><td align="center" style="padding:20px 0;">

      <!--[if mso]>
      <table role="presentation" cellspacing="0" cellpadding="0"
        border="0" width="600" align="center"><tr><td>
      <![endif]-->

      <div class="email-container email-body"
        style="max-width:600px; margin:0 auto; width:100%;
        background-color:#ffffff;">

        <!-- HEADER -->
        <table role="presentation" cellspacing="0" cellpadding="0"
          border="0" width="100%">
          <tr>
            <td style="background-color:#CC0000; padding:20px 32px;">
              <img src="https://etxkravmaga.com/wp-content/uploads/etkm-logo-white.png"
                alt="East Texas Krav Maga" width="140" height="42">
            </td>
          </tr>
        </table>

        <!-- CONTENT SECTIONS GO HERE -->

        <!-- FOOTER -->
        <table role="presentation" cellspacing="0" cellpadding="0"
          border="0" width="100%">
          <tr>
            <td style="background-color:#000000; padding:24px 32px;
              text-align:center;">
              <p style="margin:0; font-family:Arial,sans-serif;
                font-size:12px; color:#888888; line-height:1.5;">
                &copy; 2026 East Texas Krav Maga · Tyler, TX<br>
                <a href="{{unsubscribe_link}}"
                  style="color:#888888; text-decoration:underline;">
                  Unsubscribe</a>
              </p>
            </td>
          </tr>
        </table>

      </div>

      <!--[if mso]></td></tr></table><![endif]-->

    </td></tr>
  </table>
</body>
</html>
```

### Bulletproof CTA Button

```html
<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:w="urn:schemas-microsoft-com:office:word"
  href="https://etxkravmaga.com/free-trial"
  style="height:48px;v-text-anchor:middle;width:220px;"
  arcsize="8%" stroke="f" fillcolor="#CC0000">
  <w:anchorlock/>
  <center style="color:#ffffff; font-family:Arial,sans-serif;
    font-size:16px; font-weight:bold;">
    Start Your Free Trial
  </center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<table role="presentation" cellspacing="0" cellpadding="0"
  border="0" align="center">
  <tr>
    <td align="center" style="border-radius:4px; background-color:#CC0000;">
      <a href="https://etxkravmaga.com/free-trial"
        style="background-color:#CC0000; border:1px solid #CC0000;
          border-radius:4px; color:#ffffff; display:inline-block;
          font-family:Arial,Helvetica,sans-serif; font-size:16px;
          font-weight:bold; line-height:48px; text-align:center;
          text-decoration:none; width:220px;
          -webkit-text-size-adjust:none; mso-hide:all;">
        Start Your Free Trial
      </a>
    </td>
  </tr>
</table>
<!--<![endif]-->
```

### Email CSS Support Matrix

| Property | Gmail | Apple Mail | Outlook Win | Use? |
|---|---|---|---|---|
| background-color inline | ✅ | ✅ | ✅ | ✅ Yes |
| padding on td | ✅ | ✅ | ✅ | ✅ Yes |
| font-family inline | ✅ | ✅ | ✅ | ✅ Yes |
| border-radius | ✅ | ✅ | ❌ | ⚠️ VML fallback |
| CSS Grid | ❌ | ✅ | ❌ | ❌ Never |
| Flexbox | ❌ | ✅ | ❌ | ❌ Never |
| CSS custom properties | ❌ | ✅ | ❌ | ❌ Never |
| background-image | ✅ | ✅ | ❌ | ⚠️ VML fallback |
| CSS animations | ❌ | ✅ | ❌ | ❌ Never |
| Google Fonts | ❌ | ✅ | ❌ | ⚠️ Fallback required |
| Dark mode | ✅ apps | ✅ | ✅ | ✅ With meta tags |

### Pipedrive Merge Tags

```
{{person.name}}      {{company.name}}
{{deal.title}}       {{user.name}}
{{unsubscribe_link}} — required in every email footer
```

---

## OUTPUT TYPE 4 — LEAD MAGNET PDFs

### Playwright API Configuration

```javascript
const pdf = await page.pdf({
  format: 'Letter',       // Match @page size
  printBackground: true,  // REQUIRED — without this backgrounds strip
  margin: {
    top: '1in', right: '0.75in',
    bottom: '1in', left: '0.75in'
  }
  // Define margins here, not in CSS body
});
```

### Required Print CSS

```css
/* Background color preservation — BOTH prefixes required */
* {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

@media print {
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}

@page {
  size: 8.5in 11in; /* US Letter */
}

/* Page break control */
.section, .card, .plan-step { break-inside: avoid; }
.chapter { break-before: page; }

/* Orphans and widows */
p, li { orphans: 3; widows: 3; }
```

### Image URL Rules

```
✅ https://full-url.com/image.jpg  (absolute)
✅ data:image/png;base64,...        (embedded — most reliable)
❌ /relative/path.jpg               (FAILS)
❌ ./relative.jpg                   (FAILS)
❌ file:///path.jpg                 (FAILS in strict context)
```

### Font Loading

```html
<!-- Option A: CDN (when internet available) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Inter:wght@400;600&display=swap" rel="stylesheet">

<!-- Option B: Base64 embedded (offline/CI reliable) -->
<style>
@font-face {
  font-family: 'Montserrat';
  font-weight: 900;
  src: url('data:font/woff2;base64,AAAA...') format('woff2');
}
</style>
```

### Failure Prevention

| Problem | Fix |
|---|---|
| Backgrounds white | `printBackground: true` in Playwright API |
| Background colors stripped | Both `-webkit-print-color-adjust: exact` AND `print-color-adjust: exact` |
| Fonts show as Times New Roman | Embed as Base64 or `page.waitForLoadState('networkidle')` |
| Images not showing | Use absolute `https://` URLs or Base64 |
| Content splits badly | `break-inside: avoid` on containers |
| Lone lines at page edge | `orphans: 3; widows: 3;` on `p` elements |
| Margins wrong | Define in Playwright API, not CSS body |

---

## QUICK REFERENCE

| Rule | WordPress | Landing | Email | PDF |
|---|---|---|---|---|
| DOCTYPE | HTML5 | HTML5 | XHTML 1.0 Trans | HTML5 |
| Layout | Grid/Flex | Grid/Flex | Tables | Grid/Flex |
| CSS delivery | style block | style block | Inline + head | style block |
| Custom properties | ✅ | ✅ | ❌ | ✅ |
| Max width | container-xl | container-xl | 600px hardcoded | N/A print |
| Fonts | Google CDN | Google CDN | System + fallback | CDN or Base64 |
| Images | Any URL | Absolute preferred | Absolute https:// only | https:// or Base64 |
| Hero | img tag | img fetchpriority | N/A | N/A |
| Flexbox | ✅ | ✅ | ❌ | ✅ |
| CSS Grid | ✅ | ✅ | ❌ | ✅ |
| Animations | transform+opacity | transform+opacity | None | None |
