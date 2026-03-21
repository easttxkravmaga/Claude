# ETKM AI Operations Hub
> East Texas Krav Maga — Version-Controlled AI Stack
> Owner: Nathan Lundstrom | etxkravmaga.com
> Last Updated: March 2026

---

## What This Repo Is

Single source of truth for the entire ETKM AI operations stack. Every AI layer — Claude, Gemini, Manus — reads from here. Prompts, skills, workflows, email sequences, CRM logic, and backend code all live here.

---

## Repo Structure

```
easttxkravmaga/Claude/
├── README.md                  ← Master map of the stack
├── skills/                    ← Claude skill files (SKILL.md format)
├── prompts/                   ← System prompts used across the stack
├── workflows/                 ← Email sequences + Make.com docs
│   ├── WF-001-pre-trial/
│   ├── WF-002-onboarding/
│   └── WF-003-cbltac/
├── backend/                   ← Flask app (Railway)
├── crm/                       ← Pipedrive architecture docs
├── registry/                  ← Workflow registry + session protocol
└── docs/                      ← Reference docs for all AI layers
```

---

## AI Role Division

| Task | Owner |
|------|-------|
| All copywriting | Claude |
| Browser automation | Manus |
| Scripting / backend | Claude Code |
| Image prompts | Claude |
| Workflow builds | Manus |
| Research synthesis | Gemini + NotebookLM |

---

## Active Workflows

| ID | Name | Status |
|----|------|--------|
| WF-001 | Pre-Trial Funnel (8 emails) | Near deployment |
| WF-002 | 90-Day Onboarding (28 emails) | Ready to load |
| WF-003 | CBLTAC Campaign (10 emails) | Packaged |

---

## Tool Stack (March 2026)

Claude · Manus · Gemini · NotebookLM · Pipedrive · Make.com · Google Workspace · Notion · Canva · Railway · Square

---

## Brand Constants

- Colors: Black / White / Red (#FF0000)
- Typography: Anton (headlines), Barlow Condensed (body)
- Aesthetic: Swiss International
- Mission: "Go home safe."
- Prohibited words: mastery, dominate, destroy, killer, beast, crush, elite, warrior

---

## Key Links

- https://etxkravmaga.com
- https://fightbacketx.com  
- https://etkmstudent.com
