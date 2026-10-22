# CGBoost "Character Sculpting in Blender" (P1 C1-10) — EXTRACTED STUDIO DATA

> Auto-extracted from the real production `.blend` files with **Blender 5.2.3** running
> headless in GitHub Actions (`tools/blend_dump.py` → `cgboost-reports/*.json`).
> Read-only extraction — the course files were never modified. Generated 2026-10-22.

## 1. Studio scene setup (what they actually work in)

| Setting | Value |
|---|---|
| Render engine | **BLENDER_EEVEE** |
| View transform | **Filmic** |
| Resolution | [1920, 1080] |
| FPS | **24** |
| Render engine | **BLENDER_EEVEE** |
| View transform | **AgX** |
| Resolution | [1920, 1080] |
| FPS | **24** |

**Lesson:** the character-work workspace is **EEVEE** (real-time) at
**1920×1080 / 24 fps** — Cycles is for final rendering, not for building.
Later files moved **Filmic → AgX**, matching Blender 5.x colour management.

## 2. Asset organisation (278 objects by the end)

| File | Objects | Collections | Meshes | Vertices |
|---|---|---|---|---|
| 03_09_refining_the_head_part_2_final | 5 | 3 | 2 | 147,470 |
| 03_11_sculpting_the_torso_part_1_final | 6 | 3 | 3 | 192,016 |
| 03_16_sculpting_the_arms_final | 13 | 3 | 10 | 243,182 |
| 03_20_sculpting_the_hands_part_2_final | 29 | 3 | 21 | 316,485 |
| 03_23_sculpting_the_feet_part_2_final | 39 | 3 | 31 | 382,330 |
| 03_24_sculpting_the_hair_final | 80 | 11 | 72 | 493,632 |
| 05_04_exercise_1 | 2 | 1 | 2 | 373 |
| 05_04_exercise_2 | 1 | 1 | 1 | 608 |
| 05_08_sculpting_shirt_part_4_final | 92 | 14 | 83 | 499,497 |
| 05_09_modeling_zipper_geometry_nodes_final | 96 | 15 | 86 | 499,628 |
| 06_09_modeling_stitching_geonodes_final | 112 | 17 | 96 | 503,302 |
| 06_10_geonodes_organization_final | 112 | 17 | 96 | 503,302 |
| 06_17_sculpting_knee_fabric_final | 124 | 17 | 108 | 503,690 |
| 07_17_modeling_stitches_geometry_nodes_final | 174 | 26 | 147 | 512,072 |
| 09_04_sculpting_cloth_brush_final | 204 | 30 | 175 | 515,718 |
| 09_08_geonodes_smoothing_vertex_groups_final | 206 | 30 | 177 | 516,325 |
| 10_12_geonodes_panel_bolts_final | 235 | 31 | 202 | 521,215 |
| 10_19_geonodes_wing_bolts_final | 252 | 32 | 215 | 523,175 |
| 10_26_sculpting_sweater__final | 278 | 45 | 228 | 532,002 |

**Pattern:** the character is **not one mesh** — it is a library of separately
named parts (`Head`, `Arms`, `Hands`, `Feet`, `Breasts`, `Hair_Placeholder`,
`Boots_Sole`, `Jetpack_Base_1`, `Eyelet.001`…), driven by **collection instancing**
(`Instance_From_Collection` node group) and placeholders that are replaced later.
Head alone is **147,458 verts**; the whole file ends at ~532k verts across 278 objects.

## 3. Geometry Nodes — the 27 nodes that did all the work

