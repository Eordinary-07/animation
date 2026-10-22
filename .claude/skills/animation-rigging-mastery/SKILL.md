---
name: animation-rigging-mastery
description: "TRIGGER KEYWORD: blend / blender (.blend, bpy) - also trigger on armature, rig, rigging, skinning, weight paint, IK, FK, shape keys, drivers, keyframe, animation, walk cycle, lip sync, camera, shot design, storyboard, animatic, render, timing, spacing, acting, shading, texturing, PBR materials, lookdev, toolcheck (evaluate new tools/add-ons/versions against the book laws), topology, retopology, edgeloop, poly flow, quad, n-gon, manifold, mesh readiness, or any script/instruction to animate. Self-contained animation, rigging, modeling and surfacing master class for Blender distilled from 25 industry books (Cabrera, Williams, Whitaker & Halas, Thomas & Johnston, Osipa, Hooks, Dunn & Parberry, Parent, Wes McDermott, Owen Demers, Jeremy Birn, PBRT 4e, Ebert et al, James Gurney, Glebas, Bruce Block, Katz, Walter Murch, Stanchfield, Robert McKee, Gilland, William Vaughan (Digital Modeling), Tina O'Hailey (Rig It Right), Zarins (Anatomy for Sculptors), Hogarth (Dynamic Wrinkles and Drapery)). Contains ALL concepts of all books inside the skill (references/12-concept-index.md) - no PDFs or external files needed. Use whenever creating, rigging, animating, or directing anything in Blender or answering animation/rigging questions."
---

# Animation & Rigging Mastery — Project Memory

## Standing orders (every session)

1. This skill is a **self-contained master class** — all concepts of the 25 integrated books are inside
   it (`references/12-concept-index.md` is the complete A-Z map). It works with NO PDFs
   and no external files. Treat it as required reading before animation/rigging/surfacing work.
2. The Maya rigging book (Cabrera) is the rigging curriculum — but **apply its logic in Blender**.
   Every Maya technique has a Blender equivalent; see `references/02-rigging-blender.md`.
   Baseline is **Blender 5.x** (target the current stable, **5.2 LTS**: bone collections,
   Asset Browser pose assets, Library Overrides, EEVEE, slotted Actions; the legacy
   `action.fcurves` bpy API is removed) — procedures in
   `references/11-blender-how-to.md` use 5.x menu paths, and its §0 lists every
   4.x→5.x change that matters (keying defaults, shape-key UI, texture cache…).
3. When working, cite the *reason* behind a technique (the books teach essence + reason, not
   recipes). If a shot or rig decision can be justified from the books, justify it that way.
3b. **Intention first, always**: classify the input level and run the intake in
   `references/25-briefing-the-skill.md` (for sparks/briefs, return a Story Card for
   one-word approval before producing anything). Before animating, answer the five
   questions (objective / obstacle / tactic / audience feeling / one idea per shot) and
   produce the INTENTION block of the Pipeline Brief — `references/18-script-intention-engine.md`.
   Asked questions are about intention only; mechanics are decided professionally and stated.
3c. **Self-correct like a studio**: work in gates (L→B→S→P), run the self-critique battery
   and fix the top-3 flaws BEFORE presenting work, measure against the precision
   tolerances, and maintain the project's `LESSONS.md` — read it at the start of every
   task, append a rule after every mistake or user correction, never repeat a logged
   mistake — `references/19-self-correction-system.md`.
3d. **Optimize & tool up without compromise**: budgets are per-shot and protect the hero
   (ref 20); add-ons only when mechanical + inspectable + add-on-free at delivery
   (ref 21 §A); **Substance 3D Painter is the owned hero-texturing path** — Blender prep
   → Painter (OpenGL normals) → approve in Blender (ref 21 §B, procedure 11 H8).
3e. **Style + a fresh pipeline for EVERY request**: declare the style preset or derive a
   custom Style Card (ref 22 §A), design this request's pipeline from the stage menu
   (ref 22 §B) inside the Pipeline Brief, then print the plain-words Pipeline Explainer
   (ref 22 §C) so the user understands and learns the pipeline as we run it.
4. The original PDFs are OPTIONAL background only — never required, never ask for them.
   Everything needed to work is in this skill. (For the curious: the merged OCR PDF's order
   is Maya Rigging 1-408, Stop Staring 409-795, 3D Math 796-1641, Rick Parent 1642-2182,
   Acting for Animators 2183-2327, Illusion of Life 2328-2875, Timing 2876-3060,
   Survival Kit 3061-3406.)
