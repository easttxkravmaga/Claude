---
name: etkm-make-automation
description: Build, manage, and debug Make.com (formerly Integromat) scenarios for ETKM workflows. Use when creating scenarios, pushing blueprints via API, wiring Pipedrive HTTP modules, building routers with filters, or diagnosing Make.com execution errors. Encodes hard-won knowledge about Make.com API limitations, HTTP module validation quirks, cross-branch reference rules, and the correct handoff pattern for scenarios that require UI completion.
---

# ETKM Make.com Automation Skill

## Account Reference

| Field | Value |
|---|---|
| Zone | us2.make.com |
| Team ID | 51888 |
| Organization ID | 1945651 |
| API Key | 756da029-ca33-4f15-8ae6-ff8ad29bc785 |
| Pipedrive API Token | fbbcff8ade5ec73514122f32c9278c6d7ea076bc |
| Pipedrive Domain | easttexaskravmaga.pipedrive.com |
| Nathan's Owner ID | 22218870 |

---

## Make.com API — What Works vs. What Doesn't

### What the API CAN do reliably
- Create scenarios (POST `/api/v2/scenarios`)
- Push/update blueprints (PUT `/api/v2/scenarios/{id}/blueprint`)
- Activate/deactivate scenarios (PATCH `/api/v2/scenarios/{id}`)
- Create webhooks (POST `/api/v2/hooks`)
- Read blueprints (GET `/api/v2/scenarios/{id}/blueprint`)
- Delete scenarios (DELETE `/api/v2/scenarios/{id}`)
- List scenarios, connections, hooks

### What the API CANNOT do reliably
- **Initialize HTTP module Method field** — The `http:MakeRequest` v4 module requires the Method dropdown to be set via the UI. API-pushed blueprints store the value correctly but the runtime validator rejects it with "Validation failed for 5 parameter(s)" including `method`, `stopOnHttpError`, `allowRedirects`, `shareCookies`, `requestCompressedContent`. The only fix is opening each HTTP module in the UI editor and re-selecting the Method from the dropdown.
- **Clone scenarios** — The `/clone` endpoint requires `organizationId` but rejects it regardless of format.
- **Clear the `isInvalid` flag** — Once set, only a UI save clears it.

### Blueprint Push Pattern (correct)
```python
import requests, json

API_KEY = '756da029-ca33-4f15-8ae6-ff8ad29bc785'
SCENARIO_ID = <id>

blueprint = {
    "name": "Scenario Name",
    "flow": [...],
    "metadata": {
        "instant": True,
        "version": 1,
        "designer": {"orphans": []},
        "scenario": {
            "dlq": False, "slots": None, "dataloss": False,
            "maxErrors": 3, "autoCommit": True, "roundtrips": 1,
            "sequential": False, "confidential": False,
            "freshVariables": False, "autoCommitTriggerLast": True
        }
    }
}

r = requests.put(
    f'https://us2.make.com/api/v2/scenarios/{SCENARIO_ID}/blueprint',
    headers={'Authorization': f'Token {API_KEY}', 'Content-Type': 'application/json'},
    json={"blueprint": json.dumps(blueprint)}
)
```

---

## HTTP Module Blueprint Structure

The `http:MakeRequest` v4 module must be structured exactly as follows. Do NOT add extra fields (`stopOnHttpError`, `allowRedirects`, `shareCookies`, `requestCompressedContent`) to the mapper — they cause validation failures.

```json
{
  "id": 2,
  "module": "http:MakeRequest",
  "version": 4,
  "parameters": {
    "handleErrors": false,
    "useNewZLibDecompression": true
  },
  "mapper": {
    "url": "https://...",
    "method": "GET",
    "headers": [{"name": "Authorization", "value": "Bearer TOKEN"}],
    "qs": [],
    "bodyType": "raw",
    "parseResponse": true,
    "authUser": "",
    "authPass": "",
    "timeout": "",
    "shareCookies": false,
    "ca": "",
    "rejectUnauthorized": true,
    "followRedirect": true,
    "useQuerystring": false,
    "gzip": true,
    "useMtls": false,
    "contentType": "application/json",
    "data": "{\"key\": \"value\"}"
  }
}
```

**Note:** Even with this exact structure, the runtime will reject the method until it's re-selected in the UI. This is a Make.com platform limitation — the blueprint is stored correctly but the module's internal initialization state is only set by the UI dropdown interaction.

---

## Router and Filter Structure

### Router module
```json
{
  "id": 3,
  "module": "builtin:BasicRouter",
  "version": 1,
  "parameters": {},
  "mapper": null,
  "metadata": {"designer": {"x": 0, "y": 0}},
  "routes": [
    {
      "flow": [
        {
          "id": 4,
          "module": "http:MakeRequest",
          "filter": {
            "name": "Route label",
            "conditions": [[{"a": "{{expression}}", "b": "value", "o": "text:equal"}]]
          }
        }
      ]
    }
  ]
}
```

### Filter placement rule
**Filters go on the FIRST module inside the route's flow array** — NOT on the route object itself.

### Cross-branch reference rule (critical)
**A module in one router route CANNOT reference output from a module in a sibling route.** If Route 1 creates a deal (module 5) and Route 2 creates a deal (module 8), a third route CANNOT use `{{if(5.data.data.id; 5.data.data.id; 8.data.data.id)}}` — Make.com flags those modules as "not accessible."

**Fix:** Duplicate the downstream logic into each branch. Add the label router inside Route 1 (referencing `{{5.data.data.id}}`) AND inside Route 2 (referencing `{{8.data.data.id}}`).

