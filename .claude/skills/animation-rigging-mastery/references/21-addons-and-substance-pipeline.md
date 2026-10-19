# 21 — Power Tools: The Add-on Law + the Substance 3D Painter Pipeline

## A. When to use an add-on (and when vanilla wins)

> **The law: an add-on may change how fast you work; it may never change what the
> audience sees for the worse, and it may never hold your file hostage.** The books'
> doctrines decide *what good is*; add-ons only decide *how many clicks it takes*.

**An add-on is MORE efficient with zero compromise when ALL of these hold:**
1. The job is **mechanical/repetitive** (UV packing, retopology, rig assembly, scattering,
   renaming, baking queues) — not an artistic decision.
2. Its output is **standard Blender data** (mesh, UVs, armature, images) that you can
   inspect, edit, and render after the add-on is removed.
3. The result is **measurably equal** (same UV quality, denser pack; same rig behavior,
   faster build) — judged by the refs' checks, not by the add-on's marketing.
4. It survives your pinned Blender version and opens on another machine.

**Vanilla (this skill's procedures) wins when:** the task is a judgment call (posing,
timing, wear placement), the add-on's output can't be inspected, it duplicates a 3-click
native feature, it needs a runtime the render machine won't have, or the project is
near delivery (no new dependencies in the final stretch).

**Production rules:**
- **Final files must open correctly with NO add-ons**: apply/bake add-on results before
  delivery; keep one vanilla-safe checkpoint per asset.
- Pin the Blender version per production; update add-ons only between projects.
- Prefer built-in and Extensions-platform tools first: **Node Wrangler** (ships with
  Blender), **Rigify** (built-in, studio-proven rigs — pair with ref 02 doctrine).
- Proven examples by job (any tool must still pass the law above): *Auto-Rig Pro*
  (rig assembly/export speed), *RetopoFlow* (retopology), *HardOps/Boxcutter*
  (hard-surface — output is plain meshes), *UVPackmaster* (packing density — same UVs,
  less waste), *DecalMachine* (decals = Owen Demers' Fin pattern, ref 17 §6), *Geo-Scatter/
  Botaniq* (vegetation scattering as instances — ref 20 §1), *Flip Fluids* (water sims
  beyond Mantaflow's comfort), **Adobe's Substance 3D add-on** (§B7).
- Log production-approved add-ons in the Pipeline Brief (ref 14) so every session uses
  the same stack — inconsistency is how files break.

## B. Substance 3D Painter — the ultra-realistic texturing pipeline

Since this production owns **Substance 3D Painter**, it is the default path for hero
realism texturing; Blender procedural/paint (ref 17) covers stylized, animated-shader,
and minor assets. *The PBR Guide* was literally written as Painter's rulebook — every
value law in ref 16 applies inside Painter unchanged.

**B1. Prep in Blender (Painter cannot fix these later)**
- True scale (meters); clean topology; naming discipline: `Part_low` / `Part_high`.
- **UVs finished here** (ref 17 §2): seams hidden, texel-density standard set, UDIM for
  heroes, padding respected. A UV change after painting = repaint risk.
- Material slots = Painter texture sets (one per material zone); vertex colors or
  material IDs for masking; export FBX (apply modifiers intended for the low; check
  scale/tangents).

**B2. Painter project setup**
- Template: PBR – Metallic Roughness · **Normal format: OpenGL** (Blender's convention —
  DirectX here is the classic flipped-relief bug) · document resolution per asset class
  (4K hero / 2K mid / 1K background, ref 17 §9) · UDIM workflow ON if the asset is UDIM.

**B3. Bake in Painter** (interactive cage control beats blind numbers)
- Match by mesh name (`_low`↔`_high`); tune Max Frontal/Rear Distance until the cage
  hugs the high — skim artifacts are fixed here, never painted over.
- Bake: Normal, AO, Curvature, Position, Thickness, World Space Normal (the mask fuel
  for generators). Antialiasing 4×4 (8×8 hero). Inspect every map solo before painting —
  a bad curvature map poisons every wear mask downstream.

**B4. Paint with the law (refs 16–17 inside Painter)**
- Layer stack in physical order: **substrate → color variation → wear → dirt/damage →
  micro detail**. Generators (curvature/AO/position-driven) place wear where physics
  would; then *art-direct them* — untouched generator defaults and raw Smart Materials
  are recognizable and read amateur (ref 13 logic). Break every generator with at least
  one hand-painted or noise-modulated mask at a different scale (ref 17 §5).
- Roughness gets the most layers (it IS the realism channel); metallic stays binary
  (rust/paint = 0); albedo checked against the 30–240 sRGB band.
- Anchors for decals/logos/wear alignment across layers (the Fin pattern, ref 17 §6).
- Height detail painted in Painter combines with baked normals (Height→Normal) — keep
  strengths physical; crunchy relief = amateur.

**B5. Export for Blender**
- Custom export preset "Blender": **BaseColor** (sRGB, PNG 8-bit ok) · **Roughness** ·
  **Metallic** (grayscale, data) · **Normal (OpenGL)** · optional **Height** (16-bit)
  and **AO** (only for micro-occlusion per ref 16 §3). File naming the Node Wrangler
  auto-detects (`_BaseColor`, `_Roughness`, `_Metallic`, `_Normal`) so Ctrl+Shift+T
  wires instantly. Padding: dilation/infinite. UDIM: export all tiles.

**B6. Back in Blender — approve HERE, not in Painter**
- Connect (ref 11 H1), verify color spaces (data = Non-Color), tiles set to Tiled.
- Painter's viewport (ACES) and Blender's AgX disagree slightly — **final approval only
  in Blender** under the 3-light test (refs 16 §6, 11 H7). Painter is the workshop;
  Blender is the client screening room.

**B7. The Adobe Substance 3D add-on for Blender (.sbsar path)**
- Loads Substance *Designer*/library `.sbsar` materials as parametric Blender materials
  — excellent for tiling base materials and fast variations (a wall, a road, fabrics).
- It does NOT replace Painter (your painted mesh doesn't become an .sbsar). Use for:
  environment tiling materials, variation passes, look tests. **Bake to image textures
  before delivery/render-farm** (the §A hostage rule).

**B8. Iteration discipline**
- Mesh fixes → re-export with IDENTICAL names/UVs → Painter keeps your painting on
  mesh update. Geometry is negotiable after texturing; UVs are not.
- Version the `.spp` and `.blend` together (`helmet_surf_v03`). The Lessons Ledger
  (ref 19 §4) records which generator settings failed lookdev and why.
- **When to skip Painter:** stylized hand-painted looks, shaders that must animate
  (spreading wetness, burning), quick background props fully procedural (ref 17 §5),
  and anything whose texture is mostly noise — Blender nodes do it live and lighter
  (baked later per ref 20 §1 if the shot demands).
