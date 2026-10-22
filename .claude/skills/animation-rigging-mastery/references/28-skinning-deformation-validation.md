# 28 — Skinning & Deformation Validation

> **The deformation canon** (all in this repo as PDFs, all text-verified — page numbers are
> the book's own PDF pages):
> **Tina O'Hailey, *Rig It Right!*** (324 pp) — p. 18 *Basic Rules of Rigging* (Rules #1,
> #8, #9, #10), p. 56–58 *Appendix 2.A: Edgeloops for Good Deformation*,
> p. 105 + p. 148–150 *Joint Orientations*, p. 109–110 *Interactive Skinning*,
> p. 120 *Blendshape Weights*, **p. 155–160 *Chapter 8: Skinning*** (bind methods, skinning
> methods, normalization, **max influxes**, bind pose), p. 157 *Pipeline 1: proxies*.
> **William Vaughan, *Digital Modeling*** — p. 179 *rule of three*, p. 183 *rigging
> preparation*.
> **CGBoost production `.blend` files** — 19 parsed; measured numbers cited as *(measured)*.
> **Prerequisite: `27-mesh-topology-readiness.md` must PASS before any of this starts.**

## 0. Why this chapter exists — Rule #10, and the Rule #1 callback

O'Hailey p. 18, Rule #10:

> *"Skinning — make peace with it — a good rig with bad skinning is still bad."*

And the moment she closes the loop back to topology, p. 157, while describing the tedious
job of cutting proxy geometry:

> *"If the geometry did not have clear edgeloops and bend areas, then this task (along with
> UVing and texturing and skinning) will be very, very tedious. What was Rule #1? Oh yes…
> Edgeloops—a good or bad rig starts with the loops. I wasn't kidding."*

**So the sequence is not negotiable:** ref 27 passes → *then* skin. Every hour spent on
weights for a mesh with bad loops is an hour that will be thrown away when the mesh is
rebuilt.

**Definition** (p. 155): *"Skinning… is the process of making the whole mesh move along with
the skeletons by assigning how much each vertex will move with a joint or joints. It is the
extended task of being particular and working with the weights to get the proper movement."*

Note the second sentence. Binding is ten seconds of work; **weights are the job.**

---

## 1. Before you bind — the order of operations

O'Hailey p. 155–156 settles four questions that cost days when got wrong.

### 1.1 Proxy now, or skin now?
p. 155 — *"Our choices are to skin now and create proxies later, or create proxies now and
skin later. It depends on how you are going to create your proxies. If you create them
manually, skin them later. If you are going to use an automated script, skin now."*

**What a proxy is** (p. 155): *"At one place where I was employed, we called them tootsie
rolls. These are slices of a low-res geometry that are parented or parent-constrained to move
along with the joints—no skinning is necessary."*

**Why bother** (p. 155):

- *"If your geometry is going to change, you do not want to spend time skinning. If the
  geometry changes, you will need to reskin: **holy missing vertices, don't do that!**"*
- *"Usually, you do not want the animator to work with the final skinned model anyway. It
  would be incredibly slow to work with."*
- Proxies let animation begin *while* sculpting and texturing finish, in parallel.

