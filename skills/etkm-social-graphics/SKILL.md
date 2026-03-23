---
name: etkm-social-graphics
version: 2.0
updated: 2026-03-23
description: >
  Complete production system for ETKM social media graphics across Facebook,
  Instagram, and LinkedIn. Production method: HTML → Playwright → PNG.
  Font standard locked 2026-03-23: Montserrat Black 900 (headlines) +
  Inter 400/600 (body/labels). Three graphic types: Type A (Statement+Image),
  Type B (Type-Only Dark), Type C (Split Layout). Nathan gives input —
  Claude delivers three platform-specific packages including production-ready PNG.
  No Canva required. No external tools. End-to-end in one session.
trigger: >
  Load whenever: building a social media graphic, writing social copy,
  creating a carousel, building an event announcement graphic, rendering
  any ETKM graphic to PNG. Trigger phrases: "social graphic", "social post",
  "carousel", "Instagram post", "Facebook post", "LinkedIn graphic",
  "content graphic", "post image", "make a post", "build a graphic",
  "text graphic", "quote graphic", "event graphic", "render a graphic",
  "build me a post". Always load etkm-brand-kit alongside this skill.
dependencies:
  - etkm-brand-kit v4.0 (Montserrat Black 900 locked — load for all visual decisions)
  - etkm-brand-foundation (voice, copy standards, prohibited words)
  - etkm-cinematic-doctrine (image direction — Type A and C only)
  - etkm-content-templates (copy frameworks by funnel stage)
  - etkm-deliverable-qc (QC gates — run before every delivery)
fonts:
  headline: "Montserrat Black 900"
  body: "Inter 400 / Inter SemiBold 600"
  source_headline: "https://cdn.jsdelivr.net/fontsource/fonts/montserrat@latest/latin-900-normal.ttf"
  source_inter_regular: "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-400-normal.ttf"
  source_inter_semibold: "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-600-normal.ttf"
  install_path: "/usr/local/share/fonts/etkm/"
---

# ETKM Social Graphics Production System
## HTML → Playwright → PNG. One session. Production ready.

**Version:** 2.0
**Locked:** 2026-03-23
**Font:** Montserrat Black 900 + Inter — PERMANENT

---

## THE LOCKED WORKFLOW

```
STEP 1 — NATHAN PROVIDES INPUT (one of four types)
  A. Context   — situation, scenario, real-world moment
  B. Principle — training truth, doctrine, ETKM belief
  C. Quote     — Nathan, student, or sourced quote
  D. Package   — combination, optionally with image

STEP 2 — CLAUDE BUILDS THREE PLATFORM PACKAGES
  Each package contains:
  ├── Graphic type declared (A / B / C)
  ├── Canvas size declared (platform-specific)
  ├── All copy locked (category label, headline,
  │   supporting line, URL)
  ├── HTML file built (fonts + logo embedded as base64)
  └── Platform caption written (platform-specific)

STEP 3 — PLAYWRIGHT RENDERS HTML → PNG
  Exact canvas dimensions. Fonts embedded. No fallbacks.
  Production-ready file. No additional tools needed.

STEP 4 — QC — ALL 6 GATES BEFORE DELIVERY
  Any failure → fix → re-render → re-check
```

---

## FONT STANDARD (LOCKED 2026-03-23)

**Headline:** Montserrat Black 900
**Body / Labels / URL:** Inter Regular 400 / Inter SemiBold 600

These are embedded as base64 in every HTML file.
This guarantees identical rendering in every environment.
No fallbacks. No exceptions.

### Font Download and Install
```python
import urllib.request, os, subprocess

fonts_dir = '/usr/local/share/fonts/etkm'
os.makedirs(fonts_dir, exist_ok=True)

font_urls = {
    "Montserrat-Black.ttf":  "https://cdn.jsdelivr.net/fontsource/fonts/montserrat@latest/latin-900-normal.ttf",
    "Inter-Regular.ttf":     "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-400-normal.ttf",
    "Inter-SemiBold.ttf":    "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-600-normal.ttf",
}

for name, url in font_urls.items():
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = r.read()
    with open(f"{fonts_dir}/{name}", "wb") as f:
        f.write(data)
    print(f"✓ {name}: {len(data)//1024}KB")

subprocess.run(['fc-cache', '-f', fonts_dir], capture_output=True)
```