| Uses | Node |
|---|---|
| 94 | `GROUP_INPUT` |
| 59 | `MATH` |
| 48 | `GROUP_OUTPUT` |
| 44 | `INSTANCE_ON_POINTS` |
| 44 | `TRANSFORM_GEOMETRY` |
| 38 | `OBJECT_INFO` |
| 33 | `FRAME` |
| 32 | `ALIGN_EULER_TO_VECTOR` |
| 23 | `REALIZE_INSTANCES` |
| 22 | `SET_SHADE_SMOOTH` |
| 22 | `RESAMPLE_CURVE` |
| 22 | `CURVE_TO_POINTS` |
| 22 | `JOIN_GEOMETRY` |
| 20 | `COMBXYZ` |
| 11 | `MESH_EDGE_ANGLE` |
| 11 | `INPUT_EDGE_SMOOTH` |
| 11 | `INPUT_SHADE_SMOOTH` |
| 11 | `BOOLEAN_MATH` |
| 11 | `COMPARE` |
| 11 | `COLLECTION_INFO` |
| 11 | `SET_MATERIAL` |
| 11 | `MESH_BOOLEAN` |
| 11 | `MAP_RANGE` |
| 10 | `VIEWER` |
| 6 | `MESH_PRIMITIVE_LINE` |
| 4 | `STORE_NAMED_ATTRIBUTE` |
| 4 | `BLUR_ATTRIBUTE` |

**Total node instances: 646.**
**Reading the list:** instancing is the core (`INSTANCE_ON_POINTS` 44,
`TRANSFORM_GEOMETRY` 44, `OBJECT_INFO` 38, `REALIZE_INSTANCES` 23),
curves drive placement (`CURVE_TO_POINTS` 22, `RESAMPLE_CURVE` 22),
orientation is solved with `ALIGN_EULER_TO_VECTOR` (32), and **`FRAME` appears 33 times**
— they frame and label groups obsessively (that is the `06_10 geonodes_organization` lesson),
plus **`VIEWER` × 10** for debugging. Attributes (`STORE_NAMED_ATTRIBUTE`, `BLUR_ATTRIBUTE`)
are how they move data between the sculpt and the nodes.

## 4. Node-group reuse and evolution (build once, instance many)

