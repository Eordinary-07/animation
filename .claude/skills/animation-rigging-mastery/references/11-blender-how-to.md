# Blender How-To — Exact Procedures for Every Skill Task

Task-oriented click/operator manual. When the other references say WHAT to do,
this file says HOW to do it in Blender (4.x). Follow the numbered steps literally.

---

## A. RIGGING

### A1. Create the skeleton and place joints
1. `Shift+A → Armature` in Object Mode. Name the armature `DEF_rig`.
2. `Tab` into Edit Mode. Select the default bone: its tail is the first joint — place the
   hip joint with `G`. Bone length = distance to the next joint.
3. Extrude the chain: select the bone TAIL (last joint) → `E` to extrude → `G` to place the
   next joint (spine → chest → neck → head; thigh → shin → foot → toe).
4. Limbs: select the spine/chest bone tail → `E` for clavicle → `E` for upper arm → `E`
   forearm → `E` hand. Fingers: `E` per phalanx from the knuckle line.
5. Asymmetry-free naming: name every bone in the N-panel (`N → Item → Name`) or Outliner
   with `_L`/`_R` suffixes (`thigh_L`, `shin_L`…).
6. Mirror the whole side: select all → `Armature → Symmetrize`.
7. Check pivots: put the 3D cursor at each anatomical hinge (`Shift+S` snaps) and verify
   bone heads sit exactly on elbows/knees/hips/shoulders.

### A2. Fix bone roll (Maya's "joint orientation")
1. Select all bones (Edit Mode).
2. `Ctrl+R` (Recalculate Roll) → choose **Global +Z Axis** for limbs, then fine-tune:
   select a bone → `N → Item → Transform → Roll` (type degrees) or `Ctrl+R` drag.
3. Verify: `Armature Properties (green running-man) → Viewport Display → Axes` — the Y axis
   (green) must run ALONG every bone. Reason: consistent local axes = predictable rotations.

### A3. Add IK to an arm or leg
1. `Tab` to Pose Mode. Select the bone that should BEND (shin/forearm — not the thigh!).
2. Properties → **Bone Constraints** (blue bone icon) → `Add Bone Constraint → Inverse Kinematics`.
3. Target: the armature itself; Bone: the hand/foot **control** bone.
4. Chain Count: `2` (shin+thigh). Reason: 2-bone analytic solve is exact and stable.
5. Pole Target: elbow/knee control bone. Rotate the control until the knee points the right
   way; if it pops, adjust **Pole Angle** in ±45° steps (typically ±90).
6. Test: move the foot control in Pose Mode — the knee must track the pole through the
   whole range (see `02-rigging-blender.md` test battery).

### A4. Build an FK/IK switch (Maya's blending)
1. Select the master control bone → `Bone Properties → Custom Properties → New` →
   rename `ik_fk`, set min `0`, max `1` (gear icon → edit UI range).
2. Right-click the IK constraint's **Influence** slider → `Add Driver` →
   Driver Editor: type `Single Property`; Prop: the armature →
   `pose.bones["ctrl_master"]["ik_fk"]`; Expression: `1 - var` (IK off when switch = 1? —
   convention: `var` = IK strength, so IK influence = `var`, FK influence = `1 - var`).
3. Add `Copy Transforms` constraint (FK chain bones copying control FK bones) with
   Influence driven by `1 - var`.
4. Pose at `ik_fk = 0` and `1` — the limb must not jump. Fix offsets with the FK controls.

### A5. Custom controls + drivers (Maya's Set Driven Key)
1. Add a property: select control bone → `Bone Properties → Custom Properties → New`.
2. For a driven channel (e.g. shape key value, constraint influence, bone rotation):
   right-click the channel → `Add Driver` (or `Copy as New Driver` on the source property,
   then `Paste Driver` on the target).
3. Edit Driver (`Drivers` tab in Graph Editor or right-click → Edit Driver):
   `Single Property` → armature → `pose.bones["ctrl_face"]["blink_L"]`; Expression `var`.
4. For multi-influence (one slider → several keys): add more variables, use
   `min(max(var,0),1)`, `var*0.5`, etc. Keep expressions one-liners.

### A6. Weight painting (skin binding)
1. Select mesh → `Shift` select armature → `Ctrl+P → With Automatic Weights` (fast baseline),
   OR add the Armature modifier manually and skip parenting.
