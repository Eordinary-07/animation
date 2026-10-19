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
