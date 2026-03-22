"""
Bullying Research Report Builder — build_report.py
====================================================
Reads JSON data from data/ folder and renders a single self-contained
HTML report with tabbed navigation by age tier, ETKM black/white/red
brand colors, and five sections per tier.

Usage:
    python build_report.py               # builds report from all tiers
    python build_report.py --tier k2     # builds report for single tier
    python build_report.py --output report.html  # custom output path

Output:
    output/bullying_research_report.html (self-contained, no external deps)
"""

import json
import os
import sys
import argparse
from datetime import datetime

# ──────────────────────────────────────────────
# TIER METADATA (mirrors gather_research.py)
# ──────────────────────────────────────────────

TIER_ORDER = ["k2", "35", "68", "912"]

TIER_META = {
    "k2":  {"label": "K–2", "full": "Kindergarten – 2nd Grade", "ages": "Ages 5–7",  "stage": "Early Childhood"},
    "35":  {"label": "3–5", "full": "3rd – 5th Grade",          "ages": "Ages 8–10", "stage": "Late Elementary"},
    "68":  {"label": "6–8", "full": "6th – 8th Grade",          "ages": "Ages 11–13","stage": "Middle School"},
    "912": {"label": "9–12","full": "9th – 12th Grade",         "ages": "Ages 14–18","stage": "High School"},
}

# ──────────────────────────────────────────────
# DATA LOADER
# ──────────────────────────────────────────────

def load_tier_data(tier_id: str) -> dict | None:
    filepath = f"data/tier_{tier_id}.json"
    if not os.path.exists(filepath):
        print(f"  WARNING: {filepath} not found")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_tiers(tier_ids: list[str]) -> dict:
    tiers = {}
    for tid in tier_ids:
        data = load_tier_data(tid)
        if data and "error" not in data:
            tiers[tid] = data
        elif data and "error" in data:
            print(f"  SKIPPING {tid}: data contains error — {data['error']}")
    return tiers


# ──────────────────────────────────────────────
# HTML HELPERS
# ──────────────────────────────────────────────

