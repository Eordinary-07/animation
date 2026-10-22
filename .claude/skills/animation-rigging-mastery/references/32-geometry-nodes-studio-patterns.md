# 32 — Geometry Nodes Studio Patterns

> **Sources.** Every number and recipe in this file was **parsed out of real production
> `.blend` files** from the CGBoost *Master 3D Characters* course with `tools/blend_dump.py`
> under Blender 5.2 — 19 files, 12 of them carrying node groups. Full tables in
> `cgboost-analysis.md`. Nothing here is recalled or invented; where a number appears, it is
> a count of actual nodes in an actual shipping file.
> Supporting craft: **Hogarth, *Dynamic Wrinkles and Drapery*** (145 pp) for the fold
> language; **Vaughan, *Digital Modeling*** p. 168 *Clean Modeling* for the naming and
> organization discipline.

## 0. The headline number

**646 node instances across 27 node types** in the course's production files. That is the
whole vocabulary. You do not need hundreds of nodes — you need about two dozen, arranged
right. Here is the complete census, in usage order:

| Uses | Node | Family | What it is doing there |
|---|---|---|---|
| 94 | `GROUP_INPUT` | interface | **the most-used node in the file set** — every group is a reusable *tool with knobs* |
| 59 | `MATH` | utility | scaling, remapping, driving instance transforms |
| 48 | `GROUP_OUTPUT` | interface | — |
| 44 | `INSTANCE_ON_POINTS` | instancing | placing copies on a point cloud |
| 44 | `TRANSFORM_GEOMETRY` | instancing | moving/rotating/scaling what was instanced |
| 38 | `OBJECT_INFO` | input | pulling a swappable art object into the tree |
| 33 | **`FRAME`** | layout | **labelling and boxing groups — 5% of all nodes are documentation** |
| 32 | `ALIGN_EULER_TO_VECTOR` | rotation | orienting instances to a curve tangent or surface normal |
| 23 | `REALIZE_INSTANCES` | instancing | converting instances to real geometry (for boolean, deform, export) |
| 22 | `SET_SHADE_SMOOTH` | shading | — |
| 22 | `RESAMPLE_CURVE` | curve | the density/quality knob on every curve-driven effect |
| 22 | `CURVE_TO_POINTS` | curve | turning a curve into the points you instance onto |
| 22 | `JOIN_GEOMETRY` | combine | merging branches before output |
| 20 | `COMBINE_XYZ` | vector | building vectors from separate artist-facing floats |
| 11 | `MESH_EDGE_ANGLE` | input | finding creases/folds **by geometry, not by hand** |
| 11 | `INPUT_EDGE_SMOOTH` | input | reading the sculpt's own smooth/sharp marking |
| 11 | `INPUT_SHADE_SMOOTH` | input | — |
| 11 | `BOOLEAN_MATH` | logic | — |
| 11 | `COMPARE` | logic | selecting where an effect applies |
| 11 | `COLLECTION_INFO` | input | pulling a whole **collection** of variants |
| 11 | `SET_MATERIAL` | shading | — |
| 11 | `MESH_BOOLEAN` | mesh | — |
| 11 | `MAP_RANGE` | utility | converting an artist-friendly 0–1 knob into a real unit |
| 10 | **`VIEWER`** | debug | **debugging is 1.5% of the tree and they leave it in** |
| 6 | `MESH_PRIMITIVE_LINE` | primitive | generating stitch/strand geometry |
| 4 | `STORE_NAMED_ATTRIBUTE` | attribute | writing data back onto the mesh |
| 4 | `BLUR_ATTRIBUTE` | attribute | smoothing data across the surface |

**Read the census as a workflow, in four families:**

1. **Instancing is the core.** `INSTANCE_ON_POINTS` (44) + `TRANSFORM_GEOMETRY` (44) +
   `OBJECT_INFO` (38) + `REALIZE_INSTANCES` (23) = **149 instances, 23% of everything.** They
   do not model repeated detail; they place it.
2. **Curves drive placement.** `CURVE_TO_POINTS` (22) + `RESAMPLE_CURVE` (22) — a curve is
   drawn where the detail goes, and the nodes follow it.
