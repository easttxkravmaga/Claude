"""
Bullying Research Intelligence System — build_report.py
=========================================================
Reads data/master.json and renders a full HTML research report.
One page, all four tiers, tabbed navigation.
ETKM brand standards: black background, white text, red accents.
Usage:
    python build_report.py
    python build_report.py --tier k2       # single tier preview
Output:
    output/bullying_research_report.html
    output/tier_k2.html  (if --tier specified)
"""
import json
import os
import sys
import argparse
from datetime import datetime


# ──────────────────────────────────────────────
# DATA LOADER
# ──────────────────────────────────────────────

def load_master() -> dict:
    if not os.path.exists("data/master.json"):
        print("ERROR: data/master.json not found. Run gather_research.py first.")
        sys.exit(1)
    with open("data/master.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_tier(tier_id: str) -> dict:
    filepath = f"data/tier_{tier_id}.json"
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found. Run gather_research.py --tier {tier_id} first.")
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ──────────────────────────────────────────────
# HTML HELPERS
# ──────────────────────────────────────────────

def safe(val, fallback="—"):
    """Return val or fallback if empty/None."""
    if val is None:
        return fallback
    s = str(val).strip()
    return s if s else fallback


def stat_badge(source, year):
    """Small source badge."""
    parts = []
    if source:
        parts.append(f'<span class="badge-source">{source}</span>')
    if year:
        parts.append(f'<span class="badge-year">{year}</span>')
    return " ".join(parts) if parts else ""


def escalation_class(level):
    mapping = {"high": "esc-high", "medium": "esc-medium", "low": "esc-low"}
    return mapping.get(str(level).lower(), "esc-low")


def resource_type_icon(rtype):
    icons = {
        "hotline": "📞",
        "website": "🌐",
        "guide": "📄",
        "program": "🎯",
        "app": "📱"
    }
    return icons.get(str(rtype).lower(), "🔗")


# ──────────────────────────────────────────────
# SECTION RENDERERS
# ──────────────────────────────────────────────

def render_categories(categories):
    if not categories:
        return "<p class='empty'>No category data found.</p>"

    html = '<div class="categories-grid">'
    for cat in categories:
        esc = escalation_class(cat.get("escalation_risk", "low"))
        behaviors = "".join(f"<li>{b}</li>" for b in cat.get("age_specific_behaviors", []))
        signs = "".join(f"<li>{s}</li>" for s in cat.get("warning_signs", []))

        html += f"""
        <div class="category-card">
          <div class="cat-header">
            <span class="cat-name">{safe(cat.get('name'))}</span>
            <span class="escalation-badge {esc}">{safe(cat.get('escalation_risk','—')).upper()} RISK</span>
          </div>
          <p class="cat-desc">{safe(cat.get('description'))}</p>
          <p class="cat-prevalence"><em>{safe(cat.get('prevalence_note'))}</em></p>
          {f'<div class="sub-section"><span class="sub-label">Age-Specific Behaviors</span><ul>{behaviors}</ul></div>' if behaviors else ''}
          {f'<div class="sub-section"><span class="sub-label">Warning Signs</span><ul>{signs}</ul></div>' if signs else ''}
        </div>"""
    html += "</div>"
    return html


def render_commonalities(comm):
    if not comm:
        return "<p class='empty'>No commonality data found.</p>"

    targeted = comm.get("who_is_targeted", {})
    bullies = comm.get("who_bullies", {})
    bystander = comm.get("bystander_behavior", {})

    risk_factors = "".join(f"<li>{r}</li>" for r in targeted.get("risk_factors", []))
    protective = "".join(f"<li>{p}</li>" for p in targeted.get("protective_factors", []))
    traits = "".join(f"<li>{t}</li>" for t in bullies.get("common_traits", []))
    motivations = "".join(f"<li>{m}</li>" for m in bullies.get("motivations", []))
    environments = "".join(f"<li>{e}</li>" for e in comm.get("environments", []))

    return f"""
    <div class="commonalities-grid">
      <div class="comm-block">
        <h4 class="comm-title red-line">Who Gets Targeted</h4>
        <p>{safe(targeted.get('summary'))}</p>
        {f'<span class="sub-label">Risk Factors</span><ul>{risk_factors}</ul>' if risk_factors else ''}
        {f'<span class="sub-label">Protective Factors</span><ul>{protective}</ul>' if protective else ''}
      </div>
      <div class="comm-block">
        <h4 class="comm-title red-line">Who Bullies</h4>
        <p>{safe(bullies.get('summary'))}</p>
        {f'<span class="sub-label">Common Traits</span><ul>{traits}</ul>' if traits else ''}
        {f'<span class="sub-label">Motivations</span><ul>{motivations}</ul>' if motivations else ''}
      </div>
      <div class="comm-block">
        <h4 class="comm-title red-line">Bystander Behavior</h4>
        <p>{safe(bystander.get('summary'))}</p>
        <p><strong>Typical Response:</strong> {safe(bystander.get('typical_response'))}</p>
        <p><strong>Intervention Rate:</strong> {safe(bystander.get('intervention_rate'))}</p>
      </div>
      <div class="comm-block">
        <h4 class="comm-title red-line">Environment &amp; Context</h4>
        {f'<span class="sub-label">Where It Happens</span><ul>{environments}</ul>' if environments else ''}
        <p><strong>Gender Patterns:</strong> {safe(comm.get('gender_patterns'))}</p>
        <p><strong>Developmental Context:</strong> {safe(comm.get('developmental_context'))}</p>
      </div>
    </div>"""


def render_statistics(stats):
    if not stats:
        return "<p class='empty'>No statistics data found.</p>"

    national = stats.get("national", [])
    regional = stats.get("regional", [])
    outcomes = stats.get("outcomes", [])

    def render_stat_list(items):
        if not items:
            return "<p class='empty'>No data available.</p>"
        rows = ""
        for s in items:
            unverified = s.get("unverified", False)
            flag = ' <span class="unverified-flag">⚠ UNVERIFIED</span>' if unverified else ''
            rows += f"""
            <div class="stat-row">
              <div class="stat-value">{safe(s.get('value'))}</div>
              <div class="stat-text">
                <span class="stat-label">{safe(s.get('stat'))}</span>{flag}
                <div class="stat-meta">{stat_badge(s.get('source'), s.get('year'))}</div>
              </div>
            </div>"""
        return rows

    regional_note = ""
    if regional:
        reg_rows = ""
        for r in regional:
            reg_rows += f"""
            <div class="stat-row regional">
              <div class="stat-value">{safe(r.get('value'))}</div>
              <div class="stat-text">
                <span class="region-tag">{safe(r.get('region'))}</span>
                <span class="stat-label">{safe(r.get('stat'))}</span>
                <div class="stat-meta">{stat_badge(r.get('source'), r.get('year'))}</div>
              </div>
            </div>"""
        regional_note = f"""
        <div class="stats-section">
          <h4 class="stats-subhead">Regional / Texas Data</h4>
          {reg_rows}
        </div>"""

    return f"""
    <div class="stats-layout">
      <div class="stats-section">
        <h4 class="stats-subhead">National Prevalence</h4>
        {render_stat_list(national)}
      </div>
      {regional_note}
      <div class="stats-section">
        <h4 class="stats-subhead">Outcomes &amp; Impact</h4>
        {render_stat_list(outcomes)}
      </div>
    </div>"""


def render_resources(resources):
    if not resources:
        return "<p class='empty'>No resources found.</p>"

    html = '<div class="resources-grid">'
    for r in resources:
        icon = resource_type_icon(r.get("type", ""))
        url = r.get("url", "#")
        free_badge = '<span class="free-badge">FREE</span>' if r.get("free") else ''

        html += f"""
        <div class="resource-card">
          <div class="resource-header">
            <span class="resource-icon">{icon}</span>
            <div>
              <a href="{url}" target="_blank" class="resource-name">{safe(r.get('name'))}</a>
              {free_badge}
            </div>
          </div>
          <p class="resource-desc">{safe(r.get('description'))}</p>
          <p class="resource-best"><strong>Best for:</strong> {safe(r.get('best_for'))}</p>
          <a href="{url}" target="_blank" class="resource-url">{url}</a>
        </div>"""

    html += "</div>"
    return html


def render_intervention(intervention):
    if not intervention:
        return "<p class='empty'>No intervention data found.</p>"

    for_parents = "".join(f"<li>{a}</li>" for a in intervention.get("for_parents", []))
    starters = "".join(f'<li class="starter">&ldquo;{s}&rdquo;</li>' for s in intervention.get("conversation_starters", []))
    red_flags = "".join(f"<li class='red-flag-item'>{f}</li>" for f in intervention.get("red_flags_requiring_immediate_action", []))

    return f"""
    <div class="intervention-grid">
      <div class="int-block">
        <h4 class="int-title">Parent Actions</h4>
        <ul class="action-list">{for_parents}</ul>
      </div>
      <div class="int-block">
        <h4 class="int-title">Conversation Starters</h4>
        <ul class="starters-list">{starters}</ul>
      </div>
      <div class="int-block red-block">
        <h4 class="int-title">&#x1F6A8; Red Flags — Act Immediately</h4>
        <ul class="red-flags-list">{red_flags}</ul>
      </div>
    </div>"""


def render_tier_section(tier_id, tier_data, active=False):
    """Renders full HTML section for one tier."""

    active_class = "active" if active else ""
    stage = safe(tier_data.get("stage", ""))
    age_range = safe(tier_data.get("age_range", ""))
    freshness = safe(tier_data.get("data_freshness_note", ""))

    return f"""
    <div class="tier-panel {active_class}" id="panel-{tier_id}" role="tabpanel">
      <div class="tier-hero">
        <div class="tier-label">
          <span class="tier-grades">{safe(tier_data.get('grades', tier_id.upper()))}</span>
          <span class="tier-stage">{stage}</span>
        </div>
        <div class="tier-meta">
          <span class="tier-age">{age_range}</span>
          {f'<span class="freshness-note">{freshness}</span>' if freshness != "—" else ''}
        </div>
      </div>

      <div class="section-block" id="{tier_id}-categories">
        <h3 class="section-heading">
          <span class="section-num">01</span>
          Categories of Bullying
        </h3>
        {render_categories(tier_data.get("categories", []))}
      </div>

      <div class="section-block" id="{tier_id}-commonalities">
        <h3 class="section-heading">
          <span class="section-num">02</span>
          Commonalities &amp; Patterns
        </h3>
        {render_commonalities(tier_data.get("commonalities", {}))}
      </div>

      <div class="section-block" id="{tier_id}-stats">
        <h3 class="section-heading">
          <span class="section-num">03</span>
          Statistics
        </h3>
        {render_statistics(tier_data.get("statistics", {}))}
      </div>

      <div class="section-block" id="{tier_id}-resources">
        <h3 class="section-heading">
          <span class="section-num">04</span>
          Parent Resources
        </h3>
        {render_resources(tier_data.get("parent_resources", []))}
      </div>

      <div class="section-block" id="{tier_id}-intervention">
        <h3 class="section-heading">
          <span class="section-num">05</span>
          Intervention Strategies
        </h3>
        {render_intervention(tier_data.get("intervention_strategies", {}))}
      </div>
    </div>"""


# ──────────────────────────────────────────────
# FULL PAGE RENDERER
# ──────────────────────────────────────────────

TIER_META = {
    "k2":  {"label": "K–2",  "sublabel": "Ages 5–7"},
    "35":  {"label": "3–5",  "sublabel": "Ages 8–10"},
    "68":  {"label": "6–8",  "sublabel": "Ages 11–13"},
    "912": {"label": "9–12", "sublabel": "Ages 14–18"},
}


def build_full_report(master: dict) -> str:
    tiers = master.get("tiers", {})
    generated = master.get("generated", datetime.now().isoformat())

    # Build tab bar
    tab_html = ""
    for i, (tid, meta) in enumerate(TIER_META.items()):
        active = " active" if i == 0 else ""
        tab_html += f"""
        <button class="tab-btn{active}" data-tier="{tid}" role="tab" aria-selected="{'true' if i==0 else 'false'}">
          <span class="tab-grade">{meta['label']}</span>
          <span class="tab-age">{meta['sublabel']}</span>
        </button>"""

    # Build panels
    panels_html = ""
    for i, tid in enumerate(["k2", "35", "68", "912"]):
        tier_data = tiers.get(tid, {})
        if not tier_data:
            panels_html += f'<div class="tier-panel{" active" if i==0 else ""}" id="panel-{tid}"><p class="empty">No data for this tier. Run gather_research.py --tier {tid}</p></div>'
        else:
            panels_html += render_tier_section(tid, tier_data, active=(i == 0))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bullying Research Intelligence — K-12</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* ── RESET & BASE ─────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --black: #000000;
  --surface: #111111;
  --surface2: #1a1a1a;
  --surface3: #222222;
  --white: #FFFFFF;
  --gray: #575757;
  --gray-light: #BBBBBB;
  --red: #CC0000;
  --red-bright: #FF0000;
  --font-display: 'Barlow Condensed', sans-serif;
  --font-body: 'Inter', sans-serif;
}}
body {{
  background: var(--black);
  color: var(--white);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.6;
  min-height: 100vh;
}}
a {{ color: var(--red-bright); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
ul {{ padding-left: 1.2rem; }}
li {{ margin-bottom: 0.35rem; }}

/* ── HEADER ───────────────────────────────── */
.site-header {{
  background: var(--black);
  border-bottom: 3px solid var(--red);
  padding: 2rem 2.5rem 1.5rem;
}}
.header-eyebrow {{
  font-family: var(--font-display);
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  color: var(--red);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}}
.header-title {{
  font-family: var(--font-display);
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  margin-bottom: 0.5rem;
}}
.header-subtitle {{
  color: var(--gray-light);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}}
.header-meta {{
  font-size: 0.75rem;
  color: var(--gray);
}}

/* ── TAB BAR ──────────────────────────────── */
.tab-bar {{
  display: flex;
  background: var(--surface);
  border-bottom: 2px solid var(--surface3);
  padding: 0 1rem;
  gap: 0.25rem;
  overflow-x: auto;
  scrollbar-width: none;
}}
.tab-bar::-webkit-scrollbar {{ display: none; }}
.tab-btn {{
  background: none;
  border: none;
  color: var(--gray-light);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
  white-space: nowrap;
  min-width: 80px;
}}
.tab-btn:hover {{
  color: var(--white);
  border-bottom-color: var(--gray);
}}
.tab-btn.active {{
  color: var(--white);
  border-bottom-color: var(--red);
}}
.tab-grade {{
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 800;
  line-height: 1;
}}
.tab-age {{
  font-size: 0.7rem;
  color: var(--gray);
  margin-top: 0.2rem;
}}
.tab-btn.active .tab-age {{ color: var(--gray-light); }}

/* ── CONTENT AREA ─────────────────────────── */
.content-area {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 2.5rem 4rem;
}}
.tier-panel {{
  display: none;
}}
.tier-panel.active {{
  display: block;
}}

/* ── TIER HERO ────────────────────────────── */
.tier-hero {{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-bottom: 1.5rem;
  margin-bottom: 2.5rem;
  border-bottom: 1px solid var(--surface3);
}}
.tier-grades {{
  font-family: var(--font-display);
  font-size: 3rem;
  font-weight: 800;
  display: block;
  line-height: 1;
  color: var(--white);
}}
.tier-stage {{
  font-family: var(--font-display);
  font-size: 1rem;
  color: var(--red);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  display: block;
  margin-top: 0.25rem;
}}
.tier-age {{
  font-size: 0.9rem;
  color: var(--gray-light);
  display: block;
  text-align: right;
}}
.freshness-note {{
  font-size: 0.75rem;
  color: var(--gray);
  display: block;
  text-align: right;
  margin-top: 0.25rem;
  font-style: italic;
}}

/* ── SECTION BLOCKS ───────────────────────── */
.section-block {{
  margin-bottom: 3.5rem;
}}
.section-heading {{
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--surface3);
}}
.section-num {{
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--red);
  border: 1px solid var(--red);
  padding: 0.1rem 0.4rem;
  letter-spacing: 0.1em;
}}

