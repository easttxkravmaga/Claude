# ETKM Backend

Flask application deployed on Railway — serves as the middleware layer between Make.com, Pipedrive, and Claude API.

## Architecture

```
Make.com (trigger) → Flask App (Railway) → Claude API → Pipedrive (arc label + email)
```

## Core Function

Receives webhook from Make.com containing prospect contact data, sends structured prompt to Claude API for arc classification, returns classification + personalized email copy, triggers Pipedrive label update and email send via Make.com.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| ANTHROPIC_API_KEY | Claude API authentication |
| PIPEDRIVE_API_KEY | Pipedrive CRM access |
| FLASK_SECRET_KEY | App security |
| RAILWAY_ENVIRONMENT | Deployment context |

## Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| /health | GET | Railway health check |
| /classify-arc | POST | Receive contact data, return arc + email |
| /webhook/square | POST | Square payment failure → Pipedrive P4 |

## Arc Classification Logic

Classifies incoming prospects into one of 5 story arcs based on intake form data:
- Arc 1: Protection (family safety focus)
- Arc 2: Confidence (personal empowerment)
- Arc 3: Fitness (physical conditioning entry)
- Arc 4: Skill (martial arts background)
- Arc 5: Community (social/belonging motivation)

System prompt lives in: /prompts/arc-classification-system-prompt.md

## Deployment

Platform: Railway
Repo: This file's parent repository
Branch: main (auto-deploy on push)

## Status

Active — WF-001 pre-trial funnel depends on this service.
Claude Code handles all script updates to this directory.
