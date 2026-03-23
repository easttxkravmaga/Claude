# ETKM Social Graphics Format Standard
## The locked production spec. Every graphic built from this document.

**Version:** 1.0
**Locked:** 2026-03-23
**Authority:** Nathan Lundstrom / East Texas Krav Maga
**Production Method:** HTML → Playwright → PNG

---

## THE FONT STACK (NON-NEGOTIABLE)

Selected by Nathan from a live comparison on 2026-03-23.
These two fonts are the ETKM social graphics standard permanently.

| Role | Font | Weight | Use |
|------|------|--------|-----|
| **Display Headlines** | **Montserrat Black** | **900** | All headlines, supporting lines |
| **Body / UI / Labels** | **Inter** | **400 / 600** | Category labels, URL, captions |

### Font Sources (Free — No Licensing Issues)
```
Montserrat Black 900:
https://cdn.jsdelivr.net/fontsource/fonts/montserrat@latest/latin-900-normal.ttf

Inter Regular 400:
https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-400-normal.ttf

Inter SemiBold 600:
https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-600-normal.ttf
```

### Font Embedding (Required for Every Build)
Both fonts are embedded as base64 in every HTML file.
This guarantees identical rendering in every environment — no fallbacks needed.

```python
def font_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
```

```css
@font-face {
  font-family: 'Montserrat';
  font-weight: 900;
  src: url('data:font/ttf;base64,[BASE64]') format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-weight: 400;
  src: url('data:font/ttf;base64,[BASE64]') format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-weight: 600;
  src: url('data:font/ttf;base64,[BASE64]') format('truetype');
}
```

---

## COLOR PALETTE (NON-NEGOTIABLE)

| Color | Hex | Role |
|-------|-----|------|
| Black | `#000000` | All backgrounds |
| White | `#FFFFFF` | Headline text |
| Red | `#CC0000` | Category label OR supporting line — never both |
| Dark Gray | `#444444` | URL footer text |
| Mid Gray | `#333333` | Font labels, secondary info |

**Rules:**
- No gradients. Ever.
- No colors outside this palette. Ever.
- Red appears ONCE per graphic. One element only.
- No color photography. B&W photos only on Type A graphics.

---

## THE THREE GRAPHIC TYPES

### TYPE B — Type Only (Dark)
**The workhorse. Highest volume. Fastest to produce.**

```
LAYOUT STRUCTURE (1080×1080)
─────────────────────────────────────────────────────────
Background:         #000000 pure black
Padding:            0 88px (left/right), vertically centered

ELEMENTS (top to bottom):
1. Category Label   Inter SemiBold 600 / 24px / #CC0000
                    Uppercase / letter-spacing: 8px
                    Margin bottom: 32px

2. Headline         Montserrat Black 900 / 130–170px / #FFFFFF
                    Uppercase / letter-spacing: -3px
                    Line height: 0.88
                    Margin bottom: 48px

3. Red Rule         Full width / 4px / #CC0000
                    Margin bottom: 36px

4. Supporting Line  Montserrat Black 900 / 42–48px / #CC0000
                    Uppercase / letter-spacing: 1px
                    Line height: 1.1

FOOTER (pinned to bottom):
Position:           Absolute / bottom: 56px / left-right: 88px
Left:               URL — Inter 400 / 22px / #444444 / letter-spacing: 4px
Right:              ETKM Logo — 112×112px / White-Red variant
─────────────────────────────────────────────────────────
```

**When to use:** Principles, doctrine statements, quotes, high-volume content.

---

### TYPE A — Statement + Image
**Highest impact. Use for strongest statements.**