5. Read the relevant reference file(s) before starting the work:
   - Rigging / armatures / skinning / facial rig → `references/02-rigging-blender.md`
   - Timing, spacing, polish, F-curves → `references/03-timing-spacing.md`
   - Walks, runs, jumps, weight, flexibility → `references/04-body-mechanics.md`
   - Acting, performance, staging, story → `references/05-acting-performance.md`
   - Face, dialogue, lip sync → `references/06-facial-lip-sync.md`
   - Math, curves, IK solvers, springs, tools → `references/07-math-procedural.md`
   - Camera, shots, framing, lenses, movement → `references/08-camera-cinematography.md`
   - Script/instruction → full animation pipeline → `references/09-script-to-screen.md`
   - New tool/add-on/AI technique or Blender version question ('toolcheck') → `references/26-tool-intelligence.md`
   - EVERY user request starts here (what they gave you, what to ask, Story Card) → `references/25-briefing-the-skill.md`
   - ANY script/instruction → intention first → `references/18-script-intention-engine.md`
   - **Script uploaded? Build a PIPELINE BRIEF first → `references/14-pipeline-generator.md`**
   - Blender scene setup, cuts, render, delivery → `references/10-blender-production.md`
   - **Exact Blender click-by-click procedures → `references/11-blender-how-to.md`**
   - Slow scene/render, optimization budgets → `references/20-optimization-without-compromise.md`
   - Directing, staging, visual structure, editing → `references/23-directing-the-screen.md`
   - Pose/gesture quality, hand-drawn FX thinking → `references/24-pose-gesture-effects.md`
   - Animation style choice, custom pipelines, plain-words explanation → `references/22-styles-and-pipeline-design.md`
   - Add-on decisions, Substance Painter pipeline → `references/21-addons-and-substance-pipeline.md`
   - Reviewing, QA, learning from mistakes (gates, battery, LESSONS.md) → `references/19-self-correction-system.md`
   - **Amateur-vs-industry diagnosis & review codes → `references/13-amateur-vs-industry.md`**
   - **Complete concept index of all 25 books (A-Z) → `references/12-concept-index.md`**
   - **Mesh/topology readiness BEFORE rigging (quads, rule of three, edgeloops, poles,
     manifold, rest pose, scale, UV, weights, 6 validation tests) →
     `references/27-mesh-topology-readiness.md`**
   - **Skinning & deformation validation (bind methods, normalization trap, max influences
     = 3, 60/40 joints, shape-key rules, deformation battery) →
     `references/28-skinning-deformation-validation.md`**
   - **Geometry Nodes studio patterns (the 27-node vocabulary, reusable groups, curve-driven
     instancing, sculpt→sim bridge) → `references/32-geometry-nodes-studio-patterns.md`**
   - **Cloth & fabric (sculpted vs simulated, measured fold-depth tolerance, multires, the
     fold vocabulary, procedural trim) → `references/33-cloth-and-fabric.md`**
   - Book-by-book essence and provenance → `references/01-book-essence.md`
   Rule: the references say WHAT and WHY; `11-blender-how-to.md` says HOW (operators,
   buttons, shortcuts). Never improvise Blender steps when a procedure exists in 11.
   If you need "the concept from the books", it is in 12 — do not look for PDFs.

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
| **William Vaughan - Digital Modeling** | Topology, poly-count, clean modeling, production prep (ref 27) | **Rule of three**: 3 segments where it bends — one deforms, two support. "Less is always more" |
| **Tina O'Hailey - Rig It Right!** | Edgeloops for deformation, skinning, joint axes | **Rule #1**: a good or bad rig starts with the loops — quads spread "like butter" are not enough |
| Zarins - Anatomy for Sculptors | Surface anatomy, proportions, landmarks for sculpting | Form is anatomy, not details — build the landmark before the wrinkle |
| Hogarth - Dynamic Wrinkles and Drapery | Compression/tension fold language on body and cloth | Wrinkles are a *record of force* — they radiate from compression, never decorate |

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
- **The camera is the audience.** Framing says what matters, angle says who has power,
  movement says how we feel. Every shot serves the idea of its beat (see
  `references/08-camera-cinematography.md`).
