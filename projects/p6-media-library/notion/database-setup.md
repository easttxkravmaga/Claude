# ETKM Media Library — Notion Database Setup

## Step 1: Create the Database

1. In Notion, navigate to the **Operational Dashboards** parent page
2. Click `+` → **Database → Full page**
3. Name it: `ETKM Media Library`
4. Set view to **Gallery** (best for image assets)

---

## Step 2: Build the Schema

Delete the default properties, then create these in order:

| Property Name | Type | Options to Add |
|---|---|---|
| **Name** | Title | *(default — keep as-is)* |
| **Asset Type** | Select | `Image`, `Video`, `Graphic`, `Screenshot` |
| **Description** | Text | *(no options)* |
| **Tags** | Multi-select | *(see taxonomy below — add all options)* |
| **Content Use Cases** | Multi-select | *(see list below — add all options)* |
| **Date Added** | Date | Format: Month/Day/Year |
| **Drive URL** | URL | *(no options)* |
| **Source** | Select | `Drive`, `Canva`, `Event`, `Other` |
| **Status** | Select | `Active`, `Archived` |
| **Notes** | Text | *(no options)* |

---

## Step 3: Add Multi-Select Options

### Tags — add each of these as options:

**Asset Type Tags:**
`training` `demonstration` `class` `seminar` `event` `headshot` `facility` `equipment` `group` `individual` `youth` `adult` `women` `cbltac`

**Content Context Tags:**
`social-ready` `print-ready` `web-ready` `email-ready` `testimonial-context` `action-shot` `portrait` `environment` `candid` `posed`

**Campaign/Project Tags:**
`fight-back-etx` `cbltac` `armed-citizen` `youth-program` `college-safety` `private-lessons` `open-enrollment` `community-event`

**Tone Tags:**
`high-energy` `calm-focus` `community` `instructional` `real-world` `confidence`

### Content Use Cases — add each of these as options:

`Social media post` `Email header` `Landing page hero` `Print ad` `PDF/lead magnet` `Seminar promotion` `Curriculum visual aide` `Testimonial support` `Event promotion` `Website background`

---

## Step 4: Connect the Notion Integration

1. Go to **notion.so/my-integrations**
2. Click **New integration**
3. Name: `ETKM n8n Pipeline`
4. Associate with your workspace
5. Copy the **Internal Integration Secret** — this is your n8n Notion credential

**Grant access to the database:**
- Open the `ETKM Media Library` database
- Click `···` (top right) → **Connections** → **Add connections** → select `ETKM n8n Pipeline`

---

## Step 5: Get the Database ID

From the database URL:
```
https://www.notion.so/ETKM-Media-Library-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?v=...
```

The 32-character string after the last `-` and before `?v=` is the database ID.
Format it as: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` (insert hyphens at positions 8, 12, 16, 20).

Paste this ID into n8n as `NOTION_MEDIA_LIBRARY_DB_ID`.

---

## Step 6: Set Default Views

Create these views for day-to-day use:

| View Name | Type | Filter | Sort |
|---|---|---|---|
| **All Assets** | Gallery | None | Date Added DESC |
| **Active** | Gallery | Status = Active | Date Added DESC |
| **By Tag** | Gallery | None | Tags A→Z |
| **Social Ready** | Gallery | Tags contains `social-ready` | Date Added DESC |

---

## Verification

After the pipeline processes its first image, verify the record contains:
- [ ] Filename in the Name field
- [ ] Asset Type set correctly
- [ ] Description (1–2 sentences, factual)
- [ ] 3–6 tags from the approved taxonomy
- [ ] 1–3 content use cases
- [ ] Date Added populated
- [ ] Drive URL linking to the B&W file in the library folder
- [ ] Source = Drive
- [ ] Status = Active
