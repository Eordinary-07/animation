# AVA VOSS — RIG & ANIMATION VALIDATION (Solo Fight, 24s)
### Production Script Package · Clay/Geometry Pass 1

> **Locking in:** purpose = pure rig & mesh validation (no story) · range = natural
> fight movement only · look = untextured clay mesh in an empty void (no scene, no
> textures — texturing is a later pass) · hero test shots = S05, S10, S12, S15.
> Source material: the director's 24-second move list + camera table, choreographed
> into combinations so the take flows like real fighting while every beat audits a
> specific rig system. Success is not applause — success is **every RIG CHECK green**.

---

## PART 0 — PROJECT CARD

- **Title:** AVA VOSS — Rig & Animation Validation Take 01
- **Logline (functional):** A lone fighter runs a complete natural fight vocabulary —
  guard, evade, block, cross, sweep, knee, spin, back kick, floor roll, jab — in an
  empty void, so every joint system of the rig is proven on camera in 24 seconds.
- **Format:** Animation/rig test short · single character · single take-feel (17 shots)
- **Total duration:** 24.0 s = **576 frames @ 24 fps** (frame numbers rule; seconds are commentary)
- **Aspect ratio:** 16:9, 1920×1080 *(assumption — see below)*
- **Frame-rate feel:** On-ones, 24 fps; one 50% slow-motion beat (S12)
- **Target audience:** The rig's owner/reviewer (technical review, not public release)
- **Destination:** Review render (viewport-quality clay is acceptable; see Part 10)
- **Controlling idea:** N/A by design (pure demo). Replaced by the **validation
  thesis:** *"This rig performs a full natural fight vocabulary with clean
  deformation, planted contacts and zero floor penetration."* Every shot exists to
  prove or falsify one clause of that sentence.
- **Audience feeling arc:** N/A — replaced by **reviewer confidence arc:** neutral →
  increasingly demanding movement → final neutral proves the rig "returns home" clean.
- **Animation style:** Naturalistic human biomechanics (references: live MMA/boxing
  shadow-work footage; *John Wick* rehearsal tapes for economical gun-fu footwork;
  Capcom/Naughty Dog gameplay-idle-to-combat rig demos for test presentation).
- **Tone keywords:** clinical · precise · weighty · economical · honest
- **Confirmed director's choices (from interview):** intention = prove the rig ·
  range = natural only (no torture poses) · space = *no background/scene, mesh only*
  (texturing later) · checks = per-shot RIG CHECK **and** final master tick-list ·
  dialogue = none · timing/camera = your tables, kept and given reasons.
- **Assumptions I made (veto any):**
  1. **Stance = orthodox:** LEFT foot forward, LEFT hand leads (jab), RIGHT hand rear
     (cross). Your moves only chain coherently this way (right cross → left sweep →
     left knee → right back kick → left jab).
  2. **Breathing cycle ≈ 3 s**, not 0.3 s (0.3 s/breath is ~200 breaths/min —
     physically impossible; a 3 s subtle cycle is what reads on screen).
  3. **Fade-in over f1–f12** instead of a full second of black, so the neutral
     stance (your 00:00 move) is actually visible for the home-pose comparison.
  4. **Ground = shadow-catcher only** (invisible; shows contact shadow, no floor
     mesh) so foot/fingertip contact and slide are readable. Toggle off if unwanted.
  5. **Ponytail = hand-keyed bones** this pass (no simulation) — tests the chain.
  6. The template's "★ FEELING JOB" is adapted to **"★ SHOT JOB — what this shot
     must prove"**, correct currency for a validation piece.

## PART 1 — STRUCTURE: MOVE BLOCKS (the rig-test beat sheet)

Your second-by-second moves chain into real fight **combinations** — that is the
choreography. Each block audits a named rig system; "failure signature" is the
visible symptom that fails the block.

