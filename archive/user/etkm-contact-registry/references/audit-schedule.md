# ETKM Contact Registry — Audit Schedule Reference

**File:** references/audit-schedule.md
**Load when:** Running any scheduled audit — monthly, quarterly, or annual.

---

## ONGOING AUDIT (Same Day — Within 24 Hours)

Triggered by: any opt-out reply, bounce notification, or positive reply received in the sending inbox.

**Checklist:**
- [ ] Open the sending Gmail inbox
- [ ] For each opt-out reply: find the contact row in the Sheet → status → `opted_out` → add note with date and exact reply → log in Audit_Log
- [ ] For each hard bounce (undeliverable): find the contact row → status → `bounced` → add note → search for corrected email → log in Audit_Log
- [ ] For each positive reply: find the contact row → status → `replied` → add reply context to Notes → follow up manually within 24 hours → log in Audit_Log
- [ ] Verify Make scenario history shows no errors from that day's run
- [ ] Save and close

---

## WEEKLY AUDIT (During Active Sequences Only)

Triggered by: any week in which at least one segment sequence is actively sending.

**Checklist:**
- [ ] Check sending Gmail inbox — process all replies (see Ongoing Audit above)
- [ ] Open Make.com → check scenario history for all active scenarios
  - Any scenario that ran with errors → identify which rows caused the error → fix the data → re-run manually for affected contacts
  - Any scenario that didn't run on schedule → investigate → document in Audit_Log
- [ ] Check each active segment tab: confirm email_X_sent dates are populating correctly
- [ ] Tally weekly metrics per segment: emails sent this week, bounces, opt-outs, replies, conversions
- [ ] Record weekly metrics in Audit_Log

---

## MONTHLY AUDIT (First Monday of Each Month)

**Time required:** 30–45 minutes

**Part 1 — Performance Review (per active segment)**
- [ ] Total contacts in segment
- [ ] Total Email 1 sent
- [ ] Total Email 2 sent
- [ ] Total Email 3 sent (sequence complete)
- [ ] Total bounced
- [ ] Total opted-out
- [ ] Total replied
- [ ] Total converted
- [ ] Reply rate = replied / Email 1 sent × 100
- [ ] Bounce rate = bounced / Email 1 sent × 100
- [ ] If reply rate < 2% — flag the segment copy for review before next batch
- [ ] If bounce rate > 5% — audit the email addresses in that segment tab
- [ ] Record all metrics in Audit_Log with "MONTHLY_REVIEW" action tag

**Part 2 — Sheet Hygiene**
- [ ] Scan each active tab for rows where status is blank → fix to correct status
- [ ] Scan for rows where email_1_sent has a date but status is still "active" → investigate (Make may have failed to update status, or contact replied and status wasn't updated)
- [ ] Scan Pending_Review tab → assign all contacts sitting there to correct segments or mark as declined
- [ ] Remove any test rows that were left in active tabs from development

**Part 3 — Infrastructure Check**
- [ ] Verify all Make scenarios are active (not paused or errored out)
- [ ] Verify Gmail OAuth connection in Make is still valid (tokens expire)
- [ ] Verify Google Sheets connection in Make is still valid
- [ ] Send a test email manually from the sending Gmail to confirm deliverability
- [ ] Log infrastructure check in Audit_Log with "MONTHLY_INFRA" action tag

---

## QUARTERLY AUDIT (First Monday of January, April, July, October)

**Time required:** 2–3 hours

**Part 1 — Contact Accuracy Review**
For each contact in each active tab:
- [ ] Spot-check 20% of rows per segment (random sample)
- [ ] For each sampled contact: visit the org's website → confirm the person still holds that title → confirm email format still matches org pattern
- [ ] If a contact has left their role: status → `hold` → research replacement → if replacement found, add new row
- [ ] If an org has a new phone number or address (for notes): update the notes column
- [ ] Log all changes in Audit_Log with "QUARTERLY_ACCURACY" action tag

**Part 2 — Relationship Tab Review**
- [ ] Review all `RESOURCES_SEMINARS` contacts — has Nate made contact with any of them? Update notes.
- [ ] Review all `SAFETY_COMMUNICATION` contacts — any referrals received from these orgs? Log it.
- [ ] Any Relationship tab org that should now move to cold email (e.g., a new decision-maker arrived who is a direct fit)? Move them with a new row in the correct segment tab.
- [ ] Log all changes with "QUARTERLY_RELATIONSHIP" action tag

**Part 3 — Segment Taxonomy Review**
- [ ] Has ETKM launched any new programs since last quarter that create a new outreach angle? If yes, determine if a new segment or sub-angle is needed.
- [ ] Are there any orgs in Pending_Review from the last 3 months still unassigned? Resolve them.
- [ ] Log taxonomy decisions with "QUARTERLY_TAXONOMY" action tag

---

## ANNUAL AUDIT (January — Full List Rebuild)

**Time required:** Half day — schedule dedicated time

**Part 1 — Org Existence Verification**
- [ ] For every organization in every tab, verify it still exists and is operating
  - Search Google for org name + city
  - Check if website is still active
  - Check if Facebook/social presence is current
  - If org has closed: change all contacts for that org to `opted_out`, add note "ORG CLOSED [year]"
  - If org has merged: research successor, add new row if successor is a valid target

**Part 2 — Full Duplicate Scan**
- [ ] Export all tabs to a single flat CSV
- [ ] Sort by email column — find any email appearing in more than one row
- [ ] Sort by organization + title — find any org+role combination appearing more than once
- [ ] Resolve all duplicates per Section 8 of the SKILL.md
- [ ] Log all duplicate resolutions with "ANNUAL_DEDUPE" action tag

**Part 3 — Segment Taxonomy Full Review**
- [ ] Has the 10-segment structure served the outreach goals? Any segments that produced zero results should have their copy reviewed and possibly rewritten.
- [ ] Any new org categories in East Texas that should be added (new hospitals, new schools, new employers)?
- [ ] Add new orgs to Pending_Review for assignment

**Part 4 — Database Backup**
- [ ] Download a full CSV export of the entire Master Sheet
- [ ] Save to Google Drive → "ETKM Contact Operations" → "Backups" → file named "ETKM_Contact_Backup_[YYYY-MM].csv"
- [ ] Verify backup file opens correctly before closing
- [ ] Log backup with "ANNUAL_BACKUP" action tag

---

## AUDIT LOG FORMAT

Every audit entry in the `Audit_Log` tab follows this structure:

| Column | Field | Example |
|---|---|---|
| A | Date | 2026-03-26 |
| B | Action Tag | ADDED / OPTED_OUT / BOUNCED / MONTHLY_REVIEW / etc. |
| C | Tab Affected | LE |
| D | Org Name | Tyler Police Department |
| E | Contact Name | Mike Johnson |
| F | Detail | Replied "remove" — status updated to opted_out |
| G | Who Made the Change | Nate / Claude |
