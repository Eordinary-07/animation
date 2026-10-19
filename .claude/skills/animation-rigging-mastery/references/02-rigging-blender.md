# Rigging in Blender — Cabrera's Maya Curriculum, Translated

Source: Cabrera, *An Essential Introduction to Maya Character Rigging* (chapters 1-8),
plus Parent ch. 5 (IK math) and Osipa ch. 11 (facial rigging). The LOGIC is the book's;
the TOOLS are Blender's. When rigging in this project, follow this pipeline in order.

## 0. Pipeline overview (Cabrera's workflow)

Design sheets → Model for deformation → Face shape keys → Skeleton (joints) → Control rig
(FK/IK + attributes) → Cleanup → Skinning → Test battery. Never skip cleanup: a messy rig
costs the animator every day (ch. 7 "Wrapping Up the Setup").

## 1. Design & model for deformation (ch. 1-2)

- Character sheets: front/side/back orthographic. Place rotation centers ON the sheet
  (shoulder ball, elbow, knee, hip, knuckle line) before modeling.
- Model in T-pose or A-pose with **mirrored topology** (Mirror modifier + merge).
- Edge loops: concentric rings around eyes and mouth; extra loops at armpits, elbows, knees,
  waist; fingers attached with clean quad junctions. Even quad size = even deformation.