/* ── CATEGORIES ───────────────────────────── */
.categories-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
}}
.category-card {{
  background: var(--surface);
  border: 1px solid var(--surface3);
  border-left: 3px solid var(--red);
  padding: 1.25rem;
}}
.cat-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}}
.cat-name {{
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}
.escalation-badge {{
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.esc-high {{ background: var(--red); color: var(--white); }}
.esc-medium {{ background: #994400; color: var(--white); }}
.esc-low {{ background: var(--surface3); color: var(--gray-light); }}
.cat-desc {{ font-size: 0.9rem; margin-bottom: 0.5rem; }}
.cat-prevalence {{ font-size: 0.82rem; color: var(--gray-light); margin-bottom: 0.75rem; }}
.sub-section {{ margin-top: 0.75rem; }}
.sub-label {{
  font-family: var(--font-display);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--red);
  display: block;
  margin-bottom: 0.35rem;
}}
.sub-section ul {{ font-size: 0.85rem; }}

/* ── COMMONALITIES ────────────────────────── */
.commonalities-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}}
.comm-block {{
  background: var(--surface);
  border: 1px solid var(--surface3);
  padding: 1.25rem;
}}
.comm-title {{
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--red);
}}
.comm-block p {{ font-size: 0.88rem; margin-bottom: 0.5rem; }}
.comm-block ul {{ font-size: 0.85rem; margin-top: 0.25rem; }}

/* ── STATISTICS ───────────────────────────── */
.stats-layout {{ display: flex; flex-direction: column; gap: 2rem; }}
.stats-subhead {{
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gray-light);
  margin-bottom: 1rem;
  padding-left: 0.75rem;
  border-left: 2px solid var(--red);
}}
.stat-row {{
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
  padding: 0.85rem 1rem;
  background: var(--surface);
  border: 1px solid var(--surface3);
  margin-bottom: 0.5rem;
}}
.stat-row.regional {{ border-left: 3px solid #994400; }}
.stat-value {{
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--red-bright);
  min-width: 80px;
  line-height: 1.1;
  flex-shrink: 0;
}}
.stat-label {{ font-size: 0.9rem; display: block; margin-bottom: 0.35rem; }}
.stat-meta {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.25rem; }}
.badge-source, .badge-year {{
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  background: var(--surface3);
  color: var(--gray-light);
}}
.region-tag {{
  font-size: 0.7rem;
  font-weight: 600;
  background: #994400;
  color: var(--white);
  padding: 0.15rem 0.4rem;
  display: inline-block;
  margin-bottom: 0.3rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}
.unverified-flag {{
  font-size: 0.7rem;
  background: #555500;
  color: #ffff00;
  padding: 0.1rem 0.35rem;
  margin-left: 0.5rem;
}}

/* ── RESOURCES ────────────────────────────── */
.resources-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}}
.resource-card {{
  background: var(--surface);
  border: 1px solid var(--surface3);
  padding: 1.25rem;
}}
.resource-header {{
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}}
.resource-icon {{ font-size: 1.4rem; flex-shrink: 0; }}
.resource-name {{
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 700;
  display: block;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--white);
}}
.resource-name:hover {{ color: var(--red-bright); }}
.free-badge {{
  font-size: 0.65rem;
  font-weight: 700;
  background: var(--red);
  color: var(--white);
  padding: 0.1rem 0.4rem;
  letter-spacing: 0.1em;
  display: inline-block;
  margin-top: 0.2rem;
}}
.resource-desc {{ font-size: 0.87rem; margin-bottom: 0.5rem; color: var(--gray-light); }}
.resource-best {{ font-size: 0.83rem; margin-bottom: 0.5rem; }}
.resource-url {{
  font-size: 0.75rem;
  color: var(--red);
  word-break: break-all;
  display: block;
  margin-top: 0.5rem;
}}

