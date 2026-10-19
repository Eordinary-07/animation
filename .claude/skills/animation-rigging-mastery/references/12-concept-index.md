# Master Concept Index — Every Concept of All 8 Books (Self-Contained)

This index guarantees the skill works WITHOUT the PDFs. Every concept the library
teaches is listed here with its essence and where its HOW lives in this skill.
Nothing in this skill requires opening a PDF.

Format: **Concept** — essence — → reference file.

---

## 1. Rigging & Character Setup (Cabrera; Parent ch. 5, 10; Osipa ch. 11)

- **Character design for deformation** — pivots clear, silhouette strong → 02 §1
- **Character sheets (model sheets)** — front/side/back before modeling → 02 §1
- **Topology for animation** — even quads, edge loops (eyes/mouth/joints) → 02 §1
- **Blend shapes / shape keys** — sculpted targets, full-face sets → 02 §2, 06, 11 A7
- **Deformation order** — what evaluates before/after (keys vs armature) → 02 §2
- **Joint placement** — joints at anatomical rotation centers → 02 §3, 11 A1
- **Joint orientation / bone roll** — consistent local axes (Y along bone) → 02 §3, 11 A2
- **Symmetrize / mirroring** — .L/.R naming, Symmetrize → 11 A1
- **FK (forward kinematics)** — chain rotations; arcs & spine → 02 §4
- **IK (inverse kinematics)** — end-effector solves; feet/hands → 02 §4, 07 §5, 11 A3
- **IK solvers: analytic 2-bone / Jacobian / CCD / FABRIK** — when each applies → 07 §5
- **Pole targets / pole angle** — fixes the knee/elbow bend plane → 02 §4, 11 A3
- **FK/IK switching** — property-driven constraint blending, no jump → 02 §4, 11 A4
- **Stretchy limbs** — distance ratio → scale drive + squash → 02 §4, 07 §6
- **Attribute control / custom properties** — the animator interface → 02 §4, 11 A5
- **Set driven keys → drivers** — property → channel mapping → 02 §4, 11 A5
- **Control objects / widgets** — never animate deform bones → 02 §4
- **Foot roll pivots** — heel → ball → toe chain → 02 §4
- **Scene cleanup / naming** — ctrl_/def_/jnt_/wgt_, locked channels → 02 §5
- **Skinning / smooth bind** — armature modifier + vertex groups → 02 §6, 11 A6
- **Weight painting rules** — normalized, ≤4 influences, extreme poses → 02 §6, 11 A6
- **Helper/dummy influences** — shoulder/hip hard spots → 02 §6
- **Rig test battery** — touch toes, overhead reach, squat, twists → 02 §6-8
- **Face rig hybrid** — shape keys + jaw/eye bones + drivers → 02 §7, 06 §5, 11 A7/A8
- **UV mapping for deformation** — stretch zones survive posing → 01 (Cabrera ch. 4)
- **File referencing / library overrides** — rig & mesh separation; full link → override →
  animate → resync workflow → 02 §3, 11 D4
- **Twist distribution bones** — share wrist/ankle roll 0.33/0.66 to keep volume → 11 A9
- **Spline-IK spine** — 3-hook curve spine, pose-friendly stretch + even twist → 11 A10
- **Space switching** — IK/prop parent changes mid-shot without pops (Set Inverse + visual
  transform snap) → 11 A11
- **Corrective (PSD) shape keys** — pose-sculpted volume fixes driven by joint rotation →
  11 A12
- **Lid follow & inner-mouth parenting** — lid tracks the eyeball; teeth/tongue ride the
  jaw → 11 A13
- **Pose assets (Asset Browser)** — create/blend/flip golden poses across all shots → 11 B4
- **Video reference workflow** — shoot, sync by offset, steal timing not positions → 11 B5
- **Thumbnailing & draw-overs** — Grease Pencil thinking drawings + Annotate over
  playblasts (Williams p. 337) → 11 B6
- **Graph cleanup & Bake Action** — Euler Filter, Clean/Decimate, bake IK→FK for export →
  11 B7
- **Troubleshooting (symptom → cause → fix)** — IK pops, foot slide, gimbal flips, weight
  bleed, dependency cycles → 11 F
- **bpy mini-toolkit** — bone-collection sort, corrective drivers, batch bakes (4.x-safe) →
  11 G

## 2. Timing & Spacing (Williams; Whitaker; Illusion of Life)

