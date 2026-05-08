# 05 — AI Campaign Generator

The AI Generator tab posts a form to `/api/ai/generate-campaign`, which calls
the Claude API with an ETKM brand-voice system prompt and writes N draft
posts back to the App's database.

---

## Endpoint

`POST /api/ai/generate-campaign`

### Request body

```json
{
  "program": "Adult Krav Maga",
  "tone": "Direct & confident",
  "goal": "Drive sign-ups for the March Fight Back ETX workshop",
  "platforms": ["facebook", "instagram"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-14",
  "posts_per_platform": 3,
  "campaign_tag": "fight-back-march-2026"
}
```

### Validation

- `program` is **free-text** (1-120 chars). The Compose form provides 5 quick-fill buttons (Adult Krav Maga, Women's Self-Defense, Youth Program, LE / Security, General) that pre-fill this field, but the user can type anything else. No coupling to Notion's tag list.
- `tone` must be one of: `Direct & confident`, `Educational`, `Inspirational`, `Conversational`
- `goal` 10-500 chars, free text
- `platforms` non-empty subset of `["facebook", "instagram", "linkedin"]`
- `start_date` ≥ today, `end_date` ≥ `start_date`, range ≤ 60 days
- `posts_per_platform` 1-14
- `campaign_tag` 3-120 chars, lowercase + hyphens (e.g. `fight-back-march-2026`)

### Response

```json
{
  "ok": true,
  "batch_id": 47,
  "posts_created": 6,
  "redirect": "/scheduler?tab=all&campaign_tag=fight-back-march-2026"
}
```

On Claude API error, returns 502 with `{"ok": false, "error": "..."}`. UI shows red banner.

---

## Claude API call

### Model

`claude-sonnet-4-6` per CLAUDE.md latest-model guidance. Sonnet is the right tier — Opus is overkill for short-form caption generation, Haiku is too constrained on brand voice.

### Request shape (Anthropic Python SDK)

```python
from anthropic import Anthropic

client = Anthropic()  # uses ANTHROPIC_API_KEY env var

resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    system=ETKM_BRAND_VOICE_SYSTEM_PROMPT,  # see below
    messages=[
        {"role": "user", "content": user_prompt}  # see below
    ],
)
```

### System prompt — `ETKM_BRAND_VOICE_SYSTEM_PROMPT`

```
You are a copywriter for East Texas Krav Maga (ETKM) — a self-protection
school in Tyler, Texas, owned and run by Nathan Lundstrom.

You are writing social media post drafts. Nathan reviews and approves each
draft before it publishes. Your job is to produce drafts that match ETKM's
locked brand voice exactly so Nathan has minimal editing to do.

VOICE RULES — non-negotiable:

1. Direct, grounded, no fluff. Plain sentences. No academic register, no
   corporate register, no motivational-poster register.

2. Nathan speaks as a guide — not a cheerleader, not a drill sergeant. Treat
   the reader as a capable adult who is curious about self-protection.

3. When referring to Nathan's experience, use evergreen phrasing: "decades of
   experience", "over four decades", "a lifetime dedicated to self-protection".
   NEVER use a specific year count like "42 years" — those numbers age.

4. PROHIBITED words — never appear in any output:
   mastery, dominate, destroy, killer, beast, crush, elite, warrior, lethal,
   deadly, badass, savage, unstoppable, ultimate, game-changer, revolutionary,
   unleash, superpower

5. NEVER put a clickable URL in a Facebook or Instagram caption — those
   platforms suppress organic reach for posts with links. Use phrases like
   "link in bio" or "DM us for the link" instead. LinkedIn posts CAN include
   links.

6. Hashtags: Facebook posts get 2-4 hashtags max. Instagram posts get 8-15.
   LinkedIn posts get 3-5. Always include #ETKMfamily on FB and IG.

7. Caption length targets per platform:
   - Facebook: 80-200 words. Story arc preferred.
   - Instagram: 50-150 words. Hook in line 1.
   - LinkedIn: 100-300 words. Frame as professional or community-relevant.

8. Every post should serve one of four content pillars: Inspire, Educate,
   Inform, or Convert. The user message will tell you which.

OUTPUT FORMAT — return ONLY a JSON array. No commentary, no preamble:

[
  {
    "platform": "facebook",
    "title": "FB — March Fight Back ETX — Why You Should Come",
    "caption": "...",
    "hashtags": "#ETKMfamily #SelfDefense #FightBackETX",
    "pillar": "Convert",
    "scheduled_date": "2026-03-03"
  },
  ...
]

Each entry MUST include: platform, title (internal, never published, ≤80
chars), caption (the actual post body), hashtags (space-separated), pillar
(one of Inspire/Educate/Inform/Convert), scheduled_date (YYYY-MM-DD).

The scheduled_date you choose must fall inside the campaign date window
provided by the user. Distribute posts evenly across the window.
```

### User prompt template

Constructed server-side from the request body:

```
Generate {total_posts} social media post drafts for an ETKM campaign.

CAMPAIGN GOAL: {goal}
PROGRAM: {program}
TONE: {tone}
DATE WINDOW: {start_date} to {end_date}

PLATFORM DISTRIBUTION:
- Facebook: {n_facebook} posts
- Instagram: {n_instagram} posts
- LinkedIn: {n_linkedin} posts

Distribute the posts across the date window so they are roughly evenly spaced.
Vary the content pillar across the set — don't make all posts Convert. Aim for
40% Inspire, 25% Educate, 20% Inform, 15% Convert across the campaign.

Return the JSON array described in the system prompt. Nothing else.
```

### Parsing the response

Claude returns a single message with `content[0].text` — the JSON array. Parse with `json.loads()`. If parsing fails, retry once with a follow-up message:

```
The previous response could not be parsed as JSON. Return ONLY a valid JSON
array matching the format from the system prompt. No markdown fences, no
commentary.
```

If second attempt also fails, return 502 to the client.

### Persisting the result

For each entry in the parsed array:

1. Create a `posts` row:
   - `title` = entry.title
   - `caption` = `{entry.caption}\n\n{entry.hashtags}` (caption + hashtags concatenated; user can edit)
   - `platform` = entry.platform
   - `media_type` = `none` (AI doesn't generate media; Nathan adds it later in Compose)
   - `scheduled_at` = `{entry.scheduled_date}T09:00:00` (default 9 AM; Nathan adjusts in Compose)
   - `campaign_tag` = request.campaign_tag
   - `status` = `draft`
   - `approved` = false
   - `batch_id` = the new batch row's ID

2. Create a single `batches` row:
   - `name` = `AI: {request.campaign_tag}`
   - `source` = `ai`
   - `row_count` = N
   - All posts in this batch share its `id`.

3. Return the batch_id and the redirect URL.

---

## Cost model

Per call:

| Item | Estimate |
|---|---|
| System prompt | ~600 input tokens |
| User prompt | ~150 input tokens |
| Output (6 posts × ~150 tokens each + JSON scaffold) | ~1,200 output tokens |
| Total per call | ~750 input + 1,200 output |
| Sonnet 4.6 pricing | $3/M input, $15/M output |
| Cost per call | ~$0.02 |

Even at 10 campaigns/month = $0.20/month. Negligible.

### Prompt caching

Add `cache_control` to the system prompt:

```python
system=[{
    "type": "text",
    "text": ETKM_BRAND_VOICE_SYSTEM_PROMPT,
    "cache_control": {"type": "ephemeral"}
}],
```

The system prompt is identical across every call. Cache hit drops input cost to $0.30/M tokens for cached portion = ~95% savings. Worth wiring on day one.

---

## Failure modes

| Failure | Cause | Handling |
|---|---|---|
| Anthropic API 5xx | Transient | Retry once after 2s. If still failing, return 502. |
| Claude returns text instead of JSON | Model drift / prompt failure | Retry with the JSON-only follow-up. If still bad, return 502 with raw response in error field for debugging. |
| Claude returns prohibited word | System prompt failure | Server-side post-process: scan caption against the prohibited word list. If hit, regenerate that single post with an explicit "DO NOT use the word X" amendment to the user prompt. Retry max 3 times per post; if still hits, drop the post from the batch and reduce row_count. |
| Caption exceeds platform limit | Rare | Server-side truncate to platform limit minus 50 chars (room for hashtags); add `…` to indicate truncation. Nathan edits in Compose. |
| Returned date outside window | Possible | Clip to nearest in-window date. |

---

## What the AI Generator deliberately does NOT do

- **No media generation.** Nathan adds images and video manually in Compose. AI generates copy only.
- **No auto-approve.** Every generated post lands as `status="draft", approved=false`. Nathan must explicitly approve before the publisher will fire.
- **No mid-run preview.** No streaming. The user submits the form, sees a spinner, gets the redirect when complete. Total time 8-25 sec.
- **No fine-grained schedule control.** Posts default to 9 AM on their generated date. Nathan adjusts time per post in Compose if needed.

---

# Per-Platform Caption Tailor (B2)

A separate, on-demand endpoint that rewrites a single caption to match one platform's conventions. Powers the "Tailor for X" buttons in Compose.

## Endpoint

`POST /api/ai/tailor-caption`

### Request body

```json
{
  "master_caption": "Train hard. Stay sharp. Real readiness comes from showing up. #ETKMfamily",
  "target_platform": "instagram",
  "program": "Adult Krav Maga",
  "tone": "Direct & confident"
}
```

`program` and `tone` are optional context — if omitted, Claude uses the brand voice rules without program-specific framing.

### Response

```json
{
  "ok": true,
  "tailored_caption": "Real readiness doesn't come from gear or talk. It comes from showing up — every week, on the mat, doing the work.\n\nTrain hard. Stay sharp.\n\n#ETKMfamily #SelfDefense #KravMaga #TylerTX [...12 more hashtags]"
}
```

On Claude API error: 502 with `{"ok": false, "error": "..."}`.

## Claude call

### Model

`claude-sonnet-4-6`. Same as the Campaign Generator.

### System prompt

Same `ETKM_BRAND_VOICE_SYSTEM_PROMPT` as the Campaign Generator (defined earlier in this doc) — plus this addition for the Tailor endpoint:

```
TAILORING MODE:

You will be given a master caption and a target platform. Rewrite the master
caption to fit the target platform's conventions:

- Facebook: 80-200 words. Story arc preferred. 2-4 hashtags max. Links allowed
  but discouraged in caption (use "link in bio" or "DM us").
- Instagram: 50-150 words. Hook in line 1. 8-15 hashtags appended at the end
  (separated by a blank line from the body). NEVER include URLs in the caption.
- LinkedIn: 100-300 words. Professional or community-relevant framing. 3-5
  hashtags inline at the end. URLs ARE allowed for LinkedIn.

Preserve the master caption's intent and core message. Don't introduce new
claims or facts. Don't change the call-to-action.

Return ONLY the rewritten caption text. No JSON, no preamble, no commentary.
The full output is the new caption.
```

### User prompt template

```
TARGET PLATFORM: {target_platform}
PROGRAM CONTEXT: {program or "general ETKM"}
TONE: {tone or "Direct & confident"}

MASTER CAPTION:
{master_caption}

Rewrite the master caption for {target_platform}. Return only the new caption.
```

### Parsing

The response is plain text. Strip leading/trailing whitespace; that's the tailored caption. No JSON parsing.

## Cost per call

| Item | Estimate |
|---|---|
| System prompt | ~700 input tokens (cached) |
| User prompt | ~80 input tokens |
| Output | ~200 output tokens |
| Cost | ~$0.005 per tailor (with prompt caching) |

If Nathan tailors 10 captions per week × 3 platforms = 30 calls × $0.005 = $0.15/month. Negligible.

## Failure modes

| Failure | Cause | Handling |
|---|---|---|
| Claude returns prohibited word | System prompt failure | Server-side scan; if hit, retry with explicit "DO NOT use the word X" amendment. Max 2 retries. If still hits, return 502 with the offending word in the error. |
| Caption exceeds platform limit | Rare given prompt | Server-side truncate to platform max minus 50 chars; append `…`. |
| Anthropic 5xx | Transient | Retry once after 2s; on second failure return 502. |

## What it deliberately does NOT do

- No multi-platform tailoring in one call (each platform is one call — keeps the prompt focused, results consistent)
- No streaming — Compose just shows a spinner on the button
- No automatic save — the tailored caption populates the per-platform caption box; user clicks Save Post when ready

---

*Next: `06-bugs-and-brand-fixes.md` — the three live-build bugs + brand violations that the rebuild must fix.*
