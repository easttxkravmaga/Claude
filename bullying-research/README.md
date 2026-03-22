# Bullying Research Intelligence System

K-12 Research Gatherer + Report Builder

Same architecture as the Book Intelligence System. Research in → JSON stored → HTML rendered.

## Directory Structure

```
bullying-research/
├── gather_research.py      ← Step 1: calls Anthropic API + web_search, writes JSON
├── build_report.py         ← Step 2: reads JSON, renders HTML report
├── README.md               ← this file
├── data/
│   ├── tier_k2.json        ← K-2, Ages 5-7
│   ├── tier_35.json        ← 3-5, Ages 8-10
│   ├── tier_68.json        ← 6-8, Ages 11-13
│   ├── tier_912.json       ← 9-12, Ages 14-18
│   └── master.json         ← combined, all tiers
└── output/
    └── bullying_research_report.html   ← final deliverable
```

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

Full run (all 4 tiers + master + report):

```bash
python gather_research.py
python build_report.py
```

Single tier only:

```bash
python gather_research.py --tier k2
python build_report.py --tier k2
```

Valid tier IDs: `k2` | `35` | `68` | `912`

> Recommend running `--tier k2` first as a test. Web search + 7 searches per tier = ~2-3 minutes per tier. If the JSON structure comes back clean on k2, the full run will work.

## What Gets Gathered (per tier)

| Section | What It Contains |
|---------|-----------------|
| **Categories** | Physical / Verbal / Social / Cyber / Identity-based — with age-specific behaviors + warning signs |
| **Commonalities** | Who gets targeted, who bullies, bystander patterns, environments, gender patterns, developmental context |
| **Statistics — National** | Prevalence %, reporting rates, frequency — sourced from CDC, NCES, stopbullying.gov, PACER |
| **Statistics — Regional** | Texas-first, then South/Southwest, then national fallback |
| **Statistics — Outcomes** | Mental health impact, academic performance, absenteeism, long-term effects |
| **Parent Resources** | Real organizations with real URLs — hotlines, websites, guides |
| **Intervention** | Parent action steps, conversation starters, red flags requiring immediate action |

## Age Tier Definitions

| ID | Grades | Ages | Stage |
|----|--------|------|-------|
| `k2` | K–2 | 5–7 | Early Childhood |
| `35` | 3–5 | 8–10 | Late Elementary |
| `68` | 6–8 | 11–13 | Middle School |
| `912` | 9–12 | 14–18 | High School |

## Data Schema (per tier JSON)

```json
{
  "tier_id": "string",
  "grades": "string",
  "age_range": "string",
  "stage": "string",
  "research_date": "ISO date",
  "data_freshness_note": "string",
  "categories": [...],
  "commonalities": { ... },
  "statistics": {
    "national": [...],
    "regional": [...],
    "outcomes": [...]
  },
  "parent_resources": [...],
  "intervention_strategies": { ... },
  "sources_consulted": [...]
}
```

See `gather_research.py` → `SYSTEM_PROMPT` for full schema with all fields.

## Re-running / Refreshing

Data gets stale. Re-run anytime to refresh:

```bash
# Refresh single tier (fastest)
python gather_research.py --tier 68
python build_report.py

# Refresh everything
python gather_research.py
python build_report.py
```

JSON files in `data/` are overwritten each run. Add date-stamped backups manually if needed:

```bash
cp data/master.json data/master_2026-03.json
```

## Output

Single self-contained HTML file:

- Black background, white text, red accents (ETKM brand)
- Tabbed navigation by tier (K-2 / 3-5 / 6-8 / 9-12)
- Five sections per tier: Categories → Commonalities → Stats → Resources → Intervention
- Mobile-responsive
- No external dependencies