- **Timing vs spacing** — timing = force/mood; spacing = speed → 03 §1
- **Extremes / keys** — decision poses → 03 §2, 11 B1
- **Breakdowns** — path-defining poses → 03 §2-3, 11 B2
- **Inbetweens** — the tweened motion → 03 §2
- **Three ways to animate** — straight-ahead / pose-to-pose / mix → 03 §2
- **X-sheet / bar sheet / exposure charts** — planned timing → 03 §2, 10 §4
- **Ones vs twos** — smoothness vs punch at 24fps → 03 §2
- **Charts (timing charts)** — spacing diagrams → 03 §2
- **Slow-in / slow-out (ease-in/ease-out)** — inertia at rest → 03 §4
- **Spacing doctrine** — never even; packed at force ends → 03 §4
- **Elongated inbetween** — snap via asymmetric breakdown → 03 §4
- **The "ruff" approach** — big masses first, then subdivide → 03 §4
- **Arcs in motion** — natural paths curve → 03 §4, 04 §1
- **Holds** — how long to hold; breathe in/out → 03 §5
- **Anticipation (surprise / invisible)** — prepare the eye → 03 §5, 05 §1
- **Follow-through & overlapping action** — parts stop at different times → 03 §5
- **Staggers** — successive offsets; vibration formula → 03 §5
- **Whip & wave actions** — energy transfer through chains → 03 §5
- **Takes & accents** — hard accent bounces; soft continues → 03 §5
- **Weight timing** — heavy = slower starts, longer settles → 03 §5
- **Size timing** — big = more frames → 03 §5
- **Force through flexible joints** — the physics of overlap → 03 §5
- **Oscillation decay** — pendulum settles → 03 §5, 07 §6
- **Settle recipe** — overshoot 1-3%, decaying returns → 03 §7
- **F-curve practice** — stepped blocking, handles, offsets → 03 §6, 11 B1/B2

## 3. Body Mechanics & Locomotion (Williams; Whitaker; Parent ch. 9)

- **Walk: weight first** — mass before detail → 04 §1
- **Walk tempo / stride math** — frames per step; stride = 2×step → 04 §1, §6
- **Contact & passing positions** — the two planning poses → 04 §1
- **Double bounce** — hips drop twice per cycle → 04 §1
- **Weight shift / belt line / shoulder counter-tilt** → 04 §1
- **Arm swing & counteraction** — lazy, opposite, overlapped → 04 §1
- **Heel strike / foot roll / toe-off** → 04 §1
- **Normal walk spacing** — tight at contact, spread mid-swing → 04 §1
- **The Recipe** (Williams p. 163) — 15 ways to get vitality in a walk: lean, straight legs
  on contacts, twist, flop knee/feet, belt line, delay toe-off/parts, counteraction, break
  joints, ups & downs, different timings, twist feet off parallel, alter one tiny part → 04 §1
- **Loosening up / breaking symmetry** — twinless life → 04 §1
- **Sneaks & tip-toe sneak** — low COG, careful spacing → 04 §1
- **Runs (4/3/2-drawing formulas)** — controlled fall, flight phase → 04 §2
- **Jumps** — crouch → launch → flight → impact → settle → 04 §2
- **Skips** — step-hop rhythm → 04 §2
- **Flexibility** — overlap, counteraction, breaking joints → 04 §3
- **Instant read (profiles)** — silhouettes that read → 04 §3
- **Weight & effort** — pressure; effort changes everything → 04 §4
- **Synchronising action rules** — big masses lead → 04 §4
- **Animal locomotion** — lateral/rotatory sequences, gallop, flight → 04 §5
- **Foot-slide prevention** — stride vs ground speed match → 04 §6
- **Walk mechanics (algorithmic)** — kinematics + dynamics of walk → 07 §6 (Parent)

## 4. Acting & Performance (Hooks; Thomas & Johnston; Williams)

- **The 12 principles** (squash&stretch, anticipation, staging, straight-ahead vs
  pose-to-pose, follow-through/overlap, slow-in/out, arcs, secondary action, timing,
  exaggeration, solid drawing, appeal) → 05 §1
