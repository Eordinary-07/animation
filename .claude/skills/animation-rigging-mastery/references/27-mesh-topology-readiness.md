# 27 — Mesh & Topology Readiness (the gate before rigging)

> **The modeling canon** (all in this repo as PDFs, all text-verified — page numbers below are
> the book's own PDF pages):
> **William Vaughan, *Digital Modeling*** (434 pp) — ch. 4 *Fundamentals of a Digital Model*
> (p. 128 *Edges*, p. 129 *Polygonal Models*, p. 133 *Subdivision Surfaces*), ch. 6
> *Professional Modeling Practices* (p. 168 *Clean Modeling*, p. 169 *Polygon-count*,
> p. 174 *Topology*, p. 176 *Are you in the loop?*, p. 177 *Controlling polygon flow*,
> p. 178 *N-gons / four-point triangles*, **p. 179 *The rule of three***, p. 180 *Preparing a
> Model for Production*, p. 181 *Scale / Position / Final pass*, p. 182 *UV layout & seams*,
> p. 184 *T-pose*, p. 185 *Relaxed pose*).
> **Tina O'Hailey, *Rig It Right!*** (324 pp) — p. 18 *Basic Rules of Rigging* (Rule #1),
> **Appendix 2.A p. 56–58 *Edgeloops for Good Deformation***, p. 105 *Check Your Joint
> Rotational Axis*, p. 109 *Interactive Skinning*, p. 155–157 *Skinning*.
> **Uldis Zarins, *Anatomy for Sculptors*** (228 pp) and **Burne Hogarth, *Dynamic Wrinkles
> and Drapery*** (145 pp) — surface/anatomy reference (image-led, no text TOC).
> **CGBoost production `.blend` files** — 19 files parsed, measured numbers cited as
> *(measured)*; full report in `cgboost-analysis.md`.

## 0. Why this gate exists — O'Hailey's three laws

O'Hailey opens Appendix 2.A with the reason this chapter is not optional:

> **Rule #1: Edgeloops — a good or bad rig starts with the loops.** (p. 18)

Three laws, verbatim from p. 56–57:

1. *A model with bad topology cannot be rigged well.*
2. *A model with good topology that is rigged poorly cannot be animated well.*
3. *A model with bad topology that is also rigged poorly is a complete nightmare.*

And the line that kills the most common beginner mistake — evenly spaced quads:

> *"It isn't enough to have a model with quads evenly spread out across the surface like
> butter — they have to be in the right place and have to be designed to facilitate
> movement."* (p. 57)

**Definition** (p. 57): an edgeloop is *"a row of connected edges lined end to end, which
define a specific feature. This row of edges typically forms a loop, but does not have to."*

**Consequence for this skill:** topology is checked *before* any bone is placed. No rig work
begins until §8 Gate passes. A rig failure traced to geometry costs a full rebuild; the same
failure caught here costs one edit-mode pass.

---

## 1. Geometry & Topology

### 1.1 Quad-dominant topology
**Why:** quads subdivide predictably and deform evenly; triangles and n-gons pinch.

Vaughan, p. 177 (*Four-point perfection*): *"When modeling an area that will undergo heavy
deformation, you will get better results if you resist the urge to mix in any three-point
polygons where it may seem convenient and stick to using all four-point polygons (quads).
Three-point polys tend to cause pinching and strange smoothing errors in most cases."*

p. 178: *"N-gons—polygons with more than four points—are also known to cause pinching and
smoothing errors in areas with deformation, and they are not supported by all subdivision
algorithms… quads are superior for meshes that will deform while animated, and working
exclusively with quads should be the goal of every organic modeler."*

**The legal way to reduce count without breaking quad-only** (p. 178) — *four-point
triangles* (a.k.a. *pole polygons* / *diamond polygons*): quads shaped like a triangle or
diamond. *"These polygons not only help reduce poly-count, but can help define edge loops
within your mesh."*

**Blender:** count offenders in Edit Mode —
`Select → Select All by Trait → Faces by Sides`, then set *Number of Vertices = 3* (tris)
or *Type: Greater Than, 4* (n-gons). Repair tris that sit in deform zones by dissolving the
diagonal (`X → Dissolve Edge`, `Ctrl+X`) or by rotating the edge (§1.7).

*Where tris and n-gons are allowed:* p. 178 — *"try to use them in areas that won't deform or
be in plain sight."* Back of the head, underside of a prop, interior surfaces, anything that
never bends. Never on a joint line, never in the face.

### 1.2 Edge loops around joints — **the rule of three**
**Why:** concentric loops at elbows, knees, shoulders, hips let the joint bend without
collapsing. **The "≥3 loops per joint" figure has a source, and it is Vaughan p. 179:**

> *"Areas on a model that will have heavy deformations need an underlying structure that will
> support the shapes you have defined… it is a good idea to use three segments in areas that
> will deform heavily. I refer to this as the **rule of three**.*
> *The middle segment is where the deformation will take place, and the segments on either
> side support the mesh beyond the deformation."*

Vaughan's own list of rule-of-three areas (p. 179): **elbows, shoulders, knees, finger
joints, wrists, laugh lines on faces, and eyelids.**

So the loop is not a magic number — it is **three segments: one that bends, two that hold.**
That is the reason ≥3 works, and it is also the reason adding more eventually hurts (§1.7).

**Blender:** select a loop with `Alt+Click` on an edge; extend the band with
`Ctrl+Alt+Click` (loop select + grow) or `Select → Select Loops → Edge Loops`. Check every
rule-of-three area above for **at least three parallel rings** crossing the joint.

### 1.3 Edge flow follows anatomy — loops must *enclose* the bend
**Why:** this is the difference between a joint that wrinkles and a joint that collapses.

O'Hailey, p. 57–58, the finger test — the single most useful topology experiment in either
book. Three fingers, identical shape, identical rig, identical skinning, only the edgeloops
differ:

- **Finger A** — loops *straight up and down*, not contouring the bend. *"Note what happens
  when that finger is bent. The wide surface area, which was created by those straight
  edgeloops, gets pulled in and **collapses into a concave rubbery fold**."*
- **Finger B** — loops *"taper toward the area of the bend and widen on the knuckle. They
  enclose the area of maximum deformation."* Result: *"the smaller surface area creates a
  tighter wrinkle/bend on the finger."* Nothing else was changed.
- **Finger C** — adds a *"circle pad of edgeloops at the top for the knuckles… The center
  vertex was selected and chamfered."* This gives a flat area mimicking the fleshy pad on
  knuckles; O'Hailey uses the same *"little quad for elbows and patellas (knee caps)."*

Her kneepad analogy (p. 58) is the mental model to keep: kneepads that are plain cylinders
with wide bands behind the knee *"bunch up and have too much surface area to deal with"*,
while pads with *"a smaller surface area behind the knee than on the front will not bunch up
and bend better."*

**Read that as a rule:** on the *inside* (compression side) of every joint, the surface area
must be **smaller** than on the outside (extension side). Inside-of-elbow, behind-the-knee,
under-the-buttock, palm side of the fingers, under the chin — all tighter than the outside.

Vaughan's version of the same law (p. 176): edge loops *"can mimic major muscle groups,
produce more realistic-looking character models, and create more predictable deformations in
facial animation and posing"* — his Figure 6.5 highlights three sets of loops in the face that
exist purely to make facial animation predictable.

**Anatomy loops to build (the canonical set):** orbicularis oris around the mouth (the
textbook example — O'Hailey's Figure 2A.1 is literally a mouth loop), orbicularis oculi
around each eye, nasolabial / laugh lines, the pectoral sweep across the chest, the deltoid
cap over the shoulder, the lat/deltoid split at the armpit, the trapezius fan into the neck.
Sourced for sculpture from Zarins (*Anatomy for Sculptors*, 228 pp) and for compression
wrinkling from Hogarth (*Dynamic Wrinkles and Drapery*, 145 pp).

**Blender (Finger C's chamfered pad):** select the single center vertex at the knuckle,
`Ctrl+B` → bevel (works on vertices) → drag to open a small quad. Then `Ctrl+R` two rings
around it to complete the pad.

### 1.4 Appropriate density
**Why:** density is a *budget*, and it is spent where deformation happens.

Vaughan p. 169 — why to keep the count low at all: *"Fewer polygons equal fewer points,
which means fewer points to weight and assign to bones. It's also easier to create UV
textures on a low-poly, clean mesh."*

p. 174 — the hero rule: *"Objects that are seen up close are sometimes referred to as a hero
object and require far more detail and polygons than objects that sit off in the distance.
You wouldn't want a rock made up of 20,000 polygons if it will always be 20 yards from the
camera."* He labels the versions **Hero/Primary, Secondary, Tertiary** so the right LOD can be
swapped per shot.

p. 174 — the cardinal rule: *"Use as many polygons as needed, but not one polygon more than
that. The cardinal rule of professional modeling is less is always more."*

**Where the budget goes:** face, hands, and joints get density; forehead, shins, and other
static areas stay sparse and clean. This is not a guess — it is what the production files do.

**Measured** (CGBoost hero character scene `10_26_sculpting_sweater__final`, 278 objects,
532,002 verts total):

| Part | Verts | Detail depth, median | **p95** | max |
|---|---|---|---|---|
| Finger | 8,706 | 0.468 % | **1.071 %** | 4.017 % |
| Feet | 18,434 | 0.325 % | **0.718 %** | 1.246 % |
| Torso | 44,546 | 0.175 % | **0.549 %** | 1.809 % |
| Hand_New & Hands | 33,794 | 0.211 % | **0.504 %** | 1.379 % |
| Arms | 47,106 | 0.089 % | **0.235 %** | 0.340 % |
| Head | 147,458 | 0.048 % | **0.233 %** | 1.554 % |
| Legs | 43,010 | 0.111 % | **0.233 %** | 0.339 % |

*(Detail depth = deviation from a 30-pass Laplacian-smoothed version of the same mesh, as a %
of the object's bounding-box diagonal. Helpers, placeholders, and meshes under 5,000 verts
excluded; n = 11.)*

**The band to remember: p95 detail depth runs 0.233 % → 1.071 % of object size.** The
detail budget scales *inversely* with form size — fingers (≈1.07 %) carry about **4.6× the
relative deviation** of arms, legs, and head (≈0.23 %). Small forms spend their detail
budget; large forms hold form and spend almost nothing. The head is the exception on *raw*
count (147,458 verts — the densest single object) but the *flattest* in relative deviation,
because it must stay clean for facial deformation.

*Honest limit:* those numbers measure the sculpted **body surface**. Cloth folds live in
Multires displacement, not the base mesh — and **none of the production heroes carry Multires**
(only the two teaching files do: `Folds_01` levels 3 / render 3 / sculpt 0, `Folds_02`
levels 3 / render 3 / sculpt 1). See refs 32/33 for the fold side.

### 1.5 Pole placement
**Why:** a pole (a vertex where 5+ edges meet, or 3 on a subdivision cage) concentrates
deformation into a visible swirl.

Rule: poles belong in **low-deformation zones** — centre of the scapula, the armpit, the top
of the skull, the flat of the cheekbone. **Never on a joint line, never inside a rule-of-three
band, never in the middle of the face.**

O'Hailey's constructive use (p. 58) is the flip side: when you *want* a flat pad on a
knuckle, elbow, or patella, make the pole **on purpose** by chamfering a vertex into a quad
(§1.3, Finger C). Poles are not evil; *unplanned* poles on a bend line are.

**Blender:** vertex mode, `Select → Select All by Trait → Faces by Sides` won't find poles —
use the **Mesh Analysis / Statistics** overlay, or find them visually: enable
`Overlays → Geometry → Wireframe` and look for vertices where the fan count jumps. A 5-pole
reads as one vertex with five edges leaving it.

### 1.6 No n-gons in deformable areas
Covered in §1.1 (Vaughan p. 178). The added reason that makes it non-negotiable here: n-gons
are **not supported by all subdivision algorithms**, so an n-gon that looks fine under
Blender's Catmull-Clark can triangulate differently after export — the failure appears only
*after* the FBX round-trip test (§7.5), which is the most expensive place to discover it.

### 1.7 The counter-law — too many loops also pinches
Both books warn about overshooting, and this is what stops "more loops" from being free.

Vaughan p. 176: *"although loops are extremely powerful and you want to use enough to get the
shapes you're after, you need to be careful not to have too many loops. Too many can cause
pinching and unwanted creases in your object."* And p. 179: *"Too many segments or loops can
cause pinching in your mesh."*

**So the target is a band, not a maximum:** ≥3 segments to support the bend, but no more than
the shape needs. Judge it by posing, not by counting (§7).

**Blender — redirecting flow without moving points** (Vaughan p. 177 — SpinQuads / Flip Edge /
Spin Edge / Rotate Edge): select the shared edge between two quads, then the **Edge menu
(`Ctrl+E`) → Rotate Edge (CW / CCW)**, or `F3` search "Rotate Edge". *"These tools change the
dividing edge between two adjacent polygons by spinning (rotating) the edge, so that the two
ends of the edge attach to different points while leaving all of the points in the same
place."* p. 177 also notes the useful catch: *"after the third use of the tool, your edge will
end up where it started"* — there are only so many placements, so if three spins don't get you
there, the surrounding topology is wrong, not the edge.

---

## 2. Structural Integrity

Every item below breaks skinning, shading, or collision in a specific way. Fix them in this
order — cheap fixes first, because each one can expose the next.

| Check | What breaks if it fails | Blender procedure |
|---|---|---|
| **Manifold / watertight** | auto-weights leak through holes; non-manifold edges create weight spikes | Edit Mode → `Select → Select All by Trait → Non Manifold`. Everything selected must be an intentional boundary. |
| **Welded / merged** | duplicate verts split the surface; shading seams and deformation glitches | Edit Mode, `A` → `M → By Distance` (Mesh > Merge > By Distance). Raise *Distance* only until real verts start vanishing, then undo one step. |
| **Outward normals** | flips break lighting, skinning envelope direction, and cloth collision response | Edit Mode, `A` → `Shift+N` (Recalculate Outside). Verify with `Overlays → Geometry → Face Orientation` — outside faces must be **blue**, red = flipped. |
| **No floating geometry** | stray verts and loose accessories confuse auto-riggers and inflate counts | `Mesh → Clean Up → Delete Loose`. Also check the Outliner for orphan objects not in any collection. |
| **No self-intersections** | intersecting faces poke through each other during deformation | Enable the bundled **3D-Print Toolbox** add-on (`Edit → Preferences → Add-ons → Mesh: 3D-Print Toolbox`), then 3D-Print tab in the sidebar → **Check All** (reports Solid / Intersections / Contiguous / Thickness). |

**Order matters:** merge → recalculate normals → delete loose → check non-manifold → check
intersections. Merging first can change what "non-manifold" reports.

---

## 3. Pose & Symmetry

### 3.1 Rest pose — T-pose or A-pose, and why each
Vaughan p. 184–185 gives both, with the trade-off stated plainly:

- **T-pose** — *"the character is standing up straight and its arms, hands, and fingers are at
  90 degrees… the most commonly used base pose."* Benefits, verbatim: *"Positioning the arms
  and legs straight down a specific axis can make placing bones and controls much easier for a
  rigging artist. It also puts some distance between the arms and the torso, making them
  easier to see and access in multiple views."*
- **Relaxed pose** (the A-pose) — *"the character's arms are at a 45-degree angle, and all of
  the joints (knees, elbows, ankles, hands, fingers, and so on) are slightly pre-bent instead
  of straight."* Benefits: *"These pre-bends can assist in good deformations and IK (inverse
  kinematics) solving, but can make for more work for a rigging artist when placing bones and
  controls."*

**Decision rule for this skill:** use **A-pose (arms ≈45°, joints slightly pre-bent)** for
organic characters that will be heavily posed and skinned — the pre-bend is free improvement
to deformation (§1.3: it puts the compression side's smaller surface area where it belongs).
Use **T-pose** when handing the mesh to an auto-rigger or a rigger who is not you, because the
90° axes and arm/torso separation make bone placement unambiguous. Either is acceptable; what
is unacceptable is a pose nobody can reproduce.

### 3.2 Bilateral symmetry
Riggers mirror bones and weights across the centre plane; asymmetry breaks the mirror.
**Blender:** build one side, then `Mesh → Symmetrize` (or the Mirror modifier with *Clipping*
on) to generate the other; `Mesh → Snap to Symmetry` to re-align a pair that has drifted.
Check by applying a temporary Mirror modifier across X — any vertex that fails to merge is
asymmetry.

### 3.3 Origin at world centre, between the feet, on the ground plane
Vaughan p. 181: *"The majority of the time you'll want to position your finished model at the
origin, resting on the ground plane (zero in the Y axis) and rotated to face forward (towards
the positive Z axis). This not only helps the rigging department, but is quite useful for
layout, texturing, and effects artists."*
*(Y-up/Z-forward is his Maya convention; in Blender's Z-up world this means **feet at Z = 0,
facing −Y**, and the FBX exporter's Up/Forward axis settings handle the conversion — §7.5.)*
**Blender:** `Object → Set Origin → Origin to 3D Cursor` with the cursor snapped to the
world origin between the feet (`Shift+S → Cursor to World Origin`, then move in Z).

### 3.4 Limbs separated from torso
Arms and legs must not intersect the body in the rest pose, or skinning produces webbing where
the surfaces touch. The T-pose's *"distance between the arms and the torso"* (p. 184) is the
automatic fix; if using an A-pose, keep enough clearance at the armpit and crotch that no
vertices are inside another surface.

---

## 4. Scale & Poly Count

### 4.1 Real-world scale
Vaughan p. 180–181: scale is one of the three final-pass items, and he is blunt about
neglecting it — *"take a final look, measure, and adjust accordingly. You don't want to
deliver a model of a mouse the size of the Empire State Building."* Target ≈ **1.7 m** for an
adult human. Physics, collision, and engine scaling all assume real units, so a wrong-scale
model produces a cloth sim and step timing that can never be tuned right.
**Blender:** measure with the **Measure** tool in the toolbar (`N` panel → *View* tab shows
dimensions; or `Shift+Space` search "Measure"). Scene must stay *Unit System: Metric,
Length: Meters, Unit Scale 1.0* (ref 10).

### 4.2 Polygon count within target
- **Mixamo / auto-rigger ceiling: ~100 k triangles.** Beyond that, uploads fail or weights
  degrade.
- **Game engines** need LOD-appropriate counts; **film** can go much higher — the measured
  CGBoost hero scene runs 532,002 verts across 278 objects with no LOD swapping at all.
- Apply Vaughan's **Hero / Secondary / Tertiary** labelling (p. 174) when the same asset
  appears at different distances.

**Blender:** enable `Overlays → Statistics` to read Verts / Faces / **Tris** live. Report
counts as **triangles**, not quads — one quad is two triangles, and that is the number every
engine budget is written in.

### 4.3 Transformations applied
Unapplied scale or rotation breaks bone lengths, weight normalization, and export.
**Blender:** `Ctrl+A → All Transforms` (Object > Apply > All Transforms) on every mesh and the
armature, before skinning and before export. Non-uniform scale left on an object is the single
most common cause of "the rig works until I pose it."

---

## 5. UV & Texturing

Vaughan p. 182–183, from the modeler's side of the handoff:

- **Layout order:** *"start by placing the portions of the mesh that will need the most
  accurate textures. These high-detailed areas may include the head and torso of a
  character."* → **unpack the face and torso first, while there is still room.**
- **Island spacing:** *"should be close enough to not waste space, but not so close that
  textures will transfer from one island to the next. Be as efficient as you can with the
  real estate you have to work with."*
- **Seams:** *"There is no escaping UV seams, but you can minimize their effects by placing
  them in areas that are more out of sight, like the inside of a character's arm or the back
  of a character's head."*
- **Island count on organics:** *"try to use as few polygon islands as possible, creating a
  continuous island of large polygon groups."*
- **Options (p. 183):** *"There really is no right or wrong when it comes to laying out UV
  maps, so give yourself and/or the texture artist multiple options… An object can have
  multiple UV maps applied to its points."*

**Deformation requirement:** UVs must survive posing without stretching — a seam placed *on* a
joint will visibly tear when the joint bends, so keep seams off every rule-of-three band
(§1.2) and off the face.

**Blender:** mark seams in Edit Mode (`Ctrl+E → Mark Seam`), `U → Unwrap`, then pack with
`UV → Pack Islands` (set a *Margin* so islands don't bleed). Multiple UV maps live in
*Object Data Properties → UV Maps*; add a second with `+` when handing off options. Texel
density law lives in ref 17 §2.

---

## 6. Rigging & Skinning Readiness

O'Hailey's rules from p. 18, restated as mesh requirements:

| Rule (verbatim, p. 18) | What it demands of the mesh / rig |
|---|---|
| **1. Edgeloops — a good or bad rig starts with the loops** | §1 passes before anything else |
| **8. Joint placement, preferred angles, and orientations — good models can go bad with poor joint placement. Take extra care here before any other rigging — or you'll be redoing your rig** | joint axes verified before skinning |
| **9. BlendShapes — never ever freeze them** | shape keys stay live and editable; never apply them into the base mesh |
| **10. Skinning — make peace with it — a good rig with bad skinning is still bad** | weights are worked, never left at auto-default |

### 6.1 Clean skin weights
Per-vertex influence must be blended across joints, not snapped to one. Working reference:
**≈60/40 at the knee** — the joint's own bone carries ~60 %, the neighbouring bone ~40 % at
the crease, and the transition is spread over the three-segment band from §1.2.
**Blender:** Weight Paint mode; `Weight → Normalize All` after any edit; **Lock** the groups
you are not painting so a stroke can't steal weight from them. A weight of 0.0 on a vertex in
a deforming region is always a bug.

### 6.2 Joint axes (the check that saves the rig)
O'Hailey p. 105, *Check Your Joint Rotational Axis*: orient the chain, then hunt the *"rebel
Zs"* — *"Do you have any wayward Zs not facing the same direction as anyone else?"* — and
rotate them into agreement. Test: *"select each spine joint and rotate all of them in Z. The
spine should curve nicely forward and back."*
**Blender:** Edit Mode on the armature → select the chain →
`Armature → Bone Roll → Recalculate Roll` (Global ±X / ±Z / Active Bone / Cursor). Then pose
each joint one axis at a time and confirm it bends the way the bone points.

### 6.3 Bone hierarchy compatibility
Names and parent/child structure must match the target skeleton (Unreal, Unity, Mixamo,
Rigify). Use a consistent side prefix (`L_` / `R_`, or `.L` / `.R` for Blender, which mirrors
automatically). Vaughan p. 168 on naming generally: *"avoid using spaces… Opt for an
underscore (_), which is much easier to see and doesn't cause issues later down the
production line."*

### 6.4 Constraints baked before export
IK/FK must be baked to explicit FK rotation keys in FBX, or limbs float on import.
**Blender:** `Pose → Animation → Bake Action` (enable *Visual Keying* and *Clear
Constraints*). Bake to a fresh action first so the original stays editable.

### 6.5 Shape keys / blend shapes
Per Rule 9, never freeze them. Keep `Basis` untouched, keep targets as separate live keys, and
confirm each target's *Relative To* is correct before export. On export they travel as FBX
blend shapes; verify after re-import (§7.5). Facial setup detail: ref 06.

---

## 7. Validation Tests

Run these on the **rigged** model, in this order. Each one targets a specific failure mode
from §1–§6, so a failure points back to a section.

### 7.1 Extreme joint flex
Push every joint to full range: **no tearing, no pinching, no unnatural bulging.**
- Pinching at a joint → §1.2 (fewer than three segments) or §1.5 (pole on the joint line).
- Concave rubbery collapse → §1.3, Finger A failure: loops running straight through the bend
  instead of enclosing it.
- Spiral swirl → §1.5, pole misplaced.

### 7.2 Overlapping limbs
Crossed arms and hands-on-hips — **no interpenetration.** Confirm the compression side of
elbow and knee has the smaller surface area (§1.3, the kneepad law). Check the armpit and
crotch for webbing (§3.4).

### 7.3 Walk / run cycle
Smooth deformation through the full cycle; **no clipping at knees, elbows, or shoulders.**
This is the test that catches the density imbalance in §1.4 — if a joint clips, either the
count is too low for the bend radius or the loops don't follow the muscle. See ref 04 for the
cycle itself.

### 7.4 Facial expression sweep
Run every expression control through its full range: all results natural, no collapse at the
mouth corners, no tearing across the nasolabial fold. The face needs its anatomy loops
(§1.3) *and* the three sets of facial loops Vaughan builds for predictable deformation
(p. 176). Viseme/expression set: ref 06.

### 7.5 FBX round-trip
Export → re-import into the target engine; verify **skeleton, weights, textures, and
orientation (Y-up vs Z-up)**.
**Blender:** `File → Export → FBX`, set *Up: Y Up* and *Forward: -Z Forward* for
Unreal/Unity/Mixamo, enable *Bake Animation* only when shipping animation. Then re-import the
result into a clean file and compare: bone count matches, weights sum to 1.0, textures
resolve, and the model stands at the right height and facing. This is where n-gon
triangulation mismatches (§1.6) and unbaked constraints (§6.4) finally surface — run it early
enough to fix them.

### 7.6 Auto-rig success
If using an auto-rigger, successful bone placement and weight assignment is a strong proxy for
readiness. **Blender:** enable the bundled **Rigify** add-on, `Add → Armature → Human
(Meta-Rig)`, align it to the mesh, and *Generate Rig*. If Rigify's automatic alignment
fights the mesh, the rest pose (§3.1) or limb separation (§3.4) is wrong. Cap the mesh at
~100 k triangles for external auto-riggers (§4.2).

---

## 8. The Gate — printable checklist

Do not rig until every line reads **PASS**.

```
GEOMETRY & TOPOLOGY
[ ] Quad-dominant: no tris or n-gons on any joint line or in the face   (§1.1, §1.6)
[ ] Rule of three: >=3 segments at elbows, shoulders, knees, finger
    joints, wrists, laugh lines, eyelids                                (§1.2)
[ ] Loops enclose each bend; compression side has SMALLER area than
    extension side (kneepad law)                                        (§1.3)
[ ] Anatomy loops present: mouth, eyes, nasolabial, pectoral, deltoid   (§1.3)
[ ] Density: face/hands/joints dense, forehead/shins sparse; hero vs
    secondary vs tertiary labelled                                      (§1.4)
[ ] Poles only in low-deform zones (scapula, armpit, skull crown);
    intentional chamfered pads at knuckles/elbows/patellas              (§1.5)
[ ] No over-looping: no pinching or creases from excess loops           (§1.7)

STRUCTURAL INTEGRITY
[ ] Manifold / watertight (Non Manifold select = empty)                 (§2)
[ ] Welded: Merge by Distance clean
[ ] Normals outward (Face Orientation overlay = all blue)
[ ] No floating geometry (Delete Loose clean)
[ ] No self-intersections (3D-Print Toolbox Check All clean)

POSE & SYMMETRY
[ ] Rest pose chosen and repeatable: A-pose (45 deg, pre-bent) or
    T-pose (90 deg, arms clear of torso)                                (§3.1)
[ ] Bilateral symmetry verified                                         (§3.2)
[ ] Origin at world centre, feet on ground plane, facing forward        (§3.3)
[ ] Limbs clear of torso: no armpit/crotch webbing                      (§3.4)

SCALE & POLY COUNT
[ ] Real-world scale (~1.7 m adult), scene units metric                 (§4.1)
[ ] Triangle count within target (<=100k for auto-riggers)              (§4.2)
[ ] All Transforms applied (Ctrl+A) on meshes and armature              (§4.3)

UV & TEXTURING
[ ] Face/torso unpacked first; islands packed without bleeding          (§5)
[ ] Seams in hidden areas; OFF every joint and OFF the face             (§5)
[ ] Minimal island count on organics; texel density even (ref 17 §2)    (§5)

RIGGING & SKINNING READINESS
[ ] Joint axes oriented; no "rebel Zs"; each joint bends as it points   (§6.2)
[ ] Weights blended (~60/40 at knee), normalized, nothing at 0.0        (§6.1)
[ ] Bone names + hierarchy match target skeleton                        (§6.3)
[ ] IK/FK baked to FK keys with Visual Keying + Clear Constraints       (§6.4)
[ ] Shape keys live, Basis untouched, never frozen                      (§6.5)

VALIDATION TESTS
[ ] 7.1 Extreme joint flex: no tear / pinch / bulge
[ ] 7.2 Overlapping limbs: no interpenetration
[ ] 7.3 Walk/run cycle: smooth, no clipping
[ ] 7.4 Facial expression sweep: all controls natural
[ ] 7.5 FBX round-trip: skeleton, weights, textures, Y-up correct
[ ] 7.6 Auto-rig (Rigify / Mixamo) succeeds
```

## 9. Blender 5.x quick procedure index

| Task | Path |
|---|---|
| Find tris / n-gons | Edit Mode → `Select → Select All by Trait → Faces by Sides` |
| Find non-manifold | Edit Mode → `Select → Select All by Trait → Non Manifold` |
| Weld vertices | Edit Mode, `A` → `M → By Distance` |
| Fix normals | Edit Mode, `A` → `Shift+N`; check `Overlays → Geometry → Face Orientation` |
| Delete loose geometry | `Mesh → Clean Up → Delete Loose` |
| Self-intersection check | 3D-Print Toolbox add-on → 3D-Print tab → **Check All** |
| Select an edge loop | `Alt+Click` (extend: `Ctrl+Alt+Click`) |
| Redirect flow (spin edge) | `Ctrl+E` → **Rotate Edge (CW / CCW)**, or `F3` "Rotate Edge" |
| Make a joint pad (chamfer vertex) | Vertex Mode → `Ctrl+B` → bevel, then `Ctrl+R` two rings |
| Symmetrize / re-align | `Mesh → Symmetrize` / `Mesh → Snap to Symmetry` |
| Move origin | `Object → Set Origin → Origin to 3D Cursor` |
| Apply transforms | `Ctrl+A → All Transforms` |
| Live counts | `Overlays → Statistics` (Verts / Faces / **Tris**) |
| Mark seam / unwrap / pack | `Ctrl+E → Mark Seam` · `U → Unwrap` · `UV → Pack Islands` |
| Orient bone axes | Edit Mode → `Armature → Bone Roll → Recalculate Roll` |
| Normalize weights | Weight Paint → `Weight → Normalize All` |
| Bake constraints to keys | `Pose → Animation → Bake Action` (Visual Keying + Clear Constraints) |
| Add Rigify meta-rig | Rigify add-on → `Add → Armature → Human (Meta-Rig)` |
| Export FBX | `File → Export → FBX` — set **Up: Y Up**, **Forward: −Z Forward** |

## 10. The three laws, restated as a working rule

O'Hailey p. 56: *Rule #1 — a good or bad rig starts with the loops.* Everything in this file
is an expansion of that sentence. Vaughan p. 180 gives the closing discipline: *"The last ten
percent of any modeling task is to prepare it for the next phase of production"* — with the
final-pass habit that makes it stick (p. 181): *"It is good practice to take a break from the
model before doing the final pass. When possible, I like to wait until the following day so I
can review the previous day's work… This allows you to review your models with a fresh eye."*

**Run the Gate with fresh eyes, never right after finishing the mesh.**
