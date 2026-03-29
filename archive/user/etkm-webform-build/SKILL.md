---
name: etkm-webform-build
description: >
  The locked standard for designing and building any ETKM web form — contact forms,
  trial lesson request forms, event signups, Fight Back ETX inquiries, sponsorship
  forms, or any form that submits to Web3Forms and routes into Pipedrive via Make.com.
  This skill is the gatekeeper: no new field gets added to any ETKM form without
  passing the three-question filter documented here. Covers the approved field
  whitelist, Web3Forms configuration, hidden field spec, arc dropdown values and
  exact Pipedrive label strings, auto-reply setup, field-to-CRM mapping, and form
  CSS standard. Load this skill any time a form is being built, modified, audited,
  or deployed. Requires etkm-webpage-build (forms live inside pages) and
  etkm-crm-doctrine (CRM field mapping). Trigger phrases: "build a form", "contact
  form", "web form", "add a field", "form fields", "Web3Forms", "arc dropdown",
  "interest field", "form CSS", "trial request form", "signup form", "form config".
---

# ETKM Web Form Build Standard

**Version:** 1.0
**Last Updated:** 2026-03-28
**Derived from:** March 2026 webform field spec and live form audit

---

## Core Rules — Non-Negotiable

1. Every form submits to the **same Web3Forms endpoint** using the **same access key**
2. Web3Forms fires to **Make.com** which creates **Person + Deal in Pipedrive P1**
3. The `arc` field value is an **exact Pipedrive label string** — no translation required
4. `full_name` is a **single field** — never split into first/last
5. **No new field ships without passing the Three-Question Filter** (Section 3)
6. Forms inherit the ETKM visual standard from `etkm-brand-kit` and `etkm-webpage-build`

---

## 1. Web3Forms Credentials

| Item | Value |
|------|-------|
| Endpoint | `https://api.web3forms.com/submit` |
| Method | POST |
| Access Key | `8365e17b-3dd5-481d-ba48-465042f70e3d` |
| Dashboard | web3forms.com |
| Notification email | nate@etxkravmaga.com |

---

## 2. Hidden Fields — Every Form

These ship in every form as `<input type="hidden">`. The user never sees them.

```html
<input type="hidden" name="access_key" value="8365e17b-3dd5-481d-ba48-465042f70e3d">
<input type="hidden" name="subject" value="[PAGE-SPECIFIC — see Section 6]">
<input type="hidden" name="from_name" value="ETKM Website">
<input type="hidden" name="botcheck" style="display:none">
<input type="hidden" name="reply_from" value="East Texas Krav Maga &lt;nate@etxkravmaga.com&gt;">
<input type="hidden" name="reply_subject" value="We got your message — here's what happens next">
<input type="hidden" name="reply_message" value="[Email 0 copy — see Section 7]">
```

**`botcheck`:** Must be present, hidden, and never auto-populated. Web3Forms spam filter.
**`replyto`:** Web3Forms auto-populates from the submitted `email` field. Do not set manually.

---

## 3. Three-Question Filter — Required for Every Field

Before any field appears on an ETKM form, it must pass all three:

| # | Question | Pass | Fail |
|---|----------|------|------|
| 1 | **How do we use it?** Is there a defined action we take with this data? | Yes — specific, named action | "Nice to have" / "might be useful" |
| 2 | **How does it serve the CRM?** Does it map to a named Pipedrive field, label, or note? | Maps to specific Pipedrive field | No CRM home defined |
| 3 | **Is it an asset or a liability?** Does adding this field increase conversion or decrease it? | Neutral or increases conversion | Adds friction without proportionate value |

A field fails if it fails any single question. Document the pass/fail in Gate 1 (QC).

---

## 4. Approved Field Whitelist

These are the only fields approved for standard ETKM forms. Any field not on this list requires Three-Question Filter approval before use.

| Field Name | Type | Required | Maps To in Pipedrive |
|-----------|------|----------|---------------------|
| `full_name` | Text input | Yes | Person — Name (map directly, do not split) |
| `email` | Email input | Yes | Person — Email (primary) + auto-reply destination |
| `phone` | Tel input | No | Person — Phone (primary) |
| `arc` | Select dropdown | No | Person Label + Deal Label (exact label string) |
| `message` | Textarea | No | Note on Person record |

**Variant fields (page-specific, pre-approved):**