- Reason (the book's): rigging cannot fix bad topology; deformation quality is decided at
  modeling time.

## 2. Face shapes first (ch. 3) — shape keys in Blender

- Model expression targets as **shape keys** (Basis + one key per target): blink_L/R,
  browRaise_inner/outer_L/R, browDown, squint, smile, frown, jawOpen, mouthWide, mouthPucker,
  plus Osipa's viseme set (see `06-facial-lip-sync.md`).
- Make targets from duplicated, edited Basis meshes ("New Shape Key from Mix" or duplicate
  mesh → Add Shape Key → Join Shapes).
- **Deformation order matters** (Cabrera ch. 3): decide whether face shapes evaluate before
  or after the armature deform (Blender: modifier stack order Armature vs Shape Keys — shape
  keys live on the mesh data and evaluate BEFORE modifiers; use a corrective key or a second
  armature if the jaw joint needs to follow the shapes).
- Reason: expressions must survive head rotation; order decides which system "wins".

## 3. Skeleton: joint placement (ch. 5)

Build an **Armature** in Edit Mode, joints (= bone heads) at anatomical pivots:

| Chain | Joints | Rule |
|---|---|---|
| Spine | 3-5 bones (hips → chest → neck → head) | placed at the vertebrae you want to bend; even spacing |
| Shoulder/arm | clavicle → shoulder → elbow → wrist | elbow bone points at the wrist; one clean hinge axis |
| Hand | palm + 3 bones per finger + thumb 2-3 | knuckle line is a curve, not straight |
| Hip/leg | hip → knee → ankle → ball → toe | knee points forward (slight A-pose helps IK); heel pivot real |
| Face (if boned) | jaw, eyes, head-turret optional | jaw hinge at the ear joint |

Rules of the book, in Blender terms:
- **Joint orientation** (Maya) = **bone roll** (Blender): make every bone's local Y aim along
  the bone, roll aligned so bends are predictable (Ctrl+R with a target, or 3D cursor aim).
  Reason: rotations in local axes must mean the same thing on both sides.
- Mirror everything: left/right naming `_L`/`_R` prefix/suffix consistently.
- Work with the model **visible but unselectable** (collections; or "In Front" armature
  display — Cabrera's "X-Ray Joints" tip).
- Reference the mesh file vs rig file (Maya referencing) = keep rig + mesh separable
  (Blender: linked collections / Library Overrides when working in a team).

## 4. Control rig: FK, IK, attributes (ch. 6)

### FK/IK
- **FK chain** (Copy Rotation style parenting): for spine, tail, anything that arcs.
- **IK**: add an **IK constraint** on the lower arm/leg bone; target = a hand/foot control
  bone; pole target = elbow/knee control (aim the hinge; reason: prevents knee pop).
- Two-bone chains (arm, leg) solve analytically; longer chains use the IK solver
  (Parent ch. 5 explains why: Jacobian/numeric solvers generalize; analytic is exact).
- **FK/IK switching**: add a custom property `ik_fk` on a control bone; drive the IK
  constraint influence and a set of Copy Transforms (FK) constraints with it. Both states
  must match pose at 0.5/1.0 — snap and test.

### Control interface (Cabrera's "Attribute Control" → custom properties + drivers)
- Master control: a root/COG bone; custom properties for the animator:
  `ik_fk`, `foot_roll`, `toe_bend`, `head_follow`, `eyes_follow`, `stretch`,
  `spine_follow`, etc.
- **Set Driven Key (Maya) = Drivers (Blender)**: X-Property driven channel, expression or
  scripted (simple add/multiply). Every Maya SDK in the book (eye blinks, foot roll,
  stretchy limbs) is a driver here.
- Controllers = extruded/custom-shape bones (WGT objects): circles for hips, squares for
  feet, arrows for pull controls. Never make the animator select deform bones.
- Pivots: feet roll from heel → ball → toe (the book's foot roll); implement with child-of
  offsets or duplicated pivot bones driven by one property.

### Stretchy limbs (from Parent ch. 5 / rigging practice)
- Distance between hip and ankle → divide by rest length → drive scale of thigh/shin with
  "stretch" property; keep volume with squash (inverse scale) so the limb never noodles.

## 5. Wrap-up & cleanup (ch. 7)

- Freeze/reset pose button: a script or "Clear Transform" on all controls.
- Naming: `ctrl_`, `def_`, `jnt_`, `wgt_` prefixes; consistent `L/R`.
- Lock+hide every channel the animator shouldn't touch (transform locks on deform bones).
- Put things in bone collections: `DEF`, `CTRL`, `MCH` (mechanism), `WGT`.
- Save a "pose library" of test poses in the file.

## 6. Skinning (ch. 8)

- Blender: mesh + **Armature modifier**; weights in **vertex groups** (one per deform bone).
- Start: **Automatic Weights** (bone heat) for speed, then hand-fix; or Envelope for blocking.
- **Weight painting rules (the book's):**
  - Every deformed vertex is fully covered (weights sum to 1 → Normalize All).
  - Prefer 3-4 influences per vertex; hard areas (shoulder, armpit, hip, heel) need helper
    bones or smoothed manual weights.
  - Paint in EXTREME poses, not just T-pose (raise the arm, squat, twist the spine).
  - Smooth along deformation lines; keep creases where the anatomy creases (elbow/knee pits).
- Test battery (run every rig against these): overhead reach, touch toes, full squat,
  shoulder shrug, wrist twist, head turn with jaw open, smile with head rotated.
- Reason: weights are where rigs fail in production; the book drills "assign, test, refine".

## 7. Facial rig (blend of Cabrera ch. 3 + Osipa ch. 11-12)

- Primary: **shape keys** for mouth/eyes/brows (Osipa's "keys" = our shape keys).
- Optional bones: jaw (hinge), eyes (aim constraints → Track To on eye targets),
  head-turret, tongue (chain of 2-3 bones or keys).
- **Drivers**: `blink` property drives blink_L/R keys; `mouthOpen` drives jaw + keys;
  expression properties (happy, angry…) drive groups of keys at partial values.
- Osipa ch. 12 "interfaces": one clean panel of sliders per face; never expose raw keys.
- Squash/stretch/squoosh (ch. 13): add global face squash via a bone scale or lattice;
  it's what makes a face feel alive under extreme emotion.

## 8. Rig review checklist (before calling a rig done)

1. Symmetry: poses mirror exactly (X-Axis Mirror on during posing/weighting).
2. Every control has an obvious name and widget; no bare transform channels on deform bones.
3. FK/IK switch matches; no pops when scrubbing the property 0→1.
4. Knees/elbows point correctly with pole targets; no flips through a normal range.
5. All test-battery poses deform cleanly; no candy-wrapper wrists.
6. Face: all keys reachable from the interface; blinks/jaw work with head rotated.
7. File is clean: no stray objects, consistent collections, transforms applied.
