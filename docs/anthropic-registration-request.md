# Disk-Mount Skill Registration Request — ETKM

**To:** Anthropic Skills Team
**From:** Nathan Lundstrom — East Texas Krav Maga
**Repo:** `easttxkravmaga/Claude`
**Date:** 2026-04-26

---

## Purpose

Request registration of 14 ETKM skills on the Claude.ai disk mount
(`/mnt/skills/user/`) so they auto-load in chat sessions like the seven
already-mounted skills.

All 14 skills are committed to the repo at `skills/user/<name>/SKILL.md`,
pass the schema validator (`scripts/validate_skills.py`), and are listed in
the auto-generated registry at `SKILLS.md`.

## Currently Mounted (7 skills — for reference)

These are already on the disk mount. Listed in `skills/user/REGISTERED.txt`:

- `etkm-behavior-intelligence`
- `etkm-brand-foundation`
- `etkm-brand-kit`
- `etkm-deliverable-qc`
- `etkm-leadgen-architecture`
- `n8n-workflow-intelligence`
- `nate-collaboration-workflow`

## Pending Registration (14 skills — this request)

Each skill is at `skills/user/<name>/SKILL.md` in the repo. Pull the canonical
copy from there.

| Skill | Version | Purpose |
|---|---|---|
| `etkm-audience-intelligence` | 1.1 | Routing brain for all ETKM audience-specific work |
| `etkm-content-ecosystem` | 1.0 | Production routing skill for ETKM content runs |
| `etkm-crm-operations` | 1.3 | Routing brain for all ETKM CRM and automation work |
| `etkm-cta-architecture` | 1.1 | Single authority on CTA construction for every ETKM deliverable |
| `etkm-marketing-engine` | 1.2 | Routing brain for marketing, funnel, lead gen, content, offer positioning |
| `etkm-notion-intelligence` | 1.1 | Reading, writing, querying ETKM's Notion workspace |
| `etkm-pdf-pipeline` | 1.0 | Locked production pipeline for ALL ETKM branded PDFs |
| `etkm-project-standard` | 1.1 | Master production standard for every ETKM project |
| `etkm-seo` | 1.0 | Writing/reviewing/publishing content for ETKM websites |
| `etkm-system-governance` | 1.0 | Constitution for the ETKM skill and database system |
| `etkm-training-program` | 2.1 | All questions/tasks related to the ETKM training program |
| `etkm-web-production` | 1.0 | Producing HTML or CSS for ETKM |
| `etkm-workflow-registry` | 2.2 | Building/modifying/reviewing/deploying any part of the ETKM system |
| `skill-lifecycle` | 1.1 | Governs full lifecycle of ETKM skill creation and updates |

## After Registration

Once mounted, please update the registration list so we can mirror it in
`skills/user/REGISTERED.txt`. CI surfaces drift between the mount and the repo
— phantoms (registered but not in repo) are flagged in `SKILLS.md`, and
schema/freshness violations fail the build.

## Contact

Nathan Lundstrom — nathan@easttxkravmaga.com (or whatever channel Anthropic prefers).
