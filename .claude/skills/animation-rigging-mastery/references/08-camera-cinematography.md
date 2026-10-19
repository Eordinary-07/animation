# Camera & Cinematography — Shot Language for Animation

Sources: Parent ch. 1 ("Principles of filmmaking", "Sound"), Whitaker & Halas (Storyboard,
Responsibility of the Director, Timing for Broadcast vs Features), Williams (Directing:
Hook-Ups, Leica Reel), Thomas & Johnston (How to Get It on the Screen; Story).
Cinema grammar is the shared language of these books — master it and the animation
*reads* on screen.

## 1. The essence of the camera

The camera is the audience's eye and mind: **framing says what matters, angle says who has
power, movement says how we feel about it.** Reason: in a theater the audience can look
anywhere; on screen they see exactly what you frame. Staging (principle #3) IS camera work.

## 2. Shot sizes — what each one MEANS

| Shot | Contents | Psychology / use |
|---|---|---|
| EWS (extreme wide) | figure small in world | geography, isolation, epic scale |
| WS (wide) | full body + environment | where we are; body acting lives here |
| MLS/FS (medium long) | knees-up | social distance; two-hander blocking |
| MS (medium) | waist-up | conversation default; gesture readable |
| MCU (medium close) | chest-up | personal; standard for dialogue delivery |
| CU (close-up) | face | emotion, thought, the acting point |
| ECU (extreme close) | eyes/mouth/detail | intensity, story clue, impact |

Rule (Parent/Whitaker): **cut closer as emotion intensifies; cut wider for context or
release.** Don't cut at random — size changes should mean something.

## 3. Camera angles

- **Eye level** — neutral, honest (default).
- **Low angle** — power, threat, heroism (subject looms over audience).
- **High angle** — weakness, vulnerability, overview, submission.
- **Dutch/tilted** — unease, wrongness, psychological disturbance (use sparingly).
- **Over-the-shoulder (OTS)** — conversation geometry; keeps both characters in the scene.
- **POV** — we ARE the character; powerful for reveals and threats (use once per scene).

## 4. Lenses & focal length (Blender: camera data, mm)

| Focal length | Look | Use |
|---|---|---|
| 18-24 mm | exaggerated space, distorted edges, deep depth | tension, slapstick, environment-driven shots |
| 28-40 mm | slightly wide "documentary" energy | chase/action, roomy interiors |
| 50 mm | neutral, eye-like | honest conversation |
| 85-135 mm | compressed, intimate, soft background | close-ups, love/emotion, "film look" |
| 200 mm+ | extreme compression, flattening | surveillance, distance, dread |

- **Distance ≠ focal length.** Dolly-in (physical move) changes perspective; zoom does not.
  Reason: a real move gives parallax (alive); a zoom flattens (surveillance/cheap).
- Depth of field (Blender: camera → Depth of Field): focus = attention. **Focus pulls** are
  story tools (shift attention from A to B on the beat).

## 5. Framing rules

- **Rule of thirds** — eyes in the upper third; break it deliberately (dead-center = power
  or unease; symmetric frames = Wes Anderson formality).
- **Headroom** — just above the head; too much = falling, too little = crushed.
- **Leadroom / nose room** — space in front of a face/body's direction of attention;
  looking out of frame = longing/threat; looking into wall = trap.
- **Look space** in dialogue: eyelines must match cut-to-cut (both characters "look" to
  consistent screen sides).
- **Screen direction** (180° rule): keep the camera on one side of the action line so
  characters keep their left/right relationship across cuts. Crossing = disorientation
  (break only on purpose, or with a neutral "reset" shot).
- **30° rule** — successive shots of the same subject should differ ≥30° (or in size),
  else it reads as a jump cut.

## 6. Camera movement — every move is an emotion

| Move | Meaning |
|---|---|
| Static / locked | observation, comedy timing (holds land harder), stillness = tension |
| Pan / tilt (head) | following; discovery; "looking" |
| Truck / dolly lateral | traveling WITH the subject; journey |
| Dolly in | growing importance, realization, dread |
| Dolly out | release, isolation, the joke's aftermath |
| Crane / boom up | transcendence, reveal of scale |
| Crane down | entering the world, powering down |
| Handheld | immediacy, chaos, realism (add noise!) |
| Arc / orbit | hero shot, stasis in motion, tension around a center |

Rules of reason:
- **Move only with motivation** (a character moves, a reveal, an emotion grows). Random
  floating cameras read as amateur.
- **Start and end the move on a composition** — a move between two good frames; never
  drift.
- Movement must respect weight: camera has mass — ease in/out (it's a dolly, not a cursor).
- Animated camera shake: tiny, asymmetric, heavier on impacts; Williams' stagger ideas apply.

## 7. Continuity & editing (Parent 1.3.2, Williams "Hook-Ups")

- **Hook-ups**: action must connect across cuts (a gesture started in shot A lands in
  shot B). Plan the cut ON the action ("cutting on motion" hides the edit).
- Match eyelines, match screen direction, match size progression (avoid same-size jumps).
- **The cut is a timing device**: cut on accents (Whitaker) — cuts land with the beat.
- Cross-cutting builds tension by parallel storylines (Parent: editing principles).
- Sound leads picture by 1-2 frames for impact; picture leads sound for comedy (Whitaker).

## 8. Blender implementation

- Camera: `focal_length` (50mm default), `sensor_fit` HORIZONTAL, `sensor_width` 36mm.
- **Camera switching**: timeline markers → select camera → `Ctrl+B` (Bind Camera to Markers)
  — each shot gets its own camera; scrubbing plays the cut.
- Rigs: camera target empty + Track To; camera on a curve (Follow Path) for moves; add a
  "cam_rig" empty for crane/handheld; handheld = noise modifiers on rotation/location
  (small scale, different seeds per axis).
- DOF: enable, focus on an eye-level empty; f-stop ≈ 2.8-5.6 for close-ups, 8-16 for wides.
- Playblast shots individually AND as a sequence in the VSE (see `10-blender-production.md`).
- Render: EEVEE for speed/lookdev, Cycles for final lighting; always review at 24fps with
  sound.

## 9. Shot-design checklist (per shot, before animating)

1. What is the ONE idea of this shot? (staging)
2. Does size/angle/movement serve that idea and the character's objective?
3. Is the silhouette readable in frame? Eyes where?
4. Does it obey screen direction / eyeline / hook-up with neighbors?
5. Is the camera motivated, and does the move start/end on good frames?
6. Would a professional cut this here? (When in doubt: hold wider, cut later.)