| # | Block (frames) | Choreography | Rig systems exercised | Failure signature to watch |
|---|---|---|---|---|
| B1 | Ready (f1–72) | Neutral → guard up → shoulder roll, head settle | Shoulder raise, fist curl, clavicle travel, breath | Shoulder collapse at guard height |
| B2 | Settle & react (f73–120) | Exhale, knees bend → head snap right | Neck snap, spine compression, weight sink | Candy-wrapper neck, floating weight |
| B3 | Combo A — evade/block/cross (f121–216) | Front-foot pivot 45° → low block → right cross (hit f180) → retract | Foot pivot, hip rotation, arm chain full extension, spine counter-rotation | Foot skate, elbow pop, shoulder shrug at extension |
| B4 | Combo B — level change (f217–312) | Deep crouch → left leg sweep → rise → knee to chest → knee drive | Hip crease, knee/ankle extremes, hip flexion, one-leg balance | Hip mesh pinch-through, support-foot drift |
| B5 | Combo C — spin & back kick (f313–408) | 180° spin (arms tight, hair flies) → right back kick, chest height → land & settle | Spine twist distribution, ponytail secondary, hip extension, landing absorption | Single-bone twist kink, hair lag wrong direction, stiff landing |
| B6 | Composure (f409–456) | SLOW-MO hold → lip wipe | Micro-motion/breath, blink, wrist pronation, hand-to-face accuracy | Frozen statue, curve jitter (slow-mo exposes it), wrist clipping face |
| B7 | Floor & finish (f457–576) | Fingertips to floor → forward roll → slide-stand → jab hold → guard down → neutral | Spine flexion chain, finger contact, full-body floor roll line, lead-arm extension, home-return | Floor penetration, roll axis wobble, end pose ≠ start pose |

## PART 2 — CHARACTER BIBLE: AVA Voss (test-pass spec)

- **Role:** Sole performer; the mesh under audit.
- **Build:** Athletic adult female, ~1.70 m (per your spec; origin at feet center).
- **Appearance this pass:** **Untextured clay only** — single neutral material
  (Part 5). Fitted training gear and tied-back ponytail exist as *mesh forms*;
  their colors/materials are explicitly a later pass. Hair clay may be one shade
  darker purely so the ponytail's swing reads on camera.
- **Stance:** Orthodox — left foot forward, weight 55/45 toward rear at guard
  (your 00:01 note), chin down, lead shoulder slightly raised.
- **Signature silhouette:** Compact guard — elbows in, fists at cheekbones, knees
  soft; every strike returns to this home shape (the return is itself a test).
- **Expected rig inventory (what this take assumes & audits):** root/pelvis control,
  ≥3-bone spine, neck + head, clavicles, FK/IK arms & legs, foot roll (ball pivot),
  finger curls (fists + floor spread), eyelid blink, ponytail chain (≥3 bones).
  If any item is absent, its shots become the gap list — that is a valid result.
- **Acting notes (demo-minimal):** Focused athlete neutrality. Effort shows only in
  breath rate and guard tension; one blink in S12; eyes lead the head snap by
  ~3 frames (B2). No facial performance beyond this — face is a later audit.

## PART 3 — WORLD BIBLE

**None — by your instruction.** No set, no backdrop geometry, no props, no opponent.
The void is a flat world color; the only "environment" is the invisible
shadow-catcher ground plane at Z=0 (contact readability) and the floor plane line
the choreography physically respects. Reviewer feeling intended: *laboratory
confidence — nothing on screen except the truth of the deformation.*

## PART 4 — CINEMATOGRAPHY BIBLE

- **Camera philosophy:** *The camera is a witness, not a performer.* It moves only
  to keep the deformation under test readable; it never hides a joint being audited.
- **Lens kit (yours):** 50 mm = default truth lens (minimal distortion of
  proportions) · 35 mm = full-body movement shots needing limb headroom · 85 mm =
  close audits (punch extension S05, face S12, jab S16) where compression flatters
  nothing and spacing reads clearly.
- **Framing law:** In all full-body shots keep **≥0.3 m of empty frame around the
  furthest limb** (your note) — a kick leaving frame is a failed test shot.
  Camera looks at her center ≈0.9–1.2 m height per shot.
- **Movement language:** slow dolly-in = *leaning in to inspect* · static =
  *measurement shot* (any slide/skate is camera-independent, therefore real) ·
  180° orbit = *inspect the twist from every side* · tracking = *follow the root
  so limb spacing reads against a stable body*. 2–3-frame impact shakes (f180,
  kick hit, f481) mark contacts for the reviewer — small enough to never mask a pop.
- **Depth of field:** OFF everywhere. Blur hides deformation; this pass is all-sharp.
- **180° policy:** Her facing defines the axis; the S09 orbit crosses it
  deliberately and continuously (legal — the audience rides the crossing).
- **Shot-size strategy:** Each combo cycles wide (context) → close (audit) → medium
  (reset), so the reviewer alternates between choreography and deformation.

## PART 5 — COLOR & LIGHTING (clay-pass substitute for a color script)

- **Clay material:** Principled BSDF, Base Color **#8B8E93**, Roughness 0.65,
  Metallic 0. Optional hair clay **#55575C** (readability only).
