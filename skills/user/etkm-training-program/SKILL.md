---
name: etkm-training-program
version: 2.1
updated: 2026-03-29
description: >
  Use this skill for ANY question or task related to the East Texas Krav Maga (ETKM)
  training program. This includes curriculum structure, level progressions (Yellow
  through Black Belt), training methods, programs offered (Krav Maga, Fight Back ETX,
  Armed Citizen Tactics, Youth, Law Enforcement/EFC), self-defense training, coaching,
  lesson planning, student progression, class structure, workshops, drills, techniques,
  and training material. Also use for EFC (Effective Fitness Combatives) curriculum,
  module breakdowns, and law enforcement/security training content. Trigger whenever
  the user mentions ETKM training, belt levels, Krav Maga curriculum, student
  progression, drills, techniques, workshops, seminars, EFC modules, ACT program,
  Fight Back ETX, youth program, or anything about how ETKM teaches or structures
  its program — even if they don't use the word "skill" or "curriculum" explicitly.
  This skill replaces the former etkm-curriculum skill which has been retired.
  Also covers ETKM terminology and definitions — trigger for "what does X mean
  in ETKM", definition lookups, distinction pairs (Technique vs Principle,
  Fighting vs Self Defense, etc.), and any task requiring consistent ETKM language.
  Absorbs the former etkm-definitions skill.
---

# ETKM Training Program

**Version:** 2.1
**Last Updated:** 2026-03-29
**Replaces:** etkm-curriculum (retired), etkm-definitions (absorbed V2.1)

---

## Source Documents (Google Docs — Always Fetchable)

All content is maintained in Google Docs owned by ETKM. Use `google_drive_fetch`
with the document ID to retrieve current content before responding.

### How to Fetch

Use the `google_drive_fetch` tool with the document_ids parameter.
Example: google_drive_fetch(document_ids=["1iNhu_PR9BNxolM-OUGdT9LekHvy7HEHagWm9sWumkD4"])

### Document Reference Table

| Document | Google Doc ID | Use When |
|----------|--------------|----------|
| ETKM Training Structure | 1iNhu_PR9BNxolM-OUGdT9LekHvy7HEHagWm9sWumkD4 | Overall program overview, training philosophy, level summaries, all programs (Krav Maga, Fight Back ETX, ACT, Youth, LE/Security), training methods, workshops |
| ETKM Workshops | 1FCcxE8GJXNQMtWEhvp9EtLRYMHujXmOxsInbW_Tw734 | Workshop-specific content: Ground Fighting, CQF, Focus Mitt/Thai Pad, LE/Security, ACT, Weapons (handgun, long-gun, knife, blunt object) |
| Level 1 Yellow Belt | 1t2sLzlrJElUndNtrQeJdzj-Q5y0IMn_ummtmF49zuc0 | Level 1 curriculum, mindset, tactics, combatives, defenses, ground fighting, drills |
| Level 2 Orange Belt | 1D2MGaPmGCeo2DyZNxC7KdHYk10LtkK7O1O9E7GgrIYQ | Level 2 curriculum details |
| Level 3 Green Belt | 1Cl_RrXLUNFBHPlW40berfv3xaJmRpLlEoMyfsJUIWE4 | Level 3 curriculum details |
| Level 4 Blue Belt | 1kRukJyuwH7VmecRDTuXWrCzR7oks8f9AdvIEFpdQh3A | Level 4 curriculum details |
| Level 5 Brown Belt | 1Xsm7F9KS_jIFELOVAvzR0Z2Q6iH52dXqFZmms9mcOG8 | Level 5 curriculum details |
| Level 6 Black Belt | 1G1k2hIkUZd1cMjLCmwjCxMk2Aw_A0VAUVSs8JijXqMI | Level 6 curriculum details |
| EFC Program Breakdown | 1vda6UlKrQ2BzB9xlfMmCyp0mkIBVMJXye4vhNHpSEPg | EFC Control Tactics 10-module course, law enforcement/security curriculum, certification structure |

