# ETKM Workflows

Version-controlled email sequences, Make.com automations, and campaign docs.

## Active Workflows

| ID | Name | Emails | Status |
|----|------|--------|--------|
| WF-001 | Pre-Trial Funnel | 8 | Near deployment |
| WF-002 | 90-Day Onboarding | 28 | Ready to load |
| WF-003 | CBLTAC Event Campaign | 10 | Packaged |

## Folder Structure

workflows/
WF-001-pre-trial/  - Pre-trial prospect funnel (8 emails)
WF-002-onboarding/ - 90-day student onboarding (28 emails)
WF-003-cbltac/     - CBLTAC event campaign (10 emails)

## WF-001: Pre-Trial Funnel
- Trigger: Opt-in / lead magnet download
- Length: 8 emails
- Arc classification: Manus to Claude API to Pipedrive label
- Goal: Convert cold prospect to trial class booking
- Status: Near deployment

## WF-002: 90-Day Onboarding
- Trigger: Trial class attended, Level 1 pipeline move
- Length: 28 emails (15 identity + 13 competency)
- Phases: Belonging > Noticing > Becoming
- Framework: PEACE transformation arc
- Status: Ready to load into Pipedrive

## WF-003: CBLTAC Event Campaign
- Event: CBLTAC Specialty Training with John Wilson
- Date: April 24-25, 2026
- Venue: LifePoint Fellowship Church, Tyler TX
- Length: 10 emails
- Status: Fully packaged, ready for Manus installation

## Make.com Integration
All workflows are triggered via Make.com scenarios:
- Square payment events trigger Pipedrive deal updates
- Failed payments trigger P4 Payment Due label
- Form submissions start WF-001 sequence
- Trial attendance moves P1 to P2 pipeline

## Role Division
Email copy: Claude
Make.com builds: Manus
Pipedrive stage logic: Claude docs + Manus execution
Arc classification API: Claude API via Manus