| Field | Page | Maps To |
|-------|------|---------|
| `business_name` | Sponsorship forms | Note on Person record |
| `event_interest` | Events Hub | Note on Person record |

---

## 5. Arc Field — Dropdown Values and Pipedrive Label Map

The `arc` dropdown submitted value is the **exact Pipedrive label string**. Apply directly — no keyword matching, no translation.

| Form Display Text | `arc` Value (submitted) | Pipedrive Label | Arc Direction |
|-------------------|------------------------|-----------------|---------------|
| Not sure yet — I want to explore | `Arc: Default` | `Arc: Default` | Standard sequence |
| Personal safety / protect myself | `Arc: Safety` | `Arc: Safety` | Safe environment framing |
| Training for my family | `Arc: Parent` | `Arc: Parent` | Capability-for-family |
| Fitness with a purpose | `Arc: Fitness` | `Arc: Fitness` | Purpose-built fitness |
| Law enforcement / military / security | `Arc: LE/Mil` | `Arc: LE/Mil` | Peer-level, operational |
| I've trained before (martial arts) | `Arc: Former MA` | `Arc: Former MA` | Gap-filling |

**If arc is empty or missing:** Default to `Arc: Default`. Never leave the Pipedrive label blank.

**Fight Back ETX forms:** Use healing/recovery-specific display text but map to the same arc labels per audience.

---

## 6. Subject Field — Page Source Map

The `subject` hidden field tells Make.com which page submitted. Use these exact strings:

| Page | Subject Value |
|------|--------------|
| Homepage | `Homepage Contact Form — East Texas Krav Maga` |
| Contact Us | `New Contact Form Submission — East Texas Krav Maga` |
| Free Trial Lesson | `Free Trial Lesson Request — East Texas Krav Maga` |
| Events Hub | `Event Notification Signup — East Texas Krav Maga` |
| Fight Back ETX — Contact | `Fight Back ETX Contact — East Texas Krav Maga` |
| Fight Back ETX — Sponsorships | `Sponsorship Inquiry — Fight Back ETX` |

---

## 7. Auto-Reply — Email 0

Fires instantly via Web3Forms hidden fields. Manus does not trigger this.

**Subject:** `We got your message — here's what happens next`

**Body:**
```
Your message came through and we've got it.

Someone from East Texas Krav Maga will be in touch within 24 hours —
usually sooner. If you'd rather not wait, call or text us at (903) 590-0085.

Schedule a free class:
https://calendly.com/easttxkravmaga-fud9/free-trial-lesson

Nate Lundstrom
East Texas Krav Maga
(903) 590-0085
etxkravmaga.com
```

**Verification:** After building a form, submit a test entry and confirm Email 0 arrives within 60 seconds.

---

## 8. Complete Form HTML — Standard Pattern

```html
<form action="https://api.web3forms.com/submit" method="POST" class="etkm-form">

  <!-- Hidden fields — every form -->
  <input type="hidden" name="access_key" value="8365e17b-3dd5-481d-ba48-465042f70e3d">
  <input type="hidden" name="subject" value="[PAGE SUBJECT — see Section 6]">
  <input type="hidden" name="from_name" value="ETKM Website">
  <input type="hidden" name="botcheck" style="display:none">
  <input type="hidden" name="reply_from" value="East Texas Krav Maga &lt;nate@etxkravmaga.com&gt;">
  <input type="hidden" name="reply_subject" value="We got your message — here's what happens next">
  <input type="hidden" name="reply_message" value="Your message came through and we've got it. Someone will be in touch within 24 hours. Schedule a free class: https://calendly.com/easttxkravmaga-fud9/free-trial-lesson — Nate Lundstrom | East Texas Krav Maga | (903) 590-0085">

  <!-- User fields -->
  <div class="form-group">
    <label>Full Name *</label>
    <input type="text" name="full_name" required placeholder="Your name">
  </div>

  <div class="form-group">
    <label>Email *</label>
    <input type="email" name="email" required placeholder="your@email.com">
  </div>

  <div class="form-group">
    <label>Phone</label>
    <input type="tel" name="phone" placeholder="(000) 000-0000">
  </div>

  <div class="form-group">
    <label>What brings you here?</label>
    <select name="arc">
      <option value="">Select one (optional)</option>
      <option value="Arc: Default">Not sure yet — I want to explore</option>
      <option value="Arc: Safety">Personal safety / protect myself</option>
      <option value="Arc: Parent">Training for my family</option>
      <option value="Arc: Fitness">Fitness with a purpose</option>
      <option value="Arc: LE/Mil">Law enforcement / military / security</option>
      <option value="Arc: Former MA">I've trained before (martial arts)</option>
    </select>
  </div>

  <div class="form-group">
    <label>Message</label>
    <textarea name="message" rows="4" placeholder="Anything else we should know?"></textarea>
  </div>

  <button type="submit">Send Message</button>

</form>
```