```
LAYOUT STRUCTURE (1080×1080)
─────────────────────────────────────────────────────────
Background:         B&W photo — grayscale filter applied in CSS
Overlay:            Dark gradient — rgba(0,0,0,0.45–0.65)
                    Heavier at bottom to protect footer elements
Padding:            0 88px (left/right), vertically centered

Photo rules:
  - Always B&W (CSS: filter: grayscale(100%))
  - Subject faces away or in profile — never direct camera
  - No violence in progress — awareness moment only
  - Background-size: cover / background-position: center

ELEMENTS (same structure as Type B):
1. Category Label   [same spec as Type B]
2. Headline         [same spec as Type B]
3. Red Rule         [same spec as Type B]
4. Supporting Line  [same spec as Type B]

FOOTER:
Right:              ETKM Logo only — no URL on Type A
                    Position: absolute / bottom: 52px / right: 72px
                    Size: 120×120px / White-Red variant
─────────────────────────────────────────────────────────
```

**When to use:** Strongest awareness statements, TOFU scroll-stoppers,
any message that benefits from real-world scene context.

---

### TYPE C — Split Layout
**For people, events, announcements.**

```
LAYOUT STRUCTURE (1200×630 landscape)
─────────────────────────────────────────────────────────
Left panel:         40–45% width / B&W photo / subject faces right
Right panel:        55–60% width / #000000 background

RIGHT PANEL ELEMENTS (top to bottom):
1. Event/Series     Inter SemiBold 600 / 18px / #CC0000
   Label            Uppercase / letter-spacing: 6px

2. Name/Title       Montserrat Black 900 / 72–90px / #FFFFFF
                    2–3 lines maximum

3. Descriptor       Inter 400 / 22px / #BBBBBB
                    Italic, 1–2 lines

4. Key Facts        Montserrat Black 900 / 26px / #FFFFFF
                    One fact per line / bold

5. Red Rule         Full panel width / 2px / #CC0000

FOOTER BAR (full width, very bottom):
Background:         #000000
Text:               Inter 400 / 18px / #444444
                    Date · Location · URL (left)
Logo:               ETKM White-Red / 80×80px (right)
─────────────────────────────────────────────────────────
```

**When to use:** Guest instructors, events, student spotlights, announcements.

---

## PLATFORM CANVAS SIZES

| Platform | Format | Canvas | Graphic Type Priority |
|----------|--------|--------|-----------------------|
| Instagram | Square | 1080 × 1080 px | A or B |
| Instagram | Portrait | 1080 × 1350 px | A or B |
| Instagram | Story / Reel | 1080 × 1920 px | B |
| Instagram | Carousel slide | 1080 × 1080 px | B |
| Facebook | Square | 1080 × 1080 px | A or B |
| Facebook | Landscape | 1200 × 630 px | C |
| Facebook | Story | 1080 × 1920 px | B |
| LinkedIn | Square | 1200 × 1200 px | B or C |
| LinkedIn | Landscape | 1200 × 627 px | C |
| LinkedIn | Portrait | 1080 × 1350 px | B |

**Default format when not specified:**
- Instagram / Facebook: 1080 × 1080 px (Type B or A)
- LinkedIn: 1200 × 1200 px (Type B or C)

---

## LOGO STANDARDS

Three variants — use the correct one per context:

| Variant | File | Use On |
|---------|------|--------|
| White/Red | `ETKM_Circle_Logo_White_Red.png` | Dark backgrounds — default for social |
| White only | `ETKM_Circle_Logo_White.png` | Dark backgrounds where red conflicts |
| Black/Red | `ETKM_Circle_Logo_Black_Red.png` | Light backgrounds |

**Placement:** Always bottom right
**Size on 1080×1080:** 110–120px
**Embedding:** Always base64 embedded — never external URL dependency

---

## TYPOGRAPHY SCALE BY CANVAS SIZE

### 1080 × 1080 (Instagram / Facebook Square)
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Category label | Inter | 24px | 600 |
| Headline | Montserrat | 130–170px | 900 |
| Supporting line | Montserrat | 42–48px | 900 |
| URL | Inter | 22px | 400 |

### 1080 × 1350 (Portrait)
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Category label | Inter | 26px | 600 |
| Headline | Montserrat | 140–180px | 900 |
| Supporting line | Montserrat | 46–52px | 900 |
| URL | Inter | 24px | 400 |

### 1080 × 1920 (Story / Reel)
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Category label | Inter | 28px | 600 |
| Headline | Montserrat | 150–200px | 900 |
| Supporting line | Montserrat | 50–60px | 900 |
| URL | Inter | 26px | 400 |

