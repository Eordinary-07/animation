# 35 — Modeling, Sculpting & Anatomy

> **Sources.**
> **Zarins, *Anatomy for Sculptors*** (228 pp) — **image-only: 0 extractable characters across all
> 228 pages**. Used here as **plate reference via the rasterize method (ref 15 §3)** — you look at
> the muscle/origin-insertion plates, you do not quote them. No page numbers are attributed to
> Zarins text because none can be read.
> **Hogarth, *Dynamic Wrinkles and Drapery*** (145 pp) — **image-only: 0 extractable characters
> across all 145 pages**. Same treatment: plate reference for fold and form, no quoted text.
> **William Vaughan, *Digital Modeling*** — p. 63 *topology + cross-department communication*,
> p. 155–156 *texture displacement for hair/detail*, p. 157 *dynamics (soft/rigid body)*,
> index entry “head model, 213–237”.
> **CGBoost production `.blend` files** — measured object/vert counts from `cgboost-analysis.md`.
> **Prerequisite:** ref 27 Mesh & Topology Readiness must PASS before any sculpt or retopo work.

## 0. Why this chapter exists — anatomy is a plate, not a formula

Zarins and Hogarth are **plate books** — they teach by image, not by sentence. That changes how
you use them:

- **You do not memorize Zarins.** You keep the origin/insertion and muscle-plate pages open
  next to Blender and *check against them* while you sculpt the shoulder, the hip, the brow.
- **You do not quote Hogarth.** You hold the fold plates against your sculpted cloth and ask,
  “Does this compression zone read the way the plate shows it?”
- **Every claim about “anatomy says…” in this chapter must be verifiable against a plate you
  can point to.** If you cannot point to it, it is not in the chapter.

This is the honest way to use image-only books. The skill does not fake quotes from pages it
cannot read.

## 1. The anatomy-to-topology pipeline

The order that actually works in production:

1. **Block the form with anatomy plates open.** Use Zarins origin/insertion plates to place the
   major muscle masses on the blockout — deltoid, pectoral, gluteal, quadriceps. Do not refine
   until the big shapes read correctly against the plates.
2. **Sculpt the secondary forms.** Brow ridge, zygomatic, knee cap, elbow point — the landmarks
   that make a face read as *this* face, not a generic one.
3. **Retopologize for animation.** The high-res sculpt is reference; the animatable mesh is built
   over it with clean quads and edge loops (ref 27).
4. **Validate against the plates again.** Hide the sculpt, show the retopo mesh, check the
   silhouette and the joint landmarks one more time.

**Vaughan p. 63**, on why this order matters:

> *"The best 3D modelers can all rig. This gives them the understanding of where to put
> accurate edge loops."*

Anatomy tells you *where the form goes*. Topology tells you *how it moves*. You need both,
in that order.

## 2. Sculpt workflow — multires vs dyntopo vs base-mesh density

From the measured CGBoost data (`cgboost-analysis.md` §7–§8):

**The production hero meshes carry NO Multiresolution modifier.** Verified:

> *"No MULTIRES/SUBSURF on the large hero meshes — the sculpt detail lives in the base mesh in
> these files."*

The only Multires in the dataset is in the two teaching exercises (`Folds_01`, `Folds_02` at
3 levels) — multires is a **learning scaffold**, not the shipping method. Production sculpts on
dense base meshes: the head alone is 147,458 verts; the full character ends at ~532k verts
across 228 meshes.

**Detail-depth tolerance (measured, ref 27 §1.4 / ref 33 §2):**

| Detail level | p95 depth | Where it goes |
|---|---|---|
| High | ~1.071 % of object size | fingers, small facial features, tight folds |
| Medium | ~0.5–0.55 % | hands, feet, torso panels |
| Low | ~0.23–0.235 % | arms, legs, head (large forms) |

**Rule:** detail budget scales *inversely* with the size of the form. Small forms spend their
detail; large forms hold form. A fold deeper than ~1 % of the object's size is a compression
crease at a joint, not a drape fold — it belongs only where two surfaces press together.

**Blender:**
- **Base-mesh sculpt:** Sculpt mode, build detail directly on the dense mesh. No multires on
  hero assets.
- **Dyntopo:** only for blockout and detail pass where topology doesn't matter yet. Convert to
  clean quad topology before rigging (ref 27).
- **Multires:** use only to *learn* fold sculpting on the exercise files, then bake the result
  down to the base mesh for production.

## 3. Anatomy landmarks that drive topology

These are the places where anatomy *dictates* edge-loop placement — not suggestions, requirements:

