# ETKM Agent Team Playbooks
## Pattern Library — All Project Types

**Authority:** Nathan Lundstrom / East Texas Krav Maga  
**Version:** 1.0  
**Referenced by:** CLAUDE.md (main agent doctrine)  

---

## HOW TO USE THIS FILE

When Nathan gives a goal, match it to a playbook type below.
Copy the team structure, fill in the project-specific details,
and use it as your spawn prompt template.

Every playbook has:
- **Team name pattern** — what to call this team instance
- **Roles** — who does what
- **File ownership map** — who owns what, no overlaps
- **Communication sequence** — who messages whom and when
- **QA criteria** — what this project type specifically fails on
- **Final deliverables** — what Nathan receives

---

## PLAYBOOK 01 — EVENT LANDING PAGE

**Trigger phrases:** "event page", "landing page for [event]", "seminar page", "CBLTAC page", "workshop registration page"

**Team name:** `[EventName]PageTeam`  
**Agent count:** 3  
**Model:** Sonnet

### Roles

**Agent 1 — Copy Writer**  
Goal: Write all page copy for an ETKM event landing page.  
Files owned: `output/copy-draft.md`  
Receives: Event name, date, location, audience, key benefits from main agent  
Produces: Complete page copy — headline, subheadline, all body sections, CTA text, FAQ  
Voice rules: Direct, grounded. PEACE framework optional. No prohibited words.  
When done: Send `output/copy-draft.md` to Developer via message.