/* ── INTERVENTION ─────────────────────────── */
.intervention-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}}
.int-block {{
  background: var(--surface);
  border: 1px solid var(--surface3);
  padding: 1.25rem;
}}
.int-block.red-block {{ border-left: 3px solid var(--red-bright); }}
.int-title {{
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  color: var(--white);
}}
.action-list li, .starters-list li, .red-flags-list li {{
  font-size: 0.87rem;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}}
.starters-list li {{
  list-style: none;
  margin-left: -1.2rem;
  padding: 0.5rem 0.75rem;
  background: var(--surface2);
  border-left: 2px solid var(--gray);
  font-style: italic;
  color: var(--gray-light);
}}
.red-flag-item {{
  color: #ff8888;
  font-weight: 500;
}}

/* ── EMPTY STATE ──────────────────────────── */
.empty {{
  color: var(--gray);
  font-style: italic;
  font-size: 0.88rem;
  padding: 1rem;
  border: 1px dashed var(--surface3);
}}

/* ── FOOTER ───────────────────────────────── */
.site-footer {{
  border-top: 1px solid var(--surface3);
  padding: 1.5rem 2.5rem;
  color: var(--gray);
  font-size: 0.75rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}}

/* ── RESPONSIVE ───────────────────────────── */
@media (max-width: 700px) {{
  .content-area {{ padding: 1.5rem 1rem 3rem; }}
  .site-header {{ padding: 1.5rem 1rem 1rem; }}
  .tier-hero {{ flex-direction: column; align-items: flex-start; gap: 0.5rem; }}
  .tier-age, .freshness-note {{ text-align: left; }}
  .categories-grid, .commonalities-grid, .resources-grid, .intervention-grid {{
    grid-template-columns: 1fr;
  }}
  .stat-value {{ font-size: 1.2rem; min-width: 60px; }}
  .tab-btn {{ padding: 0.75rem 1rem; }}
}}
</style>
</head>
<body>

