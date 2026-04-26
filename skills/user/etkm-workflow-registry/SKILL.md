---
name: etkm-workflow-registry
version: 2.2
updated: 2026-04-01
description: >
  Use this skill at the start of ANY session involving building, modifying,
  reviewing, or deploying any part of the ETKM system. Prevents duplicate
  work, enforces role boundaries between Claude and Manus, and governs all
  handoffs. Trigger whenever the user is working on any ETKM workflow,
  automation, email sequence, Pipedrive setup, content system, or platform.
  Also trigger when asking what has already been built, or for any
  coordination question between Claude and Manus. Trigger phrases include
  "what's been built", "don't want to duplicate", "what's the status of",
  "is this already done", "before we start building", "check the registry",
  "workflow status", "what does Manus have", "handoff to Manus",
  "ready to deploy", "where did we leave off", "what's next".
---

# ETKM Workflow Registry

**Version:** 2.2
**Last Updated:** 2026-04-01

---

## ROLE DIVISION

Claude writes all copy. Manus executes all automation. Nathan owns all status decisions. Neither Claude nor Manus crosses that line.

| Role | Owner | Rule |
|------|-------|------|
| All copy | Claude | Write it, own it, lock it |
| All automation | Manus | Build it, run it, never rewrite copy |
| All trigger logic | Manus | Pipedrive stages, Calendly signals, send conditions |
| All API prompt design | Claude | System prompts Manus sends to Claude |
| Status updates | Nathan | Nathan moves status; systems only read it |

---

## WORKFLOW STATUS SYSTEM

Check the status of any workflow before starting any task.

| Status | Meaning | Claude Action |
|--------|---------|---------------|
| PLANNED | Concept only, not built | May begin if instructed by Nathan |
| DRAFT | In progress, not approved | Continue from where it stopped, do NOT restart |
| APPROVED | Copy finalized, ready for Manus | Deliver to Manus, do not rewrite unless Nathan instructs |
| LOADED | Manus has imported into system | Read only, flag any changes to Nathan |
| LIVE | Active and running | Read only, flag any changes to Nathan |
| PAUSED | Temporarily halted | Do not modify without Nathan instruction |
| DEPRECATED | Replaced or retired | Do not use or reference as current |

---

## SESSION OPENING PROTOCOL

Three mandatory steps before any build session begins.

Step 1 - Load this skill and confirm it is active.

Step 2 - Fetch the live Workflow Registry from the ETKM AI Resources folder:
https://drive.google.com/drive/folders/1QhTAuNgHYyN0lYnZItlr24O4DicwHkWj

Step 3 - Declare intent before starting work:
- "I am about to build/modify: [workflow name]"
- "Registry shows current status: [status]"
- "Dependencies required: [list]"
- "Proceeding / Flagging for Nathan review"

If status is ambiguous or a dependency is missing, STOP and ask Nathan.

---

## THE REGISTRY IS NEVER OPTIONAL

If Claude cannot access the registry, Claude does not guess.
Claude stops and tells Nathan. No registry access means no build.

---

## CRM ARCHITECTURE REFERENCE

The ETKM Pipedrive system uses 5 pipelines. Full structure and rules
live in the etkm-crm-operations skill. This is the quick reference so
every session knows the landscape.

| Pipeline | Name | Purpose |
|----------|------|---------|
| P1 | Prospects | New lead through trial and signup (WF-001 lives here) |
| P2 | Level 1 Students | Yellow Belt tracking, first 90 days, highest dropout risk |
| P3 | Adv / Exp. Students | Orange through Black Belt progression |
| P4 | At Risk / Retention | At-Risk, Intervention, Re-Engaged, PIF Due, Payment Due, Alumni |
| P5 | Private Lesson | Personalized training consultation and delivery |

Belt level and arc classification are tracked via Pipedrive labels.
PIF is a permanent Financial Status label visible across P2 and P3.
The retired "Lapsed" label does not exist in the active system.
Events are NOT a Pipedrive pipeline — managed entirely by n8n automation.
Warm event contacts are deposited into P1 with labels already applied.