2. Select mesh → `Weight Paint` mode (mode dropdown, top-left). Vertex groups already
   match bone names.
3. Paint rules (`02`): default brush on hard areas, Blur to smooth transitions,
   Subtract for cleanup. Check the far side — weights often leak through the body.
4. Normalize: `Weights → Normalize All` (weights sum to 1). Optional: `Weights → Limit Total`
   to 4 (real-time budget).
5. Paint in EXTREME poses (raise the arm, squat) — not just rest pose. Toggle Pose Mode to
   test between strokes.
6. Shoulder/hip disasters: add helper bones (small bones at armpit/shoulder cap), assign a
   few weights to them, make them deform (`Bone Properties → Deform ✓`).

### A7. Face: shape keys (Maya's blend shapes)
1. Select mesh → `Object Data Properties` (green triangle) → `Shape Keys` → `+` (auto "Basis").
2. `+` again per target: rename `vis_EE`, `vis_BMP`, `blink_L`, `brow_up_L`, `smile`…
3. Sculpt each: set its Value slider to `1.0`, `Tab` into Edit Mode, move verts with
   proportional editing (`O`). Every vertex stays in the key — full-mesh deformation.
4. Test combinations: stack sliders; fix poke-throughs with corrective keys
   (`+` → sculpt on top of the combination → New Shape Key from Mix when done).
5. Bulk-create from a posed mix: set sliders to a combo → shape-key dropdown ▼ →
   **New Shape Key from Mix**. From another mesh: **Join Shapes**.
6. Drive them from custom properties (A5) so animators use sliders, not raw keys.

### A8. Face: jaw + eyes
1. Jaw: extrude one bone from the ear joint down to the chin (Edit Mode, `E`), name `jaw`.
   Rotate in Pose Mode to open. Drive its X-rotation with `jawOpen` property (A5).
2. Eyes: two short bones from the eye center pointing FORWARD out of the face.
   Add two empties (`Shift+A → Empty`) as gaze targets.
3. Eye bones → `Bone Constraints → Damped Track` → Target: the eye empty. If the eye looks
   backwards, flip the constraint's **To** axis sign.
4. Parent both empties to a `gaze_ctrl` bone; animating that bone = eye movement.
   Lids: blink shape keys driven by `blink_L/R` (A7) or lid bones + limits.

---

### A9. Twist distribution bones (kill the candy-wrapper forearm/shin)
A single forearm bone collapses the mesh when the wrist rolls. Share the roll:
1. Edit Mode: add `DEF-forearm_twist_a.L` (at ~1/3 from elbow) and `DEF-forearm_twist_b.L`
   (at ~2/3), both children of `DEF-forearm.L`, same roll as the forearm (A2).
2. Pose Mode: each twist bone gets **Copy Rotation** → target = the hand bone, **Local
   Space → Local Space**, only the bone's local **Y** axis enabled, Influence **0.33**
   (a) and **0.66** (b). The forearm keeps 0, the hand keeps 1.0 — roll now ramps.
3. Weight Paint: split the old forearm weights across forearm → twist_a → twist_b → hand
   as a smooth gradient (Gradient tool), Auto Normalize ON, then `Normalize All`.
4. Test: roll the wrist ±180° — volume survives, no pinch. Same recipe for shin (target =
   foot bone) and upper arm (target = forearm).

### A10. Spline-IK spine (FK-friendly, stretchy, twists evenly)
1. Chain of 4–6 `DEF-spine` bones hips → chest. Add a **Bézier curve** along the spine with
   3 control points (hips / mid / chest).
2. Select each curve point → `Ctrl+H` **Hook to New Object** → rename `HK-hips`, `HK-mid`,
   `HK-chest`. Parent the end hooks to your COG and chest control bones; mid hook to a
   mid-spine control. Animators pose 3 controls, the curve does the smoothing.
3. Top DEF spine bone → Bone Constraints → **Spline IK**: Target = the curve, Chain Length
   = number of spine bones, **Y Stretch** ON, XZ Scale Mode = *Volume Preserve* for fat /
   cartoon characters, *None* for hard bodies.
4. Twist comes from rotating the chest hook around the spine axis — keep hook count at 3
   or the spline fights you. Test battery: bend/side/twist ±90°, no kinks, head stable.

