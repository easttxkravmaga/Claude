# P2 Event Production — Project Instructions

**Project:** P2 Event Production
**Last Updated:** March 2026
**Skill Stack:** etkm-event-page · etkm-event-planning · etkm-brand-kit · etkm-brand-foundation · etkm-peace-framework · etkm-deliverable-qc

---

## What This Project Does

P2 Event Production builds everything needed to market and run ETKM events —
seminars, workshops, specialty training, and guest instructor events. It produces:

- Event landing pages (HTML — deploys to WordPress)
- Email campaigns (Pipedrive-ready HTML)
- Social media calendars (22+ FB/IG + LinkedIn)
- Canva image briefs
- Day-of run sheets
- Post-event follow-up packages

---

## Primary Skill: etkm-event-page

**Always load etkm-event-page first** for any task involving building or updating an event landing page.

This skill encodes the full CBLTAC page design system — the complete layout, CSS architecture, section component library, copy doctrine, audience variant system, image handling, WordPress deployment rules, and QC gates. Three production pages were built from this system in March 2026 (CBLTAC General, Professionals, First Responders).

**Trigger phrases for etkm-event-page:**
- "build an event page"
- "make a landing page for [event]"
- "same layout as the CBLTAC page"
- "use the event page format"
- "clone this page for [audience]"
- Any event registration page request

**Reference files inside the skill:**
- `references/components.md` — Full CSS + HTML for every section component
- `references/variants.md` — Copy patterns for General / Professional / First Responder audiences
- `references/copy-doctrine.md` — Headlines, CTAs, voice rules, prohibited words

---

## Event Page Build Checklist

Before delivering any event page HTML file:

**Inputs gathered:**
- [ ] Event name, type, audience variant
- [ ] Course 1: title, date, time, price, Stripe URL
- [ ] Course 2: title, date, time, price, Stripe URL
- [ ] Both Sessions: price, Stripe URL
- [ ] Venue name and address
- [ ] Instructor photo (URL or upload)
- [ ] Classroom/proof photo (URL or upload — optional)
- [ ] Any discount (amount, who qualifies)
- [ ] Any video testimonial (WordPress upload URL — optional)

**QC before delivery (non-negotiable):**
- [ ] No `href="#"` placeholders — all buttons have real Stripe URLs
- [ ] No external image src — all images embedded as base64
- [ ] WP override block present in CSS
- [ ] All CSS scoped to unique wrapper ID
- [ ] Both hero CTA and final main button link to best-value option
- [ ] Red used max once per visible section
- [ ] Responsive breakpoint at 860px present
- [ ] `target="_blank"` on all external links

---

## WordPress Deployment Notes

All event pages deploy as Raw HTML blocks in Visual Composer.

**Critical architecture rules:**
1. Every page uses a unique wrapper div ID (e.g., `id="etkm-women-seminar"`)
2. WP container override block forces full-width layout (always include)
3. All CSS scoped to wrapper ID — never bare class names
4. All images embedded as base64 — no external file dependencies
5. Fonts load via Google Fonts link in the HTML block

See `etkm-event-page` SKILL.md for the full WordPress architecture section.

---

## Production Pages (Live Reference)

| Page | URL | Audience | Wrapper ID |
|------|-----|----------|------------|
| CBLTAC General | etxkravmaga.com/cbltac-courses/ | All audiences | cbltac-main |
| CBLTAC Professionals | etxkravmaga.com/cbltac-professionals/ | Business professionals | cbltac-pro |
| CBLTAC First Responders | etxkravmaga.com/events/cbltac-first-responders/ | LE, Fire, EMS | cbltac-fr |

These are the structural reference for all future event pages. New pages should use the same component system with a new wrapper ID.

---

## Other Event Package Assets

Load **etkm-event-planning** for:
- Complete event package structure (email sequences, social calendars, day-of run sheets)
- TYPE 1 (prospect seminars), TYPE 2 (student workshops), TYPE 3 (specialty/guest instructor)
- The WF-003 CBLTAC campaign is the reference template for TYPE 3 events

Load **etkm-brand-foundation** for all email and social copy.

Load **etkm-peace-framework** for PEACE slogans in email and social content.

Load **etkm-deliverable-qc** before delivering any file to Nathan.

---

## Nathan's Filter for This Project

Every deliverable from P2 must produce one or both:
- **More revenue** (registrations, sales, upsells)
- **Less time wasted** (faster to build, easier to deploy, no rework)

A technically impressive page that takes three sessions to build has failed.
A simple, fast, deployable page that gets registrations has succeeded.
