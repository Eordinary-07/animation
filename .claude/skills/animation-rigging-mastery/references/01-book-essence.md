# Book Essence & Provenance

Provenance (background only — NOT required): these lessons were distilled from 8 book PDFs.
The merged OCR PDF (`merged-ocr` release) order:
Maya Rigging (1-408), Stop Staring (409-795), 3D Math Primer (796-1641), Rick Parent
(1642-2182), Acting for Animators (2183-2327, image-only - no OCR text), Illusion of Life
(2328-2875), Timing for Animation (2876-3060), Survival Kit (3061-3406).

---

## 1. Cheryl Cabrera - An Essential Introduction to Maya Character Rigging
File: `an-essential-introduction-to-maya-character-rigging_compress.pdf` (408 pp, Focal Press 2008)

**Essence:** A complete first-biped rigging pipeline, taught as a production workflow:
design → model → face → shade → skeleton → control rig → cleanup → skin. Everything we do
in Blender follows this skeleton.

**Key lessons (chapters):**
1. *Designing Your First Biped Character* - character sheets (front/side/back), design for
   deformation: clear shoulders/hips/knees/elbows, avoid costume geometry that blocks joints.
   Reason: rigging starts on paper; a bad design cannot be saved by a good rig.
2. *Modeling Basics* - topology for animation: even quad distribution, edge loops around
   mouth/eyes/shoulders/armpits/knees, T-pose/A-pose modeling, symmetry.
3. *Facial Expressions via Blend Shapes* - expression targets (happy/sad/angry/surprise/brow
   raises/eye blinks), **deformation order matters** (blend before or after joints deliberately).
4. *Shading/Texturing* - UV layout that survives deformation (stretch zones).
5. *Skeleton Setup: Joint Placement* - joints at the actual rotation centers (shoulder ball,
   elbow hinge, knee hinge, hip ball, knuckle line, spine chain 3-5 joints), joint orientation
   consistent (aim at child, predictable roll), **reference the model file** so rig and mesh
   evolve separately.
6. *Control Rig Setup: IK and FK* - FK for arcs/spine, IK for planted feet/hands; attribute
   control (custom channels on a master control) drives the rig; pivot/IK snapping.
7. *Wrapping Up the Setup* - clean for animation: hide construction junk, final names
   (left_/right_/prefixes), lock unused channels, freeze/reset pose.