**Agent 2 — Developer**  
Goal: Build a production-ready HTML event landing page.  
Files owned: `output/event-page.html`  
Receives: Copy draft from Copy Writer  
Produces: Single self-contained HTML file — no external CDN, black background (#000000),
white text (#FFFFFF), red accent (#CC0000) only, Swiss layout, mobile-responsive,
Stripe or registration button as specified.  
When done: Send file path to QA Agent via message.

**Agent 3 — QA Agent**  
Goal: Validate copy and code against ETKM brand and technical standards.  
Files owned: `output/qa-report.md`  
Receives: File path from Developer  
QA checklist for this project type:
- Zero prohibited words in copy
- No light/white backgrounds anywhere — **automated:** run `node tools/playwright/qc-html.mjs output` and confirm PASS for this file in `output/qa-report-visual.md`
- Red used correctly (accent only, not decorative) — same automated check flags overuse (>12 elements)
- All CTAs present and functional
- No placeholder text remaining
- File is self-contained (no broken external links)
- Mobile layout intact — automated screenshot at 390×844 written to `output/qc-screenshots/<slug>-mobile.png`; QA reviews
- Nathan's experience described in evergreen phrasing only
If failures found: Message Developer (copy issues → message Copy Writer) with numbered list.  
When all gates pass: Confirm PASS to main agent.

### Final Deliverables
- `output/event-page.html` — deploy-ready HTML
- `output/qa-report.md` — pass log
- `output/handoff-notes.md` — WordPress deploy instructions

---

## PLAYBOOK 02 — EMAIL SEQUENCE

**Trigger phrases:** "email sequence", "nurture sequence", "drip campaign", "follow-up emails", "onboarding emails", "WF-00X email sequence"

**Team name:** `[SequenceName]EmailTeam`  
**Agent count:** 3  
**Model:** Sonnet

### Roles

**Agent 1 — Sequence Architect**  
Goal: Design the arc and structure for an ETKM email sequence.  
Files owned: `output/sequence-brief.md`  
Receives: Audience, trigger event (downloaded PDF / booked trial / attended seminar),
number of emails, goal of sequence from main agent  
Produces: Complete sequence brief — each email numbered, subject line, email type
(identity/competency/transition), primary job of each email, arc flow  
When done: Send `output/sequence-brief.md` to Writer via message.

**Agent 2 — Email Writer**  
Goal: Write all emails in the sequence per the brief.  
Files owned: `output/email-sequence.md`  
Receives: Sequence brief from Architect  
Produces: All emails written in full — subject line, preview text, body copy.
Plain text format for 1:1 Pipedrive emails. Pipedrive merge tags use [FIRST_NAME] format.
ETKM voice: direct, grounded, no fluff. No prohibited words.  
When done: Send `output/email-sequence.md` to QA Agent via message.

**Agent 3 — QA Agent**  
Goal: Validate every email against ETKM voice and Pipedrive technical standards.  
Files owned: `output/qa-report.md`  
Receives: Email sequence from Writer  
QA checklist for this project type:
- Zero prohibited words in any email
- No specific year count for Nathan's experience
- Merge tags use correct Pipedrive format [FIRST_NAME]
- Subject lines are not generic (no "Check this out")
- Each email has one clear job — not multiple asks
- Plain text format (no HTML in 1:1 sequences)
- Arc flows correctly — no identity emails in competency phase and vice versa
If failures found: Message Writer with numbered list per email.  
When all gates pass: Confirm PASS to main agent.

### Final Deliverables
- `output/email-sequence.md` — all emails with subjects and preview text
- `output/qa-report.md` — pass log
- `output/handoff-notes.md` — Pipedrive load instructions, which pipeline/stage triggers each email

---

## PLAYBOOK 03 — LEAD GEN PDF

**Trigger phrases:** "lead magnet PDF", "lead gen PDF", "opt-in PDF", "safety guide", "free download", "PDF for [audience]"

**Team name:** `[AudienceName]PDFTeam`  
**Agent count:** 4  
**Model:** Sonnet

### Roles

**Agent 1 — Strategist**  
Goal: Define the content strategy for an ETKM lead gen PDF targeting a specific audience.  
Files owned: `output/pdf-brief.md`  
Receives: Target audience, recognition/relief hook, primary fear to address from main agent  
Produces: Complete PDF brief — title, subtitle, section outline (7 sections max),
key insight per section, CTA placement, next-step funnel link  
Doctrine: Recognition → Relief content model. Lead with the problem they recognize,
deliver relief they did not expect. Every section earns the next.  
When done: Send `output/pdf-brief.md` to Writer via message.

**Agent 2 — Writer**  
Goal: Write all PDF copy per the brief.  
Files owned: `output/pdf-copy.md`  
Receives: PDF brief from Strategist  
Produces: All section copy, headlines, body paragraphs, callout boxes, CTA text.
Voice: direct, grounded. No prohibited words. Audience-specific language.
No academic jargon unless the audience expects it (nurses, LEO, etc.).  
When done: Send `output/pdf-copy.md` to Designer via message.

**Agent 3 — Designer/Builder**  
Goal: Build the production-ready PDF using ReportLab.  
Files owned: `output/[pdf-name].pdf`  
Receives: PDF copy from Writer  
Produces: Brand-compliant PDF — black background, white text, red (#CC0000) accent stripe
on section headers (Gate 4A red stripe — grep audit mandatory), ETKM logo placement,
Swiss layout, page numbers, clean typography.  
When done: Send file path to QA Agent via message.

**Agent 4 — QA Agent**  
Goal: Validate copy and design against ETKM brand standards.  
Files owned: `output/qa-report.md`  
Receives: PDF file path from Designer  
QA checklist for this project type:
- Gate 4A: Red stripe grep audit — confirm red (#CC0000) present on section headers
- Zero prohibited words
- No light/white backgrounds on any page
- No specific year count for Nathan's experience
- Recognition → Relief structure intact (problem before solution in each section)
- CTA present with correct funnel URL
- No placeholder text
- File renders correctly (open and verify)
If failures found: Message responsible agent (copy → Writer, design → Designer) with numbered list.  
When all gates pass: Confirm PASS to main agent.

### Final Deliverables
- `output/[pdf-name].pdf` — production-ready PDF
- `output/qa-report.md` — pass log with Gate 4A confirmation
- `output/handoff-notes.md` — where to host PDF, opt-in page URL, funnel connection

---

## PLAYBOOK 04 — BOOK INTELLIGENCE ASSETS

**Trigger phrases:** "book intelligence", "process this book", "book report", "cheat sheet for [book]", "field manual for [book]"

**Team name:** `[BookName]IntelTeam`  
**Agent count:** 4  
**Model:** Sonnet

### Roles

**Agent 1 — Extractor**  
Goal: Mine the book report for all ETKM-relevant intelligence.  
Files owned: `output/extraction.md`  
Receives: Book report file path from main agent  
Produces: Structured extraction — core concepts, direct applications to self-protection,
ETKM identity transformation moments, behavioral change triggers, quotable insights.
North star: "Learning only happens if there is changed behavior."  
When done: Send `output/extraction.md` to Architect via message.

**Agent 2 — Architect**  
Goal: Design the five-asset package structure from the extraction.  
Files owned: `output/asset-brief.md`  
Receives: Extraction from Extractor  
Produces: Complete brief for all five assets — Field Manual PDF, Validation Brief PDF,
Reading Companion PDF, Cheat Sheet HTML, Instructor DOCX. Each asset outlined with
section structure and key content mapped from extraction.  
When done: Send `output/asset-brief.md` to Builder via message.

**Agent 3 — Builder**  
Goal: Build all five ETKM book intelligence assets per the brief.  
Files owned: `output/field-manual.pdf`, `output/validation-brief.pdf`,
`output/reading-companion.pdf`, `output/cheat-sheet.html`, `output/instructor-guide.docx`  
Receives: Asset brief from Architect  
Produces: All five assets in correct format and brand spec.
HTML: black background, white text, red accent.  
DOCX: Arial, white background, keepWithNext headings.  
PDF: ReportLab, red stripe on section headers.  
When done: Send all file paths to QA Agent via message.

**Agent 4 — QA Agent**  
Goal: Validate all five assets against the Book Intelligence standard.  
Files owned: `output/qa-report.md`  
Receives: All file paths from Builder  
QA checklist for this project type:
- All five assets present and rendering
- Extraction accuracy — content maps back to source
- North star applied: every asset should drive behavioral change
- Brand compliance on all five formats
- No prohibited words
- Identity transformation arc present — not just information, transformation
If failures found: Message Builder with specific asset name and numbered failure list.  
When all gates pass: Confirm PASS to main agent.

### Final Deliverables
- `output/field-manual.pdf`
- `output/validation-brief.pdf`
- `output/reading-companion.pdf`
- `output/cheat-sheet.html`
- `output/instructor-guide.docx`
- `output/qa-report.md`
- `output/handoff-notes.md`

---

## PLAYBOOK 05 — SOCIAL MEDIA CAMPAIGN

**Trigger phrases:** "social campaign", "social media posts", "Facebook posts", "Instagram content", "7-week campaign", "social content for [event]"

**Team name:** `[CampaignName]SocialTeam`  
**Agent count:** 3  
**Model:** Sonnet

### Roles

**Agent 1 — Campaign Strategist**  
Goal: Design the arc and post schedule for an ETKM social media campaign.  
Files owned: `output/campaign-brief.md`  
Receives: Campaign goal, event/offer being promoted, duration, target audience from main agent  
Produces: Complete campaign brief — post schedule by week, content type per post
(awareness/education/social proof/CTA), platform (FB/IG/LinkedIn), PEACE phase mapping,
hook variety plan (no hook type repeated more than twice in a row).  
When done: Send `output/campaign-brief.md` to Writer via message.

**Agent 2 — Copy Writer**  
Goal: Write all post copy per the campaign brief.  
Files owned: `output/post-copy.md`  
Receives: Campaign brief from Strategist  
Produces: All posts written in full — hook, body, CTA, hashtags (Instagram only).
Platform character limits respected. ETKM voice throughout. No prohibited words.
Image brief line included for each post (one sentence describing the visual).  
When done: Send `output/post-copy.md` to QA Agent via message.

**Agent 3 — QA Agent**  
Goal: Validate all posts against ETKM brand and platform standards.  
Files owned: `output/qa-report.md`  
Receives: Post copy from Writer  
QA checklist for this project type:
- Zero prohibited words across all posts
- No specific year count for Nathan's experience
- Character limits respected per platform
- Hook variety — no repeated hook type 3+ in a row
- Each post has one clear CTA (or intentionally no CTA for awareness posts)
- No academic/corporate language
- Image briefs present for all posts
If failures found: Message Writer with post number and failure list.  
When all gates pass: Confirm PASS to main agent.

### Final Deliverables
- `output/post-copy.md` — all posts with platform labels, hooks, body, CTA, image briefs
- `output/qa-report.md` — pass log
- `output/handoff-notes.md` — post schedule, which tool publishes (Canva/Buffer/direct)

---

## PLAYBOOK 06 — WEB PAGE / FUNNEL PAGE

**Trigger phrases:** "web page", "funnel page", "assessment page", "quiz page", "opt-in page", "thank you page", "WordPress page"

**Team name:** `[PageName]WebTeam`  
**Agent count:** 3  
**Model:** Sonnet

### Roles

**Agent 1 — Copy Writer**  
Goal: Write all copy for the ETKM web page.  
Files owned: `output/page-copy.md`  
Receives: Page purpose, audience, funnel position, CTA destination from main agent  
Produces: All page copy — headline, subheadline, body sections, CTA text, any form labels.
Funnel position determines voice: TOFU (awareness/problem), MOFU (solution/benefit), BOFU (commitment/CTA).  
When done: Send `output/page-copy.md` to Developer via message.

**Agent 2 — Developer**  
Goal: Build the production-ready HTML page.  
Files owned: `output/[page-name].html`  
Receives: Page copy from Writer  
Produces: Single self-contained HTML — black background, white text, red accent,
no external CDN, mobile-responsive, any form or embed as specified.  
When done: Send file path to QA Agent via message.

**Agent 3 — QA Agent**  
Goal: Validate copy and code for this funnel page.  
Files owned: `output/qa-report.md`  
Receives: File path from Developer  
QA checklist for this project type:
- Copy serves its funnel position correctly
- Zero prohibited words
- No light/white backgrounds
- CTA links are present and correctly labeled
- Form fields have correct labels (no ID numbers as labels)
- File is self-contained
- Mobile layout intact
If failures found: Message responsible agent with numbered list.  
When all gates pass: Confirm PASS to main agent.

### Final Deliverables
- `output/[page-name].html` — deploy-ready HTML
- `output/qa-report.md` — pass log
- `output/handoff-notes.md` — WordPress deployment steps

---

## PLAYBOOK 07 — CURRICULUM / TRAINING MATERIAL

**Trigger phrases:** "lesson plan", "curriculum build", "training material", "class handout", "Level [X] guide", "drill sheet"

**Team name:** `[MaterialName]CurriculumTeam`  
**Agent count:** 3  
**Model:** Sonnet

### Roles

**Agent 1 — Curriculum Architect**  
Goal: Design the structure and learning objectives for this training material.  
Files owned: `output/curriculum-brief.md`  
Receives: Training topic, student level, class duration or format, delivery method from main agent  
Produces: Complete curriculum brief — learning objectives, section structure, drill/technique list,
vocabulary terms, coaching cues, progression notes.
Principle: Skills without principles are just drills. Every technique is anchored to a principle.  
When done: Send `output/curriculum-brief.md` to Writer via message.

**Agent 2 — Writer**  
Goal: Write the training material per the curriculum brief.  
Files owned: `output/[material-name].docx` or `output/[material-name].pdf`  
Receives: Curriculum brief from Architect  
Produces: Complete training material — formatted, clear, student-facing or instructor-facing
as specified. DOCX: Arial, keepWithNext headings. PDF: ReportLab, red stripe headers.
ETKM-specific terminology only (never substitute generic Krav Maga definitions).  
When done: Send file path to QA Agent via message.

**Agent 3 — QA Agent**  
Goal: Validate training material against ETKM curriculum doctrine.  
Files owned: `output/qa-report.md`  
Receives: File path from Writer  
QA checklist for this project type:
- ETKM-specific terminology used (not generic)
- Technique names match official ETKM naming
- Student level is appropriate (Yellow Belt content ≠ Orange Belt)
- Principles present alongside techniques
- No prohibited words
- Format compliance (DOCX or PDF spec)
If failures found: Message Writer with numbered list.  
When all gates pass: Confirm PASS to main agent.

### Final Deliverables
- `output/[material-name].[format]` — training material
- `output/qa-report.md` — pass log
- `output/handoff-notes.md` — where it goes, how it is used

---

## ADDING NEW PLAYBOOKS

When you complete a project type that does not have a playbook:
1. Document the team structure used
2. Note what worked and what caused problems
3. Add it to this file following the same format
4. Commit the updated file to the repo

The playbook library grows with every project. That is the point.

---

*Version 1.0 — Built 2026-03*  
*Authority: Nathan Lundstrom / East Texas Krav Maga*  
*Maintained in: easttxkravmaga/Claude → docs/agent-team-playbooks.md*
