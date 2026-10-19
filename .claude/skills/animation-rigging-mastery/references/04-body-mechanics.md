# Body Mechanics — Williams' Walks/Runs/Weight + Whitaker's Locomotion

Source: Williams (*Walks; Runs, Jumps and Skips; Flexibility; Weight*) and Whitaker
(*Timing a Walk; Animals*). Use this for cycles, locomotion, and weight in Blender.

## 1. The Walk (Williams: "Walks" + "The Recipe")

A walk is **weight repeatedly caught and thrown**. Build it in this order:

1. **Getting the weight** — before detail: the body's mass must feel heavy. Hips carry the
   weight; the leg catches it. If the walk floats, no detail will save it.
2. **Set the tempo** — decide strides-per-second first. Frames per step at 24fps:
   normal walk ≈ 12 frames per step (24 per full cycle, left+right) = 8 steps/sec? NO —
   12 frames/step ≈ 2 steps/sec, 1 step per ~0.5s (typical comfortable walk). Heavy/slow
   walks 14-16 frames/step; brisk 8-10.
3. **Contact positions** — both extreme contacts (right foot forward / left foot forward).
   The classic contact: feet straddle, legs in an upside-down V, hips already shifting.
4. **The passing position (breakdown)** — the inbetween at mid-step: standing leg straight,
   free leg passing, body at its HIGHEST point. Williams: this is the critical breakdown;
   get it wrong and the walk is wrong.
5. **Two ways to plan a walk**: (a) plan the up/down and spacing chart first, draw after;
   (b) draw the poses first, chart the spacing after. Either way — plan it.
6. **The double bounce** — hips drop TWICE per cycle (once per step): the body sinks under
   weight at mid-stance and rises at passing. Belt line dips; shoulder line counter-tilts.
7. **Weight shift** — hips sway toward the standing leg; the belt line tilts down toward the
   swing leg. The torso counter-rotates (shoulders opposite hips).
8. **Arm movements** — arms swing opposite to the legs, but LAZY: they drag, arrive late
   (overlap), and never lock. Elbows slightly bent, hands relaxed.
9. **Counteraction** — everything opposite: shoulder vs hip, arm vs leg, head stays level.
10. **The heel & foot action** — heel strikes, foot rolls flat, ankle pushes (toe-off),
    the foot then swings through with a lazy fold (no stiff ankles).
11. **Spacing** ("Normal Walk Spacing"): tight at contacts/impact, spread at the passing
    point of the swing foot (fast swing, slow stance). NEVER even.
12. **The Recipe (Williams)** — the checklist he repeats: contact poses → passing
    breakdowns → hip drop/double bounce → weight shift/belt line → arms + counteraction →
    heel/foot action → spacing chart → test → loosen up.

- **Loosening it up**: after it's correct, break the symmetry: one arm different, head
  attitude, an offset — "there's nothing like trying it" (act it out yourself).
- **Sneaks**: low center of gravity, bent knees, feet staying close to ground, careful
  spacing (slow, even-ish with tiny holds), shoulders leading, head stable. The tip-toe
  sneak: extreme bent-knee with weight high on the ball of the foot.

## 2. Runs, Jumps, Skips (Williams)

- **Run = controlled fall**: lean forward, the contact foot lands AHEAD of the mass and
  catches the fall; flight phase exists (both feet off ground).
- **The 4-drawing formula run**: 4 drawings on twos per cycle (classic Hollywood sprint) —
  contact, down/impact, passing/launch, up/flight. The 3-drawing and 2-drawing runs are
  faster formulas (for dashes and blur-fast gags). The Recipe: contacts → downs/up →
  passing → spacing (very tight at contact, spread in flight).
- **Jumps**: crouch (anticipation) → launch (fast, tight spacing) → flight (arcs, limbs
  trail) → landing impact (tight spacing, deep compression) → settle. "Weight on a jump":
  the landing carries the weight — compress proportionally to height.
- **Skips**: a walk with an extra beat — step-hop rhythm, strong up-beat, joy in the spacing.

## 3. Flexibility (Williams)

- **The breakdown**: the pose that defines the *path*, not just the middle — bend into it.
- **Simple overlap**: successive masses offset (hips → chest → head → arms).
- **Simple counteraction**: when one end goes up, the other goes down (hips vs shoulders).
- **Breaking joints**: bend the "hinge" the wrong way slightly for cartoon flexibility;
  in 3D: overshoot the elbow/knee 2-5° or use squash scale instead of cheating the mesh.
- **Face flexibility**: brows/cheeks/lips overlap the mouth action; profiles for
  "instant read" — a silhouette that reads the idea instantly.

## 4. Weight (Williams + Whitaker)

- Pressure and weight: every contact presses into the ground — feet flatten, knees absorb.
- **How much effort?** — decide per action: carrying a heavy box changes EVERY timing
  (slower starts, more muscle anticipation, longer settles).
- **Synchronising action rules of thumb**: big masses lead, extremities follow; accents
  land together on the beat; hits compress first, rebound second.
- Whitaker's law: **timing suggests weight** — heavier objects need more frames to start
  and stop; force = mass × acceleration (fast heavy = the most frames of force feeling).

## 5. Animals (Whitaker + Williams "Animal Action")

- Quadruped walk: **lateral sequence** (LH, LF, RH, RF order), four beats, head-bob at
  contacts; gallop: rotary sequence with a full flight phase; the horse's gallop has a
  rocking rise/fall of the spine.
- **Basic animal walk pattern** (Williams): study the footfall chart first, then the spine
  wave, then the head/neck counteraction. Always use **live-action reference**.
- Bird flight: figure-8 wing path (downstroke = power, upstroke = recovery with fold),
  body tilts with thrust; gliding = stillness with micro-adjustments.

## 6. Blender construction notes

- Cycles: animate in place with root motion as a separate channel (easy to retime); or on
  a treadmill root with the ground moving. Stride length: stride = 2 × step length;
  ground speed = stride × cycles/sec. Match these or the feet slide!
- Use the Dope Sheet to enforce the recipe order; X-Axis Mirror + copy-paste flipped poses
  for symmetric cycles, then break symmetry (loosen up!).
- Layer with NLA: base cycle action + additive layers for head/arms attitude.
- Check arcs: hip path = smooth sine; foot path = classic "loop with a flick".
  Motion Paths tool shows this instantly.
- Root/COG: the hips do the double bounce and the weight shift — animate root translate
  + rotate first, limbs after.
