#!/usr/bin/env python3
"""Render animation-script.md from segments.json + the prose below.

The prose lives here so the schedule tables (the part that must never drift from
the data) are generated from segments.json every run:

    python3 build_doc.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "segments.json").read_text())
SEGS = DATA["segments"]
FPS = DATA["fps"]

BLOCKS = {
    "B1": ("Opening", "Bow in, line up, ready stance",
           "Sets the discipline. Silence, no music. The class exists before the student does."),
    "B2": ("Warm-up", "Pulse raiser, mobility, balance",
           "The grind. Long takes, no cuts — the audience should feel the duration."),
    "B3": ("Basics", "Stances, blocks, punches",
           "Precision. First cuts to detail inserts. Hands and hips, not spectacle."),
    "B4": ("Kicking drills", "Six basic kicks, then combinations",
           "Escalation. The camera starts moving; the student starts breathing hard."),
    "B5": ("Poomsae", "Taegeuk Il Jang, then a slow-motion breakdown",
           "The problem beat. The form exposes the flaw; the breakdown is where the work happens."),
    "B6": ("Sparring footwork", "Stance, shuffle, counters, finishing combo",
           "The payoff. The same front kick from B5, now clean and fast."),
    "B7": ("Cool-down and close", "Breathing, stretches, closing bow",
           "Release. Slow, still, quiet. Mirror of B1."),
}


def tc(sec: float) -> str:
    return f"{int(sec // 60)}:{int(sec % 60):02d}"


def block_table(block: str) -> str:
    rows = [s for s in SEGS if s["block"] == block]
    name, content, _ = BLOCKS[block]
    out = [f"### {block} — {name}  ({tc(rows[0]['start'])}–{tc(rows[-1]['start'] + rows[-1]['dur'])}, "
           f"{sum(s['dur'] for s in rows)}s)\n",
           f"*{content}*\n",
           "| ID | TC in | Dur | Beat | Prompt |",
           "|---|---|---|---|---|"]
    for s in rows:
        chain = f" `[{s['chain']}]`" if s.get("chain") else ""
        out.append(f"| `{s['id']}` | {tc(s['start'])} | {s['dur']}s | {s['beat']}{chain} | "
                   f"{s['prompt']} |")
    return "\n".join(out) + "\n"


def schedule() -> str:
    parts = []
    for b in BLOCKS:
        parts.append(block_table(b))
    parts.append(
        "`[p1]` / `[p2]` mark chained prompts: those segments are generated in **one** "
        "`kimodo_gen` call (24 s and 29 s respectively), so Kimodo conditions each "
        "prompt on the last frames of the one before it and the form stays continuous "
        "instead of cutting between unrelated takes. `generate_all.sh` does this "
        "automatically.\n")
    return "\n".join(parts)


def block_summary() -> str:
    out = ["| Block | TC | Dur | Content | Dramatic function |",
           "|---|---|---|---|---|"]
    for b, (name, content, func) in BLOCKS.items():
        rows = [s for s in SEGS if s["block"] == b]
        start = rows[0]["start"]
        end = rows[-1]["start"] + rows[-1]["dur"]
        out.append(f"| **{name}** (`{b}`) | {tc(start)}–{tc(end)} | {end - start}s | "
                   f"{content} | {func} |")
    out.append(f"| | **0:00–10:00** | **600s** | **{len(SEGS)} prompts** | |")
    return "\n".join(out)


PROSE_HEAD = f"""# Taekwondo Practice — 10-Minute Sequence

**A production animation script for [Kimodo](https://github.com/nv-tlabs/kimodo)**
(NVIDIA kinematic motion diffusion, `Kimodo-SOMA-RP-v1.2`, SOMA skeleton).

One student. One class. Ten minutes, start to finish, from the first bow to the last.

## Delivery spec

| | |
|---|---|
| **Frame rate** | **30 fps** — Kimodo's native output rate, no retiming needed on export |
| **Duration** | 10:00 = **600 seconds** |
| **Total frames** | **18,000** |
| **Segments** | {len(SEGS)} scored prompts (4–10 s each) |
| **Skeleton** | SOMA (`somaskel30` predicted → `somaskel77` for export) |
| **Export** | BVH with a standard T-pose rest pose, retargeted to the production rig |

Every timecode in this document is 30 fps. Every `kimodo_gen` call is issued with the
duration in *seconds*; Kimodo multiplies by its own `fps` of 30, so the frame counts in
the schedule are exact, not estimates.

**Contents**

0. How to use this document
1. Research — what a Taekwondo class actually is, and what Kimodo can and cannot do with it
2. Scene architecture — story spine and the seven blocks
3. Camera and staging
4. Segment schedule — all {len(SEGS)} prompts with timecodes
5. Generation plan — volume, order, constraints, seeds, what to judge
6. Assembly and polish — retiming, feet, hands, crowd, sound, cloth
7. Risks
8. Attribution and reference

---

## 0. How to use this document

This is the **whole script in one file** — nothing else is needed to read, schedule,
brief, or budget the sequence. Sections 1–2 are the research and the story, section 4
is the shot-by-shot schedule, sections 5–6 are the production plan.

The companion files in `taekwondo-practice/` are only needed if you are the one
running the generation:

| File | What it is |
|---|---|
| `segments.json` | Source of truth: {len(SEGS)} segments, timecodes, prompts, chain groups. |
| `generate_all.sh` | Drives Kimodo over the whole sequence. `--dry-run`, `--block`, `--resume`. |
| `validate.py` | Checks every prompt against Kimodo's hard limits (≤10 s, contiguity, 2-behaviour cap). |

```bash
python3 validate.py segments.json          # must print OK before you spend GPU time
./generate_all.sh --dry-run                # eyeball all {len(SEGS)} commands, run nothing
./generate_all.sh --block B4 --samples 4   # hero pass on the kicking block
./generate_all.sh                          # full pass
```

The scene is built the way a real class is built — not as one 10-minute motion
(Kimodo caps a prompt at **10 seconds**, so a 10-minute take is impossible in one
call), but as {len(SEGS)} scored segments of 4–10 s, each one a clean, directable
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

{block_summary()}

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

{schedule()}---

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
[{{"type": "root2d",
  "frame_indices": [0, 120, 240],
  "smooth_root_2d": [[0.0, 0.0], [0.45, -0.15], [0.45, 0.35]]}}]
```

**Kick contact height (B4).** A foot end-effector at the impact frame fixes the
strike's height in space, which matters when the same kick is cut against a
head-height insert:

```json
[{{"type": "right-foot",
  "frame_indices": [22],
  "root_positions": [[0.0, 0.92, 0.0]],
  "local_joints_rot": ["..."]}}]
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
"""


if __name__ == "__main__":
    out = HERE.parent / "TAEKWONDO_10MIN_SCRIPT.md"
    out.write_text(PROSE_HEAD)
    print(f"wrote {out.relative_to(HERE.parent)}  ({len(PROSE_HEAD.splitlines())} lines, "
          f"{len(PROSE_HEAD.split())} words)")
