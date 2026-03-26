# ETKM Contact Registry — Intake Checklist Reference

**File:** references/intake-checklist.md
**Load when:** Adding any new contact or batch of contacts to the database.

---

## SINGLE CONTACT INTAKE

Use this for adding one contact at a time — found via research, referral, or event.

### Gate 1 — Required Fields Check
Before anything else — confirm you have ALL of these:
- [ ] First name (a real person's name — not "Office" or "Contact")
- [ ] Email address (individual preferred — info@ only as a last resort)
- [ ] Organization name
- [ ] Their title / role at that organization
- [ ] City the org is in

**If any field is missing:** Add to `Pending_Review` tab. Do not add to a cold email tab. Come back when the field is found.

### Gate 2 — Relationship Tab Check
Ask: Is this org a direct competitor, fitness gym, youth sports league, or media outlet?

- [ ] Competitor → Add to `Relationships` tab with `status = no_contact`, `notes = REMOVE`. Stop here.
- [ ] Fitness gym → Add to `Relationships` tab with `notes = RESOURCES_SEMINARS`. Stop here.
- [ ] Youth sports league → Add to `Relationships` tab with `notes = SAFETY_COMMUNICATION`. Stop here.
- [ ] Media → Add to `Relationships` tab with `notes = PR_RELATIONSHIP`. Stop here.
- [ ] None of the above → Continue to Gate 3.

### Gate 3 — Duplicate Check
- [ ] Search the organization name across ALL tabs in the Sheet. Does it appear?
  - If YES: Check if this specific person (by email or title) already has a row.
    - Same person = duplicate. Do NOT add. Stop here.
    - Different person, different role = valid. Continue.
    - Different person, same role at same org = flag it. Which contact is more senior? Keep the more senior one.
- [ ] Search the email address across ALL tabs.
  - If found anywhere = duplicate. Do NOT add. Stop here.

### Gate 4 — Segment Assignment
Apply the 10-segment criteria from SKILL.md Section 3 in order:
- [ ] Which segment does this org belong to?
- [ ] Is this person the right role for that segment? (e.g., if it's an LE org but this person is the Records Clerk, they are NOT the right contact — find the Training Chief instead)
- [ ] If the org is a church: does this contact's role match Security (Pastor), Women's (Minister to Women), or Youth (Youth Minister)? Add a row only to the matching angle tab.

### Gate 5 — Add the Row
Add to the correct tab:
- [ ] `first_name` — filled
- [ ] `last_name` — filled if known
- [ ] `email` — filled
- [ ] `organization` — filled, exact name
- [ ] `title` — filled
- [ ] `city` — filled
- [ ] `segment` — matches the tab name exactly
- [ ] `email_1_sent` — BLANK
- [ ] `email_2_sent` — BLANK
- [ ] `email_3_sent` — BLANK
- [ ] `status` — `active`
- [ ] `notes` — any relevant context (e.g., "Met at Rotary Club March 2026", "Referred by John at CFT")
- [ ] `sequence_start_date` — BLANK (Make populates this)
- [ ] `source` — correct source tag from SKILL.md Section 6
- [ ] `date_added` — today
- [ ] `last_verified` — today

### Gate 6 — Audit Log
- [ ] Add one row to `Audit_Log` tab:
  - Date, "ADDED", tab name, org name, contact name, source, "Nate" or "Claude"

---

## BATCH INTAKE (10+ Contacts at Once)

Use this when adding a large group — a new directory, a new county's worth of orgs, or a new segment.

### Pre-Batch Setup
- [ ] Create a staging spreadsheet (separate from the Master Sheet) with the same column headers
- [ ] Populate all contacts into the staging sheet first
- [ ] Run the full deduplication check BEFORE moving anything to the Master Sheet:
  - Sort staging sheet by email → look for any email appearing twice
  - Sort staging sheet by org + title → look for any org+title appearing twice
  - Cross-reference staging sheet against Master Sheet (export Master Sheet to CSV and use a VLOOKUP or manual scan)

### Batch Segment Assignment
- [ ] Go through every row in the staging sheet and assign a segment tag
- [ ] Flag any orgs you're unsure about → move to `Pending_Review` later
- [ ] Flag any orgs that belong in the Relationship tab → add `RELATIONSHIP` tag
- [ ] Review all flags before importing

### Batch Quality Check (10% Sample)
- [ ] Select 10% of rows randomly
- [ ] For each selected row: verify the email is real by checking the org's website staff directory or contact page
- [ ] If more than 20% of sampled emails cannot be verified → audit the entire batch before importing
- [ ] If fewer than 20% are unverifiable → add those specific rows to `Pending_Review` and import the rest

### Import
- [ ] Import relationship tab contacts to `Relationships` tab first
- [ ] Import cold email contacts tab by tab (not all at once)
- [ ] After each tab import, spot-check 5 rows
- [ ] Confirm `status = active` on all cold email contacts
- [ ] Confirm all email_sent columns are blank

### Post-Batch Audit Log
- [ ] Add ONE summary row to `Audit_Log`:
  - Date, "BATCH_ADDED", tabs affected (comma-separated), number of contacts added, source, "Nate" or "Claude"

---

## WHAT "VERIFIED" MEANS

A contact is considered verified when you have confirmed — within the last 90 days — that:
1. The person still works at that organization
2. The email address is deliverable (not bounced in a previous send or confirmed on the org website)
3. Their title is still accurate

**Verification methods (acceptable):**
- Found on the org's official website staff directory
- Confirmed via LinkedIn (active profile, current employer listed)
- Confirmed via a phone call to the org's main number
- They replied to a previous ETKM email (even to opt out — they received it)

**Not acceptable as verification:**
- "It was in the original list" — original list contacts must be verified at the quarterly audit
- "I think it's probably still right"
- A LinkedIn profile that hasn't been updated in over a year

---

## CONTACT QUALITY TIERS

Not all contacts are equal. Use these tiers to prioritize follow-up.

| Tier | Definition | Action |
|---|---|---|
| **Tier 1 — Direct Buyer** | The person who makes the training decision and controls budget | Add to active sequence immediately |
| **Tier 2 — Champion** | Can't say yes alone but will advocate internally for ETKM | Add to active sequence — they open the door to Tier 1 |
| **Tier 3 — Gatekeeper** | Screens communications before they reach decision-makers | Add with a note — sequence may be less effective, but worth including |
| **Tier 4 — FYI Only** | Accounting, admin, payroll — no decision-making role | Do NOT add to cold email sequence. They are not targets. |

**Examples by segment:**

| Segment | Tier 1 | Tier 2 | Tier 3 | Tier 4 — Skip |
|---|---|---|---|---|
| Law Enforcement | Training Chief | Assistant Chief | Records Dept. | Payroll, Admin Asst. |
| Fire / EMS | Fire Chief, EMS Section Chief | Training Chief | Main Switchboard | Kitchen Coordinator |
| Churches | Senior Pastor | Youth Minister, Min. to Women | Admin Asst. to Pastor | Finance, Payroll |
| Private Schools | Head of School | Dir. of Athletics | Admissions Office | Accounts Payable |
| Public ISDs | Dir. of Athletics / Security | Principal | Superintendent's Secretary | Business Office, Payroll |
| Colleges | VP of Student Affairs | Dir. of Athletics | Admissions | Financial Aid, Registrar |
| Employers | HR Director | VP / President | Office Manager | Payroll, Accounting |
