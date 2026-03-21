# ETKM Asset Registry — New Chat Handover
**Date:** 2026-03-15

---

## The Problem We're Solving

Every time we build something for ETKM, we're inventing it from scratch. No standard names. No locked formats. No agreement on what "a lead magnet" or "an email sequence" actually means in terms of structure, size, or purpose.

The result: Claude builds different versions of the same thing in different sessions, students and prospects get inconsistent deliverables, and workflows never get truly efficient because there's no shared vocabulary.

---

## The Goal

Build an ETKM Asset Registry — a permanent master list of every deliverable type ETKM produces, locked by:

- Permanent ID and name
- Purpose in one sentence
- Format and approximate size
- Required sections / structure
- Which skill builds it
- Which project owns it
- Who the end user is (student / prospect / instructor / Nathan)

Once this registry exists:
- Claude never invents a new asset type without checking the registry first
- "Build a lead magnet" means one specific thing, every time
- Workflows snap together because every asset is a known quantity
- End users always know what they're getting
- New skills reference the registry as their source of truth

---

## Known Asset Types (starting inventory — review and fill gaps)

### Student Assets
| ID | Name | Format | Purpose |
|---|---|---|---|
| 01 | Field Manual | PDF 10–14pp | Behavior change tool per book |
| 02 | Validation Brief | PDF 6–8pp | Third-party credibility doc per book |
| 03 | Content Bank | PDF + DOCX | Tagged content arsenal per book |
| 04 | Cheat Sheet | HTML | Permanent student portal reference |
| 05 | Curriculum Sheet | PDF | Instructor-facing lesson checklist |
| 06 | Reading Companion | PDF | Chapter-by-chapter study guide |

### Marketing & Funnel Assets
| ID | Name | Format | Purpose |
|---|---|---|---|
| 07 | Lead Magnet | PDF 7–10pp | Opt-in exchange |
| 08 | Landing Page | HTML | Single conversion purpose |
| 09 | Email Sequence | Plain text | Nurture / onboarding (Pipedrive tags) |
| 10 | Social Post | Text + brief | Platform-specific content unit |
| 11 | Blog Post | HTML/MD | SEO and awareness content |
| 12 | Video Script | Plain text | Structured for HeyGen or direct record |
| 13 | Canva Image Brief | Structured text | Visual direction document |

### Event Assets
| ID | Name | Format | Purpose |
|---|---|---|---|
| 14 | Event Package | Multi-file | Email campaign + flyer + run sheet + social |
| 15 | Seminar Slide Deck | PPTX/Canva | In-room presentation |

### Operational Assets
| ID | Name | Format | Purpose |
|---|---|---|---|
| 16 | Pipedrive Email Template | Formatted text | Merge-tag, arc-aware |
| 17 | Blueprint PDF | PDF | Personalized student training document |
| 18 | Student Agreement | PDF | Onboarding document |

---

## What We Need to Build

1. Review and finalize the 18 asset types — add missing, remove what doesn't belong
2. For each asset: lock definition, format, structure, owning skill, owning project
3. Create the ETKM Asset Registry as:
   - A GitHub markdown file (machine-readable, referenced by all skills)
   - A Notion page (human-readable, daily reference)
4. Update every relevant skill to reference the registry instead of describing asset formats inline
5. Build a "registry lookup" behavior into Claude so it checks the registry before building any deliverable

---

## Key Principle

The registry is not a catalog of everything we've ever made.
It is the canonical list of what ETKM builds — defined once, used forever.
Nothing ships that isn't on the list. Nothing on the list gets reinvented.

---

## Skill Sync — How Drive and GitHub Stay Aligned

**Drive is the master.** Claude reads skills from Drive every session automatically. GitHub is the version-controlled backup and cross-platform reference.

| Direction | How it works |
|---|---|
| Drive → Claude | Automatic. Claude reads from Drive every session. No action needed. |
| Claude → GitHub | Claude pushes new/updated skills to GitHub via Chrome after building. |
| Claude → Drive | Does NOT exist. Claude cannot write to Drive. Drive stays human-controlled. |

**The gap:** Drive and GitHub can drift if skills are updated in Drive manually without a corresponding GitHub push.

### Also build this in the Asset Registry chat

A **"Skill Sync Check"** command. Nathan says "check skill sync" and Claude:

1. Lists all skills in `/mnt/skills/user/` (from Drive)
2. Lists all skills in GitHub at `skills/user/`
3. Compares versions and timestamps
4. Reports anything that has drifted or is missing from either side
5. Offers to push any Drive-only updates to GitHub automatically

Nathan says two words. System stays in sync. No manual file management.

---

## System Context

| Item | Value |
|---|---|
| Skills location | `/mnt/skills/user/` (Google Drive sync) |
| GitHub repo | easttxkravmaga/Claude |
| Registry target | `docs/ETKM_Asset_Registry.md` |
| Reference | alongside `docs/ETKM_Project_Registry.md` |
| Active projects | P1 Book Intelligence, P2 Event Production, P3 Curriculum Development, P4 Marketing & Funnels, P5 Content Production |
