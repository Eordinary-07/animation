# 36 — Simulation Technique (fluids & hair sim)

> **Sources.**
> **ref 33 Cloth & Fabric** — the sculpted-vs-simulated decision, fold-depth tolerance,
> multires findings, the Pin Group bridge; carries forward as the cloth half of this chapter.
> **William Vaughan, *Digital Modeling*** — p. 157 *dynamics*: soft body (hair, cloth) vs rigid
> body; p. 63 *topology + cross-department communication*.
> **Blender 5.2 LTS (docs.blender.org)** — Mantaflow fluid sim, Cloth/Soft Body/Rigid Body
> physics modifiers, collision, cache baking, hair dynamics.
> **CGBoost production `.blend` files** — measured counts from `cgboost-analysis.md`.
> **Honest status:** no dedicated fluid-simulation book is in the repo's 34 PDFs. Deep
> Mantaflow parameter reference (domain resolution, inflow/outflow behavior, foam/bubble
> settings) is absent — flagged as missing in `STUDIO-SKILL-MAP.md`. This chapter covers the
> *decision framework, the workflow, and the checked-in rules*; fluid parameter deep-dives
> come from Blender docs, not from an in-repo book.
> **Prerequisites:** ref 27 (topology gate), ref 33 (cloth), ref 34 (hair grooming).

## 0. The sim decision — sculpt or simulate?

This is the single most important question in the chapter, and it is the same one ref 33 asks
for cloth and ref 34 asks for hair:

> **Does the element have to react in this shot?**

- **No** (beauty shot, held pose, single frame): sculpt it. Art-directed, cheap at render
  time, no cache surprises. This is what the CGBoost production files do — sculpted cloth on
  dense base meshes, no multires on heroes.
- **Yes** (cape in a run cycle, dress in a spin, hair in a head turn, water pouring, smoke
  drifting): simulate it. But every sim brings a cache, a bake step, and a re-bake-on-change
  rule. Sim only what must move.

**Vaughan p. 157** classifies the domain:

> *"dynamics collectively refers to any physics-based simulations… soft deformable objects
> (soft body), like hair and cloth, to rigid simulations (rigid body), such as a glass
> shattering."*

Three sim types in this chapter:
1. **Cloth** — ref 33 (recapped briefly below).
2. **Soft body / hair sim** — hair and soft deformables reacting to motion.
3. **Fluid / Mantaflow** — water, smoke, fire (honest status: workflow-level only).

## 1. Cloth sim — recap from ref 33

| Element | Setting | Rule |
|---|---|---|
| Pin group | Blurred vertex group (ref 32 §3 `Blur Vertex Group`) | roots pinned to body; rest free |
| Collision | enabled on body/shoulders | hair/cloth must not pass through the body |
| Quality steps | start 5–8, raise until no tunneling | higher = more accurate, slower |
| Self-collision | only when cloth folds onto itself | expensive; enable only when needed |
| Cache | bake before render; re-bake after any geometry change | stale cache = #1 sim bug |

## 2. Soft body & hair simulation — hair as soft body

If hair must react (swing in a run cycle, whip in a head turn), it is simulated as **soft
body** (Vaughan p. 157). The hair curves from ref 34 carry a **Cloth** physics modifier.

**Setup:**
1. **Pin group** — paint on the scalp, blur it first (`Blur Vertex Group`). Roots pinned,
   lengths free to swing.
2. **Collision** — enable on head and shoulders so hair does not pass through the body.
3. **Quality steps** — raise until hair stops tunneling through shoulders (start 5–8).
4. **Self-collision** — enable only for long hair that folds onto itself (braids, ponytails).
5. **Cache** — bake before rendering; re-bake after any groom or geometry change.

**The trap:** simulated hair looks different from groomed hair. The groom is art-directed;
the sim is physics-directed. If the shot needs a specific hero hair shape, **sculpt or groom
it, do not simulate it.**

## 3. Rigid body sim