### A11. Space switching (IK target or prop changes parent mid-shot)
Industry pattern for "hand sticks to table, then to chest, then grabs the cup":
1. Create one anchor Empty per space (`ANC-table`, `ANC-chest`), each parented into that
   space (chest anchor parented to the chest control bone via Bone parenting).
2. The IK target (or the prop object) gets **Child Of** constraints, one per anchor.
   With each, click **Set Inverse** so nothing jumps at setup time.
3. Add a custom property `space` (0.0–1.0) on the control; drive both influences:
   anchor A influence = `1 - space`, anchor B = `space` (A5 driver workflow).
4. **Animate the switch**: on the switch frame, FIRST bake the current world pose —
   object: `Ctrl+A` *Apply Visual Transform*; pose bone: `Pose → Apply → Visual Transform
   to Pose* — key it, THEN key `space` to the new value on the same frame. No pop.
5. Prop grab = the same pattern mirrored (Child Of on the prop → hand anchor, keyed on the
   contact frame; release = switch back to world anchor after a visual-transform key).

### A12. Pose-driven corrective shape keys (PSD-style volume fixes)
For the shoulder-raise collapse, elbow/knee volume loss, hip crease:
1. Pose the joint to the problem angle.
2. Mesh → Shape Keys → `+` → name it `corr_shoulder_R`, leave Value 0.
3. On the Armature modifier enable **On Cage** (the triangle "adjust edit cage" icon) so
   Edit/Sculpt mode shows the *posed* mesh; select the corrective key and sculpt the
   volume back. (Deltas are stored in rest space automatically.)
4. Return to rest pose. Right-click the key's **Value → Add Driver**: Type *Scripted
   Expression*; variable = the joint bone's rotation channel (Transforms, Local Space,
   e.g. Rot X). Map radians → 0..1, e.g. `min(1.0, max(0.0, (rot - 0.6) / 0.9))`, then
   shape the response in the driver's Graph Editor curve if needed.
5. Sweep the joint through its whole range: corrective must fade in/out cleanly and not
   fight the opposite side. Mirror with Shape Keys menu → *Mirror Shape Key* and re-test.
6. Combination problems (smile + jaw-open poke-through) get a combo key whose driver is
   the *product* of the two source values.

### A13. Lid follow + inner mouth parenting (extends A8)
- **Lid follow**: upper-lid shape key (or lid bone) driven by the eyeball bone's local X
  rotation — look down and the lid follows at ~70%. Blink remains its own key on a linear
  curve (Osipa, ref 06); never bake blink into the follow driver.
- **Inner mouth**: upper teeth weighted 100% to the head bone; lower teeth + tongue chain
  (2–3 small bones) weighted 100% to the **jaw** bone. If jaw is a shape key instead,
  parent a `MCH-jaw` bone to the head and drive its rotation from the same jaw slider so
  teeth/tongue still travel with the mouth.

## B. ANIMATION

### B1. Blocking (pose-to-pose, Stepped)
1. Pose Mode. At frame 1 pose the first extreme; select ALL bones → `I` → `Loc/Rot/Scale`.
2. Name the Action in the Action Editor (`Shift+F8` or Dope Sheet → Action). Insert a
   marker per beat (`M`, rename).
3. Jump to each beat's frame, pose the extreme, key all bones again.
4. Set interpolation to Stepped: Dope Sheet → select all keys → `T` → **Constant**
   (constant = stepped blocking). Playblast (`Ctrl+F12` with low samples) — the poses
   must read as a silent story.

### B2. Breakdowns and polish
1. Turn off Constant (`T` → Bezier) once blocking reads. Use the **Breakdowner**:
   hover the Dope Sheet between two keys, hold `Shift+E`, drag to set the breakdown's
   interpolation factor, click to insert.
2. Shaping: Graph Editor — select curves, shape handles (`V` = Vector, `A` = Aligned,
   `Y` = Free); impacts get Vector handles, settles get soft clamped curves.
3. Overlap/stagger (from `03`): select the later parts (head/chest/hair), shift their keys
   2-6 frames right in the Dope Sheet. Stagger = successive 1-frame offsets per part.
4. Arc check: Pose Mode → `Pose → Motion Paths → Calculate`. Bad kinks = fix spacing.
5. Walks: follow `04-body-mechanics.md` Recipe with X-Axis Mirror on (Options → X-Axis
   Mirror); copy flipped poses with `Ctrl+C` / `Ctrl+Shift+V`; loop with
   `Graph Editor → Add F-Modifier → Cycles`.

### B3. Dialogue & lipsync
1. Import audio: `Video Sequencer → Add → Sound` (or speaker object). Note phrase
   accents on the timeline as markers (`M`).
2. Key the mouth shapes at the RIGHT TIMES first (closures MBP exact; vowels approximate) —
   set shape-key values in the Object Data tab (or driven sliders, A7/A5).
3. Jaw follows: key `jawOpen` on the same beats.
4. Eyes/brows pass: gaze moves, blinks at thought changes (2-4 frames close), brow
   changes on acting points.
5. Offsets (Osipa "connecting"): shift brow keys 1-2 frames BEFORE mouth, cheeks after,
   lids between. Never all on the same frame.

---

### B4. Pose library — the modern Asset Browser way (Blender 4.x)
1. Create: Pose Mode, select the bones the pose needs → `Pose → Create Pose Asset`.
   Name by INTENT, not anatomy (`angry_point`, `beg_hands`, `sneak_low`). The asset lives
   in the file as an Action marked as asset.
2. Make it global: keep a `POS_lib.blend` in a folder registered under
   `Preferences → File Paths → Asset Libraries` — every shot file then sees the library.
3. Apply: Asset Browser → drag or double-click the pose; bottom-left **Blend** slider mixes
   it with the current pose (60% golden pose + 40% current is a great start); tick
   **Flipped** for the mirror; apply to *selected bones only* for partial poses (hands!).
4. Rule (Williams): library poses are *starting points* — after applying, offset timing,
   break symmetry, push the silhouette (ref 05). A pasted pose shipped unchanged reads stock.

### B5. Video reference — shoot it, sync it, steal timing not positions
1. Shoot yourself acting the shot (Hooks' rehearsal, ch. 4; Williams: act it out). Fix the
   camera at the SHOT's angle; slate the frame-1 pose; do 3 takes, keep the one with intent.
2. Import: `Add → Image → Reference` (video file) beside the set, or Camera →
   *Background Images* for in-shot comparison. Set the image's frame **Offset** so the
   reference's first contact lands on your shot's contact frame; opacity ≈ 0.5.
3. Extract: key only the *contacts, accents and eye-darts* from the reference (frame
   numbers into the dope sheet as markers `M`). Then animate YOUR spacing/arcs to those
   beats — tracing positions frame-by-frame (rotoscoping) produces dead, floaty motion
   (Hooks ch. 8). Exaggerate what the reference whispers.

### B6. Thumbnailing & draw-overs (Williams' "small thinking drawings", in Blender)
Williams: small thinking drawings "show if the idea is working" (bundled p. 337); The
Procedure tests planning drawings BEFORE key positions (ref 09). In Blender:
1. Add a **Grease Pencil** object `GP_thumbs`, draw in camera view (Draw Mode, placement =
   View). 6–10 rough stick poses at the planned key frames — one per story beat, intent
   first, anatomy last.
2. Scrub the timeline: do the beats read in sequence? If a thumb doesn't read at thumbnail
   size, the pose won't read at render size — fix it here, where it costs seconds.
3. Draw-overs on review: drop the playblast into the Video Sequencer and use the
   **Annotate** tool in the preview to sketch better arcs/poses over your own frames,
   then match the rig to the drawing. Keep the GP object in the shot file (hidden at render).

### B7. Graph Editor cleanup & baking (where polish becomes exportable)
- **Euler flips** (limb suddenly spins 360° between two keys): select that bone's Euler
  channels → Graph Editor `Key → Euler Filter`. Prevention: pick rotation orders before
  animating (shoulders/hips = order that puts the twist axis LAST; see ref 07).
- **Redundant keys**: `Key → Clean Keyframes` (small threshold) after auto-key sessions;
  after bakes/mocap use `Key → Decimate Keyframes` (Ratio mode) — then re-check every
  contact frame by hand; decimation eats accents first.
- **Read small channels**: `View → Normalize` to inspect finger/eye curves; turn it OFF
  before judging amplitudes.
- **Bake Action** (`Pose → Animation → Bake Action`): turns IK/constraints/drivers into
  plain FK keys — Visual Keying ON, frame step 1 (step 2 for a deliberate twos feel).
  Mandatory before game-engine export, retargeting, or freezing an approved cycle.
  Always bake on a DUPLICATE action/rig; the constrained original stays editable.
- Keep one Action per shot (ref 10); approved cycles get pushed to the **NLA** as strips,
  with additive strips layered for attitude (head/arms) instead of editing the base cycle.

## C. CAMERA & CUTS

### C1. Camera setup & shot binding
1. `Shift+A → Camera`. `N → Item` to place; `Ctrl+Alt+Numpad0` snaps it to your view.
2. `Camera Properties` (green camera): Focal Length (50mm neutral; 24 wide; 85 close-up),
   Depth of Field ✓ → Focus Object = an empty at the eyes → f-stop 2.8–5.6 (close-ups).
3. Multiple shots: one camera per shot (`CAM_s010`, `CAM_s020`…). In the Timeline:
   at the shot's first frame select its camera → `M` (marker) → rename `s010` →
   `Ctrl+B` (**Bind Camera to Marker**). Scrub — the cut plays.

### C2. Camera moves
1. **Dolly/pan**: keyframe the camera (or its parent empty) Location/Rotation at the move's
   start and end frames only. Ease: Graph Editor handles (auto-clamped default is fine).
2. **Arc/orbit**: add an Empty at the subject → camera gets `Child Of` (or Track To for the
   aim + parent for position) → rotate the empty; or `Follow Path` on a Bezier circle.
3. **Handheld**: insert one keyframe on camera rotation (and location) → Graph Editor →
   select each channel → `Add F-Modifier → Noise` — Scale ~20-40, Strength ~0.02-0.05
   (rotation), different Phase per axis.
4. **Focus pull**: keyframe `Depth of Field → Focus Distance` (or animate the focus empty's
   position) on the beat where attention shifts.

---

## D. PRODUCTION & DELIVERY

### D1. Playblast & animatic
1. Quick blast: `Output Properties` → Frame range, Resolution % 50, `Output → File Format
   FFMPEG → MPEG-4 (H.264)`; `Ctrl+F12` renders the animation with the viewport engine.
2. Animatic: `Video Sequencer` workspace → `Add → Scene Strip` per shot (each scene uses
   its marker-bound cameras) → `Add → Sound` for dialogue/music → drag strip edges to
   retime the cut (this is the bar sheet/Leica reel).

### D2. Render
1. `Render Properties` → Engine: **EEVEE** (fast/style) or **Cycles** (realistic light).
2. `Output Properties` → Resolution X/Y, FPS 24 (or as requested).
3. `Output → File Format`: FFMPEG/MPEG-4/H.264 + AAC audio for delivery; PNG if
   compositing.
4. `Ctrl+F12` = render animation; `F12` = current frame. Check first/last frames before
   overnight renders.

### D3. Springs & secondary motion (no-sim quick method)
1. For tails/hair/antenna: chain 3-6 bones; rotate the FIRST bone by the main action.
2. Overlap: in Graph Editor, `Add F-Modifier → Noise` on the child bones' rotation channels
   (small strength), OR shift their keys +2-4 frames and add 1-2 overshoot keys (Williams'
   stagger). For true dynamics use `Bone Constraints → Spline IK` + curve hooks or a
   softbody/cloth sim (`07-math-procedural.md`).

---

### D4. Library Override shot workflow (how real Blender productions are organized)
Never animate inside the character's source file. One source of truth, many shots:
1. **Publish**: in the character file, one collection `CHR_<Name>` holds rig + meshes
   (controls in CTRL bone collection; DEF/MCH hidden). Save. This file is read-only for
   animators from now on.
2. **Link**: in the shot file, `File → Link` → the `CHR_<Name>` collection. It arrives as
   an instance — not yet animatable.
3. **Override**: Outliner → right-click the linked collection → *Library Override → Make…*
   (choose the rig as the root). Bones/properties become locally animatable; geometry and
   rig logic still live in the source.
4. **Animate** in the shot file only (actions, poses, overrides are stored per-shot).
5. **Update**: when the rig is fixed in the source, shot files pick it up on reload;
   if structure changed, Outliner → right-click → *Library Override → Resynchronize*.
6. Solo/one-off work may `File → Append` instead — but anything multi-shot gets
   Link + Override, or rig fixes become copy-paste archaeology.

## E. Verification (run after every rig or shot)

| Check | Where |
|---|---|
| Rig symmetrical & bones oriented | Axes display (A2), Symmetrize |
| IK/FK switch no jump | A4 test at 0 / 0.5 / 1 |
| Weights normalized, ≤4 influences | `Weights → Normalize All`, `Limit Total` |
| Pose battery passes | `02-rigging-blender.md` §6 |
| Blocking reads silent | B1 playblast |
| Arcs clean | B2 motion paths |
| Cameras bound per shot | C1 marker colors in timeline |
| Output settings correct | D2 |

## F. Troubleshooting — symptom → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| IK arm/leg pops or flips mid-shot | Pole target crossed the chain plane, or chain hit perfectly straight (singularity) | Keep a whisper of bend in rest pose; move pole farther out; key the pole; cap IK stretch |
| FK↔IK switch jumps | Pose not matched at the switch frame | Visual-transform snap both ways on the switch frame (A4/A11), key the switch driver there |
| Feet slide in a walk cycle | Root speed ≠ stride length ÷ cycle time | Measure contact-to-contact stride in the viewport, set root motion to match; stance keys get even spacing |
| Forearm twists like a candy wrapper | Single bone carries all wrist roll | Twist distribution bones (A9) |
| Shoulder/armpit collapses on raise | Weights alone can't hold volume | Corrective shape key driven by upper-arm rotation (A12) + give the clavicle its own action |
| Limb spins 360° between two keys | Euler interpolation took the long way | Graph Editor `Key → Euler Filter` (B7); reorder axes before animating (ref 07) |
| Smile + open jaw poke through cheek | Two shape keys fight in combination | Combo corrective key driven by the *product* of both values (A12 step 6) |
| Spline-IK spine twists strangely | Curve point tilt / too many hooks | Clear tilt (`Alt+T` in curve edit), keep 3 hooks (A10) |
| Lip sync reads late/robotic | Mouth leads, thought trails | Body/head start 2–4 frames BEFORE the jaw (movement precedes words — Hooks ch. 6, Osipa); verify audio offset by scrubbing with sound |
| Everything feels floaty/even | Default spline interpolation, no breakdowns | Add eccentric breakdowns, shape the handles (ref 03); check with Motion Paths — "there are no inbetweens" (Williams p. 89) |
| Weights bleed onto the wrong limb | Unnormalized or stray vertex groups | Paint with Auto Normalize ON → `Weights → Normalize All` → `Limit Total (4)`; inspect per-vertex groups in Edit Mode's *Vertex Weights* panel |
| Playblast differs from viewport / a bone lags one frame | Dependency cycle (driver chasing its own target) | Read the System Console for "Dependency cycle detected"; retarget the driver to a MCH bone that doesn't depend on the driven one |
| Pose asset flips the wrong way | Applied without mirror naming | Bones must use `.L/.R` suffixes (A1); re-apply with *Flipped* (B4) |

## G. bpy mini-toolkit (Blender 4.x-safe patterns)

Script the repetitive rigging; never click 200 bones by hand. Three patterns that cover
most requests — run in the Scripting workspace, test on a copy first:

```python
# 1) Sort bones into DEF-/CTRL-/MCH- bone collections by name prefix (4.0+ API)
import bpy
arm = bpy.context.object  # select the armature first
for b in arm.data.bones:
    for prefix in ("DEF-", "CTRL-", "MCH-"):
        if b.name.startswith(prefix):
            name = prefix.strip("-")
            coll = arm.data.collections.get(name) or arm.data.collections.new(name)
            coll.assign(b)
