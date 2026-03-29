---
name: etkm-contact-registry
description: >
  The master operating system for how ETKM organizes, adds, audits, and maintains
  all outreach contacts. Load this skill whenever working with ETKM contact lists,
  adding new cold contacts, assigning organizations to segments, building or
  updating the cold email Google Sheet, running a contact audit, resolving
  duplicates, moving organizations between the cold email list and the Relationship
  tab, or making any decision about how a contact or organization should be
  categorized. Also load when answering questions like "where does this org go?",
  "is this a cold email target?", "how do I add these contacts?", "when do we audit
  the list?", "what segment does this belong to?", or "is this a duplicate?"
  Trigger phrases: "add contacts", "new contact", "segment this", "which segment",
  "contact audit", "clean the list", "update the sheet", "where does X go",
  "relationship tab", "cold email target", "contact intake", "contact process",
  "contact registry", "outreach list", "contact database", "organize contacts",
  "build the sheet", "add to the list". This skill governs ALL contact decisions
  — never assign a segment or add a contact without loading it first.
---

# ETKM Contact Registry

**Version:** 1.0
**Locked:** March 2026
**Owner:** Nathan Lundstrom / East Texas Krav Maga
**GitHub:** easttxkravmaga/Claude — skills/user/etkm-contact-registry/

---

## 1. Where Everything Lives

| Asset | Location | Access |
|---|---|---|
| **Master Contact Sheet** | Google Drive → "ETKM Contact Operations" folder → "ETKM Cold Email Database — Master" | Read/write — shared with Make.com Google account |
| **This Skill** | GitHub: easttxkravmaga/Claude → skills/user/etkm-contact-registry/SKILL.md | Claude reads at session start |
| **SOP Document** | Google Drive → "ETKM Contact Operations" folder → "ETKM Contact Registry SOP" | Human reference — open when auditing |
| **Segment Definitions** | This file (Section 3) + references/segment-definitions.md | Load reference file for full org lists |
| **Relationship Tab Strategy** | This file (Section 5) | |
| **Audit Logs** | Google Sheet → "Audit_Log" tab | Append-only — never delete entries |

---

## 2. The Google Sheet Structure

**Workbook name:** ETKM Cold Email Database — Master

### Tabs (in order)
| Tab Name | Contents |
|---|---|
| `LE` | Law Enforcement cold email contacts |
| `Fire_EMS` | Fire / EMS cold email contacts |
| `Churches_Security` | Church security angle — Senior Pastor contacts |
| `Churches_Womens` | Church women's program angle — Minister to Women contacts |
| `Churches_Youth` | Church youth angle — Youth Minister contacts |
| `Private_Schools` | Private / Christian school contacts |
| `Homeschool` | Homeschool group and co-op contacts |
| `Public_ISD` | Public school district contacts |
| `Colleges` | College / university contacts |
| `Employers_Professionals` | Large employers and professional services contacts |
| `Relationships` | Non-cold-email orgs — warm outreach only |
| `Audit_Log` | Running record of all changes — never delete rows |
| `Pending_Review` | New contacts awaiting segment assignment — holding area |

### Column Structure (identical across all cold email tabs)
| Column | Field Name | Required | Notes |
|---|---|---|---|
| A | `first_name` | YES | Blank = Make will fail |
| B | `last_name` | NO | Include if known |
| C | `email` | YES | Blank = Make will fail |
| D | `organization` | YES | Exact org name — match the master org list |
| E | `title` | YES | Their actual job title |
| F | `city` | YES | City where the org is located |
| G | `segment` | YES | Must match the tab name exactly |
| H | `email_1_sent` | AUTO | Make writes the date here after send |
| I | `email_2_sent` | AUTO | Make writes the date here after send |
| J | `email_3_sent` | AUTO | Make writes the date here after send |
| K | `status` | YES | Dropdown — see Section 4 |
| L | `notes` | NO | Manual notes — replies, context, flags |
| M | `sequence_start_date` | AUTO | Date status was first set to "active" |
| N | `source` | YES | Where this contact came from — see Section 6 |
| O | `date_added` | YES | Date row was added to Sheet |
| P | `last_verified` | YES | Date contact info was last confirmed accurate |