- **Value structure:** Mid-grey subject against near-black void (#0B0B0D world) —
  silhouette always separable; brightest point = key-side shoulder/face plane;
  darkest = void. No pure white anywhere (blown highlights hide surface pinching).
- **Light design (fixed for all shots):** KEY — large area light, camera-left,
  45° azimuth / ~40° elevation, neutral white (≈5600 K), sized for soft but
  directional modeling · FILL — camera-right at **1:4 ratio** (shadow side stays
  readable — deformation must be visible in shadow too) · RIM — top-behind,
  narrow, for silhouette edge against the void.
- **View transform:** AgX, default exposure. **FINAL GRADE: none** — deliberately.
  Forbidden this pass: textures, HDRI, colored light, vignette, grain, DoF,
  environment geometry. (All return in the later texturing/lookdev pass, where a
  true color script will be written.)
- **Delivery:** Rec.709/sRGB review render.

## PART 6 — ANIMATION STYLE CARD

- **Realism ↔ exaggeration:** **8/10 realism.** Natural human ranges only (your
  choice); the only "style" is a 2–3-frame overshoot settle on strike extensions
  (your note) — snappiness, not cartoon.
- **Timing feel:** Weight-first. Drives originate at the pelvis → spine → limbs
  (your hierarchy note). Strikes reach extension in 4–6 frames; settles take
  6–10 frames; holds are *moving holds* (breath/sway), never statues.
- **Easing law (yours, kept):** Ease-in on wind-ups/pushes; ease-out on impacts,
  holds, pull-backs. Arc discipline: every limb tip travels a clean arc with
  musical spacing — verified on motion paths before sign-off.
- **Physics/secondary:** Ponytail hand-keyed with lag & overshoot (spins S09,
  roll S15); fitted gear = no cloth sim; breath = subtle chest scale loop ≈3 s,
  visible at B1/B6 only (fight blocks are too fast to read it — don't force it).
- **Squash & stretch:** None (realism). Volume preservation is the rig's job —
  which is precisely what is being audited.
- **Facial:** Neutral focus; eyes lead head by ~3 f; one full blink in S12
  (closed 1–2 f); brow/jaw stay home this pass.
- **Dialogue:** None in any shot.

## PART 7 — SHOT-BY-SHOT SCRIPT

**Constants for all shots:** lighting & clay per Part 5 · no dialogue · sound =
review markers only (Part 8) · location = void, ground shadow-catcher at Z=0 ·
framing honors the 0.3 m limb-margin law. Exceptions noted per shot.
Times given as seconds (frames). Cumulative TC at 24 fps.

### S01 — "Home" — 3.0s · f1–f72 · TC 00:00–00:03
- **SHOT LOOK & REASON:** Fade from black into a medium-wide full body; Ava small
  and still in a large dark void, camera slowly leaning in. WHY: establishes the
  neutral "home" pose the whole take must return to, and the reviewer's baseline.
- **Framing:** Medium wide → medium; 50 mm; camera 3.0 m → ~2.4 m, height 1.2 m, eye level, straight on.
- **Camera movement:** Slow dolly-in, ease-in, settling by f72.
- **ACTION:** f1–24 neutral stance, arms relaxed. f25–36 both fists rise to guard,
  weight shifts to rear foot. f49–72 shoulders roll back, head tilts left, settles.
- **ACTING:** Objective: *become ready*. Key pose (f36): compact guard silhouette —
  fists at cheekbones, elbows ribs-in, chin tucked. Breath cycle starts.
- **TRANSITION:** Fade in from black (f1–f12) — laboratory lights-up.
- **RIG CHECK:** Shoulder/deltoid fold as fists reach guard height; fist curl
  (fingers close fully without interpenetration); clavicle travel in the shoulder
  roll. **PASS:** guard reached with no shoulder-volume collapse; head tilt keeps
  neck volume both sides.
- **★ SHOT JOB:** Prove the home pose and guard raise are clean.

### S02 — "React" — 2.0s · f73–f120 · TC 00:03–00:05
- **SHOT LOOK & REASON:** Waist-up medium, dead still camera; her upper body sinks,
  then her head whips right. WHY: a measurement shot — static camera means any
  neck/spine artifact is unambiguously the rig's.
- **Framing:** Medium (waist up); 50 mm; 2.2 m, height 1.3 m. **Camera:** static (dolly has stopped).
- **ACTION:** f73–90 exhale — chest drops, knees bend slightly (weight sinks ~4 cm).
  f97–104 head snaps right (eyes lead from ~f94); head holds, body still loaded.
- **ACTING:** Objective: *register a threat*. Key pose (f104): chin over right
  shoulder line, guard unchanged — head moved, base didn't.
- **TRANSITION:** Cut on the settle after the exhale (thought completes).
- **RIG CHECK:** Neck twist distribution (head vs neck bones share rotation);
  trapezius/sternocleidomastoid region stretching; spine compression on the sink.
  **PASS:** no candy-wrapper pinch at the neck base; sink reads as weight, feet planted.
- **★ SHOT JOB:** Prove neck snap + weight sink deform cleanly.

### S03 — "Pivot" — 1.0s · f121–f144 · TC 00:05–00:06
- **SHOT LOOK & REASON:** Full body from knee height; her front foot screws into
  the floor and her hips swing 45°. WHY: low angle makes the foot-ball pivot and
  hip rotation — the engine of the whole combo — impossible to fudge.
- **Framing:** Full body; 35 mm; ~3.5 m, height ~0.6 m (knee height), slight up-tilt. **Camera:** static.
- **ACTION:** f121–138 pivot on ball of left (front) foot; hips rotate ≈45°;
  pelvis leads, chest follows 2–3 f later; guard stays up.
- **ACTING:** Objective: *angle off the attack line*. Key pose (f138): hips bladed,
  weight coiled over the pivot foot.
- **TRANSITION:** Cut in on head-snap hold; cut out as hips reach full coil.
- **RIG CHECK:** Foot-roll/ball-pivot control (rotation about the ball, heel lifts
  naturally); ankle twist; pelvis-to-thigh rotation. **PASS:** pivot foot rotates
  in place with zero lateral skate; rear foot stays planted.
- **★ SHOT JOB:** Prove foot pivot mechanics + 45° hip coil.

### S04 — "Block" — 1.0s · f145–f168 · TC 00:06–00:07
- **SHOT LOOK & REASON:** Chest-up, slight push-in; right hand chops down across
  the body while the left fist stays glued to her chin. WHY: close enough to audit
  shoulder internal rotation — a classic deformation failure zone.
- **Framing:** Medium close (chest up); 50 mm; 1.4 m, height 1.4 m.
- **Camera movement:** slight push-in, ending ~f156.
- **ACTION:** f145–154 right hand sweeps down in a block (elbow leads, forearm
  follows); left fist never leaves the chin; small torso brace.
- **ACTING:** Objective: *deflect and stay covered*. Key pose (f154): right forearm
  diagonal across the ribs, left fist home — one hand works, one hand guards.
- **TRANSITION:** Cut out on the block's contact frame — the counter launches next.
- **RIG CHECK:** Right shoulder internal-rotation range; elbow bend volume; left
  arm holds position against torso motion (no drift). **PASS:** no armpit collapse
  at block bottom; guard fist steady within ~1 cm.
- **★ SHOT JOB:** Prove blocking-arm range with guard discipline.

### S05 — "Cross" ⭐ HERO TEST SHOT — 1.0s · f169–f192 · TC 00:07–00:08
- **SHOT LOOK & REASON:** Tight on arm and shoulder, slightly side-on; the right
  cross fires straight at us and locks at full extension. WHY: this single frame
  (f180) is the postcard of the whole rig — shoulder protraction, elbow lock,
  spine rotation and rear-heel pivot all peak simultaneously.
- **Framing:** Close-up (arm/shoulder/partial head); 85 mm; 0.9 m, height 1.5 m, slightly side-on.
- **Camera movement:** quick push-in timed to the punch; static hold on
  extension; **2–3 f impact shake at f180**.
- **ACTION:** f169–174 punch launches from the hip coil; **f180 full extension**
  (overshoot) → f181–186 settle 2–3 f; hold to f192.
- **ACTING:** Objective: *end the exchange*. Key pose (f180): straight line
  knuckle→wrist→elbow→shoulder, chin behind the punching shoulder, rear heel up.
- **TRANSITION:** Snap cut in on launch anticipation; hold the hit (Walter Murch: emotion
  first — here, evidence first).
- **RIG CHECK:** Shoulder protraction reach (clavicle + deltoid), elbow at full
  extension (no hyperextension pop, no volume loss), chest-vs-pelvis
  counter-rotation, wrist alignment. **PASS:** unbroken punch line; settle is
  smooth overshoot, not jitter; no shoulder shrug-collapse.
- **★ SHOT JOB:** Prove the full arm chain at maximum natural extension.

### S06 — "Retract" — 1.0s · f193–f216 · TC 00:08–00:09
- **SHOT LOOK & REASON:** Medium, pulling back as the fist snaps home. WHY:
  punches must return along the same line they left — the pull-back reveals arc
  cheating the outgoing speed hid.
- **Framing:** Medium; 50 mm; 2.2 m, height 1.3 m. **Camera:** pull-back to reset framing.
- **ACTION:** f193–204 fist retracts to guard (elbow drops last); f205–216 ready
  stance re-established, small weight bounce settles.
- **ACTING:** Objective: *be covered again*. Key pose (f216) = S01 guard, mirrored energy.
- **TRANSITION:** Cut out as stance resets — combo A complete.
- **RIG CHECK:** Retraction path (motion-path the wrist: out-line vs back-line
  should nearly overlap); elbow re-bend volume. **PASS:** no drooping "dead arm"
  arc; guard symmetry restored.
- **★ SHOT JOB:** Prove clean retraction and guard recovery.

### S07 — "Sweep" — 2.0s · f217–f264 · TC 00:09–00:11
- **SHOT LOOK & REASON:** Full body dropping low; at the crouch bottom the camera
  drops to 0.5 m and tracks sideways as her left leg scythes out horizontal.
  WHY: deep crouch + extended leg is the hip-crease torture corner of this take —
  the low track keeps both the crease and the leg line in profile.
- **Framing:** Full body → full body low; 35 mm; 4.0 m, height 1.2 m → 0.5 m.
- **Camera movement:** static for crouch; lateral track following the sweep.
- **ACTION:** f217–240 drop into deep crouch (weight shifts to right leg);
  f241–258 left leg sweeps in a low arc, extending horizontal at hip height,
  pivoting on right foot; f259–264 leg begins recovery.
- **ACTING:** Objective: *take the legs away*. Key pose (f252): torso
  counter-leans, sweep leg straight at hip height, arms counterbalance wide.
- **TRANSITION:** Cut in on stance reset; the level change itself justifies the cut.
- **RIG CHECK:** Deep-crouch deformation stack — hip crease fold, knee bend
  volume, ankle dorsiflexion, glute fold; sweep-leg hip flexion+abduction with
  straight knee; support-foot pivot under load. **PASS:** no mesh pinch-through
  at the crease beyond natural fold; sweep foot clears the floor; support foot
  markers stack (no drift) on the motion path.
- **★ SHOT JOB:** Prove low-game deformation: crouch + horizontal sweep.

### S08 — "Knee" — 2.0s · f265–f312 · TC 00:11–00:13
- **SHOT LOOK & REASON:** Full body rising out of the sweep; slow push to medium
  as the knee spears forward and her torso leans away. WHY: one-leg balance under
  a violent hip flexion is where weight honesty is audited.
- **Framing:** Full body → medium; 50 mm; 4.0 m → 2.2 m, height 1.2–1.3 m.
- **Camera movement:** static rise, then slow push-in on the knee drive.
- **ACTION:** f265–288 rise, left knee pulls to chest; f289–304 knee drives
  forward, upper body leans back for balance; f305–312 leg retracts toward stance.
- **ACTING:** Objective: *finish at close range*. Key pose (f298): knee at solar-
  plexus height, torso leaned back ~10°, arms pulled down-in (clinch memory).
- **TRANSITION:** Continuous from sweep recovery — no cut inside a combo.
- **RIG CHECK:** Hip flexion maximum (thigh approaching abdomen — contact
  deformation, no clip-through), lumbar extension in lean-back, support-ankle
  micro-balance. **PASS:** thigh/torso proximity deforms, never intersects;
  support foot stays planted and flat.
- **★ SHOT JOB:** Prove hip-flexion range + one-leg balance honesty.

### S09 — "Spin" — 2.0s · f313–f360 · TC 00:13–00:15
- **SHOT LOOK & REASON:** The camera orbits 180° with her spin; arms stay
  tucked, ponytail whips out and trails. WHY: orbiting keeps her front readable
  so spine-twist distribution and hair lag can be judged through the whole turn.
- **Framing:** Full body; 35 mm; 4.0 m, height 1.2 m.
- **Camera movement:** 180° orbit, look-at locked on chest (≈1.2 m), easing in/out with the spin.
- **ACTION:** f313–330 step-turn initiates (head leads — spotting); f331–354 full
  180° rotation, arms tight to body, ponytail swings out (peak lag ~f345);
  f355–360 rotation completes, weight loads for the kick.
- **ACTING:** Objective: *re-aim at the new threat*. Key pose (f345): compact
  vertical axis, chin over shoulder acquiring target, hair at max extension.
- **TRANSITION:** Cut in on knee retraction — momentum carries across the cut.
- **RIG CHECK:** Spine twist spread across all spine bones (inspect at f330/345);
  upper arms against torso (contact without clip); ponytail chain arc (smooth
  curve, lag direction = opposite rotation, no bone flips); feet pivot timing.
  **PASS:** no single-vertebra candy-wrapper; hair path is one clean arc;
  no foot skate during pivots.
- **★ SHOT JOB:** Prove twist distribution + hair secondary in rotation.

### S10 — "Back Kick" ⭐ HERO TEST SHOT — 1.0s · f361–f384 · TC 00:15–00:16
- **SHOT LOOK & REASON:** Slightly low full body; her right heel fires straight
  back at chest height, body one long diagonal line. WHY: hip extension + balance
  + look-back twist peak together — the second postcard frame of the rig.
- **Framing:** Full body, low; 35 mm; 3.5 m, height 0.7 m. **Camera:** static; 2–3 f shake on kick hit (~f368).
- **ACTION:** f361–368 right heel drives out to chest height (overshoot);
  f369–378 hold/settle; f379–384 leg begins return.
- **ACTING:** Objective: *stop whatever chased her*. Key pose (f370): heel highest
  point, torso pitched forward as counterweight, head turned back over shoulder.
- **TRANSITION:** Orbit settles into this static — motion to monument.
- **RIG CHECK:** Hip extension (glute fold compression), kicking-knee lock,
  support-leg soft-knee stability, neck look-back twist. **PASS:** straight line
  heel→hip→shoulder; support foot flat and silent on the motion path.
- **★ SHOT JOB:** Prove hip extension + counterbalanced one-leg pose.

### S11 — "Land" — 1.0s · f385–f408 · TC 00:16–00:17
- **SHOT LOOK & REASON:** Medium pull-back; she lands on the front foot and the
  guard rebuilds. WHY: landings expose fake weight faster than any strike.
- **Framing:** Medium; 50 mm; 2.2 m, height 1.3 m. **Camera:** gentle pull-back (settle with her).
- **ACTION:** f385–396 landing absorption (ankle→knee→hip compression sequence);
  f397–408 guard returns, balance micro-settle.
- **ACTING:** Objective: *own the ground again*. Key pose (f408) = guard, third time — consistency is the point.
- **TRANSITION:** Cut out on full settle — end of Combo C.
- **RIG CHECK:** Sequential joint compression (no single-joint collapse); landing
  foot placement (no slide on contact — markers stack from touch-down frame).
  **PASS:** weight visibly travels down the chain in ~6 f; zero foot drift.
- **★ SHOT JOB:** Prove landing absorption reads as real weight.

### S12 — "Composure" ⭐ HERO TEST SHOT — 1.0s · f409–f432 · TC 00:17–00:18 — SLOW MOTION 50%
- **SHOT LOOK & REASON:** Face-and-shoulders close, time thickens; almost nothing
  moves — breath, a blink, micro-sway. WHY: slow motion at close range is an
  X-ray for curve noise and the facial rig; nothing can hide.
- **Framing:** Medium close (face/shoulders); 85 mm; 1.4 m, height 1.4 m.
- **Camera movement:** very slow push-in, also at half speed (time-scale 0.5 on
  character **and** camera — animate 12 f of motion across these 24 f).
- **ACTION:** Controlled stance hold: one slow breath cycle, one full blink
  (~f418–422 perceived), guard tension micro-adjusts, ponytail settles.
- **ACTING:** Objective: *master herself*. Key pose: the guard, at its calmest —
  a moving hold, alive at 5% amplitude.
- **TRANSITION:** Time itself is the transition — speed ramps in/out over ~4 f.
- **RIG CHECK:** Eyelid blink (full closure, lids meet cleanly); chest breath
  deformation; curve smoothness everywhere (step through frame-by-frame: any
  1-frame pop = fail). **PASS:** no jitter at 50% scrutiny; blink seals; breath
  reads without shoulder pumping.
- **★ SHOT JOB:** Prove micro-motion quality + blink at close range.

### S13 — "Wipe" — 1.0s · f433–f456 · TC 00:18–00:19
- **SHOT LOOK & REASON:** Medium, normal speed snaps back; the back of her wrist
  drags across her lip. WHY: hand-to-own-face contact is the precision test —
  millimeter accuracy between two rigged surfaces.
- **Framing:** Medium; 50 mm; 2.2 m, height 1.3 m. **Camera:** static.
- **ACTION:** f433–444 right wrist rises, back-of-wrist wipes the lip line;
  f445–456 hand returns to guard; eyes drop briefly, re-engage forward.
- **ACTING:** Objective: *clear and continue*. Key pose (f440): wrist at mouth,
  elbow low, other fist still guarding.
- **TRANSITION:** Cut in exactly as slow-mo releases (speed contrast = punctuation).
- **RIG CHECK:** Forearm pronation deformation through the wipe; wrist-to-face
  clearance. **PASS:** wrist kisses the lip line with zero interpenetration and
  no visible air-gap; forearm twist distributes (no candy-wrapper at wrist).
- **★ SHOT JOB:** Prove self-contact precision (hand ↔ face).

### S14 — "Touch the Floor" — 1.0s · f457–f480 · TC 00:19–00:20
- **SHOT LOOK & REASON:** High angle looking down as she folds into a low crouch
  and her fingertips find the floor. WHY: top view exposes the spine flexion
  chain and exact fingertip-floor contact better than any other angle.
- **Framing:** Full body, high; 35 mm; 4.0 m, height 2.5 m, looking down.
- **Camera movement:** slow crane down during the fold.
- **ACTION:** f457–472 crouch deepens, one hand reaches down; f473–480 fingertips
  touch and take slight weight (fingers spread/flatten on contact).
- **ACTING:** Objective: *coil for the floor move*. Key pose (f478): rounded
  spine, hips low, fingertips planted — a sprinter's cousin.
- **TRANSITION:** Cut in on guard; the high angle itself signals "floor chapter".
- **RIG CHECK:** Full spine flexion chain (even curve, no single-bone hinge);
  shoulder reach-down range; finger spread on floor contact. **PASS:**
  fingertips meet Z=0 exactly — no floating, no sinking; back rounds evenly.
- **★ SHOT JOB:** Prove spinal flexion + fingertip floor contact.

### S15 — "Roll & Slide" ⭐ HERO TEST SHOT — 2.0s · f481–f528 · TC 00:20–00:22
- **SHOT LOOK & REASON:** Eye-level full body; she explodes forward, tucks,
  rolls across the floor and slides up standing, one foot forward. WHY: the
  roll is the only full-body floor-contact chain in the take — the hardest
  single audit of root motion, tuck deformation and floor discipline.
- **Framing:** Full body; 35 mm; 4.0 m, height 1.2 m.
- **Camera movement:** static with 2–3 f shake at f481 launch, then track with the slide.
- **ACTION:** f481–492 hands plant, tuck (chin to chest, spine rounds);
  f493–510 roll over one shoulder diagonally (shoulder→opposite hip line);
  f511–528 unfold into a standing slide, front foot braking, guard rising.
- **ACTING:** Objective: *vanish low, reappear ready*. Key pose (f502): full
  tuck ball — smallest silhouette of the take.
- **TRANSITION:** Continuous from S14's coil — the touch *is* the launch.
- **RIG CHECK:** Floor discipline (no body part below Z=0 at ANY frame — check
  f493–510 individually); tuck compression (thighs/abdomen/chin contacts);
  roll axis consistency; root path smoothness (motion-path the pelvis: one
  flowing curve, no stalls). **PASS:** zero floor penetration; roll reads as one
  diagonal line; slide-out foot plants without bounce-skate.
- **★ SHOT JOB:** Prove full-body floor contact + root-motion integrity.

### S16 — "Jab" — 1.0s · f529–f552 · TC 00:22–00:23
- **SHOT LOOK & REASON:** Medium close on lead arm and head; the left jab
  spears out and *holds*, trembling with tension. WHY: the left-side mirror of
  S05 — rigs are rarely symmetrical in quality; this audits the other shoulder.
- **Framing:** Medium close (arm/head); 85 mm; 1.4 m, height 1.4 m.
- **Camera movement:** slight push-in with the jab.
- **ACTION:** f529–535 jab extends (shoulder rolls in to cover chin);
  f536–552 extended hold — moving hold: breath and micro-tension only.
- **ACTING:** Objective: *claim the space in front*. Key pose (f540): fist at
  full reach, chin tucked behind lead shoulder, rear fist home.
- **TRANSITION:** Cut in on slide-stop (feet stop, fist goes — energy handoff).
- **RIG CHECK:** Left shoulder protraction + elbow extension (compare against
  S05's right — quality should match); hold stability. **PASS:** same clean line
  as f180 on the opposite side; hold doesn't drift or jitter.
- **★ SHOT JOB:** Prove left-side extension equals right-side quality.

### S17 — "Home Again" — 1.0s · f553–f576 · TC 00:23–00:24
- **SHOT LOOK & REASON:** Slow pull-back to full body; guard melts down, arms
  return to her sides, stillness — fade to black. WHY: the take must end where
  it began; any pose drift between f1 and f576 is quantifiable rig/animation drift.
- **Framing:** Medium wide → full body; 50 mm; 3.0→4.0 m, height 1.2 m.
- **Camera movement:** slow pull-back, static final hold; fade out f565–f576.
- **ACTION:** f553–564 guard lowers slowly (ease-out), weight centers;
  f565–576 neutral stance, one quiet breath. END.
- **ACTING:** Objective: *stand down*. Key pose (f570) = f12 neutral — bookends match.
- **TRANSITION:** Fade to black — laboratory lights-down.
- **RIG CHECK:** Home-return accuracy: overlay f12 vs f570 — joint positions
  should match within ~1 cm; final breath doesn't move the feet. **PASS:**
  bookend poses match; stillness is alive (breath) not frozen.
- **★ SHOT JOB:** Prove the rig returns home clean after 24 s of violence.

## PART 8 — SOUND (review-aid spec — optional for the verdict)

No music, no dialogue. If a review track is laid: cloth/footfall ticks on weight
transfers · whoosh peaks at f178–180 (cross), f364–368 (kick), f529–535 (jab) ·
floor contact thuds f481/f493/f511 · one audible slow breath across S12 · silence
elsewhere (sync errors hear better in silence). Sound never gates the rig verdict.

## PART 9 — FX & SPECIAL ELEMENTS

**None.** No simulation, no particles, no environment effects this pass. The
ponytail is hand-keyed bone secondary (audited in S09/S15). Camera shakes are
2–3-frame rotational offsets (Part 4), not post FX.

## PART 10 — PRODUCTION HANDOVER

**Assets needed:** Ava mesh + rig (existing — under audit) · invisible
shadow-catcher ground · 3-light clay rig · 17 cameras or one bound camera per shot
(marker-bound). **Nothing to model, texture or simulate.**

**Render/delivery spec (test pass):** 1920×1080, 24 fps, f1–f576, AgX;
Workbench (studio light) or EEVEE clay — deformation readability over beauty;
plus a frame-number burn-in or metadata stamp so tick-list references land exactly.

**The 3 hardest shots:** **S15 roll** (full floor-contact chain — animate pelvis
root path first, block contact frames on the floor plane before splining) ·
**S09 spin** (twist + hair + pivots simultaneously — key feet/head first, hair
last) · **S07 sweep** (deep crouch into horizontal leg — pose the two extremes,
then audit the transition frames for crease behavior).

**MUST-HAVE moments:** f180 cross extension · f370 back-kick line · S12 blink in
slow-mo · f570 home-return match. **MUST-AVOID:** torture-range poses (natural
only — director's choice) · any floor penetration · camera framing that crops
the joint under test · textures/environment/grade this pass · frozen holds.

**Open choices left to the animation team (max 5):** ① Workbench vs EEVEE clay
② shadow-catcher on/off ③ ponytail: bones now vs cloth sim in a later pass
④ optional orthographic front/side measurement pass after this take passes
⑤ if the rig lacks full fingers, S01/S14 checks adapt to the mitten/curl available.

### ✅ MASTER RIG TICK-LIST (scrub the render; every line must pass)

**Spine & neck** — ☐ Neck snap keeps volume (f97–104) ☐ Twist spreads across
spine in spin (f330/f345) ☐ Lean-back extension even (f289–304) ☐ Flexion chain
rounds evenly (f457–478) ☐ Roll tuck compresses without clip (f493–510)
**Shoulders & arms** — ☐ Guard raise, no deltoid collapse (f25–36) ☐ BLOCK
internal rotation clean (f145–154) ☐ RIGHT cross line unbroken at f180 ☐ LEFT
jab line matches it (f536–552) ☐ Elbows: no pop at either full extension
**Hands & fingers** — ☐ Fists close fully (from f36) ☐ Wrist pronation smooth,
no face clip (f433–444) ☐ Fingertips meet floor exactly (f473–480)
**Hips & legs** — ☐ Crouch: crease folds, no pinch-through (f217–240) ☐ Sweep
leg horizontal, knee straight (f241–258) ☐ Knee-to-chest: contact without
intersection (f265–288) ☐ Back kick: hip extension + straight heel line (f368–378)
**Feet & balance** — ☐ Front-foot pivot: rotation, zero skate (f121–138)
☐ Support foot planted in knee drive & back kick (motion-path markers stack)
☐ Landing: sequential absorption, no drift (f385–396) ☐ Slide-out plant clean (f511–528)
**Face** — ☐ Blink seals fully in slow-mo (S12) ☐ Eyes lead head snap ~3 f (f94–104)
**Hair** — ☐ Ponytail lags opposite spin, one clean arc (f331–360) ☐ Settles
without flips after spin & roll
**Global** — ☐ Zero floor penetration, all 576 frames (spot-check f457–528
frame-by-frame) ☐ Pelvis root path = one flowing curve, no stalls ☐ Every
limb tip arcs with musical spacing (motion-path audit B3–B7) ☐ f570 neutral
matches f12 within ~1 cm ☐ Slow-mo segment: zero 1-frame pops

*Director's self-check: durations sum to 576 f / 24.0 s ✓ · every shot carries
SHOT LOOK & REASON, RIG CHECK and ★ SHOT JOB ✓ · confirmed choices honored
(no story, natural range, clay/void, dual checks) ✓ · no placeholders ✓.*