- **Given circumstances** — the truth of the moment → 05 §2
- **Objective** — what the character wants NOW → 05 §2
- **Obstacle** — what's in the way → 05 §2
- **Tactics (verbs)** — animate actions on others, not words → 05 §2
- **The moment before** — energy already in motion → 05 §2
- **Thinking vs feeling** — body shows intent, face shows emotion → 05 §2
- **Movement provokes emotion** — pose the body to find the feeling → 05 §2
- **Gesture & body language** — the body cannot lie; hands → 05 §2
- **Status & posture** — power in weight and openness → 05 §2
- **Beats & turns** — tactic changes structure the scene → 05 §3
- **Contrast** — the readability principle → 05 §3
- **Acting points** — the moment the shot exists for → 05 §3
- **Twinning / symmetry** — Williams p. 324: symmetry is natural when "laying down the law";
  the sin is default, unbroken symmetry — emphasize symmetrically, then break it up → 05 §3
- **Seven Essential Acting Concepts** (Hooks ch. 1) — thinking→conclusions/emotion→action;
  acting is reacting + doing; objective; play an action until…; all action begins with
  movement; empathy is the magic key; a scene is a negotiation → 05 §2
- **Actor–audience contract / feeling of significance** (Hooks ch. 2) — lead the audience;
  everything on screen significant → 05 §2
- **Human Character Analysis (character bible)** (Hooks ch. 3, p. 22) — 21-question
  biography incl. inner rhythm, psychology, goals and dreams → 05 §2
- **Scene = negotiation; three conflicts** (Hooks ch. 4) — with another character / with
  himself / with his situation; status negotiations; scenes begin in the middle → 05 §2
- **Adrenaline moment** (Hooks ch. 4 & 12) — a scene the character would remember in old age → 05 §2
- **Power center** (Hooks ch. 5 & 11) — chest at ease; relocate it to invent character walks → 05 §2
- **Laban effort actions** (Hooks ch. 5) — Press/Wring/Glide/Float/Thrust/Slash/Dab/Flick =
  Space × Time × Weight; set spacing/ease from the verb → 05 §2, 03
- **Movement precedes words** (Hooks ch. 6) — impulse moves head/eyes/shoulders a beat ahead
  of the mouth; animate what is underneath the words → 05 §2, 06
- **Reaction shot / listen–react–speak** (Hooks ch. 7) — reactions carry 90%; closer camera =
  stiller performance → 05 §2, 08
- **Simplify: direct, simple, specific actions** (Hooks ch. 8) — play the specific action,
  not the general need; technique is whatever works → 05 §2
- **Comedy = drama exaggerated** (Hooks ch. 9) — heighten real stakes, never "funny movement" → 05 §2
- **No brainless inbetweens** (Williams p. 89) — every frame is on screen equally; design
  breakdowns, don't accept default interpolation → 03, 13
- **Eyes lead thought** — gaze, saccades, arrival order → 05 §3, 06 §3
- **Steal from life** — reference and act it out → 05 §3
- **Comedy** — surprise + contrast + timing → 05 §3
- **Dialogue as action** — subtext, phrasing, accents → 05 §3
- **Appeal & personality** — watchable characters (Illusion of Life) → 05 §1
- **Staging** — one clear idea per moment (camera + pose + timing) → 05 §1, 08
- **Story & character development** — foundation of everything → 05, 09
- **Live action reference** — study, don't copy → 05 §3

## 5. Facial & Lip Sync (Osipa)

- **Visimes, Osipa's 7 (B/M/P Closed, EE, FV, OO, IH, R, T/S + jaw sounds)** — "phonemes
  are sounds, visimes are shapes" → 06 §1 (the classic AI/E/O/U/MBP/FV/L/W/Q mouth chart
  is the traditional-animation alternative, not Osipa)
- **Consonants carry the read** — closures/accents beat vowels → 06 §2
- **Lip sync passes** — timing rough → phrasing → accents → polish → 06 §2, 11 B3
- **Phrasing & mouth rest** — mouth returns between phrases → 06 §2
- **Brow language** — inner/outer raises, furrow, cock → 06 §3
- **Eye keys** — lids, focus, saccades, blink timing (2-4 fr) → 06 §3
- **Squint** — the life in lower lids → 06 §3
- **Connecting features (offsets)** — brows→eyes→cheeks→mouth staggers → 06 §4
- **Dependencies & presets** — emotion = key combinations at partial values → 06 §5
- **Asymmetry** — one corner higher/faster → 06 §4
- **Facial landmarking** — anatomical map for modeling/rigging → 06 (ch. 3), 02 §2
- **Mouth/nose topology** — concentric loops → 02 §1, 06 §1
- **Squash, stretch & squoosh** — global face deformation life → 06 §5
- **Face interfaces** — sliders/panels, never raw keys → 06 §5
- **Dialogue shot production order** — audio → body → mouth → eyes → offsets → 06 §6

