# Registry - ETKM Workflow Registry and Session Protocol

## Overview
The single source of truth for all ETKM AI workflows. Prevents duplicate work,
enforces role boundaries, and governs all Claude/Manus handoffs.

## Role Division (Non-Negotiable)
- Claude: All copywriting, email sequences, system prompts, strategy
- Manus: Browser automation, Make.com builds, Pipedrive UI operations
- Claude Code: Scripting, Flask backend, API integrations

## Workflow Status
- WF-001: Pre-trial funnel (8-email sequence) - Near deployment
- WF-002: 90-day onboarding sequence (28 emails) - Near deployment
- WF-003: CBLTAC event campaign - Fully packaged, ready for Manus

## Session Opening Protocol
1. Load etkm-workflow-registry skill
2. Check this registry for current status
3. Confirm role assignment before building
4. Log completed work at session end

## Priority Sequence
D-01/D-02 to WF-001 completion to WF-002 load to WF-003 load to Claude API integration