| Landmark | Topology requirement | Source |
|---|---|---|
| Hairline / temple | Edge loop around the boundary (rule of three: one segment deforms, two support) | ref 27 §1.2, Vaughan p.179 |
| Orbicularis oris (mouth) | Concentric loops trace the muscle so vertices move with it | ref 27 §1.3 |
| Pectoral lines on torso | Loops follow the muscle grain | ref 27 §1.3 |
| Crown of head | Pole (5+ edges) goes here — low-deformation zone | ref 27 §1.5 |
| Scapula center / armpit | Poles in low-deformation zones, never on joint lines | ref 27 §1.5 |
| Compression side of joints (inside elbow, behind knee, under buttock) | Smaller surface area than the extension side | ref 27 §1.3 (kneepad law) |
| Nostrils, eyelids | Rule-of-three bands; too many loops pinch | ref 27 §1.7 counter-law |

**Zarins plates to check against:** origin/insertion for each muscle above. If your topology
does not let the muscle plate's shape deform correctly, the topology is wrong — not the plate.

## 4. Proportion and the head model

**Vaughan index:** “head model, 213–237” — the head-modeling chapter. The practical takeaway
for this skill:

- Block the head from anatomical proportions first (brow ridge, zygomatic, jaw angle, chin),
  then refine.
- The hairline loop is a deformation boundary — treat it like an eye or mouth loop (rule of
  three).
- No n-gons on the face or scalp (ref 27 §1.6) — n-gons triangulate unpredictably under
  subdivision and make the groomer's life miserable (ref 34).

## 5. Retopology for deformation — the hand-off rule

**The modeler's job is not done when the sculpt looks good.** It is done when the rigger can
skin it. Vaughan p. 63 again:

> *"The modeler sits between the concept artist and the artists doing the texturing and the
> rigging."*

**Hand-off checklist:**
- [ ] Quads dominate; triangles only in non-deforming static areas
- [ ] Edge loops around every joint (rule of three)
- [ ] Poles in low-deformation zones only
- [ ] No n-gons in deformable areas
- [ ] Manifold, watertight, welded vertices (ref 27 §2)
- [ ] Silhouette still matches the anatomy plates
- [ ] All transforms applied (`Ctrl+A → All Transforms`)

If the retopo fails any of these, it goes back to sculpt — not forward to rigging.

## 6. The sculpt → simulation bridge

When a sculpted element needs to simulate (cloth over the sculpt, hair on the sculpted head):

- The sculpted mask becomes a **vertex group** via ref 32's `Blur Vertex Group` — noisy
  hand-painted masks break sims; blur first.
- The vertex group feeds a **Pin Group** (cloth/soft body) or a **vertex-weight-driven**
  modifier.
- Re-bake the cache after *any* geometry change — a stale cache is the #1 sim bug.

## 7. The Gate — printable checklist

```
ANATOMY & FORM
[ ] Zarins/Hogarth plates open beside Blender during sculpting
[ ] Major muscle masses blocked against origin/insertion plates
[ ] Secondary landmarks (brow, zygomatic, knee cap, elbow) present
[ ] Silhouette matches the plates from all three orthographic views

SCULPT TECHNIQUE
[ ] Hero assets sculpted on dense base meshes, NO multires on shipping models
[ ] Detail depth inside the measured band: ~0.23–1.07% of object size
[ ] >1% depth only at true compression creases
[ ] Multires used only as a learning scaffold on exercise files

TOPOLOGY (ref 27 gate must also PASS)
[ ] Quads dominant; loops around every joint (rule of three)
[ ] Poles in low-deformation zones only (crown, scapula, armpit)
[ ] No n-gons in deformable areas (face, scalp, joints)
[ ] Watertight, welded, manifold (ref 27 §2)

RETORYPOLOGY HAND-OFF
[ ] Rigger can place bones without fighting the topology
[ ] Skinning weights will not need to be redone after a topology change
[ ] All transforms applied (Ctrl+A → All Transforms)

VERIFY
[ ] Hide sculpt, show retopo: form still reads correctly
[ ] Compare against plates one final time before freezing topology
```

## 8. Blender 5.x quick procedure index

| Task | Path |
|---|---|
| Sculpt on dense base mesh | Sculpt mode, no Multires modifier on hero assets |
| Learn fold sculpting | Add Modifier → Multiresolution → Subdivide (3 levels), then bake down |
| Check normals outward | Mesh → Normals → Recalculate Outside (`Shift+N`) |
| Merge duplicate vertices | Select All → `M → By Distance` |
| Find non-manifold | Select All by Trait → Non Manifold |
| Apply transforms | `Ctrl+A → All Transforms` |
| Retopo over sculpt | Shrinkwrap modifier + snapping, then delete shrinkwrap |
| Check edge flow | Wireframe overlay + loop select (`Alt`-click) |

## 9. The rule

Anatomy plates tell you what the body *is*. Topology tells you what it *does*. Build the form
against the plates, build the loops against the deformation, and never hand a sculpt to a
rigger that has not passed the Gate.