For full pipeline stages, label dictionary, and automation rules,
load etkm-crm-operations.

---

## MASTER WORKFLOW INVENTORY

### PRE-TRIAL FUNNEL

[WF-001] Pre-Trial Email Funnel - 6 Arcs
- Status: LIVE, three deployment dependencies remaining
- Arcs: Safety, Parent, Fitness, LE/Mil, Former MA, Default
- Emails: 8 per arc (booking confirmation with PDF, 24hr reminder, morning-of, no-show recovery, post-visit nurture, soft follow, reschedule ack, cancellation recovery)
- Trigger: Calendly Q&A answers feed Pipedrive arc classification via n8n + Claude API
- Arc classification logic: safety/fear keywords to Safety, family/kids to Parent, fitness to Fitness, LE/military keywords to LE/Mil, prior training to Former MA, empty to Default
- Deliverables: Welcome PDF ("Before You Walk In"), complete email sequence DOCX, Claude API system prompt for Manus
- Open Dependencies: See Dependency Tracker below
- Notes: Copy is locked. Do not rewrite without Nathan instruction.

### STUDENT ONBOARDING

[WF-002] 90-Day Onboarding Sequence - 28 Emails
- Status: BUILT, pending Manus load
- Structure: Phase 1 Belonging Days 1-30, Phase 2 Noticing Days 31-60, Phase 3 Becoming Days 61-90
- Composition: 15 identity emails plus 13 competency emails (C-01 through C-13)
- Email 1 delivers the ETKM Journey Map URL as primary action (triggers on Pipedrive Stage 7 Signed Up)
- Competency emails bridge to existing website articles on etxkravmaga.com
- 4 website pages flagged for voice rewrite before linking: Class Structure, What is Mindset, Beginner Tactics, Goals
- Phase-transition emails at Days 30 and 60: status DRAFT, incomplete at last session
- Deliverable: ETKM_Competency_Email_Sequence.docx (combined sequence with Manus automation rules)
- Trigger: P1-S6 stage move triggers n8n workflow, which creates P2 deal and fires sequence
- Notes: Copy substantially complete. Competency layer approved. Phase-transition emails and combined master sequence table may need completion.

### EVENT MARKETING

[WF-003] John Wilson / CBLTAC Specialty Event Campaign
- Status: APPROVED, install package delivered
- Event: April 24-25, 2026 at LifePoint Fellowship Church, 13973 State Hwy 64, Tyler TX 75704
- Courses: Impulse Control (Friday $75), Personal and Travel Safety plus Combating Stress (Saturday $125), Both Days $175
- Registration: etxkravmaga.com/cbltac-courses/
- Deliverables: 10 HTML email files on ETKM branded template, Send Calendar DOCX, Manus Install Briefing DOCX, delivered as WF-003-CBLTAC-Campaign.zip
- PEACE framework slogans integrated as attention anchors across all 10 emails
- Core pain point: the gap between knowing and doing under pressure
- Social campaign: 7-week plan, 22 FB/IG posts, 3 LinkedIn posts, 4 phases (Awareness, Interest, Urgency, Last Call), Canva image briefs delivered
- Open Dependency: Confirm Manus has loaded the install package

### SOCIAL MEDIA

[WF-004] 52-Week PEACE Slogan Social Calendar
- Status: LIVE, Nathan posts manually
- Format: Excel with Week, Phase, Heading, Sub-Headline columns, color-coded by phase
- 4 phases: Awareness to Reality to Readiness (1-13), Agency to Action to Capability (14-26), Identity to Empowerment to Presence (27-39), Leadership to Responsibility to Protector Mindset (40-52)
- Notes: Manus not involved. Lives in Google Drive.

[WF-005] March Monthly/Weekly Messaging Themes
- Status: LIVE
- 5 weekly themes around Distance Management, rebuilt in ETKM brand voice
- Includes student emails and social media bullets per week

[WF-006] The Reclaim - Sarah's Story
- Status: APPROVED, available for deployment
- Segment: Adult women
- Notes: Available for social, email, and website use.

