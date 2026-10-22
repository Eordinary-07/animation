# Kimodo Prompt Pack — "Making a Fist"

Kimodo = NVIDIA's text-to-motion diffusion model (`nv-tlabs/kimodo`). It outputs a **body** motion
(30-joint `somaskel30`) that gets expanded to the 77-joint SOMA skeleton for export.

## Read this first (it saves you a lot of retries)

Kimodo **does not animate fingers**. The docs state it plainly: `somaskel30` *"removes most finger
and hand detail"* — the model predicts the wrist, hand end, and body only, then the 77-joint
skeleton is filled in with a neutral hand pose. Hand end-effector constraints pin the **wrist +
hand end**, not the knuckles.

So:
- A prompt can get you the **arm, wrist and shoulder performance of making a fist** — the raise,
  the snap, the tension, the hold. That is most of the read on screen.
- The **actual fist** (fingers curling) has to be keyed by hand afterwards, or faked with a hand
  pose/constraint on the rig. That's ~6 keyframes of work and is covered at the bottom.

Write prompts about the **whole-body beat**, not about fingers. Prompts that describe each body
part in detail degrade Kimodo's output (see its Best Practices page).

---

## 1. Ready-to-paste prompts (start with `A person…`, keep to 1–2 behaviors)

**Cleanest read — one hand, chest height**
```
A person stands facing forward and raises their right hand to chest height, then clenches their fist.
```

**Angry / building rage (both hands, at the sides)**
```
A person stands with both hands at their sides and balls them into tight fists, shoulders rising with anger.
```

**Slow, deliberate tension (good for a close-up beat)**
```
A person slowly raises their right forearm and closes their hand into a fist in front of their chest, holding it there.
```

**Fighting stance / combat idle**
```
A person drops into a fighting stance and brings both hands up into fists near their face, bouncing lightly.
```

**Clench then release (the release sells the clench)**
```
A person clenches their right fist, then relaxes the hand and lowers their arm.
```

**Victory / celebration**
```
A person raises their right arm overhead and pumps a clenched fist.
```

**Threat / warning**
```
A person points at someone, then slowly closes their hand into a fist and lowers it.
```

---

## 2. CLI commands

```bash
# Basic — 2.5s is plenty for raise + clench + hold
kimodo_gen "A person stands facing forward and raises their right hand to chest height, then clenches their fist." \
  --model Kimodo-SOMA-RP-v1.2 \
  --duration 2.5 \
  --num_samples 4 \
  --bvh \
  --output output/fist_right

# Angry double-fist beat
kimodo_gen "A person stands with both hands at their sides and balls them into tight fists, shoulders rising with anger." \
  --model Kimodo-SOMA-RP-v1.2 \
  --duration 3.0 \
  --num_samples 4 --seed 7 \
  --bvh --bvh_standard_tpose \
  --output output/fist_angry
```

Tips that actually change the result:
- `--num_samples 4` — text prompts are a lottery on subtle beats; pick the best sample, don't reword the prompt.
- `--duration 1.5–3.0` — a clench is fast. Long durations give you drifting, aimless arms.
- If the arm motion is weak, raise the **text** weight, not the constraint weight:
  `--cfg_type separated --cfg_weight 2.5 1.5`
- `--bvh --bvh_standard_tpose` → clean T-pose BVH for Blender/Maya retargeting.
- `--no-postprocess` only if foot skate cleanup is fighting your arm pose; normally leave it on.

---

## 3. Multi-prompt beat (Kimodo timelines)

Prompts are generated in sequence, each conditioned on the last frames of the previous one, so give
each prompt full context:

```bash
kimodo_gen "A person stands relaxed with their arms at their sides. A person raises their right hand to chest height and clenches their fist. A person holds the fist at chest height, then lowers their arm." \
  --duration "1.5 2.0 2.0" \
  --num_transition_frames 5
```

Do **not** write `"Then the person clenches"` as a later prompt — it has no context and generates mush.

---

## 4. Holding the fist in place with a constraint

End-effectors are the one constraint type that helps here: pin the right wrist so the fist stays
planted while the body shifts. It constrains the wrist + hand end only. In the demo, key
`hand_right` at the clench frame and hold it for the next 10–20 frames; or in JSON:

```json
{"effector": {"hand_right": [0.25, 1.45, 0.35]}}
```

(Y-up, meters, root starts at XZ = 0,0. Author it in the demo UI rather than by hand — the axes
are easy to get wrong.)

---

## 5. Getting the actual fist (the part Kimodo won't do)

Export with `--bvh` (77 joints incl. full finger chains: `RightHandThumb1-3`, `Index1-4`,
`Middle1-4`, `Ring1-4`, `Pinky1-4`), then key the fingers yourself. At 24 fps:

| Frame | What |
|-------|------|
| 0 | Hand open, relaxed |
| 2–3 | Anticipation: hand opens a hair wider, wrist extends slightly |
| 4 | Pinky and ring start curling |
| 5–6 | Middle, then index curl — stagger them, don't curl all four in one key |
| 7 | Thumb folds across the front of index/middle (last, and it's what makes it read as a fist) |
| 8–9 | Snap into the tightest curl; small overshoot past the settle pose |
| 12 | Settle back a couple of degrees |

- Curl **per joint**, roughly 25–30° at the base, 55–65° at the middle, 40–50° at the tip.
- The stagger in step 4–5 is the whole trick. Four fingers snapping simultaneously looks like a
  claw machine; offset by 1 frame each and it looks like a hand.
- Add a wrist flex of 5–10° and forearm pronation at the snap — that's what the Kimodo body motion
  is already doing, so match it rather than fighting it.
- For an angry hold, add 1-frame, 1–2° tremor on the finger bases; dead-still fists read as CG.

If the character's rig has no finger joints, cheat it: swap the hand mesh to a pre-made fist shape
key, or hide the fingers in a glove/mitt. On a phone-sized frame nobody sees the difference.

---

## 6. Prompt-writing rules (from Kimodo's own docs)

- Start with `"A person…"` — closest to the training distribution. Stylize the subject instead:
  "An angry person…", "A tired person…", "A boxer…".
- **One or two behaviors** max per prompt. Three actions in one sentence = mush.
- Medium detail. `"A person makes a fist"` alone is too thin; a paragraph of per-joint direction is
  too much. Describe intent and body attitude, not anatomy.
- Stick to what it was trained on: locomotion, gestures, everyday activities, object interaction,
  combat, dance, and emotional styles. "Clench fist" is comfortably inside that.
- Max 10 seconds per prompt. Keep keyframe constraints under 20 per type.
- Retarget the 77-joint result onto your rig — and check the elbow/shoulder twist, since the arm
  pose is doing all the storytelling here.