3. **Orientation is solved, not fiddled.** `ALIGN_EULER_TO_VECTOR` (32) — instances are
   aligned to the curve's **tangent** rather than hand-rotated.
4. **Attributes carry data between departments.** `STORE_NAMED_ATTRIBUTE` +
   `BLUR_ATTRIBUTE` + the two `INPUT_*_SMOOTH` nodes — this is how a *sculpted* mask becomes
   data the tree can act on (§3).

**The two rows that are craft, not plumbing:** `FRAME` at 33 uses and `VIEWER` at 10. A
professional tree is **labelled and debuggable**; those 43 nodes are the difference between a
tree you can hand to someone and a tree only you can open.

---

## 1. The five reusable groups — the actual studio pattern

Only **six** distinct node groups exist across all 12 files. They are not built per-asset;
they are built once and carried forward. This table is the whole reuse story:

| Group | Nodes | Links | First appears | Reused in | Notes |
|---|---|---|---|---|---|
| `Auto Smooth` | 10 | 9 | 05_08 | **all 12 files** | utility, never edited again |
| `Instance_From_Collection` | 5 | 4 | 05_08 | **all 12 files** | utility, never edited again |
| `Zipper` | 20 | 32 | 05_09 | **11 files** | built once, **unchanged to the end** |
| `Seams_On_Curve` → `Stitch_Seams_On_Curve` | 13 → 22 | 20 → 23 | 06_09 | **9 files** | renamed then grown |
| `Bolts_On_Curve` | 22 | 22 | 10_12 | 3 files | built for jetpack panels, **re-applied to wings** |
| `Blur Vertex Group` | 7 | 10 | 09_08 | 3 files | the sculpt→simulation bridge |

**The pattern, stated once:**

- **`Zipper` is the model.** 20 nodes built in chapter 05, then reused **completely unchanged
  for the remaining 20+ chapters.** That is the goal for every group you build: *done means
  done.*
- **Groups evolve by renaming, not rewriting.** `Seams_On_Curve` (13 nodes) is renamed
  `Stitch_Seams_On_Curve` and grows to 22 nodes — the rename marks a new capability, and the
  growth is 9 nodes over 5 chapters, not a rebuild.
- **A group built for one asset gets a second job.** `Bolts_On_Curve` is built for jetpack
  panels and then applied **unchanged to the wings** — same tree, different inputs. That is
  the payoff of putting everything on the group interface.
- **`GROUP_INPUT` being the single most-used node (94) is the proof.** They externalize every
  knob. If a value might change, it is on the interface, not buried in a node.

**Blender:** `Add → Group → Geometry Nodes` to create; select the group and press `Tab` to
enter/exit. Promote a value to the interface by dragging a socket to the empty **Group Input**
node, or press `F2`-rename the group in the modifier. In Blender 5.x the interface is edited
in the sidebar's **Group** tab (`N`), where you set defaults, min/max, and tooltips.

---

## 2. `Stitch_Seams_On_Curve` — the recipe, verbatim from the file

**Interface:** `Geometry` (in/out) · `Stitch Density` (float) · `Stitch Scale` (float) ·
`Seam Object` (object) · `Displacement Object` (object).

```
Curve -> Resample Curve -> Curve to Points -> Instance on Points      (the stitches)
                                   |
                            Tangent -> Align Euler to Vector -> Rotation
                                   |
                            Rotation ------^
Stitch Density -> Map Range  -> Curve to Points.Length     (spacing of stitches)
Stitch Scale   -> Math        -> Transform Geometry.Scale
Seam Object        -> Object Info -> Transform Geometry -> Instance   (seam piece)
Displacement Obj.  -> Object Info -> Transform Geometry -> Instance   (displacement)
Instance on Points -> Realize Instances -> Join Geometry -> Group Output
```

**Four decisions in that tree are the whole lesson:**

1. **Stitches are instanced along a resampled curve** — nobody models 400 stitches.
2. **Orientation comes from the curve tangent** via `Align Euler to Vector`. Instances follow
   the seam direction automatically, so re-drawing the curve re-does the work.
