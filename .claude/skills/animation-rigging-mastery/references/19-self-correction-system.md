# 19 — The Self-Correction System (how this skill learns from mistakes)

> Studios are not AAA because their first passes are perfect. They are AAA because
> **nothing ships un-reviewed**: test first (Williams), dailies with notes, gates between
> stages, and institutional memory of what went wrong last time. This file installs that
> loop. It is the difference between a skill that *knows* and a skill that *improves*.

## 1. The stage gates (no shot skips a gate)

Work passes in stages. A stage is only *done* when its checklist passes — going back is
cheaper than polishing a mistake (Williams' Procedure, ref 01/05).

**Gate L — LAYOUT** (camera & staging)
- [ ] Shot's one idea readable from a still frame (ref 18 §1)
- [ ] True scale (meters); lens chosen for intention, not habit
- [ ] Silhouette of the hero element reads against its background
- [ ] Screen direction / eyelines continuous with neighbors (ref 08)

**Gate B — BLOCKING** (stepped keys only)
- [ ] Every beat has its punctuation pose (the Acting Point); no twinning
- [ ] Beat timing matches the emotional arc (ref 18 §2.4); holds where the feeling lives
- [ ] Contacts planted (feet/hands don't drift in stepped preview)
- [ ] Poses tell the story muted (the silent test, §3)

**Gate S — SPLINE** (mechanics)
- [ ] Arcs everywhere (head, hands, hips trace curves — graph/motion-path check)
- [ ] Weight reads: no floating, no even spacing through impacts (ref 03/04 numbers)
- [ ] Foot slip at contact ≤ ~0.5 cm across the contact frames; zero interpenetration
- [ ] No pops: knees/elbows flip-free; rotations take the short path (gimbal check)
- [ ] Overlap/follow-through offset 2–6 frames by mass (hair/cloth/props lag correctly)

**Gate P — POLISH & FINAL**
- [ ] Face: blink logic alive (not metronome), lip-sync within ±1 frame, eyes lead turns
- [ ] Materials passed the 3-light test (ref 16 §6); roughness varies; values legal
- [ ] Continuity across cuts (props, light direction, screen position)
- [ ] Render: samples/noise acceptable at 100% zoom; AgX; correct color spaces (ref 11 §H)
- [ ] Lessons Ledger checked (§4): no previously-logged mistake repeated

## 2. Precision tolerances (measure — don't eyeball)

| Check | Professional tolerance | Where to verify |
|---|---|---|
| Foot slide during contact | ≤ 0.5 cm total drift (≈ invisible) | Graph editor location curves / contact frames |
| Lip-sync offset | ±1 frame of the audio hit | Dope sheet vs waveform (ref 06) |
| Eye darts before head turn | eyes lead by 2–4 frames | Timeline scrub (ref 06) |
| Blink duration | closed 1–2 frames at 24 fps (fully closed matters) | stepped check (ref 06) |
| Interpenetration | zero visible at final camera | rendered frame at 100% |
| Spacing at impacts | largest spacing adjacent to contact, never through it | motion-path diagnostic (11 B8) |
| Arc integrity | zero unintended kinks; marker spacing accelerates monotonically outside impacts; planted-foot markers stack (no crawl) | motion path on chain tips + ghosting (11 B8) |
| Camera path smoothness | no kinks/spacing jumps in the traced camera path | object motion path (11 B8) before render sign-off |
| Texel density | one standard per production (±10%) | checker pass (ref 17 §2) |
| Base color values | 30–240 sRGB band (ref 16 §3) | histogram / eyedropper |
| Camera drift in "locked" shots | zero — lock transforms | camera curves flat |

## 3. The self-critique battery (run BEFORE showing work to the user)

1. **Intention test** — state the shot's one idea; watch once; did you feel it? If not,
   the fix is staging/timing, not more polish.
2. **Silent test** — mute dialogue/audio: does the story still read? (Charlie Chaplin rule —
   Thomas & Johnston.)
3. **Silhouette test** — does the pose read as a black shape? (render/flatten values)
4. **Mirror test** — flip the render horizontally: fresh eyes catch crooked staging and
   twinning instantly.
5. **Thumbnail test** — shrink to postage size: composition and focal point survive?
6. **2× speed test** — play fast: even-spacing dead spots and floaty weight expose
   themselves.
7. **Flaw-code sweep** — run ref 13's codes against the shot; write down hits.
8. **Fix-the-top-3 rule** — fix the three biggest flaws found, re-run the failed test,
   *then* present. First drafts are for the battery, not for the user.

## 4. The Lessons Ledger (institutional memory — the "learning" mechanism)

At the start of any project, create **`LESSONS.md`** in the project root. **Read it before
starting work; append after every correction** — whether the user caught it, the battery
caught it, or a gate failed. One row per lesson:

```
## Lessons Ledger — [project]
| Date | Shot/Asset | Mistake | Cause | Fix applied | Standing rule created |
|---|---|---|---|---|---|
| 2026-10-19 | S03 | Foot slid through the step | IK target keyed after pelvis move | Re-keyed contact first, then pelvis | RULE: contacts keyed before body, always |
```

Rules for the ledger:
- **A user correction is never just fixed — it becomes a standing rule.** ("Her hair
  should feel heavier" → RULE: this character's overlap offset = 5–6 frames.)
- **At every gate, scan the ledger** for rules touching this shot/asset type. Repeating
  a logged mistake is the one unforgivable error.
- **Distill weekly/per-deliverable:** if the same cause appears 3×, promote it to the
  project brief so it's decided *before* it can recur.
- The ledger belongs to the user's project files — it persists across sessions even
  when this conversation doesn't. That is how the work keeps learning.

## 5. Symptom → gate → fix (fast routing)

| Symptom | Failed gate | Go to |
|---|---|---|
| "Feels robotic / gamey" | B (even spacing, twinning, no holds) | refs 03, 05; flaw codes |
| "Floaty, no weight" | S (spacing at contacts) | ref 04; check impact spacing |
| "Face looks dead" | P (eyes/blinks) or B (no acting point) | refs 05, 06 |
| "Looks CG / plastic" | P (materials) | ref 16 six-point check; 3-light test |
| "Can't tell what's happening" | L (staging/readability) | ref 18 §2.6, ref 08 |
| "Boring despite being correct" | *Intention* — no gate failed, the idea did | ref 18 (re-derive the beat) |
| "Great alone, wrong in sequence" | continuity / arc | refs 08, 18 §2.4 |

## 6. Precision habits (small, compounding)

- Work at the final frame rate from the first key. Judge only from the final camera,
  at final resolution, with final lighting intent.
- Key contacts before bodies; extremes before breakdowns; breakdowns before inbetweens
  (Williams' Procedure). The computer's free inbetweens are a liability until your keys
  are right ("no brainless inbetweens").
- Version every gate pass (`shot_S03_gateB_v02.blend`) — going back must be free.
- Numbers over adjectives in self-notes: not "snappier" but "contact spacing 3→5 frames."
- When stuck between two versions, render both, apply the battery, keep the winner —
  and log *why* it won. Taste that is written down becomes a rule; taste that isn't,
  evaporates.