- **Make the movie in the animatic** (Williams' Leica reel). Re-timing an animatic costs
  minutes; re-timing animation costs days. The piece must read SILENT first.

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

**Creating animation from a script or instruction (the master workflow):**
`references/09-script-to-screen.md` — Stage 0 understand (one-sentence story + objective)
→ Stage 1 script analysis (beats, acting points, verbs) → Stage 2 shot design
(`08-camera-cinematography.md`: size/angle/lens/movement per beat) → Stage 3 storyboard +
animatic (lock the cut) → Stage 4 layout & blocking in Blender (cameras bound to markers,
Stepped poses at beats, silhouettes checked) → Stage 5 craft layers in order (reference →
blocking → breakdowns → spline/offsets → mechanics → face/dialogue → polish) → Stage 6
director's review (the 10-point checklist — silent read first) → Stage 7 delivery
(`10-blender-production.md`). Professional level is defined at the end of 09 — hold it.

## Reference map

- `references/01-book-essence.md` — per-book essence, key lessons, provenance
- `references/02-rigging-blender.md` — Cabrera's rigging curriculum in Blender
- `references/03-timing-spacing.md` — Williams + Whitaker timing/spacing doctrine
- `references/04-body-mechanics.md` — walks, runs, jumps, weight, flexibility, animals
- `references/05-acting-performance.md` — Hooks + Illusion of Life + Williams acting
- `references/06-facial-lip-sync.md` — Osipa's face system
- `references/07-math-procedural.md` — 3D math, curves, IK, springs, procedural systems
- `references/08-camera-cinematography.md` — shot sizes, angles, lenses, framing, movement
- `references/09-script-to-screen.md` — script/instruction → professional animation pipeline
- `references/10-blender-production.md` — scenes, cuts/markers, animatic, render, delivery
- `references/11-blender-how-to.md` — exact Blender procedures (rig, animate, camera, render)
- `references/12-concept-index.md` — every concept of all 25 books, A-Z, fully self-contained
- `references/13-amateur-vs-industry.md` — the exact gap: 15 differences, flaw codes, 8-point self-check
- `references/14-pipeline-generator.md` — build a custom AAA pipeline per script (drivers → matrix → Pipeline Brief)
- `references/16-shading-pbr-fundamentals.md` — the shading law: light behavior, F0 (dielectrics 0.02–0.05, metal/rough hardcodes 4%), base-color 30–240 sRGB band, measured metal tints, Principled BSDF decoded socket-by-socket, linear-workflow commandments, the 3-light lookdev test (The PBR Guide, PBRT, Jeremy Birn, James Gurney)
- `references/17-texturing-workflow.md` — Owen Demers' see→dissect→decide method, UV/texel-density standard, the PBR map set and what each map is for, baking principles, Ebert procedural theory → Blender nodes, wear logic, resolution budgets, amateur tells
- `references/18-script-intention-engine.md` — intention-first protocol for ANY script: the five questions, beat maps, one idea per shot, intention-to-technique translation tables, format adaptability matrix (dialogue/action/comedy/horror/musical/product), the realism dial, thin-script decision rules
- `references/19-self-correction-system.md` — the studio learning loop: stage gates L-B-S-P with checklists, numeric precision tolerances (foot slip, lip-sync, blinks), the self-critique battery (silent/silhouette/mirror tests + fix-top-3), and the Lessons Ledger (LESSONS.md) so mistakes become standing rules
- `references/20-optimization-without-compromise.md` — the free wins (instancing, texture-by-screen-coverage, adaptive sampling + denoise, baked frozen procedurals, per-shot budgets) vs forbidden trades; diagnosis order with numbers
- `references/21-addons-and-substance-pipeline.md` — the add-on law (when add-ons beat vanilla with zero compromise; no-hostage delivery rule; proven catalog) + the full Substance 3D Painter ultra-realistic pipeline (prep, bake, paint, export preset, approve-in-Blender, .sbsar add-on path)
- `references/22-styles-and-pipeline-design.md` — 8 animation style presets with real parameters (frame density, squash ceilings, smears, renderers) + custom Style Card derivation, the 15-stage menu for designing a fresh pipeline per request, and the always-printed plain-words Pipeline Explainer
- `references/23-directing-the-screen.md` — Bruce Block's seven visual components + contrast/affinity intensity control, Francis Glebas' attention direction and narrative questions, Steven Katz's staging/camera grammar, Walter Murch's Rule of Six for cuts
- `references/24-pose-gesture-effects.md` — Walt Stanchfield's pose law (draw verbs not nouns; one pose = one story; gesture backbone) + Joseph Gilland's Elemental Magic FX categories translated to Blender sim/shader choices
- `references/25-briefing-the-skill.md` — the input system: five brief levels (one-line spark to full script), the 6-field Mini Brief, the Story Card approval step, story-spine/beat templates, missing-info protocol (infer mechanics, ask ≤3 intention questions), and feeling-first feedback
- `references/26-tool-intelligence.md` — future-proofing: every capability is an outcome contract (measurable book-law criteria), new/unknown tools (AI in-betweening, mocap, sims, AI textures, future Blender) must pass a 5-gate scorecard on fixed golden tests; verdicts (Adopt/Trial/Park/Reject) live in the project's TOOLS.md; the 'toolcheck' ritual keeps the toolbox current
- `references/27-mesh-topology-readiness.md` — the gate before rigging: O'Hailey's Rule #1 ("a good or bad rig starts with the loops") + three laws, Vaughan's rule of three (≥3 segments: one bends, two support), quad discipline and four-point triangles, edge loops that enclose the bend (Finger A/B/C + the kneepad law: compression side must have SMALLER surface area), pole placement, density budgets (measured CGBoost numbers: p95 detail depth 0.233%–1.071% of object size; fingers ≈4.6× arms/legs), manifold/normals/loose/self-intersect checks, T-pose vs A-pose trade-off, scale + triangle caps (≤100k for auto-riggers), UV seam placement, weight/hierarchy/bake/shape-key readiness, the 6 validation tests, and a printable PASS/FAIL Gate checklist
- `references/28-skinning-deformation-validation.md` — everything after the topology gate passes: O'Hailey's Rule #10 ("a good rig with bad skinning is still bad"), order of operations (proxies/"tootsie rolls", UV before skinning, the "textures swim" gotcha, never add verts after binding), the 4 bind methods and their failure modes, linear vs dual-quaternion vs weight-blended, the Post-normalization trap (**painting 1 is not enough — you must also paint 0**), **max influences = 3** ("5 or higher… a skinning nightmare"), bind pose as the zero point, painting in POSE not at rest, the 60/40 distribution table per joint, shape keys (never freeze, vertex-group masks, the double-transform gotcha + combination targets), the joint-orientation parenting gotcha, the full deformation battery (twist + volume tests added), export baking, and a printable Gate
- `references/32-geometry-nodes-studio-patterns.md` — Geometry Nodes built from a **census of 646 real node instances across 27 node types** parsed out of 12 production `.blend` files: the full usage table (INSTANCE_ON_POINTS 44, FRAME 33, VIEWER 10…), the five reusable groups and how they evolve (`Zipper` built once and never edited across 11 files; `Seams_On_Curve` → `Stitch_Seams_On_Curve`; `Bolts_On_Curve` reused from jetpack to wings), the complete `Stitch_Seams_On_Curve` and `Blur Vertex Group` recipes verbatim from the files, curve-driven placement as the one pattern to memorize, deriving masks from geometry (Edge Angle + Compare), tree hygiene, and performance rules
- `references/33-cloth-and-fabric.md` — cloth from the garment-build progression measured across the production files (80 → 278 objects; shirt, zipper, stitching, knee fabric, cloth brush, sweater): sculpted vs simulated and when each wins, the **measured fold-depth tolerance (p95 0.233%–1.071% of object size)**, the multires surprise (production heroes carry none; only the 2 teaching exercises at 3 levels), Hogarth's fold vocabulary mapped to character zones, procedural trim, the sculpt→sim Pin Group bridge, and the honest status of what is not yet measured
- `references/15-verified-page-images.md` — catalog of 53 bundled evidence pages (`references/images/*.jpg`): real scanned pages from the image-only books — Hooks ALL 13 chapters (Seven Concepts, character bible, three conflicts, power centers, Laban efforts, reaction shots…), Williams Procedure/Acting Point/Arcs/Recipe/Twinning/Walks, Osipa squint, Illusion of Life 12 principles. When a reference cites one of these pages, OPEN the image — it is the primary source and outranks this skill's text.

Standing order for scripts: when a script or animation instruction is uploaded, FIRST produce the
Pipeline Brief from `14-pipeline-generator.md` (story → rigs → facial scope → shot list → camera →
verification), THEN execute it with 09-11. When reviewing any work, diagnose with 13's flaw codes.