### Status Dropdown Values (Column K)
| Value | Meaning | Who Sets It |
|---|---|---|
| `active` | In the sequence — will receive next scheduled email | Human (on intake) |
| `replied` | They responded — handle manually | Human (monitoring inbox) |
| `opted_out` | Requested removal — sequence stopped | Human (within 24 hours of request) |
| `bounced` | Email undeliverable — address is bad | Human or Make error handler |
| `hold` | Pause the sequence — do not email yet | Human |
| `converted` | Became a student, booked a call, or signed a contract | Human |
| `no_contact` | Relationship tab contacts who get no email | Human (on intake for Relationship tab) |

---

## 3. The 10 Segments — Decision Framework

When a new organization or contact arrives, apply these rules in order. The first segment whose criteria match is the correct assignment.

### Segment 1 — Law Enforcement
**Criteria:** Any sworn law enforcement agency, sheriff's office, constable office, ISD police department, or campus police.
**Primary contact role:** Training Chief (buyer), Police Chief or Sheriff (approver).
**ETKM angle:** CBLTAC — close-quarters combatives for LE.

### Segment 2 — Fire / EMS
**Criteria:** Any fire department (career or volunteer), EMS agency, emergency services district, fire marshal office, or emergency management coordinator.
**Primary contact role:** Fire Chief or EMS Section Chief (buyer), Training Chief (champion).
**ETKM angle:** Scene safety and violent patient/scene encounter response.

