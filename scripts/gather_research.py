"""
Bullying Research Intelligence System — gather_research.py
===========================================================
Calls Anthropic API with web_search to gather structured bullying
research for each K-12 age tier. Outputs one JSON file per tier
plus a master combined file.

Usage:
    python gather_research.py               # runs all 4 tiers
    python gather_research.py --tier k2     # runs one tier: k2 | 35 | 68 | 912
    python gather_research.py --all         # explicit full run

Output:
    data/tier_k2.json
    data/tier_35.json
    data/tier_68.json
    data/tier_912.json
    data/master.json

Requirements:
    pip install anthropic
    ANTHROPIC_API_KEY in environment
"""

import anthropic
import json
import os
import sys
import time
import argparse
from datetime import datetime

# ──────────────────────────────────────────────
# AGE TIER DEFINITIONS
# ──────────────────────────────────────────────

TIERS = {
    "k2": {
        "id": "k2",
        "label": "Kindergarten – 2nd Grade",
        "grades": "K–2",
        "age_range": "Ages 5–7",
        "stage": "Early Childhood",
        "search_terms": "kindergarten first second grade bullying ages 5 6 7",
        "parent_focus": "recognition in young children, teacher communication, emotional vocabulary"
    },
    "35": {
        "id": "35",
        "label": "3rd – 5th Grade",
        "grades": "3–5",
        "age_range": "Ages 8–10",
        "stage": "Late Elementary",
        "search_terms": "elementary school bullying grades 3 4 5 ages 8 9 10",
        "parent_focus": "social exclusion, peer groups forming, first signs of cyberbullying"
    },
    "68": {
        "id": "68",
        "label": "6th – 8th Grade",
        "grades": "6–8",
        "age_range": "Ages 11–13",
        "stage": "Middle School",
        "search_terms": "middle school bullying grades 6 7 8 ages 11 12 13",
        "parent_focus": "cyberbullying spike, social hierarchy, identity-based targeting, mental health impact"
    },
    "912": {
        "id": "912",
        "label": "9th – 12th Grade",
        "grades": "9–12",
        "age_range": "Ages 14–18",
        "stage": "High School",
        "search_terms": "high school bullying grades 9 10 11 12 ages 14 15 16 17 18",
        "parent_focus": "advanced cyberbullying, dating violence overlap, reporting reluctance, long-term mental health"
    }
}

# ──────────────────────────────────────────────
# SYSTEM PROMPT — RESEARCH EXTRACTOR
# ──────────────────────────────────────────────

SYSTEM_PROMPT = """You are a precision research analyst. Your job is to gather accurate,
current bullying research data for a specific K-12 age group and return it as structured JSON.

CRITICAL RULES:
1. Use web_search to find REAL statistics — never fabricate numbers.
2. Every stat must include its source name and approximate year.
3. If a stat cannot be verified, mark it with "unverified": true.
4. Search specifically for the age tier provided — do not substitute adjacent grade data.
5. Regional stats: prioritize Texas if available, then South/Southwest, then national.
6. Parent resources: only real organizations with real URLs.
7. Return ONLY valid JSON — no markdown, no explanation, no backticks.
8. All string values must be properly escaped.

JSON SCHEMA TO FOLLOW EXACTLY:
{
  "tier_id": "string — k2 | 35 | 68 | 912",
  "grades": "string",
  "age_range": "string",
  "stage": "string",
  "research_date": "string — ISO date",
  "data_freshness_note": "string — note about how current the data is",

  "categories": [
    {
      "name": "string — category name",
      "description": "string — what this type looks like at THIS age",
      "prevalence_note": "string — how common at this age tier",
      "age_specific_behaviors": ["string", "string"],
      "warning_signs": ["string", "string"],
      "escalation_risk": "low | medium | high"
    }
  ],

  "commonalities": {
    "who_is_targeted": {
      "summary": "string",
      "risk_factors": ["string", "string"],
      "protective_factors": ["string", "string"]
    },
    "who_bullies": {
      "summary": "string",
      "common_traits": ["string"],
      "motivations": ["string"]
    },
    "bystander_behavior": {
      "summary": "string",
      "typical_response": "string",
      "intervention_rate": "string"
    },
    "environments": ["string — where it most commonly occurs at this age"],
    "gender_patterns": "string — any notable differences between genders at this age",
    "developmental_context": "string — why THIS age group is developmentally vulnerable"
  },

  "statistics": {
    "national": [
      {
        "stat": "string — the finding",
        "value": "string — number or percentage",
        "source": "string — organization or study name",
        "year": "string",
        "unverified": false
      }
    ],
    "regional": [
      {
        "region": "string — Texas | South | Southwest | etc.",
        "stat": "string",
        "value": "string",
        "source": "string",
        "year": "string",
        "unverified": false
      }
    ],
    "outcomes": [
      {
        "stat": "string — what happens to kids who are bullied",
        "value": "string",
        "source": "string",
        "year": "string",
        "unverified": false
      }
    ]
  },

  "parent_resources": [
    {
      "name": "string — organization or resource name",
      "url": "string — real URL",
      "type": "hotline | website | guide | program | app",
      "description": "string — what it provides for parents",
      "best_for": "string — what specific situation or need this serves",
      "free": true
    }
  ],

  "intervention_strategies": {
    "for_parents": ["string — specific action a parent can take"],
    "conversation_starters": ["string — actual phrases parents can use with their child"],
    "red_flags_requiring_immediate_action": ["string"]
  },

  "sources_consulted": [
    {
      "name": "string",
      "url": "string",
      "type": "government | academic | nonprofit | news"
    }
  ]
}"""

