---
name: animation-rigging-mastery
description: Persistent project memory distilled from the 8 animation and rigging books in this repo (Cabrera - Maya Character Rigging applied in Blender; Richard Williams - The Animator's Survival Kit; Whitaker & Halas - Timing for Animation; Thomas & Johnston - The Illusion of Life; Osipa - Stop Staring; Ed Hooks - Acting for Animators; Dunn & Parberry - 3D Math Primer; Rick Parent - Computer Animation Algorithms and Techniques). Use at the START OF EVERY session in this project whenever the task involves character rigging, armatures or bones, skinning or weights, IK/FK, control rigs, facial rigs, shape keys, lip sync, animation timing or spacing, walk/run cycles, body mechanics, acting or performance, shot polish, or any Blender character pipeline work. Also use whenever the user asks animation or rigging questions, reviews shots, or builds rigs, animation tools, or pipelines in this project.
---

# Animation & Rigging Mastery — Project Memory

## Standing orders (every session)

1. This skill IS the project's long-term memory of the book library in this repo. Treat it as
   required reading before doing animation or rigging work in this project.
2. The Maya rigging book (Cabrera) is the rigging curriculum — but **apply its logic in Blender**.
   Every Maya technique has a Blender equivalent; see `references/02-rigging-blender.md`.
3. When working, cite the *reason* behind a technique (the books teach essence + reason, not
   recipes). If a shot or rig decision can be justified from the books, justify it that way.
4. The source PDFs live in the repo root. The combined OCR'd PDF
   (`Animation+rigging of maya ocred.pdf`, GitHub release tag `merged-ocr`) contains them in
   this order: Maya Rigging (pp. 1-408), Stop Staring (409-795), 3D Math Primer (796-1641),
   Rick Parent (1642-2182), Acting for Animators (2183-2327, NOT OCR'd - image only),
   Illusion of Life (2328-2875), Timing for Animation (2876-3060), Animator's Survival Kit
   (3061-3406). Prefer the individual PDFs when quoting; they are cleaner.
5. Read the relevant reference file(s) before starting the work:
   - Rigging / armatures / skinning / facial rig → `references/02-rigging-blender.md`
   - Timing, spacing, polish, F-curves → `references/03-timing-spacing.md`
   - Walks, runs, jumps, weight, flexibility → `references/04-body-mechanics.md`
   - Acting, performance, staging, story → `references/05-acting-performance.md`
   - Face, dialogue, lip sync → `references/06-facial-lip-sync.md`
   - Math, curves, IK solvers, springs, tools → `references/07-math-procedural.md`
   - Book-by-book essence and provenance → `references/01-book-essence.md`

## The library at a glance

| Book | What it gives us | Essence in one line |
|---|---|---|
| Cabrera - Maya Character Rigging | Full biped rigging curriculum (in Blender terms) | A rig is a *machine for posing* - build joints like a skeleton, controls like an interface |
| Williams - Animator's Survival Kit | Spacing/timing, walks, runs, flexibility, weight, acting | "It's all in the timing and the spacing" - movement is drawn *in time* |
| Whitaker & Halas - Timing for Animation | Timing theory: force, weight, holds, cycles, effects | Timing is the tool that conveys force, weight, size and emotion |
| Thomas & Johnston - Illusion of Life | The 12 principles, Disney craft, acting/emotion | Animation is *bringing a character to life*: thought, emotion, appeal |
| Osipa - Stop Staring | Facial modeling, visemes, lip sync, eyes/brows | The face reads in layers: mouth speaks, eyes and brows *think* |
| Ed Hooks - Acting for Animators | Acting craft for animators | Characters don't move, they *act* - emotion drives movement, movement provokes emotion |
| Dunn & Parberry - 3D Math Primer | Vectors, matrices, rotations, quaternions, curves | Understand the math so transforms, orientations and splines stop being magic |
| Rick Parent - Computer Animation | Algorithms: IK, mocap, physics, procedural, crowds | Every technique is a tool; pick the one that serves the performance |

## Core doctrine (essence and reason)

- **Pose → Breakdown → Inbetween → Polish.** Williams' "three ways to animate" (straight-ahead,
  pose-to-pose, and a mix). Reason: pose-to-pose controls structure; straight-ahead gives life;
  the mix gets both. In Blender: block keys, add breakdowns with the Breakdowner, then refine.
- **Spacing defines the movement, timing defines the force.** Same timing with different spacing
  gives different motion; the *amount* of space between drawings = speed. Reason: physics lives
  in spacing (Whitaker: "spacing of drawings" chapters; Williams: "It's All in the Timing").
- **Everything has weight.** Anticipate, overshoot, settle - through flexible joints, with overlap
  and stagger. Reason: Newton's laws; force transmits through jointed limbs (Whitaker).
- **Arcs, not straight lines.** Every natural action travels an arc (Williams: "Watch Your Arcs").
- **Acting first.** Before posing: what does the character *want* (objective), what's in the way
  (obstacle), what do they *do* about it (tactics) (Hooks). Emotional state is the seed (Illusion
  of Life: "Acting and Emotions").
- **Contrast reads.** In timing, size, posture, expression (Williams: "Look for the Contrast";
  Osipa: offset brows/eyes/lips so the face never moves as one robotic unit).
- **The rig serves the animator.** Clean control interface, named channels, no surprise spaces -
  Cabrera's "wrapping up the setup" chapter is exactly this lesson.

## Maya → Blender quick map

| Maya (Cabrera) | Blender |
|---|---|
| Joints / joint chains | Armature bones (Edit Mode), parented chains |
| Joint orientation / aim | Bone roll + local axes (Y = along bone) |
| IK Handle / ikRPsolver | Bone Constraints → Inverse Kinematics |
| FK/IK blending | Custom property + drivers on constraint influence |
| Set Driven Key | Drivers (driver editor), or the "Driven Key" style via add-ons |
| Blend Shapes | Shape Keys (Basis + targets), slider drivers |
| Skin Cluster / Smooth Bind | Armature modifier + vertex groups (weight paint) |
| Paint Skin Weights Tool | Weight Paint mode, Normalize All |
| Constraints (parent/orient/point) | Bone Constraints (Copy Transforms/Location/Rotation, Child Of) |
| Node Editor / attribute control | Custom properties on a control bone + drivers |
| File Referencing | Library Overrides / linked collections |
| Outliner layers / display layers | Collections, bone collections, viewport visibility |
| X-Ray Joints | Armature viewport display → In Front |
| Graph Editor / dope sheet | Same names in Blender |

## Session workflows

**Rigging a character:** `references/02-rigging-blender.md` order: design sheets → model for
deformation → shape keys for face → joint placement (T-pose/A-pose, symmetric) → FK/IK + control
interface → clean/names → skinning + weights → test poses. Then validate with the pose battery:
touch toes, overhead reach, shoulder shrug, hip-out lean, full squat, wrist twists.

**Animating a shot:** reference/05 for story intent + acting verbs → blocking (extremes only)
→ breakdowns (03/04) → overlap/staggers → polish pass (arcs, offsets, dents, accents) →
playblast review with the checklist in 03.

**Dialogue shot:** lipsync from 06 (visemes first, phrasing, then accents) + eyes/brows emotion
→ body acting from 05 → final offsets (06: "connecting the features").

## Reference map

- `references/01-book-essence.md` — per-book essence, key lessons, provenance
- `references/02-rigging-blender.md` — Cabrera's rigging curriculum in Blender
- `references/03-timing-spacing.md` — Williams + Whitaker timing/spacing doctrine
- `references/04-body-mechanics.md` — walks, runs, jumps, weight, flexibility, animals
- `references/05-acting-performance.md` — Hooks + Illusion of Life + Williams acting
- `references/06-facial-lip-sync.md` — Osipa's face system
- `references/07-math-procedural.md` — 3D math, curves, IK, springs, procedural systems