<header class="site-header">
  <p class="header-eyebrow">Research Intelligence</p>
  <h1 class="header-title">Bullying in America<br>K–12 Research Brief</h1>
  <p class="header-subtitle">Categories &middot; Patterns &middot; Statistics &middot; Regional Data &middot; Parent Resources</p>
  <p class="header-meta">Generated: {generated[:10]} — Data gathered via live web research</p>
</header>

<nav class="tab-bar" role="tablist" aria-label="Grade tiers">
  {tab_html}
</nav>

<main class="content-area">
  {panels_html}
</main>

<footer class="site-footer">
  <span>Bullying Research Intelligence System</span>
  <span>Data gathered via Anthropic API + web search — verify all statistics at primary sources</span>
</footer>

<script>
// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const tier = btn.dataset.tier;

    document.querySelectorAll('.tab-btn').forEach(b => {{
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    }});
    document.querySelectorAll('.tier-panel').forEach(p => p.classList.remove('active'));

    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    document.getElementById('panel-' + tier).classList.add('active');

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
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
    parser.add_argument("--tier", choices=["k2", "35", "68", "912"], help="Build single tier preview")
    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)

    if args.tier:
        tier_data = load_tier(args.tier)
        master = {
            "generated": datetime.now().isoformat(),
            "tiers": {args.tier: tier_data}
        }
        html = build_full_report(master)
        outpath = f"output/tier_{args.tier}.html"
    else:
        master = load_master()
        html = build_full_report(master)
        outpath = "output/bullying_research_report.html"

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report built: {outpath}")
    print(f"Open in browser: file://{os.path.abspath(outpath)}")


if __name__ == "__main__":
    main()
