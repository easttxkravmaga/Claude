# P6 Claude API Prompt — Finalized

**Model:** `claude-haiku-4-5-20251001`
**Max tokens:** 1024
**Updated:** April 2026 — taxonomy replaced with 14 audience arcs + 6 scene intents

---

## System Context

This prompt is embedded in the n8n workflow's Claude API node. It is sent with every image as a multimodal message (image + text). The model returns structured JSON only — no prose.

---

## Prompt Text

```
You are processing an image for East Texas Krav Maga's media library.
The image has already been converted to black and white.

Return ONLY valid JSON. No preamble, no markdown, no explanation.

{
  "description": "1-2 sentence factual description of what is in the image",
  "tags": ["tag1", "tag2"],
  "content_use_cases": ["use case 1", "use case 2"],
  "asset_type": "Image | Video | Graphic | Screenshot"
}

Tag rules:
- Assign 2-4 tags total: 1-2 audience arc tags AND 1-2 scene intent tags
- Do not invent tags outside the taxonomy below

Audience arc tags (assign based on who appears in or would use this image):
  parents, women, men, teens, older-adults, fitness, former-ma, leo-mil,
  private-security, ipv-survivors, occupational, homeschool-faith, corporate, college

Scene intent tags (assign based on what the image communicates):
  awareness   — subject reading environment, scanning, noticing
  recognition — subject has identified something, posture shifts, gaze locks
  decision    — subject positioned to act, weight shifted, path chosen
  presence    — trained confidence at rest, protector identity visible
  contrast    — two states in one frame: aware vs unaware, before vs after
  witness     — identity reveal, face visible, protector moment

Content use cases (select 1-3 that apply):
  Social media post, Email header, Landing page hero, Print ad, PDF/lead magnet,
  Seminar promotion, Curriculum visual aide, Testimonial support,
  Event promotion, Website background
```

---

## Taxonomy Reference

### Audience Arc Tags (14)

Derived from ETKM's 14 audience segments (`etkm-audience-intelligence` skill).

| Tag | Segment |
|---|---|
| `parents` | Parents & Families |
| `women` | Adult Women |
| `men` | Adult Men |
| `teens` | Teenagers (13-17) |
| `older-adults` | Older Adults (55+) |
| `fitness` | Fitness-Motivated Adults |
| `former-ma` | Former Martial Artists & BJJ |
| `leo-mil` | Law Enforcement / Military / First Responders |
| `private-security` | Private Security & Executive Protection |
| `ipv-survivors` | IPV Survivors |
| `occupational` | High-Risk Occupational Workers |
| `homeschool-faith` | Homeschool Families & Faith Communities |
| `corporate` | Corporate & Organizational Groups |
| `college` | College Students & Young Adults (18-26) |

### Scene Intent Tags (6)

Derived from ETKM's Cinematic Visual Doctrine (`etkm-cinematic-doctrine` skill).

| Tag | What It Communicates |
|---|---|
| `awareness` | Subject present, scanning, reading environment |
| `recognition` | Subject has detected something — behavioral shift |
| `decision` | Subject positioned to act — weight shifted, path chosen |
| `presence` | Trained confidence at rest — the protector identity at peace |
| `contrast` | Two states in one frame — unaware vs aware, before vs after |
| `witness` | Identity reveal — face visible, the protector moment |

---

## Design Notes

- **Haiku 4.5** is used (not Sonnet) — structured classification from image, not complex reasoning. Reliable and cost-effective at 100+ images.
- Tag count is capped at 2-4 (1-2 arc + 1-2 scene). Tighter than the original spec — better for querying.
- The `tone` field from the original spec has been removed. Scene intent tags carry that signal.
- If Claude returns malformed JSON, the Code node in n8n strips markdown fences and retries the parse before failing.
- The taxonomy connects directly to ETKM's audience system — images tagged `women` + `decision` are instantly queryable for Adult Women segment campaigns that need that visual context.