### Font Embedding in HTML
```python
import base64

def font_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

fonts_dir = '/usr/local/share/fonts/etkm'
montserrat = font_b64(f"{fonts_dir}/Montserrat-Black.ttf")
inter_rg   = font_b64(f"{fonts_dir}/Inter-Regular.ttf")
inter_sb   = font_b64(f"{fonts_dir}/Inter-SemiBold.ttf")
```

```css
@font-face {
  font-family: 'Montserrat';
  font-weight: 900;
  src: url('data:font/ttf;base64,{montserrat}') format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-weight: 400;
  src: url('data:font/ttf;base64,{inter_rg}') format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-weight: 600;
  src: url('data:font/ttf;base64,{inter_sb}') format('truetype');
}
```

---

## LOGO EMBEDDING

Logo files live in project files. Embed as base64 in every HTML.
Never use external URL — self-contained files only.

```python
with open("ETKM_Circle_Logo_White_Red.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()
# Use: src="data:image/png;base64,{logo_b64}"
```

| Variant | File | Use On |
|---------|------|--------|
| White/Red | `ETKM_Circle_Logo_White_Red.png` | Dark backgrounds — default |
| White | `ETKM_Circle_Logo_White.png` | Dark bg where red conflicts |
| Black/Red | `ETKM_Circle_Logo_Black_Red.png` | Light backgrounds |

---

## THREE GRAPHIC TYPES

### TYPE B — Type Only (Primary Format)

```html
<!-- TYPE B BASE TEMPLATE — 1080×1080 -->
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1080px; height: 1080px; background: #000; overflow: hidden; }

  .graphic {
    width: 1080px; height: 1080px;
    background: #000000;
    position: relative;
    display: flex; flex-direction: column; justify-content: center;
    padding: 0 88px;
  }
  .category-label {
    font-family: 'Inter', sans-serif; font-weight: 600; font-size: 24px;
    color: #CC0000; letter-spacing: 8px; text-transform: uppercase;
    margin-bottom: 32px;
  }
  .headline {
    font-family: 'Montserrat', sans-serif; font-weight: 900;
    font-size: 158px; /* adjust per line count */
    color: #FFFFFF; line-height: 0.88;
    text-transform: uppercase; letter-spacing: -3px;
    margin-bottom: 48px;
  }
  .red-rule { width: 100%; height: 4px; background: #CC0000; margin-bottom: 36px; }
  .supporting {
    font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 44px;
    color: #CC0000; text-transform: uppercase; letter-spacing: 1px; line-height: 1.1;
  }
  .footer {
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 0 88px 56px 88px;
    display: flex; justify-content: space-between; align-items: flex-end;
  }
  .url {
    font-family: 'Inter', sans-serif; font-weight: 400; font-size: 22px;
    color: #444444; letter-spacing: 4px; text-transform: uppercase;
  }
  .logo { width: 112px; height: 112px; object-fit: contain; }
</style>

<div class="graphic">
  <div class="category-label">[CATEGORY]</div>
  <div class="headline">[LINE 1]<br>[LINE 2]<br>[LINE 3]</div>
  <div class="red-rule"></div>
  <div class="supporting">[SUPPORTING LINE]</div>
  <div class="footer">
    <div class="url">ETXKRAVMAGA.COM</div>
    <img class="logo" src="data:image/png;base64,[LOGO_B64]">
  </div>
</div>
```

---

### TYPE A — Statement + Image

Same structure as Type B with these additions:

```css
/* Photo background — B&W always */
.photo-bg {
  position: absolute; inset: 0;
  background-image: url('[PHOTO_URL]');
  background-size: cover; background-position: center;
  filter: grayscale(100%);
}
/* Dark overlay */
.overlay {
  position: absolute; inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0,0,0,0.50) 0%,
    rgba(0,0,0,0.45) 40%,
    rgba(0,0,0,0.70) 100%
  );
}
/* Logo only — no URL on Type A */
.logo {
  position: absolute; bottom: 52px; right: 72px;
  width: 120px; height: 120px; object-fit: contain;
}
```

**Photo rules:**
- Always B&W (CSS grayscale filter)
- Subject faces away or in profile — never direct camera
- No violence in progress — awareness moment only
- Load etkm-cinematic-doctrine for full scene brief

---

### TYPE C — Split Layout