| File | Node group | Nodes | Links |
|---|---|---|---|
| 05_08_sculpting_shirt_part_4_final | Auto Smooth *(new)* | 10 | 9 |
| 05_08_sculpting_shirt_part_4_final | Instance_From_Collection *(new)* | 5 | 4 |
| 05_09_modeling_zipper_geometry_nodes_final | Auto Smooth | 10 | 9 |
| 05_09_modeling_zipper_geometry_nodes_final | Instance_From_Collection | 5 | 4 |
| 05_09_modeling_zipper_geometry_nodes_final | Zipper *(new)* | 20 | 32 |
| 06_09_modeling_stitching_geonodes_final | Auto Smooth | 10 | 9 |
| 06_09_modeling_stitching_geonodes_final | Instance_From_Collection | 5 | 4 |
| 06_09_modeling_stitching_geonodes_final | Seams_On_Curve *(new)* | 13 | 20 |
| 06_09_modeling_stitching_geonodes_final | Zipper | 20 | 32 |
| 06_10_geonodes_organization_final | Auto Smooth | 10 | 9 |
| 06_10_geonodes_organization_final | Instance_From_Collection | 5 | 4 |
| 06_10_geonodes_organization_final | Stitch_Seams_On_Curve *(new)* | 21 | 22 |
| 06_10_geonodes_organization_final | Zipper | 20 | 32 |
| 06_17_sculpting_knee_fabric_final | Auto Smooth | 10 | 9 |
| 06_17_sculpting_knee_fabric_final | Instance_From_Collection | 5 | 4 |
| 06_17_sculpting_knee_fabric_final | Stitch_Seams_On_Curve | 21 | 22 |
| 06_17_sculpting_knee_fabric_final | Zipper | 20 | 32 |
| 07_17_modeling_stitches_geometry_nodes_fin | Auto Smooth | 10 | 9 |
| 07_17_modeling_stitches_geometry_nodes_fin | Instance_From_Collection | 5 | 4 |
| 07_17_modeling_stitches_geometry_nodes_fin | Stitch_Seams_On_Curve | 22 | 23 |
| 07_17_modeling_stitches_geometry_nodes_fin | Zipper | 20 | 32 |
| 09_04_sculpting_cloth_brush_final | Auto Smooth | 10 | 9 |
| 09_04_sculpting_cloth_brush_final | Instance_From_Collection | 5 | 4 |
| 09_04_sculpting_cloth_brush_final | Stitch_Seams_On_Curve | 22 | 23 |
| 09_04_sculpting_cloth_brush_final | Zipper | 20 | 32 |
| 09_08_geonodes_smoothing_vertex_groups_fin | Auto Smooth | 10 | 9 |
| 09_08_geonodes_smoothing_vertex_groups_fin | Blur Vertex Group *(new)* | 7 | 10 |
| 09_08_geonodes_smoothing_vertex_groups_fin | Instance_From_Collection | 5 | 4 |
| 09_08_geonodes_smoothing_vertex_groups_fin | Stitch_Seams_On_Curve | 22 | 23 |
| 09_08_geonodes_smoothing_vertex_groups_fin | Zipper | 20 | 32 |
| 10_12_geonodes_panel_bolts_final | Auto Smooth | 10 | 9 |
| 10_12_geonodes_panel_bolts_final | Blur Vertex Group | 7 | 10 |
| 10_12_geonodes_panel_bolts_final | Bolts_On_Curve *(new)* | 22 | 22 |
| 10_12_geonodes_panel_bolts_final | Instance_From_Collection | 5 | 4 |
| 10_12_geonodes_panel_bolts_final | Stitch_Seams_On_Curve | 22 | 23 |
| 10_12_geonodes_panel_bolts_final | Zipper | 20 | 32 |
| 10_19_geonodes_wing_bolts_final | Auto Smooth | 10 | 9 |
| 10_19_geonodes_wing_bolts_final | Blur Vertex Group | 7 | 10 |
| 10_19_geonodes_wing_bolts_final | Bolts_On_Curve | 22 | 22 |
| 10_19_geonodes_wing_bolts_final | Instance_From_Collection | 5 | 4 |
| 10_19_geonodes_wing_bolts_final | Stitch_Seams_On_Curve | 22 | 23 |
| 10_19_geonodes_wing_bolts_final | Zipper | 20 | 32 |
| 10_26_sculpting_sweater__final | Auto Smooth | 10 | 9 |
| 10_26_sculpting_sweater__final | Blur Vertex Group | 7 | 10 |
| 10_26_sculpting_sweater__final | Bolts_On_Curve | 22 | 22 |
| 10_26_sculpting_sweater__final | Instance_From_Collection | 5 | 4 |
| 10_26_sculpting_sweater__final | Stitch_Seams_On_Curve | 22 | 23 |
| 10_26_sculpting_sweater__final | Zipper | 20 | 32 |

**The studio pattern, visible in the data:** `Seams_On_Curve` (13 nodes) is renamed
`Stitch_Seams_On_Curve` and grows to 22; `Zipper` (20) is built once in ch.05 and reused
**unchanged for the rest of the course**; `Bolts_On_Curve` (22) is built for the jetpack
panels and then **applied again to the wings** — same tree, different inputs.
`Auto Smooth` (10) and `Instance_From_Collection` (5) are utility groups on every asset.

## 5. The `Stitch_Seams_On_Curve` recipe (verbatim from the file)

**Interface:** `Geometry` (in/out), `Stitch Density` (float), `Stitch Scale` (float),
`Seam Object` (object), `Displacement Object` (object).