def esc(text) -> str:
    """Escape HTML entities."""
    if not isinstance(text, str):
        text = str(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def risk_badge(level: str) -> str:
    level = (level or "unknown").lower()
    colors = {
        "low": "#28a745",
        "medium": "#f0ad4e",
        "high": "#dc3545",
    }
    bg = colors.get(level, "#888")
    return f'<span class="risk-badge" style="background:{bg}">{esc(level.upper())}</span>'


def resource_type_badge(rtype: str) -> str:
    rtype = (rtype or "other").lower()
    colors = {
        "hotline": "#dc3545",
        "website": "#0066cc",
        "guide": "#28a745",
        "program": "#6f42c1",
        "app": "#fd7e14",
    }
    bg = colors.get(rtype, "#888")
    return f'<span class="type-badge" style="background:{bg}">{esc(rtype.upper())}</span>'


# ──────────────────────────────────────────────
# SECTION RENDERERS
# ──────────────────────────────────────────────

def render_categories(data: dict) -> str:
    categories = data.get("categories", [])
    if not categories:
        return '<p class="empty">No category data available.</p>'

    html = ""
    for cat in categories:
        behaviors = "".join(f"<li>{esc(b)}</li>" for b in cat.get("age_specific_behaviors", []))
        warnings = "".join(f"<li>{esc(w)}</li>" for w in cat.get("warning_signs", []))

        html += f"""
        <div class="card">
            <div class="card-header">
                <h3>{esc(cat.get('name', 'Unknown'))}</h3>
                {risk_badge(cat.get('escalation_risk', ''))}
            </div>
            <p class="card-desc">{esc(cat.get('description', ''))}</p>
            <p class="prevalence"><strong>Prevalence:</strong> {esc(cat.get('prevalence_note', 'N/A'))}</p>
            <div class="two-col">
                <div>
                    <h4>Age-Specific Behaviors</h4>
                    <ul>{behaviors if behaviors else '<li>No data</li>'}</ul>
                </div>
                <div>
                    <h4>Warning Signs</h4>
                    <ul class="warning-list">{warnings if warnings else '<li>No data</li>'}</ul>
                </div>
            </div>
        </div>"""
    return html


def render_commonalities(data: dict) -> str:
    c = data.get("commonalities", {})
    if not c:
        return '<p class="empty">No commonality data available.</p>'

    targeted = c.get("who_is_targeted", {})
    bullies = c.get("who_bullies", {})
    bystander = c.get("bystander_behavior", {})

    risk_factors = "".join(f"<li>{esc(r)}</li>" for r in targeted.get("risk_factors", []))
    protective = "".join(f"<li>{esc(p)}</li>" for p in targeted.get("protective_factors", []))
    traits = "".join(f"<li>{esc(t)}</li>" for t in bullies.get("common_traits", []))
    motivations = "".join(f"<li>{esc(m)}</li>" for m in bullies.get("motivations", []))
    environments = "".join(f"<li>{esc(e)}</li>" for e in c.get("environments", []))

    return f"""
    <div class="card">
        <h3>Who Is Targeted</h3>
        <p>{esc(targeted.get('summary', ''))}</p>
        <div class="two-col">
            <div>
                <h4>Risk Factors</h4>
                <ul class="risk-list">{risk_factors if risk_factors else '<li>No data</li>'}</ul>
            </div>
            <div>
                <h4>Protective Factors</h4>
                <ul class="protect-list">{protective if protective else '<li>No data</li>'}</ul>
            </div>
        </div>
    </div>
    <div class="card">
        <h3>Who Bullies</h3>
        <p>{esc(bullies.get('summary', ''))}</p>
        <div class="two-col">
            <div>
                <h4>Common Traits</h4>
                <ul>{traits if traits else '<li>No data</li>'}</ul>
            </div>
            <div>
                <h4>Motivations</h4>
                <ul>{motivations if motivations else '<li>No data</li>'}</ul>
            </div>
        </div>
    </div>
    <div class="card">
        <h3>Bystander Behavior</h3>
        <p>{esc(bystander.get('summary', ''))}</p>
        <p><strong>Typical Response:</strong> {esc(bystander.get('typical_response', 'N/A'))}</p>
        <p><strong>Intervention Rate:</strong> {esc(bystander.get('intervention_rate', 'N/A'))}</p>
    </div>
    <div class="card">
        <h3>Environments &amp; Context</h3>
        <ul>{environments if environments else '<li>No data</li>'}</ul>
        <p><strong>Gender Patterns:</strong> {esc(c.get('gender_patterns', 'N/A'))}</p>
        <p><strong>Developmental Context:</strong> {esc(c.get('developmental_context', 'N/A'))}</p>
    </div>"""


def render_statistics(data: dict) -> str:
    stats = data.get("statistics", {})
    if not stats:
        return '<p class="empty">No statistics available.</p>'

    def stat_table(items, columns):
        if not items:
            return '<p class="empty">No data in this category.</p>'
        header = "".join(f"<th>{esc(c)}</th>" for c in columns)
        rows = ""
        for item in items:
            unverified = ' class="unverified"' if item.get("unverified") else ""
            cells = []
            for col in columns:
                key = col.lower().replace(" ", "_")
                val = item.get(key, "")
                cells.append(f"<td>{esc(val)}</td>")
            rows += f"<tr{unverified}>{''.join(cells)}</tr>"
        return f"<table><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table>"

    national_html = stat_table(stats.get("national", []), ["Stat", "Value", "Source", "Year"])
    regional_html = stat_table(stats.get("regional", []), ["Region", "Stat", "Value", "Source", "Year"])
    outcomes_html = stat_table(stats.get("outcomes", []), ["Stat", "Value", "Source", "Year"])

    return f"""
    <div class="card">
        <h3>National Statistics</h3>
        {national_html}
    </div>
    <div class="card">
        <h3>Regional / Texas Data</h3>
        {regional_html}
    </div>
    <div class="card">
        <h3>Outcomes</h3>
        {outcomes_html}
    </div>"""


def render_parent_resources(data: dict) -> str:
    resources = data.get("parent_resources", [])
    if not resources:
        return '<p class="empty">No parent resources available.</p>'

    html = ""
    for r in resources:
        free_tag = '<span class="free-tag">FREE</span>' if r.get("free") else ""
        url = esc(r.get("url", "#"))
        html += f"""
        <div class="resource-card">
            <div class="resource-header">
                <h3>{esc(r.get('name', 'Unknown'))}</h3>
                <div class="resource-tags">
                    {resource_type_badge(r.get('type', ''))}
                    {free_tag}
                </div>
            </div>
            <p>{esc(r.get('description', ''))}</p>
            <p class="best-for"><strong>Best for:</strong> {esc(r.get('best_for', 'N/A'))}</p>
            <a href="{url}" target="_blank" rel="noopener noreferrer" class="resource-link">{url}</a>
        </div>"""
    return html


def render_intervention(data: dict) -> str:
    intervention = data.get("intervention_strategies", {})
    if not intervention:
        return '<p class="empty">No intervention data available.</p>'

    parent_steps = "".join(f"<li>{esc(s)}</li>" for s in intervention.get("for_parents", []))
    convos = "".join(f'<li class="convo">"{esc(c)}"</li>' for c in intervention.get("conversation_starters", []))
    red_flags = "".join(f"<li>{esc(r)}</li>" for r in intervention.get("red_flags_requiring_immediate_action", []))

    return f"""
    <div class="card">
        <h3>Parent Action Steps</h3>
        <ol class="action-list">{parent_steps if parent_steps else '<li>No data</li>'}</ol>
    </div>
    <div class="card">
        <h3>Conversation Starters</h3>
        <ul class="convo-list">{convos if convos else '<li>No data</li>'}</ul>
    </div>
    <div class="card red-flag-card">
        <h3>&#9888; Red Flags — Immediate Action Required</h3>
        <ul class="red-flag-list">{red_flags if red_flags else '<li>No data</li>'}</ul>
    </div>"""


# ──────────────────────────────────────────────
# FULL TIER RENDERER
# ──────────────────────────────────────────────

SECTION_DEFS = [
    ("categories",    "01 — Categories",          render_categories),
    ("commonalities", "02 — Commonalities",        render_commonalities),
    ("statistics",    "03 — Statistics",            render_statistics),
    ("resources",     "04 — Parent Resources",      render_parent_resources),
    ("intervention",  "05 — Intervention",          render_intervention),
]


def render_tier(tier_id: str, data: dict) -> str:
    meta = TIER_META[tier_id]

    section_tabs = ""
    section_panels = ""
    for i, (sec_id, sec_label, renderer) in enumerate(SECTION_DEFS):
        active = " active" if i == 0 else ""
        full_sec_id = f"{tier_id}-{sec_id}"
        section_tabs += f'<button class="sec-tab{active}" data-section="{full_sec_id}">{esc(sec_label)}</button>'
        section_panels += f'<div class="sec-panel{active}" id="{full_sec_id}">{renderer(data)}</div>'

    freshness = data.get("data_freshness_note", "")
    research_date = data.get("research_date", "")
    sources = data.get("sources_consulted", [])
    sources_html = ""
    if sources:
        source_items = "".join(
            f'<li><a href="{esc(s.get("url", "#"))}" target="_blank">{esc(s.get("name", ""))}</a> '
            f'<span class="source-type">({esc(s.get("type", ""))})</span></li>'
            for s in sources
        )
        sources_html = f'<div class="sources"><h4>Sources Consulted</h4><ul>{source_items}</ul></div>'

    return f"""
    <div class="tier-content" id="tier-{tier_id}">
        <div class="tier-header">
            <h2>{esc(meta['full'])}</h2>
            <div class="tier-badges">
                <span class="badge">{esc(meta['ages'])}</span>
                <span class="badge">{esc(meta['stage'])}</span>
                {f'<span class="badge date-badge">Researched: {esc(research_date)}</span>' if research_date else ''}
            </div>
            {f'<p class="freshness">{esc(freshness)}</p>' if freshness else ''}
        </div>
        <div class="sec-tabs">{section_tabs}</div>
        <div class="sec-panels">{section_panels}</div>
        {sources_html}
    </div>"""


# ──────────────────────────────────────────────
# FULL HTML TEMPLATE
# ──────────────────────────────────────────────

def build_html(tiers: dict) -> str:
    tier_ids = [t for t in TIER_ORDER if t in tiers]

    # Tier navigation tabs
    tier_tabs = ""
    for i, tid in enumerate(tier_ids):
        meta = TIER_META[tid]
        active = " active" if i == 0 else ""
        tier_tabs += f'<button class="tier-tab{active}" data-tier="{tid}">{esc(meta["label"])}<br><small>{esc(meta["ages"])}</small></button>'

    # Tier content panels
    tier_panels = ""
    for i, tid in enumerate(tier_ids):
        active = " active" if i == 0 else ""
        tier_panels += f'<div class="tier-panel{active}" data-tier-panel="{tid}">{render_tier(tid, tiers[tid])}</div>'

    generated = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bullying Research Intelligence — East Texas Krav Maga</title>
<style>
/* ── RESET & BASE ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: #111;
    color: #e0e0e0;
    line-height: 1.6;
    min-height: 100vh;
}}
a {{ color: #ff4444; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

/* ── HEADER ── */
.header {{
    background: #000;
    border-bottom: 3px solid #dc3545;
    padding: 24px 32px;
    text-align: center;
}}
.header h1 {{
    color: #fff;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.header .subtitle {{
    color: #dc3545;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}}
.header .generated {{
    color: #666;
    font-size: 12px;
    margin-top: 8px;
}}

/* ── TIER TABS ── */
.tier-nav {{
    display: flex;
    background: #1a1a1a;
    border-bottom: 1px solid #333;
    padding: 0;
    overflow-x: auto;
}}
.tier-tab {{
    flex: 1;
    min-width: 120px;
    padding: 16px 12px;
    background: transparent;
    border: none;
    color: #888;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;
    text-align: center;
}}
.tier-tab small {{
    font-weight: 400;
    font-size: 11px;
    color: #666;
    display: block;
    margin-top: 2px;
}}
.tier-tab:hover {{
    color: #ccc;
    background: #222;
}}
.tier-tab.active {{
    color: #fff;
    border-bottom-color: #dc3545;
    background: #222;
}}
.tier-tab.active small {{ color: #aaa; }}

/* ── TIER PANELS ── */
.tier-panel {{ display: none; }}
.tier-panel.active {{ display: block; }}

/* ── TIER HEADER ── */
.tier-content {{ max-width: 1100px; margin: 0 auto; padding: 24px 20px; }}
.tier-header {{ margin-bottom: 24px; }}
.tier-header h2 {{
    color: #fff;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 8px;
}}
.tier-badges {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }}
.badge {{
    background: #2a2a2a;
    color: #ccc;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid #444;
}}
.date-badge {{ color: #888; }}
.freshness {{ color: #888; font-size: 13px; font-style: italic; }}

/* ── SECTION TABS ── */
.sec-tabs {{
    display: flex;
    gap: 2px;
    background: #1a1a1a;
    border-radius: 8px 8px 0 0;
    overflow-x: auto;
    padding: 4px 4px 0;
}}
.sec-tab {{
    padding: 10px 16px;
    background: #222;
    border: none;
    color: #888;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    border-radius: 6px 6px 0 0;
    transition: all 0.2s;
    white-space: nowrap;
}}
.sec-tab:hover {{ color: #ccc; background: #2a2a2a; }}
.sec-tab.active {{
    color: #fff;
    background: #1e1e1e;
    border-top: 2px solid #dc3545;
}}

/* ── SECTION PANELS ── */
.sec-panels {{
    background: #1e1e1e;
    border-radius: 0 0 8px 8px;
    padding: 24px;
    min-height: 300px;
}}
.sec-panel {{ display: none; }}
.sec-panel.active {{ display: block; }}

/* ── CARDS ── */
.card {{
    background: #252525;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}}
.card h3 {{
    color: #fff;
    font-size: 18px;
    margin-bottom: 10px;
}}
.card h4 {{
    color: #dc3545;
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    margin-top: 12px;
}}
.card p {{ color: #bbb; margin-bottom: 8px; }}
.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}}
.card-header h3 {{ margin-bottom: 0; }}
.card-desc {{ color: #aaa; font-size: 14px; }}
.prevalence {{ color: #999; font-size: 13px; }}

/* ── LISTS ── */
ul, ol {{ padding-left: 20px; color: #bbb; }}
li {{ margin-bottom: 6px; font-size: 14px; }}
.warning-list li {{ color: #f0ad4e; }}
.risk-list li {{ color: #e88; }}
.protect-list li {{ color: #6c6; }}
.red-flag-list li {{ color: #ff4444; font-weight: 600; }}
.convo-list li {{ font-style: italic; color: #8cb4ff; }}
.action-list li {{ color: #ccc; }}

/* ── TWO COLUMN ── */
.two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 8px;
}}
@media (max-width: 700px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

/* ── BADGES ── */
.risk-badge {{
    color: #fff;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
.type-badge {{
    color: #fff;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
.free-tag {{
    background: #28a745;
    color: #fff;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 700;
}}

/* ── TABLES ── */
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    font-size: 13px;
}}
th {{
    background: #333;
    color: #fff;
    padding: 10px 12px;
    text-align: left;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
td {{
    padding: 10px 12px;
    border-bottom: 1px solid #333;
    color: #bbb;
}}
tr:hover td {{ background: #2a2a2a; }}
tr.unverified td {{ opacity: 0.6; font-style: italic; }}

/* ── RESOURCES ── */
.resource-card {{
    background: #252525;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}}
.resource-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}}
.resource-header h3 {{ font-size: 16px; margin: 0; }}
.resource-tags {{ display: flex; gap: 6px; align-items: center; }}
.best-for {{ font-size: 13px; color: #999; }}
.resource-link {{
    display: inline-block;
    margin-top: 6px;
    font-size: 13px;
    color: #dc3545;
    word-break: break-all;
}}

/* ── RED FLAG CARD ── */
.red-flag-card {{
    border-color: #dc3545;
    border-width: 2px;
    background: #2a1a1a;
}}
.red-flag-card h3 {{ color: #ff4444; }}

/* ── SOURCES ── */
.sources {{
    margin-top: 32px;
    padding: 16px 20px;
    background: #1a1a1a;
    border-radius: 8px;
    border: 1px solid #2a2a2a;
}}
.sources h4 {{
    color: #888;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}}
.sources ul {{ list-style: none; padding: 0; }}
.sources li {{
    font-size: 13px;
    color: #666;
    margin-bottom: 4px;
}}
.sources a {{ color: #888; }}
.sources a:hover {{ color: #dc3545; }}
.source-type {{ font-size: 11px; color: #555; }}

/* ── EMPTY STATE ── */
.empty {{
    color: #666;
    font-style: italic;
    text-align: center;
    padding: 40px 20px;
}}

/* ── FOOTER ── */
.footer {{
    text-align: center;
    padding: 24px;
    color: #444;
    font-size: 12px;
    border-top: 1px solid #222;
    margin-top: 40px;
}}
</style>
</head>
<body>

<div class="header">
    <h1>Bullying Research Intelligence</h1>
    <div class="subtitle">East Texas Krav Maga — Parent &amp; Educator Resource</div>
    <div class="generated">Generated {esc(generated)}</div>
</div>

<div class="tier-nav">
    {tier_tabs}
</div>

{tier_panels}

<div class="footer">
    East Texas Krav Maga &bull; Bullying Research Intelligence System &bull; Data gathered via Anthropic API with live web search
</div>

<script>
// ── Tier tab switching ──
document.querySelectorAll('.tier-tab').forEach(tab => {{
    tab.addEventListener('click', () => {{
        document.querySelectorAll('.tier-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tier-panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        const panel = document.querySelector(`[data-tier-panel="${{tab.dataset.tier}}"]`);
        if (panel) panel.classList.add('active');
    }});
}});

// ── Section tab switching (scoped per tier) ──
document.querySelectorAll('.sec-tab').forEach(tab => {{
    tab.addEventListener('click', () => {{
        const parent = tab.closest('.tier-content');
        parent.querySelectorAll('.sec-tab').forEach(t => t.classList.remove('active'));
        parent.querySelectorAll('.sec-panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        const panel = document.getElementById(tab.dataset.section);
        if (panel) panel.classList.add('active');
    }});
}});
</script>
</body>
</html>"""


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Bullying Research Report Builder")
    parser.add_argument("--tier", choices=TIER_ORDER, help="Build report for single tier only")
    parser.add_argument("--output", default="output/bullying_research_report.html", help="Output file path")
    args = parser.parse_args()

    tier_ids = [args.tier] if args.tier else TIER_ORDER

    print(f"\nBullying Research Report Builder")
    print(f"Loading tiers: {', '.join(tier_ids)}")

    tiers = load_all_tiers(tier_ids)

    if not tiers:
        print("\nERROR: No valid tier data found. Run gather_research.py first.")
        sys.exit(1)

    print(f"Building report with {len(tiers)} tier(s)...")
    html = build_html(tiers)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(args.output) / 1024
    print(f"\nSUCCESS: {args.output} ({size_kb:.1f} KB)")
    print(f"Tiers included: {', '.join(tiers.keys())}")
    print(f"Open in browser to view.")


if __name__ == "__main__":
    main()
