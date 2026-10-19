# 3D Math, Curves, IK & Procedural Systems — Dunn/Parberry + Parent

Sources: *3D Math Primer* (chs. 2, 5-8, 11-13) and *Computer Animation: Algorithms and
Techniques* (chs. 2-3, 5, 7, 9). Use this when building tools, solvers, drivers, or when
debugging transforms/orientation issues in Blender.

## 1. Vectors — the daily tools (Math Primer ch. 2)

- **Dot product** `a·b = |a||b|cosθ`: angle between bones (stretch detection!), projection
  (how much of a force acts along a limb), parallel test (`|a·b| ≈ 1`).
- **Cross product** `a×b = n` (perpendicular, right-hand rule): surface normals, joint
  axes, torque direction (`τ = r×F`), building orthonormal bases (bone roll!).
- Unit vectors normalize direction; distance formula measures bone length (IK stretch).
- Reason to care: drivers/constraints in Blender are these formulas in disguise.

## 2. Transformations (ch. 5-6 + Parent ch. 2)

- Transform = linear map (rotation/scale/shear) + translation → **4×4 homogeneous matrix**.
- **Composition order matters**: `M = T·R·S` (scale first, then rotate, then translate) is
  the usual object convention — and why parenting in Blender inherits transforms.
- Multiple spaces: object/local vs world vs view (Math Primer ch. 3). A bone's local axes
  are its own space; constraints copy between spaces — always know which space you're in.
- Extracting from a matrix (Parent 2.1.6): decomposition into T/R/S is how Blender shows
  channels; non-uniform scale + rotation compounding is why we say **apply scale / never
  scale bones in the rig**.

## 3. Orientation & rotation (Math Primer ch. 8 — the important one)

| Representation | What it is | Use when |
|---|---|---|
| Euler angles | 3 ordered axis angles | human-readable channels; gimbal lock when middle axis hits ±90° |
| Axis-angle | direction + amount | simple single-axis rotations; twist bones |
| Quaternion | 4D "arc on the unit sphere" | interpolation (slerp), additive layers, mocap, avoiding gimbal lock |
| Matrix | 9 numbers (basis vectors) | constraint math, conversions |

- **Gimbal lock** (Euler): when two of the three axes align, a DOF disappears — the classic
  reason a shoulder/hip Euler chain "flips". Reason: rotations are NOT commutative.
- **Quaternions**: represent orientation as `q = (sin(θ/2)·axis, cos(θ/2))`; interpolation
  uses **slerp** (constant angular speed) — Parent 3.3.1. Blender's Quaternion rotation
  mode + W/X/Y/Z channels is exactly this.
- Practical rule: rig twist bones and additive layers in quaternion mode; expose Euler
  only on controls animators will hand-key.

## 4. Curves & interpolation (Math Primer ch. 13 + Parent ch. 3)

- Parametric polynomial curves `P(t)`: Hermite (endpoints + tangents), **Bézier** (control
  hull), splines (piecewise with continuity).
- **Continuity**: C0 (connected), C1 (tangent matches — smooth), C2 (curvature matches —
  fluid). This is exactly F-curve handle theory: Vector = C0 break, Aligned = C1,
  Auto Clamped ≈ smooth C2-ish.
- **Ease-in/ease-out** (Parent 3.1.3): speed control along the curve = the spacing doctrine
  in math form (`03-timing-spacing.md`).
- Arc length & speed (Parent 3.2): constant speed along a path needs arc-length
  reparameterization — relevant when animating along curves (Follow Path constraint + fixed
  offset speed).
- Automatic tangent control (Math Primer 13.9) = Blender's "Auto Clamped" handles.

## 5. IK math (Parent ch. 5)

- **Hierarchies**: each bone has a local frame; the world pose = chain of matrix
  multiplies (FK). Fast, predictable, but reaching requires keying many bones.
- **IK**: solve joint angles from a desired end-effector position.
  - 2-bone analytic: law of cosines (arm/leg) — exact, stable (Blender's IK on 2-bone
    chains behaves like this).
  - **Jacobian** `J`: relates joint velocities to end-effector velocity; numeric solutions
    iterate `Δθ = J⁻¹Δx` (damped least squares for stability).
  - CCD/FABRIK (modern practice): cyclic coordinate descent (rotate each joint toward the
    target repeatedly) / forward-and-backward reaching — cheap, robust for long chains
    (tails, tentacles, spines). Implement in Blender via add-on or iterative drivers.
- **Pole vectors**: a third constraint fixing the bend plane (knee/elbow) — without it the
  chain's bend plane is undefined (the "pop" problem).

## 6. Physics for secondary motion (Parent ch. 7 + Math Primer ch. 11-12)

- **Spring-damper**: `F = -k·x - c·v` — the formula behind every settle, jiggle, tail sway.
  Underdamped = bouncy settle (cartoon), overdamped = heavy/creepy (realistic).
- Rigid bodies: free fall `a = g`, collisions (impulse), linked hierarchies (ragdoll).
- Cloth/hair: mass-spring lattices with constraints — in Blender use Simulations
  (Cloth/Hair/Softbody) or fake with driven springs (simpler, art-directable).
- Particles: emitter → attributes (life, velocity, forces) → render; use for FX timing
  (Whitaker's flames/smoke/water chapters tell you how the timing should FEEL).
- Mocap (Parent ch. 6): capture → clean noise (filtering) → **retarget** (map to skeleton)
  → blend. In Blender: retarget with the "bone constraint copy" method or add-ons;
  always clean the curves after (mocap noise kills appeal).

## 7. Blender tool-building checklist

- Drivers use simple expressions (`var*0.5`, `min/max`); keep them readable; name channels.
- For math-heavy rigs (stretchy limbs, spring tails, foot roll): use bones + constraints +
  drivers first; Python only when the math needs iteration.
- Every procedural system must have an ON/OFF and a strength property (art direction wins).
- Validate with unit tests in the file: pose extremes, check no NaNs/flips in local axes.