For props that break, shatter, or collide (Vaughan p. 157: *"rigid simulations… a glass
shattering"*):

- **Rigid Body** physics modifier on the object.
- **Collision** on the other objects.
- **Active / Passive** — active objects move and react; passive objects are static obstacles.
- **Mesh vs Convex Hull vs Box** collision shape — mesh is most accurate, box is cheapest.
- **Animation deactivation** — keyframe when a rigid body stops simulating and becomes keyed
  animation again.

**When to use:** destruction shots, prop interactions, anything that must physically collide.
**When not to:** anything that can be keyframed cheaper and faster.

## 4. Fluid & smoke — Mantaflow (honest status)

Blender 5.2 uses **Mantaflow** for fluid and smoke sims (domain → flow objects → effector
objects → cache). No in-repo book covers the deep parameter reference, so this section is the
workflow and the known rules:

**Chain:**
- **Domain** — the box the sim lives in. Resolution here is the *single biggest* quality/perf
  trade-off.
- **Flow objects** — what emits liquid/smoke (inflow) or collides (effector).
- **Cache** — baked to disk; re-bake after any change to domain, flow, or geometry.
- **Bake** → **Playback** → **Render** (use the cached sim, not real-time).

**Known rules (Blender 5.x):**
- Domain resolution is the main quality dial — higher = more detail, exponentially slower.
- Inflow/outflow settings control emission and removal.
- Foam, bubble, and spray settings exist for liquid; density/temperature/fire for smoke.
- A sim that looks right in viewport may look different at render resolution — always render
  a test frame.

**Missing from this skill:** deep Mantaflow parameter reference (specific resolution numbers
for specific looks, inflow rate tables, foam size thresholds). If you need that, add a fluid
sim book to the library — flagged in `STUDIO-SKILL-MAP.md`.

## 5. Collision & the topology connection

Every sim type needs collision, and every collision needs clean topology (ref 27):

- **Watertight, manifold mesh** — holes in the collision mesh let particles/cloth leak through.
- **Outward normals** — flipped normals break collision (ref 27 §2).
- **No self-intersections** — intersecting collision geometry causes sim explosions.
- **Thin geometry** — give thin cloth/props a little thickness (Solidify) so collision has
  volume to work with.

**Vaughan p. 63:** the modeler communicates with the sim artist. A dirty mesh is a sim that
fails, and the failure lands on the modeler's desk.

## 6. Cache workflow — the non-negotiable rules

```
[ ] Sim settings final before baking (resolution, quality steps, collision)
[ ] Bake to disk (Physics → Cache → Bake)
[ ] Play back from cache, not real-time, for final review
[ ] Re-bake after ANY change: geometry, groom, collider, domain, settings
[ ] Version the cache file name with the Blender version used
[ ] Never hand off a sim with an unstale (unbaked) cache
```

## 7. The Gate — printable checklist

```
DECISION
[ ] "Does it react?" answered: sculpt if no, simulate if yes
[ ] Sim type chosen: cloth / soft body-hair / rigid body / fluid
[ ] Not simming something that could be keyframed cheaper

CLOTH / SOFT BODY / HAIR
[ ] Pin group painted on anchor, blurred (Blur Vertex Group)
[ ] Collision enabled on all bodies the sim touches
[ ] Quality steps raised until no tunneling
[ ] Self-collision enabled only when sim folds onto itself
[ ] Cache baked before render

RIGID BODY
[ ] Active vs Passive assigned correctly
[ ] Collision shape matches visual complexity (mesh = accurate, box = cheap)
[ ] Animation deactivation keyed when sim ends

FLUID / MANTA FLOW
[ ] Domain sized tightly around the sim (wasted resolution = wasted time)
[ ] Flow objects assigned (inflow/outflow/effector)
[ ] Cache baked; test frame rendered at final resolution

CACHE
[ ] Re-bake rule posted at the rig file
[ ] Cache versioned with Blender version
[ ] No sim handed off with unbaked cache

TOPOLOGY FOR SIM
[ ] Collision meshes watertight, manifold (ref 27 §2)
[ ] Normals outward
[ ] No self-intersecting collision geometry
[ ] Thin geometry given thickness (Solidify)
```

## 8. Blender 5.x quick procedure index

| Task | Path |
|---|---|
| Add Cloth physics | `Physics → Cloth` |
| Add Soft Body physics | `Physics → Soft Body` |
| Add Rigid Body physics | `Physics → Rigid Body` |
| Add Fluid domain | `Physics → Fluid → Type: Domain` |
| Add Fluid flow | `Physics → Fluid → Type: Flow` (Inflow/Outflow/Effector) |
| Pin group for cloth/hair | Vertex group painted on anchor → Cloth/Soft Body → Pin Group |
| Enable collision | `Physics → Collision` on the body |
| Bake sim cache | `Physics → Cache → Bake` |
| Re-bake after change | `Physics → Cache → Bake` (again — after every change) |
| View from cache | Timeline → play back cached frames |
| Set domain resolution | Fluid domain → Domain settings → Resolution divisions |

## 9. The rule

Simulate only what must react. Sculpt everything else. Bake the cache. Re-bake on every
change. And remember Vaughan p. 63: the mesh you hand to the sim artist decides whether the
sim works at all — clean topology is not optional, it is the foundation.