### SALES

[WF-007] Sales Communication System
- Status: LIVE, reference document
- Includes: Post-class conversation guides, pre-packaged analogies (especially BJJ comparisons), objection responses, follow-up sequences
- Philosophy: Advisor not salesperson
- Notes: Audio study version planned by Nathan.

### CONTENT SYSTEMS

[WF-008] Core Five-Skill Brand System
- Status: LIVE
- Skills: etkm-brand-foundation, etkm-audience-map, etkm-problem-solution, etkm-story-arcs, etkm-messaging-playbook

[WF-009] Extended Skill Library
- Status: LIVE
- Skills: etkm-training-program, etkm-definitions, etkm-curriculum, etkm-brand-kit, etkm-funnel-master, etkm-content-templates, etkm-nurture-sequence, etkm-lead-gen, etkm-crm-operations, etkm-workflow-registry, nate-collaboration-workflow
- Known issues: etkm-definitions, etkm-curriculum, and etkm-training-program rely on Notion page fetching which fails due to JavaScript rendering requirements. These skills need content embedded directly. etkm-brand-kit description needs stronger trigger phrases. etkm-event-planning is listed in prior registry but not installed in skill directory.

[WF-010] Visual Aide Builder Application
- Status: LIVE
- 16 visual aide types, ETKM brand palette, transparent PNG export

[WF-011] First-Touch Landing Page PDF
- Status: APPROVED
- Title: "Protect What Matters"
- Purpose: StoryBrand-structured PDF for first-time website visitors, exposes problem and positions ETKM as solution
- 7 pages, Swiss International layout, full StoryBrand arc
- Thank you message rewritten with PDF download link (Option 2 selected)
- Notes: Needs Google Drive hosting link for deployment.

[WF-012] "Aware and Able" Blog Series
- Status: DRAFT
- 6-post series with full funnel action plan
- Arc: Posts 1-3 pure value/education (TOFU), Posts 4-6 bridge to solution (MOFU to BOFU)
- Nathan defined 7-step production workflow: outlines, discuss and configure, write draft, edits, final draft, plan of attack with flowchart mapping emails/social/PDF, implement TOFU/MOFU/BOFU
- Full action plan HTML deliverable produced covering 7-day implementation
- Notes: Outlines stage in progress. Writing not yet started.

[WF-013] Cinematic Prompt Generator
- Status: LIVE
- v4 with sightline zone builder, AR overlay system, behavioral state layer
- Scene intent categories, platform destination presets, ETKM tactical overlay doctrine
- 12 pre-built scene descriptions delivered as DOCX
- Notes: Campaign Planner layer identified as natural next build.

[WF-014] Curriculum Checklist Sheets
- Status: APPROVED
- Instructor-facing checklist sheets organized by track and two-week block codes
- Beginner (Level 1 Yellow Belt): 6 sheets A1 through B3, cycles 4x per year
- Intermediate (Levels 2-3 Orange/Green): 12 sheets A1 through D3, 1x per year
- Advanced (Levels 4-5 Blue/Brown): 12 sheets A1 through D3, 1x per year
- Format: All-white background, black font, black header bar, red accent line
- No "Sheet" in header, no Instructor/Date fields
- Notes: Balanced row counts (20-25 per sheet). Each sheet is a standalone class-building menu.

[WF-015] Student and Class Etiquette Agreement
- Status: APPROVED
- Two-page PDF, brand-compliant (red used only once as "Train Hard." attention phrase)
- Includes professional conduct policy prohibiting romantic/dating conduct between students
- Signature block: Print Name, Signature, Date (student and parent/guardian on page 2)
- Notes: Final version follows strict ETKM brand kit.

