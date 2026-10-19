# Pipeline Generator — Build the Right Pipeline Per Script (Industry/AAA Method)

> When a script or instruction is uploaded, DO NOT apply one fixed pipeline. Build a **custom
> pipeline** for THAT story the way studios do it (Illusion of Life: the story dictates the
> production; Survival Kit: plan the film before animating; Cabrera: rig only what the
> performance needs). This file is the method. Output: a Pipeline Brief (§E) before any work.

---

## A. The industry method (how studios design a pipeline)

The pipeline is a function of the story, not a template:
1. **Story first** (Illusion of Life; Acting for Animators): what is the emotional core? What
   must the audience feel? Everything downstream serves this.
2. **Break down demands** (Survival Kit; Parent): shot count, action complexity, dialog density,
   characters, style — these determine rigs, tools, and schedule.
3. **Design only what's needed** (Cabrera): a dialog scene needs a face and acting; a creature
   film needs quadruped/flight deformation. Don't build a feature rig for a pantomime short.
4. **Prove, then scale** (Williams, "The Procedure": TEST at every stage — storyboard →
   Leica reel → planning thumbnails → key positions → extremes → passing positions):
   run one hero shot through the whole pipeline before mass production.
5. **Gates at every phase** (ref 09/10): nothing advances until its gate passes.

---

## B. Script analysis — extract the 7 drivers

Read the script/instruction and fill this in (ask the user only for what's genuinely missing):

| Driver | Extract | Drives |
|---|---|---|
| D1 Genre & tone | comedy/drama/action/horror… sincere or satirical (Acting for Animators) | acting style, timing personality |
| D2 Emotional core | the one feeling the film must deliver | every decision's tie-breaker |
| D3 Characters | count, anatomy (human/creature/prop), relationships | rigs needed (Cabrera scope) |
| D4 Dialog density | none / light / heavy | facial system depth (Osipa) |
| D5 Action complexity | pantomime / acting-only / full body stunts / creature action | body mechanics scope (ref 04), simulation needs |
| D6 Style | realism / stylized 2D-in-3D / cartoon squash / limited | rig feature set, timing style, render |
| D7 Scale | one shot / short / sequence / feature-length | reuse strategy, schedule, verification depth |

## C. Pipeline decision matrix (the generator)

For each driver, select the pipeline components:

**Rigging scope (from D3+D5+D6):**
- Acting-only human → core skeleton + spine + arms + face (Cabrera §B): twist bones on forearms,
  shoulder free-collars, FK/IK arms, head/eye/face controls — FULL FACE (dialog).
- Action hero → add: full leg IK/FK switch, hip lock, space switching (world/chest/COG/hand),
  stretch optional (exaggerated styles), tested squash/stretch regions.
- Creature (quadruped/flying) → mirrored leg chains with free-collars, tail chain (FK spline),
  wing membrane stretch regions, spine rigidity per species.
- Prop/limited character → controls only where the performance lives; never overbuild.

**Facial scope (from D4):**
- None → skip face; invest in body acting (pantomime rules of ref 04/06).
- Light → jaw + mouth corners + brow + eyes; viseme shapes for A/E/O/MBP at minimum.
- Heavy dialog → full Osipa rig (ref 06): 9+ visemes, cheek/jaw/nose/ear controls, 3 blink types,
  correct shaping order, pose-based approach.

**Animation approach per shot (from D5+D6, Williams):**
- Big action / stunts → pose-to-pose with golden poses → breakdowns → full mechanics pass.
- Dialog acting → blocking with emotional extremes (Osipa) → refinement → polish.
- Limited/cartoon style → plan less keys, sharper extremes, snappier spacing (Timing for Animation).
- Never straight-ahead for complex shots unless deliberately choosing its energy.

**Camera plan (from D1+D2, ref 08):**
- Storyboard every shot; shot size = emphasis; obey 180°; motivated moves only.
- Comedy → wider, more cuts, snappier timing; drama → longer takes, holds; action → clear staging.

**Verification depth (from D7):**
- Every shot: golden pose + mechanics + polish gates (ref 09/10).
- Sequences: continuity checks (emotion continuity — Osipa; style/physics consistency).
- Feature scale: Williams' "The Procedure" test ladder first (Leica/animatic → thumbnails →
  keys → extremes → passing positions, testing each), then batch with gates.

**Schedule shape (from D7):**
- Short: pipeline once, verify end-to-end.
- Long: preflight test scene → proven pipeline → parallel shot production with per-shot gates.

## D. Reuse & economy (industry discipline)

- Reuse rigs and shot templates AFTER one proves out; keep reference/pose research the way
  Williams prescribes ("Steal It!" — steal from life, not from other cartoons), and save
  approved golden poses as your pose library (industry practice).
- Save every approved golden pose (Williams "save useful poses").
- Cut everything that doesn't serve the emotional core (Acting for Animators; Illusion of Life).

## E. Output — the Pipeline Brief (produce this FIRST for any uploaded script)

Before keying anything, output a brief like this and follow it:

```
PIPELINE BRIEF — [title]
0. INTENTION (ref 18 — answer first, always): objective / obstacle / tactic | audience feeling | one idea per shot | emotional arc | style (realism dial) | format type
1. STORY: 1-2 lines | emotional core: [D2]
2. CHARACTERS & RIGS: [D3] → [rig scope list from matrix]
3. FACIAL: [D4] → [facial scope]
3b. SURFACING: materials/textures (11 §H) → [per asset: texel-density standard, tex resolution class, map set, procedural/painted split (refs 16–17)]
4. SHOT LIST: [count] shots — # | description | size | acting beats | approach (pose/dialog/limited)
5. CAMERA PLAN: [D1] style → [shot-size/move strategy]
6. APPROACH PER SHOT TYPE: [from matrix]
7. VERIFICATION: gates at golden/mechanics/polish + continuity checks
8. SCHEDULE: test scene first → [production shape]
```
Then execute shot-by-shot with the refs (11 for Blender steps, 13 for quality diagnosis).

## F. AAA bar for the pipeline itself

A pipeline is AAA when: every driver is answered, nothing is built that the story doesn't need,
the test scene proved it end-to-end, every phase has a gate, and the final work passes the
ref 09 director's review AND ref 13 amateur-vs-industry checklist.
