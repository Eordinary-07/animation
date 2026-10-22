# 33 — Cloth & Fabric (sculpted, simulated, and assembled)

> **Sources.** Production numbers parsed from the real CGBoost *Character Sculpting in
> Blender* `.blend` files (19 files, Blender 5.2.3 headless, `tools/blend_dump.py`) — full
> tables in `cgboost-analysis.md`; that course is *overwhelmingly a cloth course*, so the
> garment pipeline is the best-documented thing in the dataset.
> **Hogarth, *Dynamic Wrinkles and Drapery*** (145 pp) — **verified: the PDF is image-only
> (0 extractable characters across all 145 pages)**, so it is used as **plate reference via
> the rasterize method in ref 15**, not as quoted text. Fold categories below are read off
> the book's structure; anything stated as a *number* comes from the CGBoost files.
> **Fabric plates:** `studio-reference/fabric/` (spandex/athletic-fabric tension folds).
> **Prerequisites:** `27-mesh-topology-readiness.md` (clean mesh), `32-geometry-nodes-studio-patterns.md`
> (stitches, zippers, and the sculpt→sim vertex-group bridge).

## 0. What the production files actually say about cloth

The garment chapters dominate the course, and the object counts show a **build order that is
itself a method** — each chapter adds a garment layer, and the scene grows by adding parts,
never by merging them:

| Chapter file | Objects | Collections | Meshes | Total verts | What the chapter adds |
|---|---|---|---|---|---|
| 03_24_sculpting_the_hair_final | 80 | 11 | 72 | 493,632 | body + hair done |
| **05_08_sculpting_shirt_part_4_final** | 92 | 14 | 83 | 499,497 | **shirt** (+12 objects) |
| 05_09_modeling_zipper_geometry_nodes_final | 96 | 15 | 86 | 499,628 | **zipper** (GeoNodes) |
| 06_09_modeling_stitching_geonodes_final | 112 | 17 | 96 | 503,302 | **stitching** (GeoNodes) |
| 06_10_geonodes_organization_final | 112 | 17 | 96 | 503,302 | reorganized (no geometry change) |
| **06_17_sculpting_knee_fabric_final** | 124 | 17 | 108 | 503,690 | **knee fabric folds** |
| 07_17_modeling_stitches_geometry_nodes_final | 174 | 26 | 147 | 512,072 | **stitches across the suit** (+50 objs) |
| **09_04_sculpting_cloth_brush_final** | 204 | 30 | 175 | 515,718 | **cloth brush sculpting** |
| 09_08_geonodes_smoothing_vertex_groups_final | 206 | 30 | 177 | 516,325 | vertex-group blur (ref 32 §3) |
| 10_12_geonodes_panel_bolts_final | 235 | 31 | 202 | 521,215 | panel bolts |
| 10_19_geonodes_wing_bolts_final | 252 | 32 | 215 | 523,175 | wing bolts |
| **10_26_sculpting_sweater__final** | 278 | 45 | 228 | 532,002 | **sweater** (+26 objects) |

**Three readings that matter:**

1. **Nothing is ever merged.** 278 objects at the end. Shirt, zipper, stitching, knee fabric,
   sweater, bolts are **separate named parts**. A garment is an *assembly*, not a boolean
   union — so any piece can be re-sculpted, swapped, or hidden without touching the rest.
2. **Hardware and trim are procedural.** Zipper, stitching, and bolts are **Geometry Nodes**
   (ref 32), not modeled. That is why `07_17` can add **50 objects in one chapter** — they are
   instanced along curves, not placed by hand.
