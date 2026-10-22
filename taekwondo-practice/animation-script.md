# Taekwondo Practice — 10-Minute Sequence

**A production animation script for [Kimodo](https://github.com/nv-tlabs/kimodo)**
(NVIDIA kinematic motion diffusion, `Kimodo-SOMA-RP-v1.2`, SOMA skeleton).

One student. One class. Ten minutes, start to finish, from the first bow to the last.

---

## 0. What's in this folder

| File | What it is |
|---|---|
| `animation-script.md` | This document — the script you read. |
| `segments.json` | Source of truth: 66 segments, timecodes, prompts, chain groups. |
| `generate_all.sh` | Drives Kimodo over the whole sequence. `--dry-run`, `--block`, `--resume`. |
| `validate.py` | Checks every prompt against Kimodo's hard limits (≤10 s, contiguity, 2-behaviour cap). |

```bash
python3 validate.py segments.json          # must print OK before you spend GPU time
./generate_all.sh --dry-run                # eyeball all 66 commands, run nothing
./generate_all.sh --block B4 --samples 4   # hero pass on the kicking block
./generate_all.sh                          # full pass
```

The scene is built the way a real class is built — not as one 10-minute motion
(Kimodo caps a prompt at **10 seconds**, so a 10-minute take is impossible in one
call), but as 66 scored segments of 4–10 s, each one a clean, directable
unit that survives being re-generated, replaced or retimed independently.

---

## 1. Research: what a Taekwondo class actually is

### 1.1 The shape of a class

Published class structures converge on the same spine: opening etiquette →
warm-up (8–15 min) → fundamentals (10–20) → kicking drills → poomsae (10–20) →
partner work or sparring (10–20) → conditioning → cool-down → closing bow.
Classes run 45–90 minutes; a 10-minute scene is therefore a **compressed class**
— one representative beat from each section, not a real 60-minute session.

What makes it read as authentic is not completeness, it's **ritual**: the bow at
both ends, the ready stance, the group moving to a count, the sudden silence
before a form.

### 1.2 The curriculum behind block B5

Kukkiwon colour-belt forms are the eight **Taegeuk** poomsae; black-belt forms are
the **yudanja** series (Koryo → Keumgang → Taebaek → Pyongwon → Sipjin → Jitae …).
Our scene uses **Taegeuk Il Jang** — the 8th-geup form, and therefore the one a
beginner in this class would actually be drilling.

Taegeuk Il Jang: **18 movements (20 techniques)**, walked on a **T-shaped floor
pattern**, built entirely from walking stance and front stance, low block, inside
middle block, high block, middle punch, and front kick — ending on a **kihap**.
That limited vocabulary is exactly why it's the right choice: every one of those
techniques is plausible for a motion model, and none of them require a partner,
a pad, or a prop.

### 1.3 The language (use it in notes, not in prompts)

Kimodo does not understand Korean technique names — it was trained on English
natural-language descriptions of mocap. Keep Korean for your shot notes and use
plain English in the prompt.

| Korean | English | In the script |
|---|---|---|
| charyeot / kyeong-nye | attention / bow | B1-S02, B7-S66 |
| junbi seogi | ready stance | B1-S03, B3-S15 |
| gunnun seogi / ap kubi / dwi kubi | walking / front / back stance | B3-S16, S21, S22 |
| juchum seogi | horse riding stance | B3-S23 |
| arae makki / momtong makki / olgul makki | low / middle / high block | B3-S16, S19, S18 |
| momtong jireugi | middle punch | B3-S17, B3-S21 |
| sonnal mok chigi | knife-hand neck strike | B3-S20 (see §1.4) |
| ap / dollyo / yeop / dwi / naeryeo / huryeo chagi | front / roundhouse / side / back / axe / hook kick | B4 |
| poomsae / kyorugi | form / sparring | B5 / B6 |
| kihap | spirit shout | B3-S24 (body only — sound is post) |
| hana, dul, set, net, daseot, yeoseot, ilgop, yeodeol | one → eight | count-in for every drill |

### 1.4 What Kimodo can and cannot do here — read this before generating

This is the difference between a script that survives production and one that
wastes a week of GPU time.

**It cannot animate hands.** Kimodo predicts on `somaskel30`, which removes finger
detail. Every hand in the sequence is effectively a fist or a neutral hand.
*Consequence:* knife-hand strikes (B3-S20), palm-heel blocks and open-hand
poomsae shapes are **blocking only** — key the hand shape in the graph editor over
the generated motion. Budget roughly six keys per hand pose.

**It cannot perform a form.** Kimodo's training data covers locomotion, gestures,
everyday actions, videogame combat and dance — not Kukkiwon poomsae. It will
produce a plausible "step, block, punch", and it will not produce the correct
18-movement sequence, the correct T-pattern, or the correct chamber. *Consequence:*
B5 is a **blocking pass for a human animator**, not a final. Expect to correct
four out of five poomsae segments against reference footage. The floor pattern is
the part Kimodo gets most wrong, so pin it with `root2d` waypoints (§5.3).

**It cannot generate props, partners or cameras.** No pad, no opponent, no
instructor, no cloth. *Consequence:* the instructor, the pad holder and the
sparring partner are separate characters generated separately (or replaced with
3D assets), and the kihap is sound design.

**One character per generation.** *Consequence:* the class is a **crowd made in
post** — three variants of each group drill, offset in time and space (§6.4).

**10 seconds per prompt, max.** *Consequence:* the segmentation in this document.

What it *is* genuinely good at here: kick mechanics (chamber → extension →
retraction → plant), stance transitions, breathing, weight shifts, and the
emotional read of a body under fatigue. That is most of the scene.

---

## 2. Scene architecture

### 2.1 Story spine

A drill list is not a scene. The spine: **a student preparing for a grading test.**
The ten minutes are one class, and the class has an arc.

- **0:00–2:05 — discipline.** Ritual and warm-up. Nothing is at stake yet.
- **2:05–4:00 — precision.** Basics. The body is being corrected.
- **4:00–6:10 — escalation.** Kicks get higher and harder; fatigue enters.
- **6:10–8:00 — the problem.** The form exposes the flaw: the front kick-and-punch
  beat is late on the punch, because the foot lands heavy. The slow-motion
  breakdown (B5-S50–53) is the student working the flaw.
- **8:00–9:15 — the payoff.** Sparring. The same front kick, now fast and
  balanced, and the finishing combo lands.
- **9:15–10:00 — release.** Cool-down, breathing, bow. Mirrors the opening.

Cast the performance into the prompts where it matters: `A tired person…` in
B2-S13 and B7-S62, `A focused person…` in B4-S27 and B5, `A determined person…`
at the axe kick. Kimodo responds to subject stylisation, and it keeps the body
from reading as a default mannequin at exactly the moments the audience is
watching.

### 2.2 Blocks

| Block | TC | Dur | Content | Dramatic function |
|---|---|---|---|---|
| **Opening** (`B1`) | 0:00–0:25 | 25s | Bow in, line up, ready stance | Sets the discipline. Silence, no music. The class exists before the student does. |
| **Warm-up** (`B2`) | 0:25–2:05 | 100s | Pulse raiser, mobility, balance | The grind. Long takes, no cuts — the audience should feel the duration. |
| **Basics** (`B3`) | 2:05–4:00 | 115s | Stances, blocks, punches | Precision. First cuts to detail inserts. Hands and hips, not spectacle. |
| **Kicking drills** (`B4`) | 4:00–6:10 | 130s | Six basic kicks, then combinations | Escalation. The camera starts moving; the student starts breathing hard. |
| **Poomsae** (`B5`) | 6:10–8:00 | 110s | Taegeuk Il Jang, then a slow-motion breakdown | The problem beat. The form exposes the flaw; the breakdown is where the work happens. |
| **Sparring footwork** (`B6`) | 8:00–9:15 | 75s | Stance, shuffle, counters, finishing combo | The payoff. The same front kick from B5, now clean and fast. |
| **Cool-down and close** (`B7`) | 9:15–10:00 | 45s | Breathing, stretches, closing bow | Release. Slow, still, quiet. Mirror of B1. |
| | **0:00–10:00** | **600s** | **66 prompts** | |

---

## 3. Camera and staging

Kimodo outputs **world-space character motion and nothing else** — no camera, no
lens, no cut. The camera plan is authored after retargeting; writing it here keeps
the generated motion complicit with the edit (turn directions, screen left/right,
where a kick ends up in frame).

**Set.** 12 × 12 m mat, mirror wall on the front (camera-side) wall, back wall
plain. Camera axis on the mat diagonal so turns read as turns, not as spins in
place. The student works on the centre line; the crowd is staggered behind.

**Coverage per block**

| Block | Master | Coverage | Insert | Notes |
|---|---|---|---|---|
| B1 | Wide, static, long lens | — | Close on the bow | Hold the wide for the whole block; the silence is the point. |
| B2 | Wide, static | Slow dolly-in across the whole warm-up | Low-angle feet, 2 shots | Cut *on* the count, not between counts. Let the takes breathe. |
| B3 | Medium wide | 3/4 front, waist-up | Hands at chest height, shallow DOF | First real cutting. Match-cut block → punch on the beat. |
| B4 | Medium, drifting | Low-angle 3/4 for kicks (hero angle) | Foot-on-impact, 60 fps for slow-mo | Camera drops low and *stays* low — kicks read against the ceiling line. |
| B5 | **One unbroken wide** | — | Overhead (T-pattern), slow-mo insert | Poomsae is traditionally shown uncut. Do not cut the run. |
| B6 | Handheld, loose | 3/4 with breathing camera | Feet, 50 fps | Handheld = stakes. Slightly wider lens than B4. |
| B7 | Wide, static | — | Close on the final bow | Return to the exact B1 framing. Same lens, same height. |

**Cut rhythm.** Every drill in B2–B4 is on an **8-count** (hana → yeodeol). Cuts
land on odd counts, never on the 8 — the 8 is the reset, and cutting on it clips
the recovery that makes the rhythm legible. In B5 there are no cuts. In B6, cut on
impact, not on the chamber.

**Frame rate.** Generate everything at Kimodo's native 30 fps. Shoot the inserts
in the *edit* at 60 fps by retiming the generated clip (optical-flow retime, not
frame blending) — the axe kick and the spinning back kick both want a 40% speed
insert.

---

## 4. Segment schedule

### B1 — Opening  (0:00–0:25, 25s)

*Bow in, line up, ready stance*

| ID | TC in | Dur | Beat | Prompt |
|---|---|---|---|---|
| `B1-S01` | 0:00 | 8s | Enter and line up | A person walks onto a mat and stops, then stands at attention with feet together and arms at their sides. |
| `B1-S02` | 0:08 | 8s | Bow (kyeong-nye) | A person stands at attention and bows at the waist toward the front, then straightens up. |
| `B1-S03` | 0:16 | 9s | Ready stance (junbi seogi) | A person stands with feet shoulder width apart and both fists held at waist height in front of the body, holding still. |

### B2 — Warm-up  (0:25–2:05, 100s)

*Pulse raiser, mobility, balance*

| ID | TC in | Dur | Beat | Prompt |
|---|---|---|---|---|
| `B2-S04` | 0:25 | 10s | Jog in place | A person jogs in place with light bouncy steps and relaxed shoulders. |
| `B2-S05` | 0:35 | 9s | High knees | A person runs in place lifting each knee high toward the chest. |
| `B2-S06` | 0:44 | 9s | Heel kicks | A person jogs in place kicking their heels up behind them toward their glutes. |
| `B2-S07` | 0:53 | 10s | Jumping jacks | A person performs jumping jacks, opening and closing the arms and legs in rhythm. |
| `B2-S08` | 1:03 | 9s | Arm circles | A person stands with arms extended to the sides and circles them in large slow loops. |
| `B2-S09` | 1:12 | 10s | Hip circles and torso twist | A person stands with hands on their hips, circles the hips, then twists the torso side to side. |
| `B2-S10` | 1:22 | 9s | Front leg swings | A person balances on one leg and swings the other leg forward and back in a straight line. |
| `B2-S11` | 1:31 | 10s | Side leg swings | A person balances on one leg and swings the other leg across the body from side to side. |
| `B2-S12` | 1:41 | 9s | Knee lift balance | A person lifts one knee to waist height and holds it with arms out for balance, then lowers it. |
| `B2-S13` | 1:50 | 10s | Walking lunges | A tired person performs slow forward lunges, lowering the hips and rising back to standing. |
| `B2-S14` | 2:00 | 5s | Walk back to the line | A person takes two small steps backward and settles into a standing ready position. |

### B3 — Basics  (2:05–4:00, 115s)

*Stances, blocks, punches*

| ID | TC in | Dur | Beat | Prompt |
|---|---|---|---|---|
| `B3-S15` | 2:05 | 9s | Chamber both fists | A person in a ready stance slowly draws both fists back to the hips and holds them there. |
| `B3-S16` | 2:14 | 10s | Low block, both sides | A person steps forward into a long stance and swings one forearm down in a low block, then repeats with the other arm. |
| `B3-S17` | 2:24 | 10s | Middle punches x3 | A person in a long stance throws three straight punches at chest height, twisting the hips each time. |
| `B3-S18` | 2:34 | 10s | High block | A person steps forward and raises one forearm overhead in a high block, then brings it down. |
| `B3-S19` | 2:44 | 10s | Inside middle block | A person steps forward and swings one forearm inward across the chest in a middle block. |
| `B3-S20` | 2:54 | 9s | Knife-hand strike | A person in a back stance extends one open hand outward at neck height in a slow controlled strike. |
| `B3-S21` | 3:03 | 10s | Front stance punch | A person steps forward into a deep forward stance and throws one straight punch. |
| `B3-S22` | 3:13 | 10s | Back stance shift | A person shifts most of their weight onto the rear leg into a back stance, then returns forward. |
| `B3-S23` | 3:23 | 10s | Horse stance punch | A person stands with feet wide and knees deeply bent and throws one punch forward while pulling the other fist back. |
| `B3-S24` | 3:33 | 9s | Kihap / focus punch | A person in a forward stance snaps one punch forward and tenses the whole body for a moment. |
| `B3-S25` | 3:42 | 10s | Pivot 90 and block | A person pivots 90 degrees on the ball of the foot into a walking stance and performs a low block in the new direction. |
| `B3-S26` | 3:52 | 8s | Reset to ready | A person steps back into a ready stance and stands still. |

### B4 — Kicking drills  (4:00–6:10, 130s)

*Six basic kicks, then combinations*

| ID | TC in | Dur | Beat | Prompt |
|---|---|---|---|---|
| `B4-S27` | 4:00 | 10s | Chamber hold | A focused person balances on one leg and raises the other knee to waist height, holding the chamber steady. |
| `B4-S28` | 4:10 | 10s | Slow front kick | A person slowly extends one leg forward in a front kick and pulls it back to the chamber. |
| `B4-S29` | 4:20 | 10s | Fast front kick x2 | A person snaps two fast front kicks with the right leg, returning to the chamber between them. |
| `B4-S30` | 4:30 | 10s | Roundhouse right | A person pivots on the standing foot and snaps a roundhouse kick at waist height with the right leg. |
| `B4-S31` | 4:40 | 10s | Roundhouse left | A person pivots and snaps a roundhouse kick at chest height with the left leg. |
| `B4-S32` | 4:50 | 10s | Side kick | A person raises the knee across the body and drives a side kick straight out, striking with the heel. |
| `B4-S33` | 5:00 | 10s | Back kick | A person turns their back to the front and drives a straight back kick behind them while looking over the shoulder. |
| `B4-S34` | 5:10 | 9s | Axe kick | A determined person raises one leg high in front of the body and chops it down with the heel. |
| `B4-S35` | 5:19 | 10s | Hook kick | A person swings one leg out to the side and hooks it back across the front of the body. |
| `B4-S36` | 5:29 | 9s | Pad roundhouse | A person steps in and throws a fast roundhouse kick at chest height, then resets their stance. |
| `B4-S37` | 5:38 | 10s | Front kick into roundhouse | A person throws a front kick with one leg, plants it, then pivots into a roundhouse kick with the other leg. |
| `B4-S38` | 5:48 | 10s | Double roundhouse | A person throws two roundhouse kicks in a row, switching legs without putting the first foot down. |
| `B4-S39` | 5:58 | 6s | Spinning back kick | A person spins around and throws a back kick, then lands facing the front. |
| `B4-S40` | 6:04 | 6s | Recover to stance | A person settles into a fighting stance and bounces lightly on the balls of their feet. |

### B5 — Poomsae  (6:10–8:00, 110s)

*Taegeuk Il Jang, then a slow-motion breakdown*

| ID | TC in | Dur | Beat | Prompt |
|---|---|---|---|---|
| `B5-S41` | 6:10 | 8s | Line 1: turn left, low block `[p1]` | A focused person stands in a ready stance, then pivots 90 degrees to the left into a walking stance and performs a low block. |
| `B5-S42` | 6:18 | 8s | Line 1: step and punch `[p1]` | A person steps forward in a walking stance and throws a straight middle punch, then draws the other fist back. |
| `B5-S43` | 6:26 | 8s | Line 1: 180 turn, low block, punch `[p1]` | A person pivots 180 degrees into a walking stance, performs a low block, then steps forward and punches. |
| `B5-S44` | 6:34 | 9s | Line 2: front stance, block, punch | A person in a deep forward stance performs a low block and then a straight punch without moving the feet. |
| `B5-S45` | 6:43 | 9s | Line 2: inside blocks | A person turns into a walking stance swinging one forearm inward in a middle block, then steps forward and punches. |
| `B5-S46` | 6:52 | 9s | Line 3: high block | A person turns 90 degrees into a walking stance and raises one forearm overhead in a high block. |
| `B5-S47` | 7:01 | 10s | Line 3: front kick, land, punch `[p2]` | A person performs a front kick, sets the foot down in front, and throws a straight punch in a walking stance. |
| `B5-S48` | 7:11 | 9s | Line 3: mirror kick `[p2]` | A person turns 180 degrees and performs a front kick with the other leg, landing forward and punching. |
| `B5-S49` | 7:20 | 10s | Line 4: closing low block and punch `[p2]` | A person turns into a forward stance, performs a low block, then steps forward and punches sharply. |
| `B5-S50` | 7:30 | 8s | Breakdown: slow chamber | A focused person slowly raises one knee into a chamber and holds the leg folded, balanced on the standing leg. |
| `B5-S51` | 7:38 | 9s | Breakdown: slow extension | A person slowly extends the folded leg forward at half speed and holds it straight in the air. |
| `B5-S52` | 7:47 | 9s | Breakdown: slow retract and set down | A person slowly pulls the extended leg back and sets the foot down in front into a deep forward stance. |
| `B5-S53` | 7:56 | 4s | Hold: punch at extension | A person holds a straight punch at full extension without moving. |

### B6 — Sparring footwork  (8:00–9:15, 75s)

*Stance, shuffle, counters, finishing combo*

| ID | TC in | Dur | Beat | Prompt |
|---|---|---|---|---|
| `B6-S54` | 8:00 | 9s | Fighting stance bounce | A person bounces lightly on the balls of their feet in a fighting stance with both fists up near the face. |
| `B6-S55` | 8:09 | 9s | Shuffle forward and back | A person shuffles forward and back in a fighting stance without crossing their feet. |
| `B6-S56` | 8:18 | 9s | Switch step | A person switches their feet quickly while bouncing in a fighting stance. |
| `B6-S57` | 8:27 | 10s | Step-in high roundhouse | A person steps in with a small bounce and throws a fast roundhouse kick at head height. |
| `B6-S58` | 8:37 | 9s | Counter back kick | A person spins and throws a back kick as a counter attack, then returns to the fighting stance. |
| `B6-S59` | 8:46 | 9s | Front kick into roundhouse combo | A person throws a front kick and immediately follows with a roundhouse kick from the other leg, staying light on the feet. |
| `B6-S60` | 8:55 | 10s | Lean-back evasion | A person shifts their weight back and leans the upper body away from a high kick, then returns upright. |
| `B6-S61` | 9:05 | 10s | Finishing combo | A person throws a spinning back kick, lands facing forward, and drops into a stable fighting stance. |

### B7 — Cool-down and close  (9:15–10:00, 45s)

*Breathing, stretches, closing bow*

| ID | TC in | Dur | Beat | Prompt |
|---|---|---|---|---|
| `B7-S62` | 9:15 | 9s | Stand and breathe | A tired person stands with feet apart and hands on their hips, breathing deeply with the chest rising and falling. |
| `B7-S63` | 9:24 | 10s | Forward fold stretch | A person bends forward at the waist with straight legs and reaches toward their feet. |
| `B7-S64` | 9:34 | 9s | Seated butterfly stretch | A person sits on the floor with the soles of their feet together and presses the knees down toward the ground. |
| `B7-S65` | 9:43 | 8s | Stand and straighten dobok | A person stands up from the floor and smooths down the front of their uniform. |
| `B7-S66` | 9:51 | 9s | Closing bow | A person stands at attention and bows, then holds the position facing forward. |

`[p1]` / `[p2]` mark chained prompts: those segments are generated in **one** `kimodo_gen` call (24 s and 29 s respectively), so Kimodo conditions each prompt on the last frames of the one before it and the form stays continuous instead of cutting between unrelated takes. `generate_all.sh` does this automatically.
---

## 5. Generation plan

### 5.1 Volume and cost

| | |
|---|---|
| Generation calls | 66 segments → **62 calls** (2 chained groups fuse 3 prompts each) |
| Draft pass | 2 samples/call = **124 generations** |
| Hero pass | 4 samples on ~18 beats (B3–B6 highlights) = **+72** |
| Total | **196 generations** for a 10-minute final |
| Output | 18,000 frames @ 30 fps (10:00) |

Kimodo needs ~17 GB VRAM with the text encoder on GPU; set
`TEXT_ENCODER_DEVICE=cpu` to drop under 3 GB at the cost of speed. Run the draft
pass overnight per block and **never re-run a block you haven't reviewed** — at
this volume, selection is the bottleneck, not generation.

### 5.2 Order of work

1. `python3 validate.py segments.json` — must print `OK`.
2. Draft pass, **one block at a time** (`--block B2`), 2 samples, `--resume`.
3. Assembly review: drop every clip into a sequence at its timecode (use
   `output/manifest.csv`) and watch the whole ten minutes as a black-and-white
   blocking pass. You are judging **timing and staging only** — ignore hands.
4. Hero pass on the beats that survive: `--block B4 --samples 4`.
5. Retarget to the production rig, then the correction passes in §6.

### 5.3 Constraints that earn their keep

Most segments need none — text is enough and constraints fight the prompt when
they disagree. Three exceptions:

**Poomsae floor pattern (B5).** This is where generation fails most visibly, so
pin the T. Three sparse waypoints per line, Y-up, metres, root starting at
`(0, 0)`, and `first_heading_angle` set to the form's start direction:

```json
[{"type": "root2d",
  "frame_indices": [0, 120, 240],
  "smooth_root_2d": [[0.0, 0.0], [0.45, -0.15], [0.45, 0.35]]}]
```

**Kick contact height (B4).** A foot end-effector at the impact frame fixes the
strike's height in space, which matters when the same kick is cut against a
head-height insert:

```json
[{"type": "right-foot",
  "frame_indices": [22],
  "root_positions": [[0.0, 0.92, 0.0]],
  "local_joints_rot": ["..."]}]
```

Author it in the demo UI and export — hand-writing the joint rotations is a trap.

**Sparring root motion (B6).** Shuffle and step-in beats need real translation or
they read as kicking in place. Two waypoints, not ten.

### 5.4 Seed policy

`generate_all.sh` assigns `seed = 1000 + call index`, deterministic per segment,
so a re-run reproduces a take you liked. Log the winner of every selection round
in `selects.csv` (`segment,seed,note`) — six weeks later that file is the only
thing that tells you why shot B4-S32 looks right and its neighbour doesn't.

### 5.5 What to judge, in order

1. **Timing** — does the kick read at the right frame count? (Retime later; a bad
   *rhythm* is un-fixable.)
2. **Root logic** — does the turn go the right way, on the right foot?
3. **Contact** — is the foot planted, or skating?
4. **Line** — is the silhouette clean at the camera angle?

Hands, expression and cloth come last, because they're all fixed in post.

---

## 6. Assembly and polish

### 6.1 Retiming

Kimodo's output is temporally too even — every phase gets roughly equal frames.
Real kicks are **fast out, slow settle**:

- chamber: 8–10 frames (this is the anticipation; don't clip it)
- extension: **3–4 frames**
- impact hold: **2–3 frames**, never more
- retraction + plant: 8–10 frames

Squash the extension, stretch the recovery. Do this before any polish work; every
correction downstream is wasted on a badly timed clip.

### 6.2 Feet and contact

Leave post-processing **on** (don't pass `--no-postprocess`). It cleans foot skate,
and skate during a pivot destroys a roundhouse. After retarget, check the
supporting foot on every kick: if it rotates with the hips instead of pivoting on
the ball, fix it manually — it's the single most common tell of generated motion.

### 6.3 Hands

One pass, in this order: fist shape (§ B3, B4, B6), knife-hand (B3-S20), open-hand
poomsae shapes (B5). See the fist-keying breakdown in `../kimodo-fist-prompt.md`
for the stagger rule — fingers curl one frame apart, thumb last.

### 6.4 Making a class out of one character

Kimodo generates one person at a time. For a dojang of 8–12 students:

- generate **3 variants** of each group drill (different seeds — `--seed` 3 values)
- offset each variant **0.15–0.40 s** in time so the room is never in lockstep
  (a perfectly synchronised crowd reads as CG immediately)
- space rows **1.8–2.2 m** apart, stagger laterally by half a body width
- mirror one variant (scale X = −1) for the far side of the mat
- the hero student uses the corrected, hand-keyed take; the crowd uses the raw
  generated takes, because nobody is looking at them

For 10 minutes of class, 3 variants × 64 calls is not affordable — so **generate
the crowd once per block**, not once per segment, and reuse with the time offsets
above. The eye forgives repetition it can't synchronise.

### 6.5 Kihap and voice

The kihap (B3-S24) is body only: a snap, a full-body tension, one frame of held
stillness. The shout is sound design. Same for the count — the instructor's
`hana, dul, set` is a voice track that the cuts are built on. **Lay the count
first, then cut to it**; retrofitting a count to a finished edit never lands.

### 6.6 Cloth

No simulation, no dobok. Kimodo gives you a body in a neutral suit. The uniform is
a 3D asset skinned and simulated over the retargeted motion — and it's what sells
"taekwondo" at a glance more than any individual kick. Budget for it early.

---

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Poomsae sequence is wrong beyond fixing | High | Treat B5 as blocking; correct against reference footage; keep the one-take wide and hide the least-correct beats behind inserts |
| Hands read as claws | Certain | Hand-keying pass; if the rig has no fingers, use a fist-shape mesh swap |
| Foot skate on pivots | High | Post-processing on; manual pivot check per kick (§6.2) |
| Crowd looks cloned | High | 3 variants, time offsets, mirrored copies (§6.4) |
| Kicks not high enough | Medium | Text CFG up (`--cfg_type separated --cfg_weight 2.5 1.5`); foot EE constraint at target height |
| 10 minutes of same-angle motion | Certain | The camera plan in §3 is not optional — it's what makes 10 minutes watchable |
| GPU time blows up | Medium | Block-by-block draft pass, `--resume`, 2 samples until it earns 4 |

---

## 8. Attribution and reference

Motion generation: [NVIDIA Kimodo](https://github.com/nv-tlabs/kimodo) — text-to-motion diffusion,
`Kimodo-SOMA-RP-v1.2`, SOMA skeleton, 30 fps, NVIDIA Open Model License (commercial use permitted).
Prompting guidance from Kimodo's *Best Practices* page (`docs/key_concepts/limitations.md` in the repo).

Taekwondo reference: Kukkiwon poomsae curriculum (Taegeuk 1–8, yudanja series);
Taegeuk Il Jang movement breakdown (18 movements, T-pattern, kihap close);
Kukkiwon kick nomenclature (ap / dollyo / yeop / dwi / naeryeo / huryeo chagi);
typical class structure from published dojang guides (45–90 min, 8–15 min warm-up,
10–20 min fundamentals, 10–20 min poomsae, 10–20 min partner work).