---

## How to Use This Skill

### Step 1 — Identify the Relevant Area

| User Topic | Fetch This Document |
|------------|-------------------|
| What programs does ETKM offer? | Training Structure |
| Self-defense training specifics | Training Structure |
| How ETKM teaches, class structure, training methods | Training Structure |
| Workshop content or workshop-specific topics | Workshops AND Training Structure |
| Curriculum goals and belt progression overview | Training Structure |
| Specific belt level content, techniques, or skills | The relevant Level doc (1-6) |
| Comparing two belt levels | Both relevant Level docs |
| Fight Back ETX, women's self-defense program | Training Structure |
| Armed Citizen Tactics (ACT) program | Training Structure |
| Youth self-defense program | Training Structure |
| Law enforcement or security training | Training Structure AND EFC Program Breakdown |
| EFC modules, certification, control tactics | EFC Program Breakdown |
| Lesson planning for a specific level | The relevant Level doc plus Training Structure for methods |

### Step 2 — Fetch the Document(s)

Use `google_drive_fetch` with the document ID(s) from the table above.
If the question spans multiple areas, fetch multiple documents.

### Step 3 — Respond Using Fresh Content

Answer using the fetched content. Be clear, practical, and organized.
If a fetch fails, note it and offer to answer based on the structural
reference below.

---

## ETKM Curriculum Overview (Structural Reference)

This is a structural reference for when fetching is not possible or
for quick orientation. Always fetch the live documents for actual content.

### Belt Level Progression

| Level | Belt | Theme | Timeline |
|-------|------|-------|----------|
| 1 | Yellow | Foundation — Core principles, basic strikes, situational awareness | 4-6 months at 2x/week |
| 2 | Orange | Control and Counter — More pressure, more angles, stronger escapes | Progressive |
| 3 | Green | Fight for Position — Clinch, takedown survival, chained skills | Progressive |
| 4 | Blue | Advanced Problem Solving — Complexity, fatigue, chaos, environment | Progressive |
| 5 | Brown | Weapons and Higher Threat — Knife/blunt threats, weapon presence | Progressive |
| 6 | Black | Performance Under Stress — Integration, leadership, scenario mastery | Progressive |

### Training Progression Model

Mindset → Tactics → Skills → Drills → Proficiency

This is the ETKM operating sequence. Mindset determines willingness
and clarity. Tactics determine smart choices. Skills determine capability.
Drills determine performance reliability. Proficiency determines
real-world usefulness.

### ETKM Programs

| Program | Audience | Key Focus |
|---------|----------|-----------|
| Krav Maga (Levels 1-6) | General public | Progressive self-defense curriculum |
| Fight Back ETX | Women and youth | Trauma-informed self-defense, 4 levels of readiness |
| Armed Citizen Tactics (ACT) | Concealed carriers, home defenders | Firearms integration with hand-to-hand, shoot house training |
| Youth Self-Defense | Ages 8-14 | Awareness, bully defense, abduction recognition, 3 pillars |
| EFC Control Tactics | Law enforcement, private security | 10-module principle-based defensive tactics, certification |
| Workshops | Current ETKM students | Deep-dive training blocks (Ground, CQF, Weapons, Pads, LE) |

### EFC Five Principles

1. Awareness — Recognition of threats and pre-attack indicators
2. Ability to Maintain Mobility — Movement is life in a weapons-based environment
3. Distance Management — Control when to engage and disengage
4. Winning the Angles — Positioning for leverage, balance, and control
5. Improvise — Disciplined adaptability under dynamic conditions

### EFC 10 Modules (4 hours each)

1. The Fundamentals
2. Single Officer Apprehension and Takedowns
3. Multiple Officer Apprehension and Takedowns
4. Cuffing Compliant and Non-Compliant Subjects
5. Weapon Retention
6. Weapon Defense (Handgun)
7. Weapon Defense (Knife)
8. Weapon Entanglement
9. Wall Pin to Custody
10. Vest Grips and Vehicle Extractions