[WF-016] Student Intake Form and Flask Backend
- Status: BUILT, pending Railway deployment
- Multi-step HTML form (3 steps: Starting Point, Goals, Learning Profile) on etkmstudent.com
- ETKM brand standards: black/white/red palette, Barlow Condensed headlines, tile-style inputs
- Backend: Flask app (app.py) creates Person, Deal, and formatted Note in Pipedrive
- Deployment: Railway with 4 Pipedrive credentials as environment variables
- Open Dependencies: Nathan needs Railway account, Pipedrive API token, Pipeline ID, Stage 7 ID
- Notes: Manus built the backend. no-cors flag must be removed once Railway is live.

[WF-017] "The Awareness Advantage" Content Ecosystem
- Status: APPROVED
- 5 blog articles (13,031 total words), 7-email sequence, 20 Facebook posts, 15 LinkedIn posts
- Series based on Left of Bang / situational awareness doctrine
- Notes: Complete content ecosystem ready for deployment.

[WF-018] Free Trial Landing Page Rewrite
- Status: APPROVED
- Full StoryBrand-structured rewrite of etxkravmaga.com/free-trial-lesson/
- Delivered as markdown with change log
- Highest priority actions: verify form renders (test incognito desktop and mobile), add real student testimonial
- Notes: Copy delivered. Implementation on WordPress pending.

### PLATFORMS

| Platform | Status | Notes |
|----------|--------|-------|
| etxkravmaga.com | LIVE | General training site, free trial page rewrite pending implementation |
| fightbacketx.com | LIVE | Women's self-defense |
| etkmstudent.com | PLANNED | Content rewrite queued, intake form built but not yet deployed |
| Pipedrive CRM | LIVE | 5-pipeline architecture (P1-P5), 27+ labels, Manus runs all automation |
| Manus Automation | LIVE | Calls Claude API via claude-sonnet-4-6 |
| Calendly | LIVE | Integrated directly with Pipedrive, drives arc classification |
| Notion | LIVE | Curriculum database, definitions |
| n8n | LIVE | All webhook workflows and platform integrations — etxkravmaga.app.n8n.cloud |
| Make.com | DEPRECATED | Fully removed from stack — replaced by n8n (April 2026) |
| Railway | PLANNED | Flask backend for intake form |
| Google Drive | LIVE | AI Resources folder, PDF hosting, shared documents |

---

## OPEN DEPENDENCY TRACKER

| ID | Item | Needed By | Status | Notes |
|----|------|-----------|--------|-------|
| D-01 | Live Calendly booking URL in arc emails | WF-001 | VERIFY | May already be resolved via direct Calendly-Pipedrive integration |
| D-02 | Google Drive PDF link in Email 1 | WF-001 | PENDING | Welcome PDF needs hosted link |
| D-03 | Anthropic API key activation | Manus to Claude API | IN PROGRESS | Nathan walked through console.anthropic.com setup |
| D-04 | John Wilson event registration URL | WF-003 | VERIFY | etxkravmaga.com/cbltac-courses/ may already serve this purpose |
| D-05 | etkmstudent.com content rewrite | Platform, WF-016 | PLANNED | Queued but not started |
| D-06 | 4 website pages voice rewrite | WF-002 competency emails | PENDING | Class Structure, What is Mindset, Beginner Tactics, Goals |
| D-07 | Railway account and credentials | WF-016 | PENDING | Nathan needs to create Railway account and gather 4 Pipedrive values |
| D-08 | Real student testimonial | WF-018 | PENDING | Needed for free trial landing page conversion |
| D-09 | Form render verification | WF-018 | PENDING | Test free trial page form in incognito on desktop and mobile |
| D-10 | Manus load confirmation for WF-003 | WF-003 CBLTAC campaign | VERIFY | Install package delivered, confirm Manus has loaded |
| D-11 | WF-002 phase-transition emails | WF-002 | DRAFT | Days 30 and 60 transition emails incomplete |
| D-12 | Notion skill migration | WF-009 skills | PLANNED | etkm-definitions, etkm-curriculum, etkm-training-program need content embedded directly |
| D-13 | n8n workflow builds | WF-001, WF-002, Events, At-Risk | IN PROGRESS | Manus handoff brief delivered (ETKM_Make_to_n8n_Handoff.docx). Priority: 1A Calendly→Pipedrive, 1B WF-001 arc classification, 2 WF-002 trigger, 3 Events, 4 At-Risk |