## 6. Camera & Cinematography (Parent ch. 1; Whitaker; Williams)

- **Shot sizes (EWS→ECU)** — each size is a psychological tool → 08 §2
- **Angles (eye/low/high/dutch/OTS/POV)** — power & feeling → 08 §3
- **Lenses & focal length** — 18mm→200mm language; dolly ≠ zoom → 08 §4
- **Depth of field & focus pulls** — focus = attention → 08 §4
- **Framing (thirds, headroom, leadroom, look space)** → 08 §5
- **180° rule & screen direction** — continuity of left/right → 08 §5
- **30° rule & jump cuts** → 08 §5
- **Camera moves (pan/tilt/truck/dolly/crane/handheld/arc)** — every move = emotion → 08 §6
- **Motivated movement; start/end on compositions** → 08 §6
- **Hook-ups & cutting on action** — continuity editing → 08 §7
- **Cuts as timing** — cut on accents; sound lead rules → 08 §7
- **Camera binding in Blender** — markers + Ctrl+B → 08 §8, 11 C1
- **Camera rigs** — Track To, Follow Path, handheld noise → 08 §8, 11 C2
- **Shot-design checklist** — one idea per shot → 08 §9

## 7. Directing & Production (Williams; Whitaker; Thomas & Johnston)

- **One-sentence story** — if you can't say it, you don't get it → 09 Stage 0
- **Script analysis: beats** — units of action/tactic change → 09 Stage 1
- **Shot list / slug lines** — beat → shot mapping → 09 Stage 2
- **Slugging & shot durations** — planning time (Whitaker) → 09 Stage 2
- **Storyboard & animatic (Leica reel)** — make the movie cheaply first → 09 Stage 3
- **Layout & blocking** — best foot forward; silhouettes in camera → 09 Stage 4
- **Silent-read test** — staging must carry the story → 09 Stage 6
- **Director's 10-point review** — the professional bar → 09 Stage 6
- **Professional level definition** — the quality contract → 09 end
- **Production procedures** (story→layout→animation→cleanup) — Disney pipeline → 01, 09
- **Voice recording, hook-ups, research, editing** (Williams Directing) → 09, 05 §4
- **Delivery & versioning** — codecs, playblasts, organized files → 10 §7, 11 D

## 8. Math & Technical Foundations (Dunn & Parberry; Parent ch. 2-3)

- **Vectors: add/sub/magnitude/unit/distance** → 07 §1
- **Dot product** — angles, projection, parallel tests → 07 §1
- **Cross product** — normals, axes, torque, bone roll → 07 §1
- **Coordinate spaces (object/world/view)** — transforms connect them → 07 §2
- **Transform composition (T·R·S order)** — why parenting works → 07 §2
- **Matrices: rotation/scale/shear/projection** → 07 §2
- **4×4 homogeneous matrices** — translation inside matrix math → 07 §2
- **Determinants, inverse, orthogonal matrices** → 07 §2 (01: Math ch. 6)
- **Polar/spherical coordinates** → 07 §2 (01: Math ch. 7)
- **Orientation vs rotation** — state vs change → 07 §3
- **Euler angles & gimbal lock** — the shoulder/hip flip problem → 07 §3
- **Axis-angle & exponential map** — twist bones → 07 §3
- **Quaternions & slerp** — gimbal-free interpolation → 07 §3
- **Hermite / Bézier / splines** — curve families → 07 §4
- **Continuity C0/C1/C2** — F-curve handle theory → 07 §4
- **Arc length & speed control** — reparameterization → 07 §4
- **Geometric primitives & intersection tests** — ray/sphere/AABB/plane/triangle → 07 §2 (01: Math ch. 9, App. A)
- **Kinematics (velocity, acceleration, calculus)** → 07 §6 (01: Math ch. 11)
- **Dynamics (Newton, forces, momentum)** → 07 §6 (01: Math ch. 12)
- **Spring-damper systems** — k & c; under/over-damped → 07 §6
- **Skeletal animation theory** — skinning matrices, palette → 07 (01: Math ch. 10.8)

## 9. Technical & Procedural Animation (Parent)