```

```python
# 2) Driver for a corrective shape key from a bone's local X rotation (see A12)
import bpy
mesh = bpy.data.objects["Body"]
key = mesh.data.shape_keys.key_blocks["corr_shoulder_R"]
drv = key.driver_add("value").driver
drv.type = 'SCRIPTED'
var = drv.variables.new(); var.name = "rot"; var.type = 'TRANSFORMS'
var.targets[0].id = bpy.data.objects["Rig"]
var.targets[0].bone_target = "DEF-upperarm.R"
var.targets[0].transform_type = 'ROT_X'
var.targets[0].transform_space = 'LOCAL_SPACE'
drv.expression = "min(1.0, max(0.0, (rot - 0.6) / 0.9))"  # radians -> 0..1
```

```python
# 3) Bake constraints/IK to FK keys on the ACTIVE pose (duplicate the rig first!)
import bpy
bpy.ops.nla.bake(frame_start=1, frame_end=120, step=1, only_selected=False,
                 visual_keying=True, clear_constraints=False, bake_types={'POSE'})
```

Cautions: `bpy.ops` calls depend on context (active object + mode) — set them explicitly;
Blender 4.4+ uses *layered Actions* (slots), so legacy scripts that poke `action.fcurves`
directly may need `action.layers[…].strips[…].channelbag.fcurves` instead — prefer
operators and drivers over raw f-curve surgery, and keep production scripts in `tools/`
(ref 10) so the pipeline is reproducible.

---

## H. Shading & texturing (refs 16–17)

### H1. Connect a PBR texture set (Node Wrangler)
1. Object Mode → select object → **Shading workspace** → **New** material.
2. Select the Principled BSDF → **Ctrl+Shift+T** → in the file dialog, multi-select the
   set (basecolor, roughness, metallic, normal) → **Principled Texture Setup** wires
   them with correct color spaces. (Node Wrangler ships enabled in 4.x; otherwise
   Edit → Preferences → Add-ons.)
3. Verify manually, every time: Base Color = **sRGB**; roughness/metallic/normal =
   **Non-Color**; Normal Map node present (strength 1). Imported DirectX normal? Add a
   Separate Color → invert Green → Combine Color before the Normal Map node.
4. Judge in **Rendered** shading (Z), never Material Preview alone — its pretty HDRI
   hides illegal values.

### H2. Procedural worn painted metal (no images)
1. Principled: Metallic 1 (driven below), Base Color = steel F0 (0.56, 0.57, 0.58).
2. Geometry → **Pointiness** → Color Ramp (tighten) = edge-wear mask; Texture Coordinate
   (Object) → Noise Texture (scale 5, detail 5) = grime variation; second Noise (scale
   25) → Bump (strength 0.15, distance 0.002 at true scale).
3. Mix the edge mask into **Roughness**: edges ≈ 0.35, field ≈ 0.65 (Math/Mix node) —
   handled metal polishes on edges.
4. Paint layer: big-scale Noise (scale 2) → Color Ramp as a chipped-paint mask → Mix
   Shader-ish mixing of Base Color (paint color vs steel) AND Metallic (paint 0 vs
   steel 1) with the *same* mask — chips reveal substrate and flip the metal bit
   together (ref 16 §3). Rust in the cavities: same mask trick, Pointiness inverted,
   rust albedo in the 30–240 band, Metallic 0, Roughness 0.9.

### H3. Skin (connect to A9/A12 facial work)
1. Albedo map (no baked shading) → Base Color. **Subsurface Weight 0.3–0.5**, Radius
   ≈ (1.0, 0.35, 0.2) — character MUST be real height in meters or SSS reads wax.
2. Pore/wrinkle normals at Strength ≈ 0.7 (over-strong pores = orange peel); micro-bump
   from the roughness map's inverse for pore sheen.
3. Roughness map zones: T-zone (forehead/nose/chin) ≈ 0.45, cheeks ≈ 0.6, lips ≈ 0.35 —
   paint zones, never one value. Thickness map → ears/nostrils glow correctly under rim.
4. Prove it under the three-light test (H7) at ECU distance — skin that only works in
   one HDRI fails on set.

### H4. Glass / water / car paint (quick recipes)
- **Glass**: Transmission Weight 1 · IOR 1.5 · Roughness 0.05 · solid geometry (or
  Surface Thickness) · the object behind must exist — glass is mostly refraction.
- **Water**: Transmission 1 · IOR 1.33 · Base Color white (the tint comes from
  Volume Absorption in the Volume socket for depth).
- **Car paint**: metallic-flake base (Base Color = paint color, Metallic 0.6–1 flake
  trick *or* metallic flakes via noise mask), **Coat Weight 1, Coat Roughness 0.05** —
  the clear coat is a separate physical layer; don't fake it with low base roughness.

### H5. Bake high-poly → low-poly (Cycles)
1. Low-poly: clean UVs (§B/H6), smooth shading set before baking, margin ≥ 16 px.
2. In low-poly's material: add an **Image Texture** node with a NEW blank image
   (4096², Non-Color for normal), select that node (white outline = bake target).
3. Render Properties (Cycles) → **Bake**: Bake Type **Normal**, **Selected to Active**
   ON, Extrusion ≈ 0.02–0.1 m (must enclose the high-poly), Max Ray Distance a little
   more. Margin 16.
4. Outliner: select HIGH-poly first, then Shift-select LOW (active object highlighted)
   → **Bake**. Inspect: black patches = rays missed → raise Extrusion; wavy edges =
   low-poly shading mismatch (support loops / hard edge = UV seam).
5. Repeat for AO (Bake Type Ambient Occlusion) and curvature proxies; save images
   (Image → Save As) — bakes are unsaved until you do.

### H6. UV unwrap + texel density
1. Edit Mode → select seam edges (**Ctrl+E → Mark Seam**) at hidden places (ref 17 §2).
2. Select all (A) → **U → Unwrap** (Angle Based default; Conformal for cylindrical
   forms). UV Editor: check with a checker texture (Image → New → Generated Type:
   **Color Grid**) — squares must be even and uniformly sized.
3. Texel density: UV menu → **Average Island Scale**, then **Pack Islands** (margin
   0.003–0.01). Face exception: scale face island 2× before packing.
4. UDIM: Image Texture → Source **Tiled**; UV Editor **N-panel → Add Tile**; islands
   per tile (face 1001, body 1002…) — bake/paint per tile.

### H7. Lookdev scene (3-light test, ref 16 §6)
1. World: neutral studio HDRI, Strength 1. Render → Color Management → **AgX**.
2. Add a chrome ball + grey ball + color checker prop next to the asset (the classic
   lookdev trio — Jeremy Birn's workflow chapter logic): if the balls look right and the asset
   doesn't, the recipe is wrong.
3. Swap: high-noon sun HDRI → interior warm HDRI. Approve ONLY materials that read
   correctly under all three, at the shot's final camera distance.
4. Save the lookdev .blend as a library asset (B6) — every hero material passes here
   before it touches a shot.

### H8. Substance 3D Painter round-trip (hero texturing standard — doctrine in ref 21B)
1. **Blender prep**: true scale; names `Part_low`/`Part_high`; UVs finished + texel
   density set (H6); material slot per texture set; vertex-color IDs if needed.
2. Export FBX (selected objects; check scale pre/post). Keep the low's UVs frozen after
   this point.
3. **Painter**: New Project → template *PBR - Metallic Roughness*, Normal = **OpenGL**,
   resolution per asset class, UDIM on if the asset uses tiles → select the low FBX.
4. Texture Set Settings → **Bake Mesh Maps**: load the high FBX, match by name, tune
   Max Frontal/Rear distances, bake Normal/AO/Curvature/Position/Thickness/WS-Normal,
   AA 4×4. Solo-inspect each baked map.
5. Paint in physical layer order (substrate → variation → wear → dirt → micro);
   generators art-directed and broken by hand/noise masks; albedo in the 30–240 band;
   metallic binary; roughness carries the most variation.
6. Export Textures with the Blender preset (`_BaseColor/_Roughness/_Metallic/_Normal`,
   Normal OpenGL, padding dilation-infinite; Height 16-bit only if used).
7. **Blender**: connect with Ctrl+Shift+T (H1), verify Non-Color on data maps, Tiled
   source for UDIM, approve ONLY via the 3-light test here (H7) — Painter's ACES
   viewport is not the approval room.

### H9. Pre-render optimization pass (ref 20)
1. Render Properties → Performance: **Persistent Data** ON (animation). Simplify OFF
   for finals (viewport-only drug).
2. Sampling: **Adaptive** with noise threshold (0.01 final / 0.005 hero ECU), Denoise =
   OpenImageDenoise. Light Paths: clamp indirect 10; caustics off unless hero;
   transparent/transmission bounces counted from the shot's actual layers (Jeremy Birn rule).
3. Per-object: Subsurf viewport 1 / render per-shot; instances instead of copies;
   off-camera sets disabled in render (not just hidden).
4. Texture audit: sort by size in the Outliner (Blend file view) — anything 4K that is
   never seen above ~800 screen px gets a 1K version for this shot.
5. Bake approved sims; freeze approved procedural stacks to maps (archive the live
   nodes in a disabled collection). Render 1 test frame at 100% + check stats (time/
   peak) before committing the range; log numbers in LESSONS.md (ref 19 §4).
