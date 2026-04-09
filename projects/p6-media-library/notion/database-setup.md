# ETKM Media Library — Notion Database Setup

**Updated:** April 2026 — taxonomy replaced with 14 audience arcs + 6 scene intents

---

## Step 1: Create the Database

1. In Notion, create a new **Full page database** (fresh, no parent required)
2. Name it: `ETKM Media Library`
3. Set view to **Gallery** (best for image assets)

---

## Step 2: Build the Schema

Delete the default properties, then create these in order:

| Property Name | Type | Notes |
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

### Tags — Two Groups

**Group 1 — Audience Arc Tags** (who appears in or would use this image):

| Tag | Audience Segment |
|---|---|
| `parents` | Parents & Families |
| `women` | Adult Women |
| `men` | Adult Men |
| `teens` | Teenagers (13-17) |
| `older-adults` | Older Adults (55+) |
| `fitness` | Fitness-Motivated Adults |
| `former-ma` | Former Martial Artists & BJJ |
| `leo-mil` | Law Enforcement / Military / First Responders |
| `private-security` | Private Security & Executive Protection |
| `ipv-survivors` | IPV Survivors |
| `occupational` | High-Risk Occupational Workers |
| `homeschool-faith` | Homeschool Families & Faith Communities |
| `corporate` | Corporate & Organizational Groups |
| `college` | College Students & Young Adults (18-26) |

**Group 2 — Scene Intent Tags** (what the image communicates):

| Tag | Meaning |
|---|---|
| `awareness` | Subject reading environment, scanning, noticing |
| `recognition` | Subject has identified something — posture shifts, gaze locks |
| `decision` | Subject positioned to act — weight shifted, path chosen |
| `presence` | Trained confidence at rest — protector identity visible |
| `contrast` | Two states in one frame: aware vs unaware, before vs after |
| `witness` | Identity reveal — face visible, protector moment |

**Add all 20 tags to the Tags multi-select field.**

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
| **By Arc** | Gallery | None | Tags A→Z |
| **Social Ready** | Gallery | Content Use Cases contains `Social media post` | Date Added DESC |

---

## How Tagging Works (Claude assigns these automatically)

Every image receives 2–4 tags:
- **1–2 audience arc tags** — based on who appears in the image or which segment would use it
- **1–2 scene intent tags** — based on what the image communicates

**Example:** A photo of a woman in a parking garage looking alert would receive:
- `women` (audience arc)
- `awareness` (scene intent)

This makes the library queryable by both audience and intent — you can find "images of women in a decision scene" for a specific campaign without manual search.

---

## Verification

After the pipeline processes its first image, verify the record contains:
- [ ] Filename in the Name field
- [ ] Asset Type set correctly
- [ ] Description (1–2 sentences, factual)
- [ ] 2–4 tags: mix of audience arc + scene intent tags
- [ ] 1–3 content use cases
- [ ] Date Added populated
- [ ] Drive URL linking to the B&W file in the library folder
- [ ] Source = Drive
- [ ] Status = Active