# ──────────────────────────────────────────────
# RESEARCH PROMPT BUILDER
# ──────────────────────────────────────────────

def build_research_prompt(tier: dict) -> str:
    return f"""Research task: Gather comprehensive bullying data for {tier['label']} ({tier['age_range']}, {tier['stage']}).

SEARCH SEQUENCE — execute these searches in order:

1. CATEGORIES: Search "{tier['search_terms']} types of bullying statistics"
   Find: physical, verbal, social/relational, cyberbullying, identity-based categories
   Get age-specific manifestations — what does each TYPE look like for {tier['age_range']}?

2. STATISTICS — NATIONAL: Search "{tier['search_terms']} bullying prevalence statistics data"
   Target sources: stopbullying.gov, CDC, NCES, Pacer Center, HRSA
   Find: prevalence %, frequency, reporting rates, gender breakdown

3. STATISTICS — OUTCOMES: Search "{tier['age_range']} bullying mental health academic outcomes research"
   Find: anxiety rates, depression correlation, academic impact, absenteeism data

4. REGIONAL/TEXAS: Search "Texas bullying statistics schools" and "Southeast United States bullying rates"
   Find: any Texas-specific data, state report cards, TAPR data if available

5. WHO IS TARGETED: Search "{tier['search_terms']} who gets bullied risk factors"
   Find: characteristics of targets, risk factors, protective factors at this age

6. PARENT RESOURCES: Search "bullying resources for parents {tier['age_range']} help"
   Find: stopbullying.gov resources, PACER, local Texas resources, hotlines
   Verify URLs are real before including

7. INTERVENTION: Search "how parents should respond to bullying {tier['age_range']}"
   Find: evidence-based parent responses, conversation strategies, school reporting steps

Now compile all findings into the required JSON schema.
Age tier ID for this run: {tier['id']}
Research date: {datetime.now().strftime('%Y-%m-%d')}

Return ONLY the JSON object. No preamble, no explanation."""


# ──────────────────────────────────────────────
# API CALLER
# ──────────────────────────────────────────────

def gather_tier_data(tier_id: str, client: anthropic.Anthropic) -> dict:
    """Calls Anthropic API with web_search for one age tier. Returns parsed JSON dict."""

    tier = TIERS[tier_id]
    print(f"\n{'='*60}")
    print(f"  RESEARCHING: {tier['label']} ({tier['age_range']})")
    print(f"{'='*60}")

    prompt = build_research_prompt(tier)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ],
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the final text block (after tool use cycles)
        raw_text = ""
        for block in response.content:
            if block.type == "text":
                raw_text = block.text

        if not raw_text:
            print(f"  WARNING: No text content returned for {tier_id}")
            return {"error": "No text content", "tier_id": tier_id}

        # Strip any accidental markdown fences
        raw_text = raw_text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            raw_text = raw_text.rsplit("```", 1)[0]

        data = json.loads(raw_text)
        print(f"  SUCCESS: {len(data.get('statistics', {}).get('national', []))} national stats | "
              f"{len(data.get('categories', []))} categories | "
              f"{len(data.get('parent_resources', []))} parent resources")
        return data

    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON parse failed for {tier_id}: {e}")
        print(f"  Raw response preview: {raw_text[:300] if raw_text else 'empty'}")
        return {"error": f"JSON parse error: {str(e)}", "tier_id": tier_id, "raw": raw_text}

    except anthropic.APIError as e:
        print(f"  ERROR: API error for {tier_id}: {e}")
        return {"error": f"API error: {str(e)}", "tier_id": tier_id}


# ──────────────────────────────────────────────
# FILE WRITER
# ──────────────────────────────────────────────

def save_tier_data(tier_id: str, data: dict):
    """Saves tier data to data/tier_{id}.json"""
    os.makedirs("data", exist_ok=True)
    filepath = f"data/tier_{tier_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  SAVED: {filepath}")
    return filepath


def build_master_file():
    """Combines all tier JSON files into data/master.json"""
    master = {
        "title": "Bullying Research Intelligence — K-12",
        "generated": datetime.now().isoformat(),
        "tiers": {}
    }

    for tier_id in ["k2", "35", "68", "912"]:
        filepath = f"data/tier_{tier_id}.json"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                master["tiers"][tier_id] = json.load(f)
        else:
            print(f"  WARNING: {filepath} not found, skipping from master")

    with open("data/master.json", "w", encoding="utf-8") as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    print(f"\n  MASTER FILE: data/master.json ({len(master['tiers'])} tiers)")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Bullying Research Gatherer")
    parser.add_argument("--tier", choices=list(TIERS.keys()), help="Run single tier only")
    parser.add_argument("--all", action="store_true", help="Run all tiers (default)")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set in environment")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    tiers_to_run = [args.tier] if args.tier else list(TIERS.keys())

    print(f"\nBullying Research Intelligence System")
    print(f"Running tiers: {', '.join(tiers_to_run)}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for tier_id in tiers_to_run:
        data = gather_tier_data(tier_id, client)
        save_tier_data(tier_id, data)

        # Pace API calls — don't hammer the endpoint
        if tier_id != tiers_to_run[-1]:
            print("  Waiting 3s before next tier...")
            time.sleep(3)

    # Always rebuild master if we ran everything
    if not args.tier:
        build_master_file()

    print(f"\nDone. {datetime.now().strftime('%H:%M:%S')}")
    print("Next step: python build_report.py")


if __name__ == "__main__":
    main()