### Workshop Categories

- Ground Fighting
- Close Quarter Fighting
- Focus Mitt / Thai Pad Work
- Law Enforcement / Security
- Armed Citizen Tactics
- Handgun Defense and Retention
- Long-gun Defense and Retention
- Knife Defense and Offense
- Blunt Object Defense and Offense
- Women's Self Defense Training (Fight Back ETX)
- Youth Self Defense Training

---

## Key Principles to Apply Across All Content

When generating content, lesson plans, coaching advice, or explanations
about ETKM, always reflect these core training principles:

- Realism First — Training simulates real-world threats, not sport
- Progressive Overload — Each level systematically increases complexity and pressure
- Mindset Before Technique — Awareness and decision-making precede physical response
- Principles Over Choreography — Universal concepts over memorized sequences
- Functional Fitness — Physical conditioning is integrated, not separate
- Instructor-Led Consistency — All instruction follows ETKM defined methodology
- Operational Honesty — Train what works, not what looks cool

---

## Common Use Cases

- Generating level-appropriate lesson plans or class outlines
- Explaining what a student should know at any given level
- Comparing two belt levels
- Drafting student progression assessments or testing criteria
- Explaining training methods or program options to prospective students
- Creating drill descriptions or technique breakdowns
- Answering instructor questions about curriculum intent
- Supporting marketing or promotional content about ETKM programs
- Writing EFC proposals or training descriptions for departments
- Building workshop outlines or seminar content
- Creating Fight Back ETX or Youth program marketing materials

---

## ETKM Definitions (Absorbed from etkm-definitions V2.0)

### Definitions Source Document

All definitions are maintained in a Google Doc. Fetch before responding to any terminology question.

Use `google_drive_fetch` with: `document_ids=["1i67-SjMLUrhpsldjCmQMlVQ5VNg2Z8AKqSUPhDqL6nE"]`

### Core Progression

Mindset → Tactics → Skills → Drills → Proficiency

### Core Terms (Quick Reference — always fetch the live doc for full definitions)

| Term | Definition |
|------|-----------|
| Mindset | Mental framework governing perception and response to stress and threat |
| Tactics | Decision-making strategies guiding what you do and when in a dynamic situation |
| Skills | Physical abilities developed through focused repetition of specific movements |
| Drills | Structured exercises combining skills with decision-making under pressure |
| Proficient | Capable of performing reliably and efficiently under pressure, not perfectly |
| Violence | Deliberate use of physical force — understood as reality requiring preparation |
| Fighting | Voluntary willingness to engage in combat, typically ego-driven |
| Self Defense | Response to imposed violence requiring immediate protective action |

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

### Usage Rule

ETKM definitions are principles-first and performance-based. Always use the ETKM-specific definition as written. Do NOT substitute generic Krav Maga, martial arts, or fitness industry definitions. When the Google Doc is updated by Nathan, this skill automatically reflects changes on next fetch.

---

## Notes

- The former etkm-curriculum skill pointed to Notion URLs that could not
  be fetched due to JavaScript rendering requirements. That skill is now
  retired. All curriculum content lives in this skill via Google Docs.
- The former etkm-definitions skill has been absorbed into this skill (V2.1).
  Definitions source document (Google Doc) reference preserved above.
- When Google Docs are updated by Nathan, this skill automatically
  reflects the changes on next fetch. No skill file edits needed.
- If new programs or documents are added, update the Document Reference
  Table above with the new Google Doc ID.

---

## CHANGELOG

- V2.1 — 2026-03-29 — Absorbed etkm-definitions (core terms, distinction pairs, Google Doc reference). Added changelog.
- V2.0 — 2026-03-09 — Full restructure replacing retired etkm-curriculum skill.
