# P6 Claude API Prompt — Finalized

**Model:** `claude-haiku-4-5-20251001`  
**Max tokens:** 1024  
**Use:** Image tagging and description in the n8n pipeline

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
  "tags": ["tag1", "tag2", "tag3"],
  "content_use_cases": ["use case 1", "use case 2"],
  "asset_type": "Image | Video | Graphic | Screenshot",
  "tone": "high-energy | calm-focus | community | instructional | real-world | confidence"
}

Tag rules:
- Assign 3-6 tags from this approved taxonomy only:
  Asset types: training, demonstration, class, seminar, event, headshot, facility, equipment, group, individual, youth, adult, women, cbltac
  Content context: social-ready, print-ready, web-ready, email-ready, testimonial-context, action-shot, portrait, environment, candid, posed
  Campaign/project: fight-back-etx, cbltac, armed-citizen, youth-program, college-safety, private-lessons, open-enrollment, community-event
  Tone: high-energy, calm-focus, community, instructional, real-world, confidence
- Tags must be lowercase, hyphenated
- Do not invent tags outside the taxonomy
- If the image clearly shows youth, always include youth
- If the image is from a CBLTAC event, always include cbltac

Content use case options (select 1-3 that apply):
Social media post, Email header, Landing page hero, Print ad, PDF/lead magnet,
Seminar promotion, Curriculum visual aide, Testimonial support, Event promotion, Website background
```

---

## Design Notes

- **Haiku 4.5** is used (not Sonnet) — this is a classification task, not complex reasoning. Haiku handles structured JSON extraction from images reliably and at lower cost. At 100+ images, cost difference is material.
- The prompt returns `tone` as a single string (not array) — Notion stores it in the Tags field alongside the other tags, or it can be mapped to a separate Select field if Nathan wants it separated later.
- If Claude returns malformed JSON, the Code node in n8n strips markdown fences and retries the parse before failing.
- If Claude API fails entirely, n8n retries once then routes to the Error Logger node.