---

## 9. Form CSS Standard

Forms inherit the ETKM black/white/red palette. CSS to include in the page `<style>` block:

```css
.etkm-form {
  max-width: 560px;
  width: 100%;
}

.etkm-form .form-group {
  margin-bottom: 20px;
}

.etkm-form label {
  display: block;
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.7);
  margin-bottom: 8px;
}

.etkm-form input,
.etkm-form select,
.etkm-form textarea {
  width: 100%;
  background: #111;
  border: 1px solid #333;
  border-radius: 2px;
  color: #fff;
  font-family: 'Inter', sans-serif;
  font-size: 15px;
  padding: 12px 14px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.etkm-form input:focus,
.etkm-form select:focus,
.etkm-form textarea:focus {
  outline: none;
  border-color: #CC0000;
}

.etkm-form select option {
  background: #111;
  color: #fff;
}

.etkm-form button[type="submit"] {
  background: #CC0000;
  color: #fff;
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 16px 36px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-top: 8px;
}

.etkm-form button[type="submit"]:hover {
  background: #aa0000;
}
```

**On white-background sections:** Change form input background to `#f5f5f5`, border to `#ddd`, text to `#000`, labels to `rgba(0,0,0,0.6)`.

---

## 10. Full JSON Payload — What Make.com Receives

```json
{
  "access_key": "8365e17b-3dd5-481d-ba48-465042f70e3d",
  "subject": "New Contact Form Submission — East Texas Krav Maga",
  "from_name": "ETKM Website",
  "full_name": "Jane Smith",
  "phone": "(903) 555-1234",
  "email": "jane@example.com",
  "arc": "Arc: Safety",
  "message": "Optional message text",
  "timestamp": "2026-03-28T14:22:00Z"
}
```

---

## 11. QC Gates — Run Before Delivery

### Gate 1 — Field-to-CRM Mapping
- [ ] Every user-submitted field maps to a named Pipedrive field, label, or note — document it
- [ ] `full_name` maps to Person Name as a single field (not split)
- [ ] `arc` value is an exact Pipedrive label string from the approved list in Section 5
- [ ] Any field not on the approved whitelist passed the Three-Question Filter (Section 3)
- [ ] No field ships with "nice to have" as its justification

### Gate 2 — Web3Forms Config
- [ ] `access_key` = `8365e17b-3dd5-481d-ba48-465042f70e3d` present in hidden fields
- [ ] `subject` hidden field matches the exact string for this page (Section 6)
- [ ] `botcheck` hidden field present and not auto-populated
- [ ] `reply_subject` and `reply_message` (Email 0) present in hidden fields
- [ ] Arc dropdown option values match Pipedrive label strings exactly (e.g., `Arc: Safety` not `safety` or `Safety`)

### Gate 3 — Three-Question Filter Documentation
- [ ] For each field in the form, the three-question pass/fail is documented in the build notes
- [ ] No fields marked as "might be useful" — all have a specific named use
- [ ] Any field that failed Gate 3 was removed before delivery

---

## 12. Testing Checklist

| # | Test | Expected Result |
|---|------|----------------|
| 01 | Submit form — arc = `Arc: Safety` | Person created in Pipedrive P1, Stage 1, Label: Arc: Safety |
| 02 | Submit form — arc left blank | Person created, Label defaults to Arc: Default |
| 03 | Submit with existing email | No duplicate Person — new Deal added to existing Person |
| 04 | Check Email 0 | Arrives in submitted email inbox within 60 seconds |
| 05 | Check Make.com scenario | Scenario ran, no errors in execution log |
| 06 | Check error handler | Disconnect Pipedrive module, submit — error email to nate@etxkravmaga.com with full payload |

---

## 13. What This Skill Does NOT Cover

- CRM architecture, pipeline structure, label definitions → use `etkm-crm-doctrine`
- Make.com scenario build steps → use Manus briefing doc
- Page layout containing the form → use `etkm-webpage-build`
- Copy voice for form labels and confirmation messages → use `etkm-brand-foundation`
