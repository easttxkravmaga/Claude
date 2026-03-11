# PIPEDRIVE CLEANUP — MANUS TASK
**Date:** 2026-03-11
**Status:** Partially complete — one item remaining for Manus

---

## COMPLETED VIA API (already done — do not redo)

### Deal Labels — CLEANED ✅
Removed 9 redundant labels. Two remain:
- Not Interested
- Invalid

### Person Labels — CLEANED ✅
Removed Cold lead, Hot lead, Warm lead (replaced by ETKM Arc Type field).
17 labels remain (see CRM doctrine for full list).

---

## YOUR TASK — Duplicate CBLTAC Field

There are two identical custom Person fields named "CBLTAC Enrolled Date" with different keys:
- Key 1: `8cae8f528afa52fd268f...`
- Key 2: `74815de35eaa10f03497...`

**What to do:**
1. Open Pipedrive → Settings → Data Fields → Person fields
2. Find both "CBLTAC Enrolled Date" fields
3. Check which one has actual data in it (open a few CBLTAC-enrolled person records and see which field is populated)
4. Delete the EMPTY duplicate — leave the one with data
5. Report back to Nathan: which key was deleted, how many records had data in the kept field

**Do not delete both. Do not guess — verify data first.**

---

## WHEN COMPLETE
Update Workflow Registry: Pipedrive Audit → COMPLETE
Notify Nathan.