### Segment 3 — Churches (Security)
**Criteria:** Any Christian church or faith congregation. This is Angle 1 of 3 for churches.
**Primary contact role:** Senior Pastor or Lead Pastor.
**ETKM angle:** Congregation safety awareness seminar — no cost to the church.
**NOTE:** Every church gets THREE rows — one per angle (Security, Women's, Youth) in three separate tabs, IF the church has ministry roles that match all three angles. A very small church with only a senior pastor gets Security angle only.

### Segment 4 — Churches (Women's)
**Criteria:** Same church orgs as Segment 3. This is Angle 2 — only add a row if the church has a women's ministry or minister to women contact.
**Primary contact role:** Minister to Women, Women's Ministry Director, or equivalent.
**ETKM angle:** Fight Back ETX women's self-defense workshop.

### Segment 5 — Churches (Youth)
**Criteria:** Same church orgs as Segment 3. This is Angle 3 — only add a row if the church has a youth ministry contact.
**Primary contact role:** Youth Minister, Minister to Students, or Student Ministry.
**ETKM angle:** ETKM youth program — confidence, discipline, values alignment.

### Segment 6 — Private / Christian Schools
**Criteria:** Any private, parochial, or Christian K–12 school that is NOT a public ISD campus.
**Primary contact role:** Head of School (buyer), Director of Athletics (champion).
**ETKM angle:** Character development, confidence, whole-child philosophy.
**WATCH FOR:** Schools that are attached to a church. The school and the church are two separate organizations — each gets its own rows.

### Segment 7 — Homeschool Groups
**Criteria:** Any homeschool co-op, homeschool athletic association, or homeschool enrichment program. Includes groups organized around a church but operating as a separate educational program.
**Primary contact role:** Group Director, Co-op Lead, Program Contact.
**ETKM angle:** PE-credit-eligible personal protection curriculum.

### Segment 8 — Public ISDs
**Criteria:** Any Texas public school district (ISD). Note: ISD police departments go to Segment 1 (Law Enforcement), not here.
**Primary contact role:** Director of Athletics or Director of School Security (champion). NOT the Superintendent first.
**ETKM angle:** Youth program, school safety, after-school enrichment.
**CRITICAL RULE — ONE ROW PER DISTRICT:** Multiple entries for the same ISD (District Office, Communications, Auxiliary Services, etc.) are consolidated to ONE row. Use the District Office contact or the Athletic Director. The other contacts are irrelevant to ETKM's outreach.

### Segment 9 — Colleges & Universities
**Criteria:** Any accredited college or university — 2-year community college or 4-year institution.
**Primary contact role:** VP of Student Affairs (buyer), Director of Athletics.
**ETKM angle:** Fight Back ETX women's workshop as a campus program.
**NOTE:** Theological seminaries go here, not Churches — they are educational institutions.

### Segment 10 — Large Employers & Professionals
**Criteria:** Any large employer (100+ employees) OR professional services firm in healthcare, banking, mortgage, real estate, insurance, staffing, or finance.
**Primary contact role:** HR Director or Director of Human Resources (buyer).
**ETKM angle:** Workforce wellness and employee safety confidence. Women's safety for professional women in client-facing roles.
**EXAMPLES:** CHRISTUS Trinity Mother Frances, UT Health, Target Distribution, Tyler Pipe / McWane, Citizens 1st Bank, Southside Bank, CMG Home Loans, Keller Williams Realty, Express Employment, Remedy Staffing.

---

## 4. Relationship Tab — Three Strategies

Organizations that do NOT get cold email. They go in the `Relationships` tab with `status = no_contact` and a strategy tag in the `notes` column.

| Strategy Tag | Who Gets It | What It Means |
|---|---|---|
| `REMOVE` | Direct competitors | No contact. No sequence. Reference only. |
| `RESOURCES_SEMINARS` | Fitness gyms, wellness studios | Warm relationship — seminars, referral partnerships, community presence. Personal outreach by Nate only. |
| `SAFETY_COMMUNICATION` | Youth sports leagues, community orgs | Safety resources and warm communication. Position ETKM as a community resource. Build referral channel to youth program. |
| `PR_RELATIONSHIP` | Media, newspapers | Editorial relationship. Story pitches, community safety column. Not a sales conversation. |

**Competitors (permanent REMOVE tag — never reclassify):**
- Tiger-Rock Martial Arts of Tyler
- Gracie Barra Tyler BJJ
- Relson Gracie / Lone Star MMA Academy
- Tyler Kung Fu & Fitness

---

## 5. New Contact Intake Process

### Step 1 — Collect Required Information
Before adding ANY contact to the Sheet, confirm ALL required fields exist:
- [ ] First name (real, not "Contact" or "Office")
- [ ] Email address (individual, not generic info@ unless no other option)
- [ ] Organization name (exact match to master org list)
- [ ] Title / role
- [ ] City
- [ ] Source (where did this contact come from?)

If any required field is missing — the contact goes to `Pending_Review` tab, NOT a cold email tab. Do not add incomplete contacts to active tabs.

### Step 2 — Segment Assignment
Apply Section 3 rules in order. If the org matches multiple segments (e.g., a church with women's and youth ministry) — create multiple rows, one per applicable angle, in the correct tabs.

### Step 3 — Duplicate Check
Before adding a new row:
1. Search the organization name across ALL tabs
2. Search the email address across ALL tabs
3. If org already exists — check if the role is different. Same org + same role = duplicate, do not add. Same org + different role (e.g., Training Chief AND Police Chief) = two rows are acceptable.
4. If email already exists anywhere in the Sheet = duplicate. Do not add.

### Step 4 — Relationship Tab Check
Check whether the org belongs in the Relationship tab first (Section 4). If it's a fitness gym, youth sports league, competitor, or media org — it goes to Relationships, not a cold email tab.

### Step 5 — Add the Row
Add to the correct tab with:
- All required fields populated
- `status` = `active` (for cold email contacts) or `no_contact` (for Relationship tab)
- `email_1_sent`, `email_2_sent`, `email_3_sent` = BLANK (Make reads blank as "not sent")
- `date_added` = today's date
- `last_verified` = today's date (you're adding it now, so it's verified now)
- `source` = where this came from

### Step 6 — Audit Log Entry
Add one row to the `Audit_Log` tab:
- Date, action ("ADDED"), tab name, org name, contact name, reason/source, who added it.

---

## 6. Contact Sources

Track every contact's source in Column N (`source`). Use these standard tags:

| Source Tag | Meaning |
|---|---|
| `ORIGINAL_LIST` | From the March 2026 founding contact list |
| `MANUAL_RESEARCH` | Found via web search, LinkedIn, org website |
| `REFERRAL` | Someone referred this contact to ETKM |
| `EVENT` | Met at an event, seminar, or community gathering |
| `INBOUND` | They reached out to ETKM first |
| `GOOGLE_MAPS` | Found via Google Maps search for org type in area |
| `CHAMBER_DIRECTORY` | From a Tyler or regional chamber of commerce directory |
| `ISD_WEBSITE` | Found via school district staff directory |
| `LE_DIRECTORY` | Found via Texas law enforcement agency directory |

---

## 7. Audit Schedule

Read references/audit-schedule.md for the full audit checklist per cadence.

| Cadence | Trigger | What Gets Audited |
|---|---|---|
| **Ongoing** | Any opt-out or bounce reply | Update status in Sheet within 24 hours. Log in Audit_Log. |
| **Weekly** | During any active email sequence | Check sending inbox. Update replied/opted_out/bounced. Review Make scenario history for errors. |
| **Monthly** | First Monday of each month | Segment performance review. Clean stale statuses. Verify Make scenarios still running. |
| **Quarterly** | First Monday of Jan, Apr, Jul, Oct | Contact accuracy audit — people change jobs. Verify titles and emails are still current. |
| **Annually** | January | Full list rebuild — orgs that have closed, merged, or rebranded. Full duplicate scan. Segment taxonomy review. |
| **Post-Launch** | After each segment completes its 3-email sequence | Segment post-mortem: sent, bounced, replied, opted-out, converted. Document in Audit_Log. |

---

## 8. Duplicate Resolution Rules

| Situation | Rule |
|---|---|
| Same email address, different rows | Keep one. Delete the duplicate. Log in Audit_Log. |
| Same org, same role, different email | Verify which email is current. Keep current, update old to bounced. |
| Same org, different roles | Both rows are valid. Keep both. |
| Same org listed under two different names | Standardize to one name. Merge rows if the contact is the same person. |
| Multiple ISD entries for same district | One row per district. Keep the most senior decision-maker contact. Remove the rest or move to a Notes column. |

---

## 9. What To Do When...

**A contact opts out:** Change `status` → `opted_out` within 24 hours. Do not delete the row. Add a note. Log in Audit_Log.

**An email bounces:** Change `status` → `bounced`. Note the bounce type (hard vs. soft) if known. Try to find a corrected email before giving up. Log in Audit_Log.

**A contact replies positively:** Change `status` → `replied`. Follow up manually within 24 hours. Move them toward a call or trial. Update notes with the reply context.

**A contact changes jobs:** Change `status` → `hold`. Update title and org fields if they moved to another org in the list. If they moved outside East Texas or to an irrelevant role, change status to `opted_out` (they're no longer a valid target) and log it.

**An organization closes or merges:** Change all contacts for that org to `hold`. Research the successor org. If a new org emerges from a merger and it's a valid segment target, add a fresh row with `source = MANUAL_RESEARCH`. Log the closure in Audit_Log.

**You're unsure which segment an org belongs to:** Add it to `Pending_Review` tab. Flag it with a note. Review at the next monthly audit or bring it to a Claude session for segment assignment. Never guess.

---

## 10. Reference Files

Load these when needed:

| File | Load When |
|---|---|
| `references/segment-definitions.md` | Need the full org-by-org assignment list or detailed segment criteria examples |
| `references/audit-schedule.md` | Running a monthly, quarterly, or annual audit — contains the full checklist |
| `references/intake-checklist.md` | Adding a batch of new contacts — the step-by-step intake form |
| `references/relationship-tab-orgs.md` | Reviewing or updating the Relationship tab — full org list with strategy tags |
