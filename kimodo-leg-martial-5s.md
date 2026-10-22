# Kimodo — Leg-Only Martial Art Prompt (5 Seconds)

## Short answer

There's no martial art that *literally* forbids arms, but three are effectively leg-only:

| Art | Why it counts | Animation value |
|---|---|---|
| **Taekkyon** (Korea) | Historically called *gakhui* — "sport of legs." Sparring scores by kicking, sweeping and tripping. No punches, no headbutts, no boxing-style body blows. | Best fit for your ask. Low pushing kicks, sweeps, rhythmic bouncy footwork (*pumbalbgi*, "stepping on triangles"). |
| **Savate** (France) | Kicks exclusively with the **foot** — no shin, no knee. Toe, heel, sole, instep as separate striking surfaces. | The cleanest silhouette read: 4 named kicks (`fouetté`, `chassé`, `revers`, `coup de pied bas`) with distinct arcs. |
| **Taekwondo** | ~90% of scoring technique is kicking; hands mostly guard. | Most legible to a general audience. Big, fast, spinning kicks. |

Savate still allows boxing punches, Taekkyon uses hands to grab and trip, so the honest version:
**pick Taekwondo for spectacle, Savate for precision, Taekkyon for the "nothing but legs" feel.**

### Which one is famous in the US?

**Taekwondo, and it isn't close — by roughly three orders of magnitude.**

| Art | US presence |
|---|---|
| **Taekwondo** | 3–8M practitioners (estimates vary by source), ~3,500–6,000 clubs. Olympic sport since 2000, NCAA Emerging Sport for Women, USA Taekwondo ranked #1 member federation in the world in 2025. |
| **Savate** | A couple of dozen clubs clustered in ~10 states (CA, IL, NJ, VA, MD, DC, TX…). US federation founded 1994. Chicago's main Savate school advertises itself as "one of the few places in the U.S." to learn it. |
| **Taekkyon** | Effectively no storefront schools. The main organisation (Widae) is based in LA, and its own school there has closed. Finding a teacher in the US is a word-of-mouth problem. |

So for a US audience: **Taekwondo is the only one that reads instantly.** Savate and Taekkyon
motion will be interpreted as generic kicking unless you name them, and 95% of viewers won't know
the reference. Build the move on Taekwondo mechanics (the three-kick volley above) and treat Savate
or Taekkyon as flavor notes — a Savate-style heel push or Taekkyon's bouncy bent-knee stance — if
you want the motion to feel less like a sport and more like a real fight.

Kimodo's training data explicitly includes *videogame combat* and *gestures*, so plain-language kick
descriptions ("front kick", "roundhouse kick", "spinning back kick") are in-distribution. Named
styles and Korean/French technique terms are not — describe the kick, not its name.

---

## The 5-second move (Taekwondo-style three-kick volley)

This is the main prompt set. 5.0 s at 30 fps = **150 frames**.

### Option A — single prompt (fastest, slightly less reliable)

```
A person throws a fast front kick, then pivots into a high roundhouse kick, then spins into a back kick and lands in a fighting stance.
```

Three behaviors in one prompt is over Kimodo's recommended limit of two, so expect some smearing
between kicks. Fine for a blocking test, not for final.

### Option B — three-prompt timeline (recommended)

```bash
kimodo_gen "A person stands in a fighting stance and throws a fast front kick with the right leg. A person pivots on the standing foot and throws a high roundhouse kick with the left leg. A person spins around and throws a back kick, then lands back in a fighting stance." \
  --model Kimodo-SOMA-RP-v1.2 \
  --duration "1.4 1.8 1.8" \
  --num_transition_frames 4 \
  --num_samples 4 \
  --seed 12 \
  --bvh --bvh_standard_tpose \
  --output output/taekwondo_volley_5s
```

Each prompt restates the full context ("A person pivots…", not "Then the person kicks") — Kimodo
conditions each segment on the last frames of the previous one, and a context-free follow-up
generates mush.

### Option C — Savate version (foot-only, precise arcs)

```bash
kimodo_gen "A person in a fighting stance snaps a low kick with the front foot. A person steps in and drives a straight push kick with the heel. A person whips a high roundhouse kick and recovers to the stance." \
  --duration "1.4 1.8 1.8" --num_transition_frames 4 --num_samples 4 \
  --bvh --output output/savate_volley_5s
```

