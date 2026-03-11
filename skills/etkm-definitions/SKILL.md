---
name: etkm-definitions
description: >
  Use this skill whenever a term, concept, or phrase used in the East Texas Krav Maga
  (ETKM) training program needs to be defined, explained, or applied. This includes
  terminology across curriculum levels, coaching language, training concepts, tactical
  phrases, and ETKM-specific vocabulary. Also use for critical distinction pairs:
  Technique vs Principle, Aggression vs Controlled Violence, Confidence vs Dominance,
  Avoidance vs Submission, De-escalation vs Hesitation, Fighting vs Self Defense,
  Skills vs Drills. Trigger when the user asks "what does X mean in ETKM", references
  a training term, needs a definition for a lesson plan or handout, when consistent
  ETKM language is needed in generated content, when writing copy that must use ETKM
  terminology correctly, or when the distinction between two related concepts matters.
  Always use ETKM definitions — never substitute generic Krav Maga or martial arts
  definitions.
---

# ETKM Definitions

**Version:** 2.0
**Last Updated:** 2026-03-09

---

## Source Document (Google Docs — Always Fetchable)

All definitions are maintained in a single Google Doc owned by ETKM.
Use `google_drive_fetch` to retrieve current content before responding.

### How to Fetch

Use the `google_drive_fetch` tool with the document_ids parameter:
google_drive_fetch(document_ids=["1i67-SjMLUrhpsldjCmQMlVQ5VNg2Z8AKqSUPhDqL6nE"])

### Document Reference

| Document | Google Doc ID |
|----------|--------------|
| ETKM Definitions | 1i67-SjMLUrhpsldjCmQMlVQ5VNg2Z8AKqSUPhDqL6nE |

---

## How to Use This Skill

### Step 1 — Fetch the Definitions Document

Use `google_drive_fetch` on the document ID above before answering
any question involving ETKM terminology. Do not rely on the structural
reference below as a substitute for fetching — it exists only as a
fallback and quick orientation.

### Step 2 — Locate the Term

Find the term(s) the user is asking about in the fetched content.

### Step 3 — Apply the Definition

Use the ETKM-specific definition as written. Do NOT substitute general
Krav Maga, martial arts, or fitness industry definitions. ETKM's
language is intentional and principles-first. Preserve the framing
and tone of how ETKM defines each concept.

### Step 4 — Provide Context if Helpful

If the user needs more than a bare definition (lesson plan, student
handout, marketing copy, explaining to a new student), expand using
the definition as the anchor. Do not drift from it.

---

## When ETKM Definitions Apply

Use this skill (and fetch the definitions document) any time you are:

- Writing or reviewing ETKM lesson plans, class outlines, or instructor notes
- Creating student-facing materials (handouts, progressions, assessments)
- Drafting marketing or program descriptions for ETKM
- Explaining training concepts to a student or prospective member
- Ensuring generated content uses consistent ETKM language
- Answering questions about what a specific term means within ETKM
- Writing copy where the distinction between two related concepts matters
- Building content that references the Mindset to Tactics to Skills to Drills to Proficiency progression

---

## Structural Reference (Fallback Only)

This is a quick reference for when the fetch is not possible. Always
use the live document for actual definitions.

### Core Terms

| Term | One-Line Reference |
|------|--------------------|
| Mindset | Mental framework governing perception and response to stress and threat |
| Tactics | Decision-making strategies guiding what you do and when in a dynamic situation |
| Skills | Physical abilities developed through focused repetition of specific movements |
| Drills | Structured exercises combining skills with decision-making under pressure |
| Proficient | Capable of performing reliably and efficiently under pressure, not perfectly |
| Violence | Deliberate use of physical force — understood as reality requiring preparation |
| Fighting | Voluntary willingness to engage in combat, typically ego-driven |
| Self Defense | Response to imposed violence requiring immediate protective action |

### Core Progression

Mindset → Tactics → Skills → Drills → Proficiency

### Critical ETKM Distinction Pairs

| Pair | Key Difference |
|------|---------------|
| Technique vs Principle | Specific mechanical solution vs universal concept governing effective action |
| Aggression vs Controlled Violence | Emotional reactive energy vs deliberate purposeful force |
| Confidence vs Dominance | Quiet certainty from preparation vs need to assert superiority |
| Avoidance vs Submission | Intelligent disengagement vs yielding from fear |
| De-escalation vs Hesitation | Intentional tension reduction vs delay from uncertainty |
| Fighting vs Self Defense | Voluntary engagement vs necessary protective response |
| Skills vs Drills | Building capability (how to move) vs building usability (when and why to move) |

### Unifying Theme

Nearly every training failure comes from confusing motion with decision,
emotion with effectiveness, passivity with strategy, appearance with
capability, or delay with control. ETKM training reinforces:
Clarity → Decision → Action

---

## Core Principle for Using ETKM Definitions

ETKM definitions are principles-first and performance-based. They
describe why something matters and what it produces, not just what
it is. When applying or paraphrasing a definition, preserve this
framing. Avoid generic or decorative language that doesn't reflect
how ETKM actually trains.

---

## Notes

- The former version of this skill pointed to a Notion URL that could
  not be fetched due to JavaScript rendering requirements. This version
  uses a Google Doc that is fully accessible via google_drive_fetch.
- When the Google Doc is updated by Nathan, this skill automatically
  reflects the changes on next fetch. No skill file edits needed.
- If additional definition documents are created, add their Google Doc
  IDs to the Document Reference table above.