**Blender:** the proxy rig is the low-poly mesh bound with Automatic Weights; the hero is
bound later, or driven by a **Surface Deform** modifier bound to the proxy. Keep them in
separate collections (`PRXY`, `GEO`, `SKEL`, `CNTRL` — O'Hailey Rule #4, p. 18).

### 1.2 UV and texture **before** skinning (if the model shares the rig file)
p. 156, verbatim: *"If your model resides in the same file as the rig, then you will want to
complete the UVing and texturing prior to skinning."*

### 1.3 The "textures swim" gotcha
p. 156, verbatim: *"Remember to delete the history on the model after you UV and prior to
skinning. Not deleting history after adjusting the UVs can cause the textures to swim after
skinning."*

**Blender equivalent:** apply or remove every modifier above the Armature modifier before
binding (Mirror and Subdivision especially), and confirm no modifier below the armature is
recomputing UVs. A Mirror modifier left live under a skinned mesh is the classic
"the texture crawls when I pose it" report.

### 1.4 Never add vertices after skinning
p. 156: *"if you bring in a model with new vertices after you have skinned them, those new
vertices will need to be skinned, and your overall skinning may have to be tweaked, if not
redone."*

This is the enforcement clause on ref 27's Gate: **topology freezes at bind time.** If you
must edit after binding, do it with the armature in rest position, and re-run §11.

### 1.5 Version stability
p. 156: *"when you get to the skinning stage, be very careful about software versions and
patches… I have noticed many skinning errors and changes happening when skinning in one
version and then opening in a different version."*
**Rule for this skill:** bind, weight, and export on the same Blender version. Note the
version in the rig file's name.

---

## 2. Bind methods — four ways to get the first draft

O'Hailey p. 158–159. The bind is only a starting guess; the point of knowing these is
knowing *which one fails how*.

| Method (O'Hailey) | How it works | Known failure | Blender equivalent |
|---|---|---|---|
| **Closest distance** | distance from bone to skin; ignores hierarchy | *"It can cause small areas like fingers and legs to take ownership of the wrong vertices."* | Armature modifier → **Bone Envelopes** (distance-based, hierarchy-blind) |
| **Closest in hierarchy** | as above, but hierarchy respected — only the parent gets more influence | better on limbs, still dumb about volume | — (Blender's Automatic Weights is closer to the next row) |
| **Heat map** | diffusion; needs influence objects (low-res muscles) inside the skeleton | influence objects and all joints must be **inside** the skeleton | **Automatic Weights** (`Ctrl+P → Armature Deform → With Automatic Weights`) — heat-diffusion based |
| **Geodesic Voxel** | *"fills the skin volume up with voxels and then calculates where those voxels meet the skin"* | *"Skeletons need to be contained inside the mesh… Also, normals need to be facing out."* | no direct equivalent — **Automatic Weights** is the practical default |

Two settings worth knowing from the voxel bind, because they describe the trade you always
make (p. 159): **Falloff** — *"1 = very rigid bind. 0 = very smooth bind."* **Resolution** —
*"the higher the number, the more precise the calculation, but the longer it will take."*

**Why this matters even in Blender:** geodesic voxel *"works across multiple meshes, even
intersecting meshes, and even non-watertight meshes"* — which is excellent news and a trap.
It will happily bind a mesh that ref 27 §2 would fail. **A clean bind on a dirty mesh is not
a pass.** Run the Gate first.

**Blender:** select mesh, `Shift`-select armature, `Ctrl+P → Armature Deform → With Automatic
Weights`. Expect to repaint fingers, shoulders, and hips by hand — the same places O'Hailey
flags.

---

## 3. Skinning methods — how the deformation is calculated

p. 159:

- **Classic Linear** — *"a smooth binding method that was used in pre-2011 Maya."* Fast,
  standard, and it **loses volume when a bone twists** (the candy-wrapper effect on a
  rotating forearm or shoulder).
- **Dual quaternion** — *"A method of skinning that preserves volume in areas that twist."*
- **Weight blended** — *"A blend between the two skinning methods listed above based on a
  painted weight map you create."*

**Blender:** the Armature modifier's **Preserve Volume** checkbox is the dual-quaternion path.
Turn it on for characters with twisting limbs (forearms, upper arms, thighs, neck) and for
any cartoon/stylized build where volume loss reads instantly; leave it off for realistic builds
where linear skinning's slight collapse is easier to correct with shape keys. **Weight
Blended** has no single toggle — it is reproduced with a corrective shape key driven by the
twist angle (§9).

---

## 4. Normalization — the gotcha that eats an afternoon

p. 159–160. *"The trick is to get everything 'normalized,' or back into a 0–1 range."*

| Mode | Behaviour | Verdict |
|---|---|---|
| **None** | *"allows you to have weights that are over 1 or less than 0, but it does not normalize them. It can cause issues with the rig… I don't use it."* | never |
| **Interactive** | *"All skinning weights are adjusted so that they only equal 1."* | predictable |
| **Post** (default) | *"the actual normalization… happens when you deform the mesh, not when you paint the weights."* | default, but read the warning |

**The Post-mode trap, verbatim (p. 159–160):**

> *"any tricks you used to have about setting one weight value to 1, thus automatically
> setting all other weights to 0, will no longer work. **You have to paint weights to 1 for
> one joint and then physically paint 0 as well for all of the other joints.**"*

This is the single most common weight-painting confusion: you paint a region fully to the
forearm, and it *still* follows the upper arm, because the upper arm's weight was never
zeroed. **Painting 1 is not enough — you must also paint 0.**

Weight distribution options (p. 159): **Distance** — *"Closer joints are given higher skin
weights"*; **Neighbors** — *"Calculated based on neighboring vertex weights."*

**Blender:** `Weight → Normalize All` forces every vertex's deform-group weights to sum to
1.0. Run it after *every* painting session and before every test pose. Then
`Weight → Clean` to drop weights below ~0.01 — a vertex carrying 0.004 to a bone is noise
that will show up as jitter.

---

## 5. Max influences — the number is 3

p. 160, on **Maintain Max Influxes** (the cap on how many joints may influence one vertex):

| Cap | Result (verbatim) |
|---|---|
| 1 | *"that would equal rigid binding"* |
| 2 | *"that's a little more smooth"* |
| **3** | *"there's more influence, and that can help you simulate skin better"* |
| **5 or higher** | *"you have made yourself a skinning nightmare: only do that if you really have a reason"* |

**Use 3.** It is enough to blend a joint naturally (the two bones either side, plus one
helper or twist bone) and not enough to turn the mesh to soup.

**The built-in gotcha (p. 160):** *"if you set the max influence to a low number, say 2, and
want to paint in a third joint, the system will keep the influence at 2 by removing influence
from an existing joint and giving it to the third joint… This can be surprising when skinning
at 3 am and not understanding why your skinning assignment keeps subtracting itself from the
joints you had working."*

**Blender:** Weight Paint mode → `Weights → Limit Total`, set **Limit = 4** (Blender counts
the cap inclusively; 4 here lands on O'Hailey's 3-plus-one headroom). Blender has no hard
cap by default — without `Limit Total`, a vertex can accumulate weight to every bone in the
armature, which is exactly the "nightmare" case and is also slow.

---

## 6. The bind pose — the zero point

p. 160: *"The bind pose is the 'neutral' state of the geometry versus the skeleton system.
Think of it as the 'zero, zero, zero' point, which all things should come back to."*

p. 160 also notes **Allow Multiple Bind Poses** — *"super-useful when you have multiple
pieces of geometry being bound to the same skeleton… If turned OFF, all geometry must be
bound at the same time."*

**Blender:** the rest pose is stored on the armature; `Pose → Clear Transform → All`
(`Alt+G` / `Alt+R` / `Alt+S`) returns to it. Anything you change in Edit Mode after binding
changes the rest pose and therefore every weight you have painted — **Edit Mode is closed
once weights are approved.** If you must add a bone after binding, re-check normalization
(§4) before testing.

---

## 7. How to paint — pose first

p. 110, on why you cannot judge weights on a straight model:

> *"it is difficult to see what you are doing unless the character is in a pose."*

Her interactive tool's colour code (p. 110) is the mental model to keep while painting
anywhere: **orange = the area of most influence, blue = the area of least.**

**Working loop:**

1. Put the rig in an extreme pose (the pose that will fail, not a neutral one).
2. Paint the region that is wrong.
3. `Weights → Normalize All`, then `Weights → Clean`.
4. Return to rest, move to the next extreme pose, repeat.

**Blender:** pose the armature, then switch to Weight Paint mode — the mesh stays posed and
you paint on the deformed shape. Use **X Mirror** for symmetric pairs, and **Lock** every
group you are not painting so a stroke cannot steal weight from them.

## 8. The 60/40 joint — what "correctly blended" looks like

The user-facing target from the readiness table: **≈60/40 across a joint.** Concretely, for a
three-segment band (ref 27 §1.2 — one segment bends, two support):

| Joint | Upper / proximal | Lower / distal | Notes |
|---|---|---|---|
| Knee | thigh **60** | shin **40** | the crease itself is the 50/50 point |
| Elbow | upper arm **60** | forearm **40** | add the twist bone's influence without exceeding cap 3 |
| Shoulder | upper arm **60** | clavicle / torso **40** | the falloff must span the deltoid, not the armpit |
| Hip | torso **60** | thigh **40** | watch the crotch — the classic webbing spot (ref 27 §3.4) |
| Ankle | shin **70** | foot **30** | stiff by design; feet barely blend |
| Wrist | forearm **70** | hand **30** | as above |
| Spine | even 3-way falloff | — | no single vertebra should own more than ~50% |

**Hard checks:**
- Every deform weight sums to **1.000** (Normalize All).
- No vertex sits at **0.0** in a region that moves.
- No vertex exceeds the influence cap (§5).
- The falloff across a joint is **monotonic** — no hot spot in the middle of a bone.

---

## 9. Shape keys / blend shapes — Rule #9

p. 18, Rule #9: *"BlendShapes — never ever freeze them."*

**Blender:** keep `Basis` untouched, keep each target as a live separate shape key, and
verify each target's **Relative To** is set correctly before export. Never apply a shape key
into the base mesh — that is "freezing," and it destroys your ability to retune the
expression later.

### 9.1 Painting blendshape weights
p. 120: *"This usage allows you to paint how much vertices should obey the blendshape… A
completely white character means that all vertices have a value of 1: 100% listening to the
blendshape. A black character visually means 0, so the vertices are completely ignoring the
blendshape. In-between are shades of gray: 0.5 = 50% listening."*
And the fix: *"Replace with 0 by painting in black. Paint out areas that the blendshape
should not affect."*

**Blender:** shape keys have a **Vertex Group** field on each key — assign a group and paint
it to mask where the shape applies. This is how you stop a brow shape key from dragging the
scalp, or a smile from inflating the cheek.

### 9.2 The double-transform gotcha and combination targets
p. 120, verbatim: *"If you had a left happy and a right happy that were both adjusting the
center vertices, when you turn on both blendshapes, those center vertices will be told to
move twice, once by each blendshape. The solution? Either make the blendshapes taper off at
the crossover points (the center vertices) or you can create a combination target."*

**Two fixes, in order of preference:**
1. **Taper at the crossover** — paint the shape's mask (§9.1) so the two shapes share no
   vertices at full strength. Cheap, no extra assets.
2. **Combination target** — a shape key that exists only to correct the *combination* of two
   others, driven on only when both parents are active.

**Blender:** drive the corrective with a driver reading both parents' values
(e.g. `min(a, b)` or `a * b` for a smooth blend-in). The facial set itself lives in ref 06.

---

## 10. Joint orientation, and the parenting gotcha

p. 148: *"Select the Spine; Skeleton>Orient Joint to get the X-axis all lined up. Since this
is a complete FK unit… we want it to have the same Z-axis throughout… Snap step rotate the Zs
so that they all point the same way. I tend to point all the Zs off to the character's right
(screen left). All the Ys should point out the back of the spine, out the bend."*

**Her test (p. 148):** *"select all spines individually (and the neck and head, too) and
rotate them in Z. A proper bend forward and back should happen, or else your joint
orientations are incorrect."*

**The gotcha that ruins finished rigs (p. 148), verbatim:**

> *"if you make the spine a child of the lower back and out of habit click on orient
> joints—that carries through from the parent. Parenting or orienting joints after parenting
> will adjust what you just set up. So always give another careful look around your joint
> system after you have parented and/or oriented joints."*

**Blender:** Edit Mode → `Armature → Bone Roll → Recalculate Roll` (Global ±X / ±Z / Active
Bone). Then the one-axis test: rotate each bone on one axis only and confirm it bends the way
the bone points. Re-run this after *every* reparent. O'Hailey's "rebel Zs" hunt (p. 105) is
the same exercise on the spine: find the axes that disagree and snap them into line.

**Naming:** p. 148 — *"Remember to put in a 'JNT' or 'jnt' suffix in there to ease selecting
all joints later on in life."* Blender convention: `.L` / `.R` suffix on the bone name
enables automatic mirroring; keep a separate `_jnt` style suffix only if the pipeline
requires it.

---

## 11. The deformation battery — validation

Run these in order. Each one names the section that fixes its failure, so a fail points
somewhere specific rather than at "the skinning."

| # | Test | Pass condition | If it fails |
|---|---|---|---|
| **T1** | **Extreme joint flex** — every joint to full range | no tearing, no pinching, no unnatural bulging | ref 27 §1.2 (rule of three) · §5 (cap) · §8 (60/40) |
| **T2** | **Overlapping limbs** — crossed arms, hands on hips | no interpenetration; no armpit/crotch webbing | ref 27 §3.4 · §8 (hip/shoulder falloff) |
| **T3** | **Walk / run cycle** | smooth; no clipping at knees, elbows, shoulders | ref 04 · §8 · ref 27 §1.4 (density) |
| **T4** | **Facial expression sweep** | every control natural; no double-transform artifacts | §9.2 · ref 06 |
| **T5** | **FBX round-trip** | skeleton, weights, textures, and Y-up orientation all correct on re-import | §12 · ref 27 §7.5 |
| **T6** | **Auto-rig success** (Rigify / Mixamo) | bone placement and weights assign cleanly | ref 27 §3.1 (rest pose) · §4.2 (≤100k tris) |

### T1 — the twist test (add this; it catches what flex does not)
Twist each limb segment 180° along its length. **Candy-wrapper collapse** at the forearm or
upper arm → §3, enable **Preserve Volume** on the Armature modifier, or add a twist bone with
its own weight band. This failure does not appear in a bend test at all.

### T1b — the volume test
Check the joint's cross-section at full bend against the same section at rest. A joint that
visibly **thins** as it bends is losing volume; a joint that **bulges into a hard crease** has
too few supporting segments (ref 27 §1.2).

### T2 — the compression-side check
At full bend, the inside of the joint must show **one or two tight folds**, not a wide
concave collapse. A wide rubbery fold means the loops run straight through the bend — ref 27
§1.3, Finger A's failure, not a weight problem.

### T5 — the FBX round-trip, in full
**Blender:** `File → Export → FBX` → **Up: Y Up**, **Forward: −Z Forward**, enable *Bake
Animation* only when shipping animation (§12). Then re-import into a **clean** file and
verify:
- bone count and hierarchy match the source;
- deform weights still sum to 1.0 and nothing reads 0.0;
- every material and texture resolves;
- the model stands at the right height, facing the right way, feet on the ground.

This is where unbaked constraints (§12), frozen shape keys (§9), and n-gon triangulation
mismatches (ref 27 §1.6) finally surface. Run it early enough that you can still fix them.

---

## 12. Export readiness — bake before you ship

Constraints must be baked to explicit FK rotation keys, or limbs float on import.
**Blender:** `Pose → Animation → Bake Action` → enable **Visual Keying** and **Clear
Constraints**. Bake into a *fresh* action first so the original stays editable, then confirm
T5.

Also before export: `Ctrl+A → All Transforms` on mesh and armature (ref 27 §4.3); shape keys
live and relative (§9); and the file's Blender version recorded (§1.5).

---

## 13. The Gate — printable checklist

Ref 27 §8 must read PASS before this one is started.

```
BEFORE BINDING
[ ] ref 27 Gate passed; topology frozen (no verts added after this point)     (§1.4)
[ ] Proxy decision made: manual proxies -> skin later; scripted -> skin now   (§1.1)
[ ] UV + texturing complete; all modifiers applied/removed above armature     (§1.2, §1.3)
[ ] Blender version fixed for bind -> weight -> export                        (§1.5)

BIND
[ ] Automatic Weights used as the STARTING guess, not the answer              (§2)
[ ] Preserve Volume ON for twisting limbs                                     (§3)
[ ] Bind pose recorded as the zero point                                      (§6)

WEIGHTS
[ ] Weights -> Normalize All run: every deform sum = 1.000                    (§4)
[ ] Weights -> Clean run: nothing below ~0.01                                 (§4)
[ ] Painted 1 AND painted 0 (Post-normalization trap)                         (§4)
[ ] Weights -> Limit Total = 4 (O'Hailey's cap of 3 + headroom)               (§5)
[ ] Painted in POSE, not at rest                                              (§7)
[ ] 60/40 at knee/elbow/hip/shoulder; monotonic falloff; no hotspots          (§8)
[ ] No vertex at 0.0 in any region that moves                                 (§8)

SHAPE KEYS (if facial)
[ ] Basis untouched; keys live; NEVER applied into the base mesh              (§9)
[ ] Vertex Group masks painted so shapes taper at crossover points            (§9.1)
[ ] Combination targets / drivers for double-transform overlaps               (§9.2)

JOINTS
[ ] Axes oriented; one-axis bend test passes on every chain                   (§10)
[ ] Re-checked AFTER every reparent (orientation carries through parent)      (§10)
[ ] Naming convention + .L/.R mirroring consistent                            (§10)

VALIDATION
[ ] T1 extreme joint flex clean
[ ] T1 twist test: no candy-wrapper collapse                                  (§11)
[ ] T1b volume test: no thinning or hard creasing at full bend                (§11)
[ ] T2 overlapping limbs: no interpenetration, compression side folds tight   (§11)
[ ] T3 walk/run cycle smooth, no clipping
[ ] T4 facial sweep natural, no double-transform
[ ] T5 FBX round-trip: skeleton, weights, textures, Y-up correct
[ ] T6 auto-rig (Rigify/Mixamo) succeeds

EXPORT
[ ] Constraints baked: Visual Keying + Clear Constraints, into a new action   (§12)
[ ] All Transforms applied (Ctrl+A)                                           (§12)
```

## 14. Blender 5.x quick procedure index

| Task | Path |
|---|---|
| Bind with automatic (heat) weights | select mesh → `Shift`-select armature → `Ctrl+P → Armature Deform → With Automatic Weights` |
| Distance-based bind | Armature modifier → enable **Bone Envelopes** |
| Preserve volume on twist | Armature modifier → **Preserve Volume** |
| Force weights to sum to 1 | Weight Paint → `Weights → Normalize All` |
| Drop noise weights | Weight Paint → `Weights → Clean` |
| Cap influences per vertex | Weight Paint → `Weights → Limit Total` (**Limit = 4**) |
| Symmetric painting | Weight Paint → enable **X Mirror** |
| Protect groups from a stroke | Weight Paint → Vertex Groups list → **Lock** the group |
| Pose while painting | pose the armature, then switch to Weight Paint mode |
| Mask a shape key | Shape Keys panel → the key's **Vertex Group** field |
| Return to rest pose | `Pose → Clear Transform → All` (`Alt+G` / `Alt+R` / `Alt+S`) |
| Orient bone axes | Edit Mode → `Armature → Bone Roll → Recalculate Roll` |
| Bake constraints to keys | `Pose → Animation → Bake Action` (**Visual Keying** + **Clear Constraints**) |
| Apply transforms | `Ctrl+A → All Transforms` |
| Export FBX | `File → Export → FBX` — **Up: Y Up**, **Forward: −Z Forward** |

## 15. The rule this chapter is built on

O'Hailey p. 18, Rule #10, once more — *"a good rig with bad skinning is still bad"* — paired
with her closing line from p. 157: *"What was Rule #1? Oh yes… Edgeloops—a good or bad rig
starts with the loops. I wasn't kidding."*

**Topology decides what is possible. Skinning decides whether you get it.** Neither can be
skipped, and the order is never reversed.