---

## UPCOMING BUILD QUEUE

Items discussed but not yet started. Nathan determines sequence.

| Item | Source Session | Notes |
|------|---------------|-------|
| Campaign Planner layer for Cinematic Prompt Generator | WF-013 session | 4-week content arc sequencer |
| PEACE framework reusable skill | WF-003, WF-004 sessions | Prepared, Empowered, Aware, Capable, Engaged with slogans per letter |
| Reusable email campaign style skill | WF-003 session close | Nathan wants to document the CBLTAC email style and PEACE integration as a repeatable skill |
| Shopify store build | Strategy session | Replace Ecwid, connect to n8n and Pipedrive, merchandise plus digital products plus event tickets |
| Remaining monthly messaging themes (April through December) | WF-005 session | March complete, 9 months remaining |
| YouTube content development | Social media strategy | Platform identified but not yet active |
| HeyGen integration | Tool stack planning | Coming soon per Nathan |
| Master roadmap from brain dump session | Roadmap session | 5 buckets identified, brain dump not yet completed |

---

## COPY RULES

Prohibited words: mastery, dominate, destroy, killer, beast, crush, elite, warrior

Merge tag format: [square_bracket] style only, Pipedrive standard

Primary domain: etxkravmaga.com

Women's domain: fightbacketx.com

Student portal: etkmstudent.com

Voice: Advisor not salesperson. Student is the hero. ETKM is the guide.

Core mission: Go Home Safe.

Tagline: No fluff, touch the stress, expose realities, train to GO HOME SAFE.

PEACE Framework: Prepared, Empowered, Aware, Capable, Engaged.

---

## HANDOFF PROTOCOL: CLAUDE TO MANUS

When delivering approved copy, Claude provides:
1. Workflow name and version number
2. Status: APPROVED
3. Complete copy with all merge tags in place
4. List of all dependencies and open items
5. Explicit note that Manus does not rewrite this copy

When Manus needs a change: Manus flags to Nathan, Nathan instructs Claude, Claude delivers revision, Manus loads revised copy.

---

## TOOL STACK REFERENCE

| Tool | Role |
|------|------|
| Claude (chat, Cowork, Code) | All writing, copy, documentation, planning, skill development |
| Manus | Browser automation, n8n builds, Pipedrive implementation |
| ChatGPT | Secondary AI, specific use cases |
| Pipedrive | CRM, 5-pipeline architecture, email delivery |
| Google Workspace | Drive storage, Docs for shared references, AI Resources folder |
| n8n | All webhook workflows and platform integrations — replaces Make.com |
| Notion | Curriculum database, definitions |
| NotebookLM | Research and reference |
| Gemini | Secondary AI |
| Canva | Graphic design, social media images |
| HeyGen | Video content (coming soon) |
| Calendly | Trial booking, arc classification source |
| Railway | Flask backend hosting (planned) |

---

## WHEN IN DOUBT

1. Check the registry first
2. If status is unclear, ask Nathan before proceeding
3. If a workflow exists in any non-PLANNED status, do not rebuild from scratch
4. If Claude and Manus outputs conflict, Nathan resolves it
5. If a dependency is marked VERIFY, confirm with Nathan before assuming resolved

---

## CHANGELOG

- V2.2 — 2026-04-01 — Make.com fully removed from stack. All automation references updated to n8n (etxkravmaga.app.n8n.cloud). Platforms table updated: Make.com → DEPRECATED, n8n → LIVE. Tool Stack updated. WF-001 trigger note updated. WF-002 trigger note updated. Shopify queue item updated. D-13 added for n8n build tracking. CRM Architecture Reference updated (etkm-crm-doctrine reference corrected to etkm-crm-operations). No copy or logic changes.
- V2.1 — 2026-03-29 — V2 skill consolidation. etkm-make-automation archived. etkm-crm-operations established as replacement for etkm-crm-doctrine + etkm-pipedrive-manus + etkm-make-automation.
