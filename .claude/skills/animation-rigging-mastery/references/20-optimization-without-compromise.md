# 20 — Optimization Without Compromise (fast scenes, intact realism)

> **The law: optimize what the camera cannot see; never touch what the feeling needs.**
> Realism is lost by cutting the visible 5% that sells the shot — speed is won in the
> invisible 95%. Budgets are set **per shot**, because (Owen Demers, ch. 5) what matters is
> the asset *"at the time of the shot"* — and detail density is composition (ref 17 §9).
> Principles below tie to Jeremy Birn's rendering-algorithms craft (raytrace depth discipline,
> ch. 9), PBRT's sampling logic (ch. 2–3), and the PBR Guide's texel budgets — applied
> as standard Blender production practice.

## 1. The free wins (zero quality cost — always do these)

**Geometry**
- **Instance, don't duplicate**: linked duplicates (Alt+D), collection instances, and
  geometry-node instances cost memory once. 10,000 grass blades = 1 mesh.
- **Viewport ≠ render subdivision**: Subsurf Viewport 1 / Render 2–3 (or shot distance).
  You animate light, you render dense.
- **Camera culling**: Cycles → Simplify → camera/distance culling for huge sets; hide
  off-camera objects per shot (holdout still costs — disable in render instead).
- **LOD thinking**: silhouette carries quality. A background house needs roofline +
  texture, not modeled window frames (ref 17 Owen Demers Tire rule: real relief only where
  the silhouette shows it).

**Textures (the biggest silent cost)**
- **Resolution follows screen coverage**: if an asset never exceeds ~800 px on screen, a
  4K map is pure waste — 1K is identical *in the render*. Texel-density standard
  (ref 17 §2) makes this automatic.
- **16-bit only where banding bites** (height/displacement gradients, subtle roughness):
  base color at 8-bit is perceptually identical and half the memory.
- **Share**: one tileable grunge/trim across a set beats 40 unique 2K maps. Reuse is
  invisible when breakup varies (ref 17 §5 frequency stacking).

**Shading & lights**
- **Light-path discipline** (Jeremy Birn's rule): bounces/ray depth set by *need* — count the
  transparent/reflective layers in the shot; depth beyond that renders nothing visible
  at real cost. Transparent/Transmission bounces are the expensive ones.
- **Clamp indirect** (e.g. 10) kills firefly-chasing samples with no visible change in
  AgX. Caustics OFF unless a hero moment needs them.
- **Bake frozen procedurals**: a 6-layer noise stack evaluated per-sample per-frame is
  rent you pay 250 times per shot. If the material doesn't move/change, bake it to maps
  (keep the live version archived). Hero close-up materials stay live — §2.

**Render (Cycles)**
- **Adaptive sampling + denoising is the no-compromise pair**: set a noise *threshold*
  (0.01 typical final, 0.005 hero), let flat areas stop early; OpenImageDenoise finishes.
  Fixed 4096-sample renders are amateur economics (PBRT's core lesson: samples should
  go where the variance is).
- **Persistent Data** ON for animation (keeps BVH/textures between frames).
- **Render passes/layers** so a note ("warmer light") is a comp tweak, not a re-render.
- Test at 25–50% resolution with render regions; approve timing/materials small, render
  big once.

**Animation data**
- Animate on **proxy rigs** (low-res mesh, subsurf off) via Library Overrides; swap to
  hero for render (ref 10/11). Playback speed is an acting tool — protect it.
- **Bake simulations** (cloth/particles) once approved; never let final renders re-sim.
- Purge orphan data, keep relative paths, avoid duplicate datablocks (`.001` creep).

## 2. The honest trades (small quality cost — allowed only where invisible)

| Trade | Cost | Acceptable when |
|---|---|---|
| Lower texture resolution | softness if camera pushes in | background / motion-blurred / out-of-focus assets |
| Baked procedural → static maps | no per-frame change; UV seams return | anything not animated in shader space |
| Reduced samples + denoise | slight detail smearing in noise-prone areas (hair, SSS edges) | mid/wide shots; raise for ECU heroes |
| Lower render % for review renders | none to final | all approvals except final QC |
| Fewer light bounces | darker indirect corners | interiors without mirror-like chains |
| Decimation of background meshes | silhouette facets | only beyond focus distance |

**Forbidden trades** (these DO compromise realism): killing Fresnel/specular to "speed
up", flattening roughness variation, dropping SSS on skin heroes, 8-bit-normal banding
on smooth heroes, denoiser-as-crutch on ECUs, cutting contact shadows. If a shot is too
slow, optimize around the hero — never through it.

## 3. The per-shot budget (write it in the Pipeline Brief, ref 14)

```
SHOT S07 (ECU dialogue): samples threshold 0.005 · textures: face 4K UDIM, bg 1K ·
subdiv render 3 (face) / 1 (set) · SSS full · bounces: transmission 4 (glasses) ·
proxy rule: animate at viewport-subdiv 1, hair hidden until Gate P
SHOT S08 (wide chase): threshold 0.01 · motion blur covers texture softness →
set textures capped 2K · instances for crowd · volumetrics half-step
```

Rule of thumb: the ECU gets 10× the per-frame budget of the wide — and deserves it
(Hooks ch. 7: the close-up is where the audience reads thought).

## 4. Diagnosis order (when a frame is slow)

1. Check the render stats: peak memory + time per pass. Guess-free, always.
2. Turn off one system at a time (volumetrics → hair → transmission → SSS) to find the
   eater; optimize *that*, not everything.
3. Texture memory first (usual suspect #1), then samples wasted on fireflies (clamp),
   then geometry evaluated off-camera, then un-baked sims.
4. Re-measure. Optimization without before/after numbers is superstition (ref 19 §6:
   numbers over adjectives).

## 5. Viewport performance (your iteration speed = quality)

Slow playback produces bad timing decisions — protecting fps *is* protecting realism.
Keep an "animation mode": proxy meshes, no volumetrics, Material Preview only for
surfacing checks, simplify ON in viewport only. **Simplify is a preview drug: OFF for
final renders** (it caps subdiv/textures globally — a classic silent quality killer).

## Blender 5.x performance notes (use these before sacrificing anything visible)

- **Cycles Texture Cache (5.2)** — `Render Properties → Performance → Texture Cache`
  + Auto Generate: textures convert to `.tx` in `blender_tx/` and only needed tiles/
  resolutions load per render tile. Big texture sets stop blowing VRAM (Blender's
  benchmarks show texture memory cut dramatically on texture-heavy scenes) at a
  small render-speed and disk cost. Pair with `Simplify → Texture Resolution %`
  for viewport work. This replaces the old "shrink everything to 1K" panic move.
- **EEVEE instance speed (5.2)** — up to ~2× in instance-heavy scenes; crowds/sets
  via instances are cheaper than in 4.x. Note the 5.2 screen-space raytracing
  overhaul can change the look of 4.x files — re-approve hero lighting after upgrade.
- **Action evaluation ~2× faster (5.1)** — heavy rigs and shape-key stacks play at
  noticeably higher fps; raise the rig-complexity budget before cutting controls,
  but keep testing playback at full fps (ref 19 gates still rule).
- `Use Tiling` was removed (5.0) — old tiling advice is void; `Performance → Memory
  → Tile Size` now mainly steers texture-cache loading.