3. **`Map Range` converts an artist-friendly density into curve length.** The animator tweaks
   "0–1 more/less dense"; the tree turns it into actual spacing. Never expose raw units when
   you can expose intent.
4. **The art is an object input, not built in.** `Seam Object` and `Displacement Object` are
   `OBJECT_INFO` sockets — swap the stitch model without opening the tree.

**This same tree is `Bolts_On_Curve`.** Change what you instance and what curve it follows;
the structure is identical. That is why one group served both the jetpack and the wings.

**Blender, from scratch:** add a **Geometry Nodes** modifier → `New`. Inside:
`Add → Curve → Resample Curve` (set *Count* or *Length*) → `Add → Curve → Curve to Points` →
`Add → Instances → Instance on Points`. For orientation, `Add → Utilities → Rotation → Align
Euler to Vector` with the curve's **Tangent** as the vector, fed into
`Add → Instances → Transform Geometry`. Remap your density knob with
`Add → Utilities → Map Range`. Feed the swappable art with `Add → Input → Object Info`,
enable **As Instance**. Finish with `Realize Instances` → `Join Geometry` → `Group Output`.

---

## 3. `Blur Vertex Group` — the sculpt → simulation bridge

**7 nodes, 10 links.** This is the most portable trick in the whole set, and it solves a
problem almost everyone does by hand.

```
Group Input.Factor  -> Math.001 -> Store Named Attribute.Value
Group Input.Repeats -> Blur Attribute.Iterations
Group Input (vertex group) -> Blur Attribute.Value
Blur Attribute.Value -> Store Named Attribute.Selection
Blur Attribute.Value -> Math -> Math.001
Group Input.Output Vertex Group name -> Store Named Attribute.Name
Store Named Attribute.Geometry -> Group Output
```

**Why it matters:** a mask painted or sculpted by hand is noisy. Cloth sims, displacement, and
modifiers all behave badly on noisy masks. This group converts a *sculpted* mask into a
clean, blurred **vertex group** — with the blur amount and iteration count exposed as knobs —
and writes it back under a name you choose.

**Where it is used in the course:** `09_08` (geonodes smoothing vertex groups), then carried
into `10_12` (panel bolts) and `10_19` (wing bolts) and `10_26` (sweater) — once it exists, it
is the standard way to get a clean mask.

**Blender:** `Add → Attribute → Blur Attribute` (set *Iterations*, feed your group into
*Value*), then `Add → Attribute → Store Named Attribute` to write the result under a new name.
The receiving side (a Cloth modifier's *Pin Group*, a Displace modifier's *Vertex Group*) then
selects that new named attribute. **This is the bridge between sculpting and simulation.**

---

## 4. Curve-driven placement — the one pattern worth memorizing

Every placement group in the census (`Stitch_Seams_On_Curve`, `Bolts_On_Curve`,
`Instance_From_Collection`) is the same five-step shape:

1. **Draw a curve** where the detail should go. The curve is the artistic decision; it is
   editable forever.
2. **Resample** it — this is the quality/density knob, and it belongs on the interface.
3. **Curve to Points** — turn it into a point cloud.
4. **Instance on Points** — place your art.
5. **Align Euler to Vector** — orient each instance to the curve's tangent.

**Why curves and not the mesh:** the curve survives changes to the underlying geometry. Re-model
the panel and the bolts follow. Re-model the seam and the stitches follow. If you instance off
mesh vertices instead, every re-topology (ref 27) destroys the placement.

**Collection instancing for variation** (`COLLECTION_INFO`, 11 uses; `Instance_From_Collection`
in all 12 files): instance a *collection* rather than a single object and each point can pick a
different variant — sizes, damages, stitch types. One tree, unlimited variation, and adding a
variant means dropping an object into a collection, not editing nodes.

---

## 5. Finding folds by geometry, not by hand

`MESH_EDGE_ANGLE` (11), `INPUT_EDGE_SMOOTH` (11), `INPUT_SHADE_SMOOTH` (11), `COMPARE` (11),
`MESH_BOOLEAN` (11), `SET_MATERIAL` (11) all appear **eleven times each** — the same count,
which means they are one repeated cluster, not six habits. That cluster reads the mesh's own
geometry to decide where an effect applies:

- **`Mesh Edge Angle`** → find creases by angle. This is *Hogarth's fold language turned into
  a query*: the tight folds are the high-angle edges.
- **`Compare`** → threshold that angle to select only the creases.
- **`Set Material` / `Mesh Boolean`** → act on the selection.

**Why this matters for cloth (ref 33):** you do not paint where wear, darker creases, or
stitching go — you **derive** it from the fold angle. When the sculpt changes, the derived mask
updates itself.

**Blender:** `Add → Input → Mesh → Edge Angle`, then `Add → Utilities → Compare` to threshold
it, feeding a `Set Material` node or a `Store Named Attribute` you can use downstream.

---

## 6. Tree hygiene — what the 33 `FRAME`s and 10 `VIEWER`s are telling you

Two rows of the census are pure professionalism, and they are easy to skip:

- **`FRAME` × 33 (5% of all nodes).** Box and label every functional block
  (`Add → Layout → Frame`, or `Ctrl+J` over a selection). A tree with labelled regions is a
  tree a colleague can open; an unlabelled one is a personal artifact.
- **`VIEWER` × 10.** They keep the debug probes in. `Viewer` shows any value in the
  spreadsheet (`Spreadsheet` editor → *Geometry* → the `viewer` column), which is how you
  debug a tree — see what the data is, not what you assume it is.

**Naming** (Vaughan p. 168, and it is why `Seams_On_Curve` could be renamed cleanly):
*"avoid using spaces… Opt for an underscore (_), which is much easier to see and doesn't cause
issues later down the production line."* Name groups by **what they do**
(`Instance_From_Collection`, `Blur Vertex Group`), not by what they were first used for — that
is precisely what let `Bolts_On_Curve` move from jetpack panels to wings.

---

## 7. Performance rules that follow from the data

- **Stay instanced as long as possible.** `REALIZE_INSTANCES` appears only 23 times against
  44 `INSTANCE_ON_POINTS` — they instance, and only realize when they genuinely must (for a
  boolean, a deformation, or export). Realizing early throws away the memory win.
- **Realize once, at the end.** `Instance on Points → Realize Instances → Join Geometry` is
  the closing sequence in the recipe (§2). Do not realize mid-tree.
- **Put density on the interface, not in the node.** `Resample Curve` count and `Map Range`
  belong on `Group Input` so a heavy tree can be lightened for viewport work without editing
  it.
- **Frames and viewers cost nothing.** Do not strip them for performance; strip them never.

---

## 8. Readiness checklist

```
STRUCTURE
[ ] Everything on the group interface (GROUP_INPUT is your most-used node)
[ ] One group = one job, named by what it DOES, not where it was first used
[ ] Reused unchanged across assets - if you are rebuilding it, it is not finished
[ ] Frames + labels on every functional block
[ ] Viewer probes left in for debugging

PLACEMENT
[ ] Detail instanced along a RESAMPLED CURVE, not baked onto vertices
[ ] Orientation from Align Euler to Vector + curve tangent
[ ] Art provided as an Object Info / Collection Info input (swappable)
[ ] Density exposed as an artist-friendly 0-1 knob via Map Range

ATTRIBUTES
[ ] Masks derived from geometry (Mesh Edge Angle + Compare) where possible
[ ] Sculpted masks blurred through Blur Attribute before any sim reads them
[ ] Named attributes written back with Store Named Attribute under a clear name

PERFORMANCE
[ ] Instances realized only once, at the end
[ ] Resample count on the interface for viewport lightening
[ ] No realize-before-boolean mid-tree

VERIFY
[ ] Re-draw the source curve: does the detail follow without rework?
[ ] Swap the Object Info art: does the whole look change without editing nodes?
```

## 9. The rule

The census says it better than any principle could: **six groups and twenty-seven node types
produced an entire course's worth of production assets.** The craft is not in knowing more
nodes — it is in building a small group so well that you never open it again.

`Zipper`: 20 nodes, built once, never edited across 11 files. That is the target.