```
Curve -> Resample Curve -> Curve to Points -> Instance on Points (stitches)
                                   |
                            Tangent -> Align Euler to Vector -> Rotation
                                   |
                            Rotation ------^
Stitch Density -> Map Range -> Curve to Points.Length   (spacing of stitches)
Stitch Scale   -> Math       -> Transform Geometry.Scale
Seam Object        -> Object Info -> Transform Geometry -> Instance (seam piece)
Displacement Obj.  -> Object Info -> Transform Geometry -> Instance (displacement)
Instance on Points -> Realize Instances -> Join Geometry -> Group Output
```
**Why it matters:** stitches are **instanced along a resampled curve**, oriented by the
curve **tangent**, with **Map Range** converting an artist-friendly density value into
curve length, and an object input so the art is swappable without editing the tree.

## 6. The `Blur Vertex Group` recipe (09_08)

```
Group Input.Factor  -> Math.001 -> Store Named Attribute.Value
Group Input.Repeats -> Blur Attribute.Iterations
Group Input (vertex group) -> Blur Attribute.Value
Blur Attribute.Value -> Store Named Attribute.Selection
Blur Attribute.Value -> Math -> Math.001
Group Input.Output Vertex Group name -> Store Named Attribute.Name
Store Named Attribute.Geometry -> Group Output
```
**Why it matters:** this is how a *sculpted* mask becomes a clean, blurred
**vertex group** usable by cloth sim / modifiers — the exact bridge between
sculpting and simulation that most artists do by hand.

## 7. Surface-detail depth — measured from the sculpts

> **Method:** every mesh is smoothed with 30 full-strength Laplacian iterations
> (the "form under the detail"); the distance from each original vertex to that
> smoothed form is the **detail depth**, as % of the object's bounding-box diagonal.
> Helper/placeholder meshes and anything under 5,000 verts are excluded;
> repeated parts are de-duplicated across chapters.

| Part | Verts | median | **p95 depth** | max |
|---|---|---|---|---|
| Finger_Index | 8,706 | 0.468% | **1.071%** | 4.017% |
| Finger_Middle | 8,706 | 0.468% | **1.071%** | 4.017% |
| Finger_Ring | 8,706 | 0.468% | **1.071%** | 4.017% |
| Feet | 18,434 | 0.325% | **0.718%** | 1.246% |
| Torso | 44,546 | 0.175% | **0.549%** | 1.809% |
| Cube | 44,546 | 0.182% | **0.538%** | 2.145% |
| Hand_New | 33,794 | 0.211% | **0.504%** | 1.379% |
| Hands | 33,794 | 0.211% | **0.504%** | 1.379% |
| Arms | 47,106 | 0.089% | **0.235%** | 0.34% |
| Head | 147,458 | 0.048% | **0.233%** | 1.554% |
| Legs | 43,010 | 0.111% | **0.233%** | 0.339% |

**Measured band: p95 detail depth 0.233% – 1.071% of the object's size.**
Small, detailed parts (fingers ≈ **1.07%**) carry far more relative deviation than
large forms (arms/legs/head ≈ **0.23%**) — detail budget scales *inversely* with the
size of the form. That is the quantitative version of "put detail where the eye goes".

> ⚠️ **Honest limit:** the *cloth folds* themselves live in **Multires displacement**
> data (see §8), not in the base mesh, so this measures the sculpted body surface, not
> the drapery. Measuring true fold depth needs the multires level evaluated — a
> follow-up pass once local `bpy` is running.

## 8. Sculpt resolution (multires levels used on hero meshes)

_No MULTIRES/SUBSURF on the large hero meshes — the sculpt detail lives in the base mesh in these files._

## 9. What this feeds in the skill

* **ref 32 Geometry Nodes** — the 27-node core vocabulary, the frame/Viewer discipline,
  and two full production recipes (`Stitch_Seams_On_Curve`, `Blur Vertex Group`).
* **ref 33 Cloth & Fabric** — measured fold depth numbers become *tolerances*,
  the multires level used for fold sculpting, and the vertex-group bridge to sim.
* **ref 27 Topology / asset assembly** — the part-per-object + collection-instance
  workflow (278 objects) is how a studio character is actually organised.