### 1200 × 1200 (LinkedIn Square)
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Category label | Inter | 26px | 600 |
| Headline | Montserrat | 140–175px | 900 |
| Supporting line | Montserrat | 46–52px | 900 |
| URL | Inter | 24px | 400 |

---

## COPY STANDARDS

### Headline Rules
- Always uppercase
- Maximum 4 words per line
- Maximum 3 lines
- One clear message — no compound ideas
- Must communicate in under 2 seconds at scroll speed

### Supporting Line Rules
- Always uppercase
- One line maximum — two if essential
- Answers ONE question: "what does that mean?" OR "what do I do?"
- Never restates the headline

### Category Label Rules
- Always uppercase
- Always Inter SemiBold
- Always red (#CC0000)
- Examples: AWARENESS / STRESS / PROTECTION / PREPARED / MINDSET / TRAINING

### URL Footer Rules
- Always: ETXKRAVMAGA.COM
- Never: easttxkravmaga.com or any variant
- Always Inter Regular, dark gray (#444444)
- Always present on Type B
- Always present on Type C
- Type A: logo only, no URL

### Prohibited Words (Brand-Wide)
mastery / dominate / destroy / killer / beast / crush / elite / warrior

---

## PRODUCTION METHOD

```
INPUT:   Nathan gives context, principle, quote, or package
         (no additional direction required)

STEP 1:  Claude reads input → identifies message →
         selects graphic type → selects platform

STEP 2:  Claude writes all copy:
         - Category label
         - Headline
         - Supporting line
         - Caption (per platform)

STEP 3:  Claude builds HTML file:
         - Fonts embedded as base64
         - Logo embedded as base64
         - Exact canvas dimensions set as viewport
         - All copy locked in HTML

STEP 4:  Playwright renders HTML → PNG:
         python3 render.py [filename] [width] [height]

STEP 5:  QC — 6 gates before delivery

OUTPUT:  Production-ready PNG at exact platform dimensions
         Ready to post — no additional tools required
```

---

## RENDER SCRIPT (STANDARD)

```python
from playwright.sync_api import sync_playwright
import sys, os

def render(html_path, output_path, width, height):
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
        print(f"Rendered: {output_path} ({os.path.getsize(output_path)//1024}KB)")

# Usage:
# render("graphic.html", "graphic.png", 1080, 1080)
```

---

## QC GATES (ALL 6 — RUN BEFORE DELIVERY)

**GATE 1 — Message Clarity**
- [ ] Headline readable in 2 seconds at scroll speed
- [ ] One clear message — no compound ideas
- [ ] Supporting line answers exactly one question

**GATE 2 — Font Compliance**
- [ ] Headline: Montserrat Black 900 — visually confirmed
- [ ] Labels / URL: Inter — visually confirmed
- [ ] No fallback fonts rendering (Arial, sans-serif defaults)

**GATE 3 — Brand Standards**
- [ ] Background is pure black (#000000)
- [ ] Red used once only
- [ ] No gradients
- [ ] B&W photo only on Type A — no color
- [ ] No violence in progress in imagery

**GATE 4 — Platform Spec**
- [ ] Canvas matches declared platform exactly
- [ ] Text within safe zone (80px from all edges)
- [ ] Logo not clipped
- [ ] Mobile legible at 375px screen width

**GATE 5 — Copy Standards**
- [ ] No prohibited words
- [ ] URL correct: ETXKRAVMAGA.COM
- [ ] Logo: White-Red variant on dark backgrounds
- [ ] Caption written platform-specifically

**GATE 6 — North Star**
- [ ] Would this stop Nathan's scroll?
- [ ] Does this look like it belongs in a Nike campaign?
- [ ] Is this unmistakably ETKM — not generic self-defense content?

---

*Version 1.0 — Locked 2026-03-23*
*Font locked: Montserrat Black 900 (selected by Nathan from live comparison)*
*Production method locked: HTML → Playwright → PNG*
*Authority: Nathan Lundstrom / East Texas Krav Maga*