---

## Webhook Creation

```python
r = requests.post(
    'https://us2.make.com/api/v2/hooks',
    headers={'Authorization': f'Token {API_KEY}', 'Content-Type': 'application/json'},
    json={
        "name": "Webhook Name",
        "teamId": 51888,
        "typeName": "gateway-webhook",
        "theme": "theme_001"
    }
)
hook = r.json()['response']['hook']
hook_id = hook['id']
webhook_url = hook['url']
```

Reference the hook in the webhook module:
```json
{
  "id": 1,
  "module": "gateway:CustomWebHook",
  "version": 1,
  "parameters": {"hook": HOOK_ID, "maxResults": 1},
  "mapper": {},
  "metadata": {}
}
```

---

## Pipedrive API Patterns (used in HTTP modules)

### Person search
```
GET https://easttexaskravmaga.pipedrive.com/api/v1/persons/search?term={{1.email}}&fields=email&exact_match=true
```
Check result count: `{{2.data.data.items.length}}` — 0 = new person, >0 = existing.

### Create person
```
POST https://easttexaskravmaga.pipedrive.com/api/v1/persons
Body: {"name": "...", "email": [{"value": "...", "primary": true}], "owner_id": 22218870, "FIELD_HASH": "VALUE"}
```

### Update person
```
PUT https://easttexaskravmaga.pipedrive.com/api/v1/persons/{{2.data.data.items[].item.id}}
```

### Create deal
```
POST https://easttexaskravmaga.pipedrive.com/api/v1/deals
Body: {"title": "...", "person_id": "{{4.data.data.id}}", "pipeline_id": 1, "stage_id": 1, "owner_id": 22218870, "status": "open"}
```

### Set deal label
```
PUT https://easttexaskravmaga.pipedrive.com/api/v1/deals/{{5.data.data.id}}
Body: {"label": "LABEL_ID"}
```

### Create note
```
POST https://easttexaskravmaga.pipedrive.com/api/v1/notes
Body: {"person_id": "...", "deal_id": "...", "content": "..."}
```

---

## Queue Management

When a scenario fails repeatedly, Make.com queues the payloads and deactivates the scenario. Before re-activating after a fix:

```python
r = requests.delete(
    f'https://us2.make.com/api/v2/scenarios/{SCENARIO_ID}/incomplete-executions',
    headers={'Authorization': f'Token {API_KEY}'}
)
```

Or in the UI: Edit scenario → Show queue → select all → delete.

---

## Handoff Pattern — When to Stop and Hand to Nathan

**Build via API:**
- Creating the scenario shell and blueprint structure
- Pushing flow, routers, filters, field values
- Creating webhooks, Pipedrive custom fields, labels

**Hand to Nathan when:**
- HTTP module Method validation is needed (UI-only — re-select Method dropdown per module)
- Cross-branch reference errors need route restructuring in the UI
- Canvas module interactions are required (Make.com's WebGL canvas doesn't respond reliably to coordinate-based browser automation)

**Correct handoff deliverable:** An HTML file with exact copy-paste values for every field, the flag→label ID table, and numbered steps. Nathan can complete UI work in 20–30 minutes with a good reference doc.

---

## ETKM Quiz Scenario Reference

**Scenario ID:** 4472085  
**Webhook URL:** `https://hook.us2.make.com/wb9nys6x92yiq9pakglsqv2a6m6dtfj1`  
**Hook ID:** 2040689  

### Quiz Custom Fields (Person object)
| Hash | Field | Type |
|---|---|---|
| 50 | Quiz — Entry Reason | Long text |
| 51 | Quiz — Safety Readiness Score | Number |
| 52 | Quiz — Score Tier | Dropdown |
| 53 | Quiz — Identity Statement | Long text |
| 54 | Quiz — Closing Vision Statement | Long text |
| 55 | Quiz — Confidence Type | Dropdown |
| 56 | Quiz — Primary Objection | Dropdown |
| 57 | Quiz — Firearm Status | Dropdown |
| 58 | Quiz — Family Motivation | Yes/No |
| 59 | Quiz — Must Protect Flag | Yes/No |
| 60 | Quiz — Prior Incident | Yes/No |
| 61 | Quiz — Returning Practitioner | Yes/No |
| 62 | Quiz — Auto PDF Delivered | Text |
| 63 | Quiz — Bonus PDF Selected | Dropdown |
| 64 | Quiz — Urgency Flag | Yes/No |
| 65 | Quiz — Completed Date | Date |

### Quiz Flag → Label ID Map
| Flag | Label ID |
|---|---|
| HIGH_URGENCY | 99 |
| AWARENESS_GAP | 100 |
| CONFIDENCE_GAP | 101 |
| FALSE_CONFIDENCE_URGENT | 102 |
| HIGH_COACHABILITY | 103 |
| NO_BASELINE_SKILLS_GAP | 104 |
| PRIOR_INCIDENT_CONSULT_CARE | 105 |
| REALITY_EXPOSURE_GAP | 106 |
| PARENT_FAMILY_ARC | 107 |
| MUST_PROTECT_CONSULT_FIRST | 108 |
| ACT_CONSULT_PRIORITY | 109 |
| ACT_CANDIDATE_ADVANCED | 110 |
| RETURNING_PRACTITIONER_PRIORITY | 111 |
| IDENTITY_BARRIER_OPEN_WITH_INCLUSION | 112 |
| NO_FIREARM_ACT_AWARENESS | 113 |
| COACHABILITY_NEEDS_WARMUP | 114 |
| ENCOURAGEMENT_PATH | 115 |