```css
/* Type C — 1200×630 landscape */
body { width: 1200px; height: 630px; }

.split { display: flex; width: 1200px; height: 630px; }
.photo-panel {
  width: 45%; background-size: cover; background-position: center;
  filter: grayscale(100%);
}
.info-panel {
  width: 55%; background: #000000;
  display: flex; flex-direction: column;
  justify-content: center; padding: 0 60px;
  position: relative;
}
.event-label {
  font-family: 'Inter'; font-weight: 600; font-size: 18px;
  color: #CC0000; letter-spacing: 6px; text-transform: uppercase;
  margin-bottom: 16px;
}
.name {
  font-family: 'Montserrat'; font-weight: 900; font-size: 80px;
  color: #FFFFFF; line-height: 0.9; text-transform: uppercase;
  margin-bottom: 20px;
}
.facts {
  font-family: 'Montserrat'; font-weight: 900; font-size: 24px;
  color: #FFFFFF; line-height: 1.5;
}
.footer-bar {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 12px 60px;
  display: flex; justify-content: space-between; align-items: center;
}
```

---

## PLATFORM CANVAS SIZES

| Platform | Format | Width | Height | Primary Type |
|----------|--------|-------|--------|--------------|
| Instagram | Square | 1080 | 1080 | A or B |
| Instagram | Portrait | 1080 | 1350 | A or B |
| Instagram | Story | 1080 | 1920 | B |
| Instagram | Carousel | 1080 | 1080 | B |
| Facebook | Square | 1080 | 1080 | A or B |
| Facebook | Landscape | 1200 | 630 | C |
| Facebook | Story | 1080 | 1920 | B |
| LinkedIn | Square | 1200 | 1200 | B or C |
| LinkedIn | Landscape | 1200 | 627 | C |
| LinkedIn | Portrait | 1080 | 1350 | B |

---

## RENDER SCRIPT

```python
from playwright.sync_api import sync_playwright
import os

def render_graphic(html_path, output_path, width, height):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_timeout(800)
        page.screenshot(
            path=output_path,
            clip={"x": 0, "y": 0, "width": width, "height": height}
        )
        browser.close()
    size = os.path.getsize(output_path)
    print(f"✓ {output_path} — {width}×{height} — {size//1024}KB")
    return output_path
```

---

## CAPTION STANDARDS BY PLATFORM

**FACEBOOK**
- Community tone, slightly longer
- Hook line → 2–3 short sentences → single CTA
- Hashtags: 3–5 max, end of caption
- Always include URL if event-related

**INSTAGRAM**
- First line must work as standalone — no context assumed
- Punchy, short lines, one idea each
- Single CTA: "Free trial → link in bio"
- Hashtags: 5–8, end only — no emojis

**LINKEDIN**
- Practitioner peer voice — Nathan speaks to practitioners
- Short paragraphs, white space between every paragraph
- Soft CTA or question at close
- 3 hashtags maximum

---

## COPY FORMULAS

**Truth Statement** (Type B default)
State a reality the audience already feels but hasn't said.
→ "Emergencies don't announce themselves."
→ "Danger doesn't wait."

**Reframe** (MOFU)
Challenge a belief they hold.
→ "You don't fail under pressure because you weren't prepared."

**Imperative Sequence** (Type A — high impact)
→ "BE ALERT. BE AWARE. BE PREPARED."

**Category Label + Statement** (Type B — most common)
→ AWARENESS / "The most dangerous moment is the one you didn't see coming."

---

## QC GATES — ALL 6 BEFORE DELIVERY

| Gate | Check |
|------|-------|
| 1 — Message | Readable in 2 seconds. One idea. Supporting line answers one question. |
| 2 — Font | Montserrat Black 900 on headlines — visually confirmed. Inter on labels. |
| 3 — Brand | Black background. Red once only. No gradients. B&W photo only. |
| 4 — Platform | Canvas matches spec. Text in safe zone. Logo not clipped. |
| 5 — Copy | No prohibited words. URL correct. Caption platform-specific. |
| 6 — North Star | Stops the scroll. Nike level. Unmistakably ETKM. |

**Any failure = fix, re-render, re-check. Never skip.**

---

## WHAT THIS SYSTEM NEVER DOES

- Uses any headline font other than Montserrat Black 900
- Uses color photography
- Uses gradients
- Puts red in more than one place per graphic
- Copies captions across platforms unchanged
- Shows violence in progress in imagery
- Delivers a PNG without passing all 6 QC gates
- Starts building before copy is locked

---

*Version 2.0 — 2026-03-23*
*Font locked: Montserrat Black 900 — selected by Nathan from live comparison*
*Production method: HTML → Playwright → PNG*
*Maintained in: easttxkravmaga/Claude → skills/etkm-social-graphics/SKILL.md*
