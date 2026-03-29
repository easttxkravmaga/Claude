---
name: etkm-cinematic-doctrine
description: >
  Use this skill whenever creating AI image prompts, Canva image briefs, social media
  visual direction, or any visual content description for ETKM. This encodes the
  cinematic visual doctrine developed for the ETKM Prompt Generator v5 — including
  sightline zone composition, the locked HUD overlay system (v5), kinematic behavioral
  state language, scene intent categories, platform destination presets, and subject
  positioning. Trigger for "image prompt", "image brief", "Canva brief", "scene
  description", "social media image", "visual direction", "cinematic", "AI image",
  "Midjourney prompt", "DALL-E prompt", "HUD overlay", or any request to describe a
  visual scene for ETKM content. Also trigger when creating batches of image
  descriptions for social campaigns. Always load etkm-brand-kit alongside this skill
  for color and typography rules.
---

# ETKM Cinematic Visual Doctrine

**Version:** 2.0
**Last Updated:** 2026-03-26
**Source:** Cinematic Prompt Generator v5 build session

This skill encodes the visual composition rules and scene-building doctrine
for all ETKM image content. It is the difference between generic self-defense
imagery and ETKM's signature visual language.

---

## Core Principle

ETKM images demonstrate awareness, not violence. The visual story is always
about the moment before — the recognition, the spatial decision, the behavioral
state that changes the outcome. The subject is not fighting. The subject is
seeing, positioning, deciding.

---

## The Five Composition Panels

When building a scene description, work through these five layers in order.

### 1. Platform Destination

Set the canvas shape first. This determines aspect ratio language in the
output prompt.

| Platform | Aspect Ratio | Canvas Shape |
|----------|-------------|-------------|
| Instagram Square | 1:1 | Square |
| Instagram Story / Reel | 9:16 | Tall vertical |
| Facebook Post | 1.91:1 | Wide horizontal |
| LinkedIn Banner | 4:1 | Ultra-wide |
| Blog Hero | 16:9 | Wide horizontal |
| Print / Event Poster | Various | Specify dimensions |

### 2. Scene Intent

What is this image trying to communicate? Scene intent drives everything
that follows — subject positioning, lighting mood, overlay density, and
environmental choice.

| Intent | Visual Focus | Example Use |
|--------|-------------|-------------|
| Awareness | Subject reading environment, scanning, noticing | PEACE Prepared/Aware posts, situational awareness content |
| Recognition | Subject has identified something — posture shifts, gaze locks | Pre-attack indicator content, Left of Bang themes |
| Decision | Subject positioned to act — weight shifted, path chosen | PEACE Capable posts, training transformation content |
| Presence | Subject at rest but radiating trained confidence | PEACE Engaged posts, protector identity content |
| Contrast | Two states in one frame — aware vs unaware, before vs after | Diptych pairs, transformation arcs |
| Witness | Face visible — the identity reveal shot | Used sparingly, only for protector identity moments |

### 3. Subject Positioning

ETKM's visual signature is the back-turned or profile subject. This is
intentional — it puts the viewer into the subject's perspective rather
than looking at the subject.

**Default:** Back-turned or three-quarter turn. Subject faces away from
camera, toward the environment they are reading.

**Profile:** Side view. Used when sightlines need to be visible —
the viewer can see both the subject's gaze direction and what they
are looking at.

**Witness (rare):** Face visible. Reserved for the identity reveal —
the moment where the subject is the protector, not the observer.
Used once per campaign at most. It earns the face.

**Never:** Direct-to-camera heroic poses. Aggressive stances that belong to sport martial arts, not ETKM awareness content.

### 4. Sightline Zone Builder

This is the compositional layer that makes ETKM images structurally
different from generic awareness content. Sightlines are spatial geometry
that proves the subject is trained.

**How it works:**

The scene is divided into zones based on the subject's awareness field.
The subject always faces 12 o'clock. All figure positions and sightline
geometry calculate from this anchor.

| Zone | Description | Visual Treatment |
|------|-------------|-----------------|
| Primary Sightline | Where the subject is actively looking | Clear line of sight, nothing blocking. The environment in this direction is detailed and sharp. |
| Peripheral Field | Areas the subject is monitoring without direct gaze | Slightly softer focus but still visible. Background figures here suggest ambient monitoring. |
| Blind Spot | Behind or beside the subject outside awareness | If subject has positioned to eliminate blind spots (back to wall, corner position), this zone is absent — which itself communicates training. |
| Threat Zone | Where a behavioral anomaly exists | HUD overlay concentrates here. The trained mind has registered something. |

**Sightline composition rules:**
- The primary sightline should cross at least 60% of the frame
- Environmental elements should not block the primary sightline
- If the subject is seated, they are positioned with wall behind or
  corner advantage — never center-of-room with back exposed