8. *Skinning* - smooth bind + weight painting: 100% coverage, normalized weights, max 4-ish
   influences per vertex for real-time, helper/dummy influences for hard areas (shoulder, hip),
   test extreme poses while weighting (don't weight in T-pose only).

**Reason it matters here:** this is our rigging bible. Its logic is Maya; our implementation is
Blender - see `02-rigging-blender.md` for the full translation.

## 2. Richard Williams - The Animator's Survival Kit
File: `The Animator's Survival Kit - Richard Williams.pdf` (346 pp, scan - text via merged OCR)

**Essence:** "A manual of methods, principles and formulas for classical, computer, games, stop
motion and internet animators." Williams' thesis: animation is *drawing in time* - if you
control the spacing and the timing, you control everything.

**Structure & key lessons (real TOC):**
- *Why This Book / Drawing in Time / Time to Draw* - the medium is time, not pictures.
- *It's All in the Timing and the Spacing* + *Lesson 1* + *Advancing Backwards to 1940* -
  charts, inbetweens, extremes vs breakdowns, keys, "three ways to animate" (straight-ahead,
  pose-to-pose, combination), testing, the X-sheet, ones vs twos ("The Great Ones and Twos
  Battle"), pegs.
- *More on Spacing* - classic inbetween mistakes, watch your arcs, movement within the mass,
  the elongated inbetween, the major beginner's mistake (even spacing = floaty), the "ruff"
  approach, take the long short cut.
- *Walks* - getting the weight, set the tempo, the passing position/breakdown, two ways to
  plan a walk, the double bounce, loosening up, the heel, foot action, normal walk spacing,
  weight shift, the belt line, arm movements, counteraction, **The Recipe**; sneaks, tip-toe sneak.
- *Runs, Jumps and Skips* - 4/3/2-drawing formula runs, **The Recipe**, jumps, weight on a jump.
- *Flexibility* - the breakdown, simple overlap, overlapping action, simple counteraction,
  breaking joints, flexibility/overlap in the face, instant read (profiles).
- *Weight* - pressure and weight, how much effort do we expend, dancing, synchronising action.
- *Anticipation* - surprise anticipations, invisible anticipations.
- *Takes and Accents* - a hard accent bounces back, a soft accent continues.
- *Timing, Staggers, Wave and Whip* - stagger timings, the side-to-side vibration formula,
  whip action, wave action.
- *Dialogue* - phrasing, picture and sound sync, accents, attitude, "The Secret" (act it).
- *Acting* - change of expression, look for the contrast, an acting point, body language,
  symmetry/twinning (never mirror - it kills life), steal from life, eyes.
- *Animal Action* - live-action reference, basic animal walk pattern.
- *Directing* - the brief, Leica reel, casting, voice recording, hook-ups, research, editing.

## 3. Harold Whitaker & John Halas - Timing for Animation (3rd ed, ed. Tom Sito)
File: `Timing for Animation by Harold Whitaker and John Halas 3rd Edition.pdf` (185 pp)

**Essence:** Timing is not "how many frames" - it is how you make the audience *feel* force,
weight, size, mood and story. Spacing + timing = the physics and psychology of motion.

**Key lessons:** storyboards and bar sheets; the basic unit of time (ones/twos, frames vs
seconds); animation & properties of matter: cause and effect, Newton's laws, objects thrown
through the air (parabolic arcs), rotating/irregular objects; **force transmitted through
flexible joints and jointed limbs** (the delay chain); spacing of drawings (general + specific);
timing slow vs fast actions; getting into/out of holds; how long to hold; anticipation;
follow through; overlapping action; oscillating movement; **timing to suggest weight and
force (4 chapters!)**; repeat action; character reactions and "takes"; feeling of size
(big = slower, more frames to travel); friction/air/water resistance; cycles (flag); multiple
characters; digital crowds; effects: flames, smoke, water, rain, snow, explosions; timing a
walk; types of walk; spacing in perspective; horses, quadrupeds, gallops, bird flight;
speed lines/motion blur.

## 4. Frank Thomas & Ollie Johnston - The Illusion of Life
File: `the-illusion-of-life-disney-animation_compress.pdf` (548 pp, scan; embedded OCR is noisy)

**Essence:** The Disney master text. Animation = creating the *illusion of life*: a character
that thinks, feels, wants. The 12 principles (ch.3) are the craft's constitution.

**Key lessons:** the 12 principles - squash & stretch (life/deformation), anticipation
(prepare the eye), staging (clarity of idea), straight-ahead vs pose-to-pose, follow-through
& overlapping action, slow-in/slow-out, arcs, secondary action, timing (mood/intent),
exaggeration, solid drawing (weight/volume in 3D thinking), appeal (readable, interesting
design - not "cute"). Later chapters: appeal & dynamics, our procedures (the Disney pipeline),
how to get it on the screen, story (the foundation), character development, animating
emotions and dialogue, acting and emotions (what happens *inside* the character shows
outside). Personality is the goal; effects without intent are noise.

## 5. Jason Osipa - Stop Staring: Facial Modeling and Animation Done Right (2nd ed)
File: `stop-staring_compress.pdf` (387 pp, Wiley)

**Essence:** The face is a system of independent but coordinated parts. Mouth = speech,
eyes/brows = thought and emotion. Master the shapes and the offsets.

**Key lessons:** lip sync basics (the sound matters less than the read); eyes and brows tell
us what a character thinks; facial landmarking; **visimes** (Osipa's 7: B/M/P Closed, EE Wide,
FV, OO Narrow, IH, R, T/S + jaw/open sounds — "phonemes are sounds, visimes are shapes")
and lip sync technique; constructing mouth/nose; **mouth keys** (the standard shape set);
building emotion with eyes; constructing eyes/brows; **eye and brow keys**; connecting the
features (offsets, squints, dependencies so it never moves as one block); skeletal setup,
weighting and rigging for faces; interfaces (controllers/sliders); **squash, stretch and
"squoosh"**; a shot in production (full dialogue shot workflow).

## 6. Ed Hooks - Acting for Animators
File: `acting-for-animators-pdf_compress.pdf` (145 pp, scan - image-only, no text layer;
all 13 chapters verified visually from bundled page images — see
`15-verified-page-images.md`)

**Essence:** Acting craft adapted from Stanislavski for animators. Characters must *act*:
have an objective, face an obstacle, choose tactics, and show emotional state. Movement
provokes emotion; emotion provokes movement.

**Key lessons (from the standard Hooks framework):** the actor's script analysis - given
circumstances, objective (what the character wants NOW), obstacle, tactics (verbs!); the
"moment before" (characters exist before the shot starts); thinking vs feeling (stage vs
screen subtlety); gesture and body language (the body cannot lie); emotional state is
readable in posture/timing; scene analysis: beats, turns, escalation; comedy (surprise,
contrast, timing); dialogue as action (people speak to get what they want); animal behavior
reference; playing intentions not words.

## 7. Fletcher Dunn & Ian Parberry - 3D Math Primer (2nd ed)
File: `3D Math Primer for Graphics and Game Development 2nd Edition.pdf` (846 pp)

**Essence:** The math you actually need: vectors, matrices, rotations, curves, mechanics -
explained for implementers, not mathematicians.

**Key lessons:** Cartesian spaces; vectors (dot: angle/projection, cross: perpendicular/
normal/torque); multiple coordinate spaces (object/world/view - transforms connect them);
matrices and linear transforms (rotation/scale/shear/projection, combining = composition
order matters); 4x4 homogeneous matrices (why 3x4 isn't enough); polar/spherical coords;
**rotation in 3D: orientation vs rotation, Euler angles (and gimbal lock), axis-angle,
quaternions** (representation + conversion + why slerp); geometric primitives & intersection
tests; graphics pipeline & skeletal animation overview; **mechanics 1-2: velocity,
acceleration, Newton's laws, forces, momentum, springs**; **curves in 3D: parametric
polynomials, Hermite, Bézier, splines, continuity (C0/C1/C2), automatic tangent control**
(this is F-curve theory).

## 8. Rick Parent - Computer Animation: Algorithms and Techniques (3rd ed)
File: `Rick Parent - Computer animation_ algorithms and techniques-Elsevier _ Morgan Kaufmann (2012).pdf` (541 pp)

**Essence:** The algorithmic toolbox: how the techniques behind the art actually work, and
when to reach for each.

**Key lessons:** motion perception (what sells motion); heritage/principles of animation &
filmmaking; spaces & transformations, orientation representations (fixed/Euler/axis-angle/
quaternion/exp map); interpolation (ease-in/out, arc length, speed control, quaternion
interpolation, path following); keyframe systems; shape interpolation & morphing;
**kinematic linkages: hierarchies, FK, IK (analytic, Jacobian, numeric solutions)**; motion
capture (processing, retargeting, combining); **physically based animation: spring-dampers,
particles, rigid bodies, cloth, constraints**; fluids; **human figures: reaching/grasping,
the mechanics of walking, clothing/hair**; **facial animation (FACS, parameterized models,
blend shapes)**; behavioral animation (flocking, agents, crowds, personality/emotion);
special models (implicit surfaces, plants/L-systems).

---

**Provenance note:** Acting for Animators is a scan with no OCR text anywhere (its section in
the merged PDF is image-only). ALL 13 of its chapters were verified visually: every
chapter's opening page plus the load-bearing interiors (Human Character Analysis, Power
Centers, Laban efforts) — 26 pages bundled in this skill (`references/images/hooks-*.jpg`,
catalogued in `15-verified-page-images.md`) — and every section heading was checked via
contact sheets of the full scan. Chapter-interior prose beyond the bundled pages is taught
only where a bundled page or verified heading supports it. The Survival Kit's structure was
recovered from the merged OCR (its scan has no local text layer); its eight most
load-bearing doctrine pages are also bundled as images. Illusion of Life's local text layer
is garbled OCR; quotes from it should be paraphrased, not quoted verbatim.

## 9–14. The surfacing canon (essence; full treatment in refs 16–17)

9. **Wes McDermott — The PBR Guide**: the metal/roughness law in numbers (F0 2–5%,
   base color 30–240 sRGB); Substance's own rulebook. Text-verified.
10. **Owen Owen Demers — Digital Texturing and Painting**: see → dissect → decide; observation
    before painting. Contents + key chapters page-verified (ref 15).
11. **Jeremy Jeremy Birn — Digital Lighting & Rendering** (1st-ed. scan): lighting judgment;
    specular color law; five qualities of light.
12. **Matt Pharr, Wenzel Jakob, Greg Humphreys — Physically Based Rendering 4e**: BSDF/sampling theory
    explaining Cycles. Text-verified (ch. 9–10 core).
13. **Ebert, F. Kenton Musgrave, Darwyn Peachey, Ken Perlin, Worley — Texturing and Modeling**: noise families
    and procedural composition → Blender nodes. Text-verified.
14. **James James Gurney — Color and Light**: observed light behavior (transmitted light,
    four zones on leaves). Contents + key page verified.

## 15–21. The directing canon (essence; full treatment in refs 23–24)

15. **Francis Francis Glebas — Directing the Story**: directing = directing attention; narrative
    questions; storyboard thinking; aiming for the heart. Text-verified.
16. **Bruce Bruce Block — The Visual Story**: seven visual components; contrast and affinity as
    the intensity control; visual structure parallels story structure. Text-verified.
17. **Steven D. Steven Katz — Film Directing Shot by Shot**: continuity style; staging patterns;
    moving-camera choreography. Text-verified.
18. **Walter Walter Murch — In the Blink of an Eye**: the Rule of Six for cuts. *Uploaded copy is a
    chapter-summary edition — used at summary level; full text pending.*
19. **Walt Walt Stanchfield — Drawn to Life Vols. 1–2**: draw verbs not nouns; the pose as a
    one-drawing story; gesture is the backbone. Vol. 1 text-verified, Vol. 2 contents.
20. **Robert Robert McKee — Story**: *uploaded scan is not page-readable in this environment
    (no text layer, non-extractable page images) — NOT integrated; awaiting a readable
    edition. Do not cite from it.*
21. **Joseph Joseph Gilland — Elemental Magic Vol. 1**: classical FX categories (liquids; fire,
    smoke, explosions; magic) as behavior design → Blender sim/shader choices.
    TOC-verified (PDF split losslessly into two parts at repo ingestion).
