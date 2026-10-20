# Timing & Spacing Doctrine — Williams + Whitaker/Halas

Sources: *The Animator's Survival Kit* (chapters: Timing and Spacing, Advancing Backwards
to 1940, More on Spacing, Anticipation, Takes and Accents, Timing/Staggers/Wave/Whip) and
*Timing for Animation* (spacing, holds, anticipation, follow-through, weight/force chapters).
Use this whenever keyframing, polishing, or reviewing motion in Blender.

## 1. The two levers (memorize)

- **Timing** = how many frames an action takes → conveys *weight, mood, size, intent*.
- **Spacing** = where the drawings/keys sit within those frames → conveys *speed and force*.
- Essence (Williams): "It's all in the timing and the spacing."
- Reason: the eye reads distance-per-frame as velocity and acceleration as force. Same
  keyframes + different spacing = a different physical event.

## 2. The working vocabulary (charts → Blender F-curves)

| Classical term | Blender equivalent |
|---|---|
| Extremes / keys | Key poses (the story poses) |
| Breakdowns | Breakdown poses (Breakdowner or breakdown keys) |
| Inbetweens | Tweened F-curve motion |
| Chart (timing chart) | F-curve handles + key spacing in the Graph Editor |
| X-sheet / exposure sheet | Dope Sheet + frame rate; scene fps 24 |
| Ones vs twos | Key every frame vs every 2nd frame (24fps: 12 drawings/sec) |

- **Ones vs twos** (Williams "The Great Ones and Twos Battle"): fast action & dialogue on
  ones (smooth), medium action on twos (punchy, classic feel). In 3D: constrain key density
  accordingly; at 24fps, pose-to-pose on twos still interpolates on ones — emulate the
  twos feel by stepping or holding breakdowns (Stepped interpolation for blocking!).
- **Three ways to animate** (Williams): straight-ahead (alive, risky), pose-to-pose
  (structured), and the recommended combination: pose-to-pose structure, then straight-ahead
  passes for life. In Blender: block with Stepped keys → Breakdowner pass → smooth + polish.

## 3. Blocking rules

1. **Block extremes only** at first: contact/story poses, no inbetweens.
2. Every key must be an *idea* (Williams: keys are decisions, not positions).
3. **Breakdowns decide the path** between extremes — pose them deliberately (the arc goes
   up? through? around?), don't let the computer choose.
4. Test constantly (Williams: "Testing, testing, testing") — playblast every pass.

## 4. Spacing doctrine (Williams: "More on Spacing")

- **The major beginner's mistake**: even spacing everywhere = floaty, "computer" motion.
  Natural motion packs drawings at acceleration/deceleration ends, spreads in the middle.
- **Slow-in / slow-out** (Illusion of Life principle #5; Parent 3.1.3 "ease-in/ease-out"):
  actions accelerate out of rests and decelerate into rests — except when force demands
  otherwise (a punch *arrives* fast).
- **The elongated inbetween**: when you need snap, place the breakdown closer to the extreme
  the action is *leaving*, and stretch the distance into the arriving pose.
- **Watch your arcs** (Williams, p. 90): "Most actions follow arcs… either in a wavelike
  arc or in a sort of figure 8. But sometimes it is angular or straight. **Straight lines
  give power**." Short distances go straight; long distances go in an arc. Breakdowns are
  *eccentric* (off the straight midpoint — the foot lifts, the hand changes shape), never
  brainless midpoints: "in one sense there are no inbetweens — all the drawings are on the
  screen for the same amount of time" (p. 89; both pages bundled in `references/images/`).
  In Blender: check motion paths — they draw this spacing chart in 3D, one marker per
  frame (display/refresh, how to read kinks & spacing, edit-on-path smoothing: 11 B8);
  never ship default spline interpolation between keys.
- **Movement within the mass**: overlapping parts (chest vs head vs hips) get their own
  spacing; the body is never one block.
- **Ruff approach**: pose the big masses first with a few strong keys, then subdivide.
- **Take the long short cut**: do the deep breakdown work early; polish gets faster.

## 5. Timing doctrine (Whitaker/Halas)

- **Holds**: "How long to hold?" — holds are timing too. Get in and out of holds with
  spacing that breathes (settle in, lead out). A held pose still thinks (eyes, micro-drift).
- **Anticipation** (ch. + Williams): every big action is prepared. Size of anticipation
  ∝ size of action. *Surprise* anticipation (tiny, fast) for gags; *invisible* anticipation
  (part of the move itself) for realism.
- **Follow-through & overlapping action** (chapters separate!): parts continue past the stop
  and return at *different times* (stagger). Hair, cloth, flesh, props lags = 2-5 frame
  offsets typically.
- **Timing conveys weight**: heavier = slower start, more overshoot, longer settle
  ("Timing to Suggest Weight and Force" 1-4). Lift tests: how many frames to get moving?
- **Timing conveys size**: big things move slower in frame terms ("a feeling of size").
- **Force through flexible joints** (Whitaker ch.): force ripples down a chain with delay —
  the hip leads, the knee follows, the foot lands. This is the physical reason overlap exists.
- **Oscillations decay** ("Timing an Oscillating Movement"): a pendulum/settle loses amplitude
  each swing — spring math (see `07-math-procedural.md`).
- **Takes & accents** (Williams): a hard accent **bounces back** (overshoot + settle);
  a soft accent **continues** (moves through to the new pose). Choose by emotion.
- **Staggers** (Williams "Timing, Staggers, Wave and Whip"): the side-to-side vibration
  formula — successive parts offset by 1-2 frames each in a wave; use for dizziness, hits,
  flexible machinery. Whip = fast energy transfer with a follow-through snap.

## 6. Blender F-curve practice

- Block with **Stepped** interpolation → Breakdowner (hover in Dope Sheet) → then set
  keys to Bezier for polish. Never polish on default auto-clamped everywhere: shape handles
  deliberately (Vector handles for impacts, Aligned for arcs).
- Keep curves clean: no noise in the middle of a hold; dents (dents = little dips in the
  curve) only where the body "dents" (settle overshoots).
- Offset keys per channel for overlap: head after chest, chest after hips, hair/cloth last
  (2-6 frames). Stagger = successive 1-frame offsets (Williams' stagger).
- Playblast at speed, in the shot's camera, with sound for dialogue. Review with this list:
  1. Is the silhouette readable at every extreme? (staging)
  2. Do arcs exist? 3. Does the spacing avoid floaty evenness? 4. Does the weight feel right?
  5. Is there overlap/stagger? 6. Any robotic simultaneous starts? 7. Does the acting read?

## 7. Quick recipes

- **Settle** (Williams/Whitaker): overshoot 1-3%, return 1-2% past rest, decay to rest —
  2-4 swings total. Heavier → fewer, slower swings.
- **Quick head turn**: anticipation opposite 2-4 frames → fast turn on ones → small overshoot
  → settle with eye lead (eyes arrive first).
- **Stop a run**: brake spacing on the last 4-6 frames + forward lean + follow-through steps.
- **Dialogue body**: accent with the voice (Whitaker: synchronising action) — but body
  accents land 1-2 frames after the sound accent for natural lag.