- Sightline geometry should be inferable from the image even without
  the HUD overlay
- HUD overlays appear ONLY on figures in Direct or Peripheral sightline
  zones — never on figures in a blind spot the subject cannot see

### 5. ETKM HUD Overlay System — v5 Locked

This is the signature ETKM visual element: a tactical AR overlay that
reveals how a trained mind perceives the environment. It is proof of
awareness, not decoration.

**One style. Fixed forever. No alternatives.**

The style never changes — only state and color change per figure.
No bounding boxes. No reticle corners. No skeleton wires. No scan lines.
No geometric bracket markers. No data readout text. The glow follows
the human body — that is the only shape.

**Style (non-negotiable):**
Thin clean body outline tracing the full silhouette. Soft outer glow
extending 8–15px beyond the silhouette edge. No fill pattern. The
overlay annotates the person's physical form — it does not replace it.

---

**State drives opacity — two active states:**

| State | Fill Opacity | Meaning |
|-------|-------------|---------|
| Off | None | Figure present but untagged. No outline, no glow. The way an untrained person sees everyone. |
| Notice | 15–20% | Figure has entered awareness. Glow present but subtle. Not alarm — recognition. |
| On | 35% | Figure is locked and registered. Glow fully active. Decision pending. |

**Color — Red only:**

| Color | Hex | Meaning |
|-------|-----|---------|
| Red | #CC0000 | Threat. Registered. Intent suspected. Decision pending or made. |

---

---

**Figure rendering rule (critical):**

All HUD-tagged figures must be rendered as fully realized real people:
visible clothing, physical body weight, human presence. NOT silhouettes.
NOT shadow masses. NOT dark shapes. A real person with clothes and a body,
seen clearly, with the HUD overlay applied on top of them. The overlay
annotates their form. It does not replace it.

No weapons visible on any figure. No overtly aggressive facial expressions.
No readable intent on face. Figures may be backlit or partially shadowed
but must have physical mass and clothing detail.

---



**Per-figure prompt template (mandatory for every HUD-tagged figure):**

> *"Figure at [clock position], [distance tier] — [specific distance],
> [clothing description], [behavior description]. HUD: [Color] / [State] —
> thin clean body outline, soft outer glow extending [8–12]px beyond
> silhouette edge, [15–20% / 35%] fill [hex color].
> [State meaning: Figure has entered awareness / Figure is locked and
> registered / Assessed and cleared]."*

**Example (Red / On):**
> *"Figure at 2 o'clock, mid distance — one car length, trench coat,
> converging at angle toward subject's path. HUD: Red / On — thin clean
> body outline, soft outer glow extending 12px beyond silhouette, 35%
> fill #CC0000. Figure is locked and registered. Decision pending."*

**Example (Red / Notice):**
> *"Figure at 10 o'clock, close — within 8 feet, hooded, stationary
> against tree line, no purposeful task. HUD: Red / Notice — thin clean
> body outline, soft outer glow extending 10px beyond silhouette, 18%
> fill #CC0000. Figure has entered awareness. Assessment ongoing."*

---

## Color and Atmosphere

All visual direction follows the etkm-brand-kit, with these additional
rules for cinematic image content:

**Base treatment:** Desaturated or monochromatic. The world in the image
is muted — blacks, grays, cool tones. This isn't colorless, but deliberately
pulled back so that color has meaning when it appears.

**Color discipline with HUD active:**

When HUD is in use, environmental red accents (exit sign, brake light,
neon reflection) are still permitted as a single environmental accent.
The HUD red exists in the overlay layer — perceptual, not environmental.
A scene can carry one environmental red accent AND red HUD overlays
simultaneously because they occupy different visual planes.

When HUD is NOT in use (clean scene): Red appears only once — overlay,
environmental accent, or subject detail. Never in multiple places.

**Lighting mood by scene intent:**

| Intent | Lighting |
|--------|---------|
| Awareness | Even, natural, slightly cool — the world as it is |
| Recognition | Contrast increases — shadows deepen, subject hits a pool of light |
| Decision | Directional — one strong light source, clear shadow geometry |
| Presence | Warm backlight or rim light — the subject glows slightly against the environment |
| Contrast | Split lighting — aware side lit, unaware side in shadow |

---

## Behavioral State Layer

Every subject in an ETKM image carries a behavioral state. This is
communicated through body mechanics — specific joint positions, weight
distribution, and hand placement. Not vague posture descriptions. Not
feelings. Anchored physics that give the AI model actual constraints.

The description must tell the model what each limb is doing, where the
weight is, and what the hands are near. The model cannot interpret
"calm readiness." It can render "right foot forward, weight loaded on
the ball of the foot, knees soft, hips square."

