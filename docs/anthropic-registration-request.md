# ETKM Skill Registration Request
**Account:** easttxkravmaga@gmail.com
**Repo:** https://github.com/easttxkravmaga/Claude
**Mount path:** /mnt/skills/user/
**Date:** 2026-04-26

## Request

Please add the following 14 skills to the ETKM disk mount at `/mnt/skills/user/`.
All skills are validated, have correct YAML frontmatter, and are committed to
the repo at `skills/user/<skill-name>/SKILL.md`.

## Skills to Register

| Skill | Path | Version | Purpose |
|---|---|---|---|
| etkm-audience-intelligence | skills/user/etkm-audience-intelligence/SKILL.md | 1.1 | Routing brain for audience-specific work |
| etkm-content-ecosystem | skills/user/etkm-content-ecosystem/SKILL.md | 1.0 | Production routing for all content runs |
| etkm-crm-operations | skills/user/etkm-crm-operations/SKILL.md | 1.3 | Routing brain for CRM and automation work |
| etkm-cta-architecture | skills/user/etkm-cta-architecture/SKILL.md | 1.1 | Single authority on CTA construction |
| etkm-marketing-engine | skills/user/etkm-marketing-engine/SKILL.md | 1.2 | Routing brain for all marketing and funnel work |
| etkm-notion-intelligence | skills/user/etkm-notion-intelligence/SKILL.md | 1.1 | All tasks reading/writing ETKM Notion workspace |
| etkm-pdf-pipeline | skills/user/etkm-pdf-pipeline/SKILL.md | 1.0 | Locked production pipeline for all ETKM branded PDFs |
| etkm-project-standard | skills/user/etkm-project-standard/SKILL.md | 1.1 | Master production standard for every ETKM project |
| etkm-seo | skills/user/etkm-seo/SKILL.md | 1.0 | Writing/reviewing/publishing ETKM website content |
| etkm-system-governance | skills/user/etkm-system-governance/SKILL.md | 1.0 | Constitution for the ETKM skill and database system |
| etkm-training-program | skills/user/etkm-training-program/SKILL.md | 2.1 | All questions/tasks related to the ETKM training program |
| etkm-web-production | skills/user/etkm-web-production/SKILL.md | 1.0 | Any task producing HTML or CSS for ETKM |
| etkm-workflow-registry | skills/user/etkm-workflow-registry/SKILL.md | 2.2 | System maintenance, audits, and registry sessions |
| skill-lifecycle | skills/user/skill-lifecycle/SKILL.md | 1.1 | Skill authoring and deployment protocol |

## Currently Registered (do not remove)

- etkm-behavior-intelligence
- etkm-brand-foundation
- etkm-brand-kit
- etkm-deliverable-qc
- etkm-leadgen-architecture
- n8n-workflow-intelligence
- nate-collaboration-workflow

## After Registration

Once confirmed, update `skills/user/REGISTERED.txt` (add the 14 new names,
alphabetically sorted) then run `python scripts/generate_skills_registry.py`
and commit the result.
