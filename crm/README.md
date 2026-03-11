# CRM - Pipedrive Doctrine and Client Journey

## Overview
ETKM CRM architecture covering pipeline structures, label dictionaries, and client lifecycle logic.
All Pipedrive configuration follows etkm-crm-doctrine v1.2.

## Pipeline Structure
- P1: Prospects - Pre-trial leads and cold outreach
- P2: Level 1 Students - Active beginner students
- P3: Adv/Exp. Students - Advanced and experienced students
- P4: At Risk/Retention - Churn risk and payment issues
- P5: Private Lessons - One-on-one training clients

## Automation Triggers
- Payment Due: Square to Make.com to Pipedrive on failed payment
- PIF Due: Proactive outreach before Paid in Full expiry
- Trial Booked: Calendly to Make.com to Pipedrive deal creation

## Files
- pipedrive-stage-map.md
- label-dictionary.md
- arc-classification.md