- **Keyframe systems & interpolation functions** → 07 §4, 03
- **Shape interpolation / morphing / FFD deformation** → 07 (01: Parent ch. 4)
- **Motion capture: processing, retargeting, blending** → 07 §6
- **Particle systems** — generation, attributes, forces, lifespan → 07 §6
- **Rigid bodies & collision** — free fall, linked dynamics → 07 §6
- **Cloth & soft constraints** — mass-spring, energy minimization → 07 §6
- **Fluids (water, clouds, fire, CFD/SPH)** — FX timing → 07 §6 (01: Parent ch. 8)
- **Clothing & hair** — layered/physical coverings → 07 §6 (01: Parent ch. 9.4)
- **FACS & parameterized faces** — face as action units → 06, 07 (01: Parent ch. 10)
- **Behavioral animation: flocking, agents, crowds** — boids, autonomy → 07 §6 (01: Parent ch. 11)
- **Personality & emotion models** — parametric characters → 07 (01: Parent ch. 11.3)
- **Implicit surfaces & level sets** — metaballs/SDF modeling → 07 (01: Parent ch. 12)
- **Plants & L-systems** — procedural growth → 07 (01: Parent ch. 12.2)
- **Procedural discipline** — every system: ON/OFF + strength property → 07 §7

---

## Coverage guarantee

Every chapter of all 8 books maps to entries above (front-matter chapters excluded).
If a session needs "the concept from the books", it is HERE — the PDFs are never required.
For the step-by-step Blender execution of any rigging/animation/camera/render concept,
use `11-blender-how-to.md`; for the reasoning, use the doctrine files (03-09).

## 10. Shading & texturing (surfacing)

- **Shading vs texturing** — the recipe vs the maps that vary it; law first (16§1).
- **Diffuse / specular** — light that enters & tints vs light that bounces; metals have
  no diffuse, their color is tinted reflection (16§2).
- **Microfacet theory** — roughness = statistical mirror angles; PBRT ch. 9 BSDFs (16§2).
- **Energy conservation** — blurrier highlight = dimmer highlight; never outshine the source (16§2).
- **Fresnel / F0** — head-on reflectance: dielectrics 0.02–0.05 (metal/rough hardcodes
  4%), metals 0.5–1.0 tinted; chart `surf-05` (16§3).
- **Base color band** — 30–50 sRGB floor, 240 ceiling (coal → fresh snow); no baked AO (16§3).
- **Metallic binary law** — 0 or 1; rust/paint/dirt = dielectric 0 even on steel (16§3–4).
- **Metal/roughness workflow** — Principled BSDF's model; correct/incorrect: `surf-06` (16§3).
- **Linear workflow** — color maps sRGB, data maps Non-Color; judge under AgX (16§5).
- **3-light test** — approve materials under studio/sun/interior before shots (16§6, 11 H7).
- **Texel density / UDIM** — one px-per-meter standard; tiles for heroes (17§2, 11 H6).
- **Map set** — base color/metal/rough/normal/height/AO/thickness each with one job (17§3).
- **Procedural layering** — Ebert: texture spaces + layered composition; noise families
  (gradient=Noise, cellular/Worley=Voronoi) (17§5).
- **Wear logic** — edges polish, cavities dirt, gravity streaks down (17§7).
- **Baking** — cage encloses, margin guards, normals first (17§4, 11 H5).
- **2D vs 3D procedurals** — UV-defined (cloth/checkers) vs world-filled volume textures
  that ignore UVs (granite/wood); verbatim-alone reads fake, combined reads real (17§5, `surf-09`).
- **Specular color law (Jeremy Birn)** — non-metal highlights stay white/gray; metals tint the
  highlight with the material color — the F0 law in pre-PBR words (16§6, `surf-11`).
- **Five qualities of light (Jeremy Birn)** — Softness, Intensity, Color, Throw, Animation —
  the vocabulary for judging lookdev test lights (16§6, `surf-12`).
- **Transmitted light (James Gurney)** — backlit thin material: transmitted zone most
  saturated, top-lit brightest but dullest; four-zone check for SSS (16§6, `surf-13`).
- **Study and question (Owen Demers)** — the 12-question battery for reading reference before
  texturing from it (17§1, `surf-08`).
- **Map coherence** — color pattern must resemble the relief pattern; relief is layered;
  audit all maps of one asset side by side (17§6, `surf-10`).