### Option D — Taekkyon version (low, rhythmic, no aerial kicks)

```bash
kimodo_gen "A person bounces lightly on bent knees in a rhythmic stance and pushes a low kick at the opponent's legs. A person steps in with a sweeping low kick and shifts weight back. A person trips forward with the leg and settles into a bouncy stance." \
  --duration "1.7 1.7 1.6" --num_transition_frames 4 --num_samples 4 \
  --bvh --output output/taekkyon_volley_5s
```

---

## Frame breakdown (what to fix after generation)

| Frames | Beat | Notes |
|---|---|---|
| 0–12 | Stance, weight shift, small bob | Kimodo often under-does the idle. Add a 2° hip sway. |
| 12–20 | **Chamber** — knee lifts, heel to butt | This is the anticipation *and* the power. 8 frames, slow-in. |
| 20–24 | Kick extends | 4 frames. Snappy. Hips rotate ahead of the foot. |
| 24–27 | Impact hold | 2–3 frames max. Longer reads as floaty. |
| 27–38 | Retract and plant | 8–10 frames, decelerating. |
| 38–50 | Weight transfer to the pivot foot | Check the supporting knee — it's the tell. |
| 50–62 | Chamber for kick 2 | Hips already rotating from the plant. |
| 62–66 | Roundhouse whip | 3–4 frames. Pivot on the ball of the standing foot. |
| 66–70 | Follow-through, torso counter-rotates | Overshoot past target by ~10°. |
| 70–90 | Recover to stance | Longest section — don't rush it. |
| 90–105 | Spin windup | Head leads the turn; body follows. |
| 105–112 | Back kick drives straight back | The heel travels in a straight line, not an arc. |
| 112–125 | Recoil, re-plant | |
| 125–150 | Settle into fighting stance, breath | End on a held pose, not mid-motion. |

Kimodo will not hit these frames. Use it as the blocking pass, then retime — generative output is
usually too even. Squash the extension frames, stretch the recovery frames.

---

## Constraints that actually help kicks

**Pin the kicking foot at impact.** Foot end-effectors constrain the heel position + toe, which is
exactly what you want for a strike that has to land on a specific point in space (a target, an
opponent's head height, a pad). Key `foot_right` at the impact frame:

```json
{"effector": {"foot_right": [0.0, 1.55, 0.75]}}
```

Y-up, meters, root starts at XZ = (0, 0). Author it in the demo UI — the axes are easy to get
backwards by hand.

**Root path for a travelling combo.** A volley that steps in needs the root to actually move.
Two sparse waypoints beat ten:

```json
{"path": [[0.0, 0.0], [0.35, 0.35], [0.75, 0.30]]}
```

**Keep post-processing ON** (don't pass `--no-postprocess`). It cleans foot skate, and foot skate is
murder on pivots — a supporting foot sliding during a roundhouse destroys the whole read.

**Foot-contact constraints are not exposed** in the Python API or demo UI yet (trained, just not
wired up), so don't plan a workflow around them.

**CFG:** if the kicks are weak or dragged, raise the text weight rather than the constraint weight:

```bash
--cfg_type separated --cfg_weight 2.5 1.5
```

---

## Two things to expect

1. **Hands will do weird stuff.** With no arm behavior specified, Kimodo often leaves hands awkward
   or half-guarding. Fix the guard in the graph editor — or add a hand end-effector to pin the
   guard up. Cheaper than fighting the prompt.
2. **Kicks are 50% hips.** If you retarget onto a rig and the hips look flat, no amount of leg
   polish saves it. Check pelvic rotation first: for a roundhouse the hips must turn ~45–60° through
   the strike, and the chest counter-rotates against them.

## Notes on the model, for reference

`--num_samples 4` because text prompts are a lottery on fast beats; pick the best, don't reword.
Max 10 s per prompt, so 5 s is comfortable — half the reason this reads clean is that there's room
to extend and recover. Keep each prompt to 1–2 behaviors (`"A person…"` opener). Export BVH for
retargeting; add `--bvh_standard_tpose` for SOMA → Maya/Blender.