| State | Kinematic Description |
|-------|-----------------------|
| Baseline Aware | Right foot slightly forward, weight centered between both feet. Knees soft, not locked. Hips square to 12 o'clock. Both arms away from body, hands open, fingers relaxed, thumbs forward. Head turned 15–20° toward primary sightline. Shoulders level. |
| Heightened | Weight shifted to balls of both feet. Left heel slightly elevated. Knees bent 10–15°. Shoulders rotate to square toward threat zone. Chin drops 5°. Both hands rise to waist level, open, inside the frame of the body. |
| Decided | Right foot advanced 12–18 inches toward exit or toward threat. Body angled 30–45° from original position. Left foot anchored, heel down. Left hand extended slightly, palm open and forward. Right hand at sternum height. Head square to direction of movement. |
| Protective | Body bladed — turned 45° to create a physical barrier. Non-dominant arm extended back and slightly down, making contact with or guiding the person being protected. Dominant hand forward, palm open. Weight on front foot. |
| At Rest (Trained) | Seated. Back against wall or corner structure behind subject. Weight distributed across both hips, feet flat on floor. Non-dominant hand holds object (beverage, phone). Dominant hand free, resting on thigh. Head oriented toward entry points, chin level. |

---

## Environmental Settings

Choose environments that are universal and relatable. The goal is for
any viewer to think "I've been in that exact place."

**Strong settings:**
- Parking garage (levels, shadows, echo, isolation)
- Coffee shop (seated awareness, entry point monitoring)
- Grocery store parking lot (transition space, distractions)
- Hotel lobby or hallway (travel safety, unfamiliar environment)
- Walking path at dusk (low light, limited exits)
- Gas station at night (isolated, transactional, vulnerable)
- Airport terminal (crowds, luggage, distraction)
- School pickup line (parent protection, child awareness)
- Downtown sidewalk (urban density, multiple stimuli)
- Church or community building (sanctuary space, unexpected threat)
- Public park (open environment, multiple approach vectors)

**Avoid:**
- Generic martial arts gym interiors
- Dark alleys (cliché — already dangerous, no discovery moment)
- Obviously dangerous locations (assumes the worst, removes the tension
  of ordinary turned charged)

---

## Scene Description Output Format

When generating a prompt for AI image tools (Midjourney, DALL-E, Flux, etc.)
or a Canva image brief, produce output in this exact order. No slots skipped.
Doctrine defaults fire for any slot without explicit user input.

1. **Platform and aspect ratio** — canvas shape, dimensions
2. **Scene intent** — one word from the intent table
3. **Setting** — specific environment with architectural and lighting details
4. **Subject** — gender presentation, approximate age, clothing, positioning
5. **Behavioral state** — kinematic description (joints, weight, hands)
6. **Sightline geometry** — clock positions, what zones are covered, what advantage the position gives
7. **Environmental figures** — each figure described with clock position, distance, clothing, behavior
8. **HUD overlay** — each figure: Color / State / glow spec / meaning. Or: "No HUD — clean scene."
9. **Color treatment** — base grade, where color accents appear, HUD color conflict check
10. **Mood line** — one sentence capturing the emotional register of the image

---

## Campaign Sequencing

When building a multi-image campaign, sequence scenes across the
PEACE transformation arc:

| Position | PEACE Pillar | Scene Intent | Subject State | HUD Suggestion |
|----------|-------------|-------------|---------------|---------------|
| Posts 1–2 | Prepared | Awareness | Baseline Aware | Off — no HUD, untagged environment |
| Posts 3–4 | Aware | Recognition | Heightened | Red / Notice — something registered |
| Posts 5–6 | Capable | Decision | Decided | Red / On — threat locked, decision made |
| Post 7 | Engaged | Presence | At Rest (Trained) | Off — environment clear, no active threat |

The Contrast intent works as a diptych pair at any point in the sequence —
same environment, same subject, two states. Panel 1: No HUD (unaware).
Panel 2: Full HUD active (aware). Same scene, different mind.

---

## Rules

- Every image demonstrates awareness, never violence
- Back-turned or profile subjects are the default; face is earned
- HUD overlay is earned by the scene — it exists because the subject
  detected something. If nothing warrants detection, HUD is absent.
- HUD style is fixed: thin body outline, soft outer glow, opacity by state.
  Never bounding boxes, reticle corners, scan lines, or geometric brackets.
- HUD-tagged figures are fully realized real people — never silhouettes
- Behavioral state uses kinematic language — joints, weight, hands, not feelings
- Sightline geometry must be compositionally logical and clock-anchored
- Environmental settings must be universally relatable — "ordinary turned charged"
- The mood is quiet confidence, not aggression
- The variable that changes the outcome is always the decision, never the technique
