# 24 — Pose, Gesture & Effects Craft (Walt Stanchfield · Joseph Gilland)

## A. Walt Walt Stanchfield — *Drawn to Life* Vols. 1–2 (the Disney master classes)

Walt Stanchfield taught gesture drawing at Disney for ~20 years (Tim Burton, Brad Bird, Glen Keane,
Andreas Deja sat in that room — Vol. 2 Foreword). Vol. 1 is text-verified; Vol. 2
verified at contents level (`images/dir-01-stanchfield2-contents.jpg`): its lectures
run **Innovation → Drawing → Expression** (68 lectures). The doctrines that change
Blender work:

- **"Draw Verbs Not Nouns"** (Lecture 46). Pose the *action and attitude*, not the
  anatomy exhibit. In Blender terms: a key pose should be nameable as a verb —
  *pleading, sneaking, collapsing, showing off*. If the pose's best description is a
  noun ("standing man, arm raised"), it fails Gate B (ref 19).
- **"The pose — A One-Drawing Story"** (Lecture 93). One pose must carry its beat's
  whole story point, readable at a glance. Test: show the single frame, no context —
  does a stranger know what just happened and what's felt? This is the blocking
  standard (ref 18's Acting Point, made visual).
- **Gesture is the backbone**: *"A scene of animation is more or less a series of
  gesture drawings"* and once you have found *"the essence of the pose or action, the
  details will nearly take care of themselves."* Order of work in every pose: line of
  action/essence first (30 seconds), structure second, anatomy/props last. Reversing
  this order is the root of stiff CG acting (ref 13).
- **First impression is the intended goal** (Lectures 52/105/115): the audience reads
  the gesture in the first fraction of a second; design for that read (silhouette
  clarity — Francis Glebas' "Clear Silhouettes" discipline, ref 23 — then let detail reward
  the second look.
- **Workflow translation**: thumbnail the beat's poses (Grease Pencil, ref 11) before
  touching the rig — 6 thumbnails, pick the clearest verb. Pose in passes: hips/line
  of action → spine → head → limbs → hands (Vol. 2 dedicates lectures to hands and to
  "Forces (Energy, Animation, Power, Vim, Vigor, and Vitality)"). Caricature the
  essence, not the features: push the *relationship* that tells the story.

## B. Joseph Joseph Gilland — *Elemental Magic Vol. 1* (hand-drawn FX → Blender principles)

Verified contents: 1 History of Classical Animated SFX · 2 The Art of Drawing and
Animating Special Effects · 3 The Specific Effects Categories · 4 **Liquids** ·
5 **Fire, Smoke, and Explosions** · 6 **Magic** · 7 Props and Everything (Else) ·
8 The Last Element. The book is 2D craft; its transferable law for Blender:

- **FX are characters with behavior, not decorations.** Each element has a nature:
  liquids maintain volume and seek level; fire rises, tears, and dies upward; smoke
  expands and dissipates; explosions are pressure events (fast out, slow settle).
  Animate/simulate the *behavior* and the audience believes the element; copy the
  *shape* and they don't. Give every hero effect the ref 18 treatment: what is it
  doing, in beats (build → release → aftermath)?
- **Design in cycles and phases.** Classical FX are built from repeating, offset cycles
  (flames licking in staggered loops; splashes as crown→column→drops phases). In
  Blender: shader-driven loops (noise offset over time) and simulation caches are the
  same idea — build cycles you can art-direct, don't accept one opaque sim take.
- **Choose the Blender weapon per effect** (decision table):
  | Effect | First choice | Why |
  |---|---|---|
  | Water surfaces/splashes | FLIP simulation (baked) for heroes; animated normal/noise shaders for calm surfaces | physics sells mass; shaders sell sparkle |
  | Fire | Volume shader + animated noise (stylized/controlled) or Mantaflow fire sim (realistic) | control vs realism dial (ref 22 §A) |
  | Smoke/dust | Mantaflow smoke, baked; volume noise cards for background | dissipation behavior is sim-native |
  | Magic/sparkles | Particles + shader glow (hand-timed emission) | magic is timing and design, not physics |
  | Rain/snow | Particle systems (instanced) | cheap, cycle-friendly (ref 20) |
  | Cloth/hair dynamics | Blender cloth/hair sims, baked at Gate S | secondary motion with physical lag |
- **Timing belongs to the element's physics**: heavy water moves slower than it looks;
  flame tips move faster than the base; smoke decelerates as it expands. Check FX
  against reference footage frame-by-frame (Owen Demers' observation discipline, ref 17 §1)
  and against the style dial — cartoon fire and film fire obey different contracts.
- **Integrate or it floats**: FX must touch the world — light cast by fire, wetness
  darkening ground (roughness down, ref 16), smoke catching key light, splashes
  reacting to the hero's motion. An effect that doesn't affect its surroundings reads
  as a sticker, however good the sim (Gate P check, ref 19).