3. **`06_10` changed zero geometry.** Objects 112 → 112, verts 503,302 → 503,302. That chapter
   is pure **organization** — and it exists in a professional course as its own lesson.
   Treat tree/file organization as billable work, not as tidying (Vaughan p. 168: *"Lack of
   organization is the one problem that I've seen bring a production to a screeching halt more
   than any other issue."*).

---

## 1. The two ways cloth is made, and when each wins

The course uses **both**, and the choice follows what the shot needs:

| | **Sculpted cloth** | **Simulated cloth** |
|---|---|---|
| Used for (in the files) | shirt, knee fabric, sweater — every hero garment | not present in these files |
| Lives in | the mesh's own vertices | the Cloth modifier + cache |
| Strengths | total art direction; holds a pose on a still frame | reacts to motion automatically |
| Costs | does not move by itself | must be re-simmed and re-cached on any change |
| Verdict for a **posed/stylized hero** | ✅ this is what the studio files do | overkill |

**The deciding question:** does the garment have to **react** in this shot? For a hero
character in a beauty shot, a film, or any single frame, sculpted cloth is *better* — it is
art-directed, it is cheap at render time, and it never surprises you. Reach for simulation
when cloth must respond to movement over time (a cape in a run cycle, a dress in a spin).

**Measured consequence:** sculpting cloth into the mesh is exactly why the character ends at
**532,002 verts across 228 meshes**. That is the price, and on a modern workstation it is a
price worth paying for control.

## 2. Fold depth — the measured tolerance

From ref 27 §1.4 (30-pass Laplacian smoothing, deviation as % of the object's bounding-box
diagonal):

**Measured band: p95 detail depth 0.233 % → 1.071 % of the object's size.**

| Part | Verts | median | p95 | max |
|---|---|---|---|---|
| Fingers | 8,706 | 0.468 % | **1.071 %** | 4.017 % |
| Feet | 18,434 | 0.325 % | **0.718 %** | 1.246 % |
| Torso | 44,546 | 0.175 % | **0.549 %** | 1.809 % |
| Hands | 33,794 | 0.211 % | **0.504 %** | 1.379 % |
| Arms | 47,106 | 0.089 % | **0.235 %** | 0.340 % |
| Head | 147,458 | 0.048 % | **0.233 %** | 1.554 % |
| Legs | 43,010 | 0.111 % | **0.233 %** | 0.339 % |

**How to use the band for garment folds:**

- The **detail budget scales inversely with the size of the form.** Fingers carry ~1.07 %;
  arms, legs, and head ~0.23 %. Small forms spend their detail; large forms hold form.
- Applied to cloth: **fold depth on a large panel (a torso, a skirt) should sit near the low
  end of the band (~0.2–0.5 % of the object's size).** Deep folds belong on small, close-to-camera
  elements — cuffs, collars, knees, elbows — where the eye can read them.
- **A fold deeper than ~1 % of the object's size is a compression fold, not a drape fold** —
  that is a crease at a joint, and it should only exist where two surfaces are actually being
  pressed together.

> ⚠️ **Honest limit, restated.** These numbers measure the **sculpted body surface**, not the
> drapery: the cloth folds in these files live in the base mesh at the evaluated level, so the
> measurement does capture garment geometry on the clothed parts — but it cannot separate
> "fold" from "anatomy" on a part like the torso. True per-fold depth needs the multires
> displacement evaluated, which is blocked until local `bpy` runs (see §6).

## 3. Multires — and the surprise in the data

**The production hero meshes carry no Multiresolution modifier at all.** Verified: *"No
MULTIRES/SUBSURF on the large hero meshes — the sculpt detail lives in the base mesh in these
files."*

The only Multires in the entire dataset is in the two teaching exercises:

| File | Object | Levels | Render | Sculpt | Total |
|---|---|---|---|---|---|
| `05_04_exercise_1` | `Folds_01` | 3 | 3 | 0 | 3 |
| `05_04_exercise_2` | `Folds_02` | 3 | 3 | 1 | 3 |

**Read that as a workflow:** folds are **practiced** on a multires exercise (3 levels, sculpting
at level 0–1), but the **production garments are sculpted directly on dense base meshes**
(up to 147,458 verts for the head alone). The multires workflow is a *learning scaffold*, not
the shipping method.

**Blender:**
- **Exercise / learning path:** `Add Modifier → Multiresolution` (Generate section) → press
  **Subdivide** to add levels; set **Viewport**, **Render**, and **Sculpt** levels separately.
  Sculpt coarse folds at a low *Sculpt* level, then raise it for surface detail.
- **Production path (what the files do):** work on a dense mesh directly. Budget the vertex
  count per part (§2) and keep every garment a separate object (§0) so you can re-sculpt one
  piece without reloading the character.

## 4. The fold vocabulary (Hogarth, read from the plates)

Hogarth's *Dynamic Wrinkles and Drapery* is 145 pages of drawing with no extractable text —
it is a **plate book**, and it is used here the way ref 15 uses image books: you look at it.
Its organizing idea, and the one that maps onto Blender work:

**Folds are a record of force, not decoration.** A fold exists because something pushed,
pulled, or twisted the cloth. Identify the force and the fold type follows.

The vocabulary the book builds, and where each appears on a character:

| Fold type | Cause | Where you put it |
|---|---|---|
| **Compression / zigzag** | cloth pushed together along its length | inside of elbows, behind knees, under the buttock |
| **Tension / radiating** | cloth pulled from a single point | across a shoulder, from a button, at a knee cap |
| **Pipe / round** | cloth hanging under its own weight | sleeves, trouser legs, skirts, capes |
| **Spiral / corkscrew** | twist along a limb | sleeve around a rotated forearm, twisted torso |
| **Half-lock** | cloth folding over itself and reversing | waistbands, cuffs, collar rolls |
| **Diaper** | cloth caught between two points | crotch, armpit, between straps |
| **Inert / dead** | cloth lying on a surface, no force | hem resting on the ground, fabric over a chair |

**The rules that make folds read as real:**

1. **Folds radiate from their cause.** Every fold points back to the point of tension or the
   line of compression. Folds that wander independently read as noise.
2. **Compression side gets tight, many, small folds; tension side gets few, long, smooth
   ones.** This is the same law as ref 28 §11's compression-side check and ref 27 §1.3's
   kneepad law — the compression side of a joint must have **smaller surface area** than the
   outside, which is exactly why it shows tight folds.
3. **Folds cross the form, they do not run along it** — except on pipe folds, which follow the
   hang direction.
4. **Fabric type changes everything.** The plates in `studio-reference/fabric/` show athletic
   spandex: **many small, tight, high-frequency tension folds**, because the material is thin,
   stretched, and clings. Heavy wool gives few, broad, soft folds. **Decide the material before
   you sculpt a single fold.**

**Blender (sculpting folds):** Sculpt mode. Use **Cloth** brush / **Cloth Filter** for
simulation-backed fold generation, then **Crease** for compression lines, **Smooth** to
control the tension side, and **Snake Hook** to pull broad pipe folds. Work at a low strength
and build up — a fold carved in one stroke looks carved.

## 5. Trim, hardware, and seams — all procedural

Everything on the surface of the cloth is instanced, not modeled (ref 32):

- **Stitching** — `Stitch_Seams_On_Curve`: stitches instanced along a resampled curve,
  oriented by tangent, density exposed as a 0–1 knob. Build once, reuse on every seam.
- **Zippers** — `Zipper` (20 nodes, 32 links): built in chapter 05, **reused unchanged through
  chapter 10+**.
- **Bolts / eyelets / panels** — `Bolts_On_Curve` (22 nodes): built for jetpack panels, then
  applied unchanged to the **wings**. Same tree, different inputs.

**The rule:** if a garment element repeats more than a handful of times, it is a Geometry
Nodes group driven by a curve. That is how `07_17` added 50 objects in a single chapter.

## 6. The sculpt → simulation bridge

When a garment *does* need to simulate, the handoff is the `Blur Vertex Group` group from
ref 32 §3: a hand-sculpted or painted mask is noisy, and sims behave badly on noisy masks.

```
sculpted mask -> Blur Attribute (iterations) -> Store Named Attribute -> named vertex group
                                                                          |
                                          Cloth modifier -> Shape -> Pin Group
```

The Cloth modifier's **Pin Group** wants a *clean, smooth* mask. Blur it first — that is what
the 7-node group exists for, and it is why `09_08` (vertex-group smoothing) sits right before
the bolt/sweater chapters in the course.

**Blender (Cloth setup):** `Physics → Cloth`. Set **Pin Group** to your blurred group;
enable **Collision** on the body (`Physics → Collision`); raise **Quality Steps** (start at 5–8)
until the cloth stops tunneling; enable **Self Collision** only when the garment folds onto
itself. Bake the cache (`Cache → Bake`) before rendering, and **re-bake after any geometry
change** — a stale cache is the most common cloth bug.

## 7. Known follow-up (honest status)

**True per-fold depth is not yet measured.** It requires evaluating Multires displacement in
the two exercise files, which needs `bpy` — and local `bpy` is currently **broken in this
sandbox** (`ImportError: libXrender.so.1`; the bundled libs don't ship it and there's no root
to install it). The CI-with-Blender route works and is how everything above was measured; this
particular pass has not been run yet. §2's numbers are the valid substitute meanwhile.

## 8. Readiness checklist

```
ASSEMBLY
[ ] Every garment is a separate named object - nothing booleaned or merged
[ ] Parts organized into collections; placeholders swapped for real geometry
[ ] Trim/hardware (stitches, zipper, bolts) is Geometry Nodes on curves
[ ] Reusable groups reused UNCHANGED (Zipper: built once, never edited)

FOLD CRAFT
[ ] Fabric type decided BEFORE sculpting (spandex = many tight folds; wool = few broad)
[ ] Every fold traces back to a force: compression, tension, twist, or hang
[ ] Compression side: many small tight folds. Tension side: few long smooth ones
[ ] Fold depth inside the measured band: ~0.2-1.0% of object size; >1% only at
    true compression creases
[ ] Folds radiate from their cause; none wander independently

TECHNIQUE
[ ] Multires only as a learning scaffold - production sculpts on dense base meshes
[ ] Sculpt at low strength, building up; Smooth used to control the tension side
[ ] Cloth brush / filter used for the base pass, hand-work for the read

SIMULATION (only if the garment must react)
[ ] Pin Group is a BLURRED vertex group (Blur Attribute first, ref 32 §3)
[ ] Collision enabled on the body
[ ] Quality Steps raised until no tunneling (start 5-8)
[ ] Cache baked; re-baked after any geometry change

VERIFY
[ ] Hide one garment layer: does the character still read correctly underneath?
[ ] Re-draw a seam curve: does the stitching follow without rework?
[ ] Compare fold scale against the measured band in §2
```
