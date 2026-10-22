# Mesh topology scorer

Short answer to the question: **yes — but topology is not one thing.** For a deforming character
"good topology" means seven separate properties, and each one fails differently on screen. This
tool measures all of them and gives you a number plus a list of what to fix, in priority order.

```bash
python3 topology_check.py --selftest                      # proves the scorer works, no mesh needed
python3 topology_check.py --mesh model.obj                # score
python3 topology_check.py --mesh model.obj --joints auto --report r.md --heatmap map.png
```

Inside Blender or Maya: `blender_topology_check.py` / `maya_topology_check.py` — they read the
active object directly (no export) and leave the problem vertices selected.

Demo you can run right now:

```bash
python3 make_examples.py
python3 topology_check.py --mesh examples/arm_good.obj   --joints examples/joints_arm.json
python3 topology_check.py --mesh examples/arm_coarse.obj --joints examples/joints_arm.json
```

| mesh | score | why |
|---|---|---|
| `arm_good` | **97.8 (A)** | 40 rings, 8 loops across the elbow, 4 at each end |
| `arm_coarse` | **77.7 (B)** | 9 rings: the elbow has 2 loops, edge lengths vary 13× |
| `arm_ngon_caps` | **75.2 (B)** | same as good, but capped with two n-gons. The cost shows up as **poles**: the single face makes all 16 rim vertices valence-3, so two invisible faces at the ends drop the score 22 points |
| `arm_triangulated` | 78.3 (B) with `--mode tri` | fine as triangles; **13.6 (F)** if you judge it by quad rules |

---

## 1. What each score means

| category | weight | what it measures | how it fails on screen |
|---|---|---|---|
| **quad purity** | 22 | % quads; n-gons are penalised harder than tris | a tri on a bending surface fans into a starburst; an n-gon collapses to a crease and cannot be subdivided |
| **poles** | 20 | interior vertices with valence ≠ 4, weighted by how much the surface bends where they sit | a pole on a deforming surface dents and catches light wrong when the muscle moves |
| **flow** | 20 | grid coherence: at every vertex, do the incident loops fall into two perpendicular families? | loops that cross the limb axis shear and slide when it bends |
| **loops** | 14 | loop lengths; loops that die after a few edges can't carry a bend | long loops distribute rotation; short ones concentrate it into one quad |
| **density** | 12 | edge-length spread (CV, p95/p5) and quad squareness (skew) | a dense patch next to a sparse one tears at the seam |
| **joints** | 12 | rings crossing each joint, poles inside it, local density | fewer than 3 rings across an elbow = candy-wrapper |

Grades: A ≥ 90, A- ≥ 85, B+ ≥ 80, B ≥ 75, C+ ≥ 68, C ≥ 60, D ≥ 50, F below.

**Hygiene is a hard cap, not a weight.** Non-manifold edges cap the score at 40, degenerate faces
at 55, bowtie vertices at 65. Those are bugs, not style — a non-manifold mesh has no unambiguous
normal, so every shading and skinning result after it is unreliable.

---

## 2. The measurements, in the order that matters

### 2.1 Quad purity — 22 points

Quads subdivide, bend predictably, and let Catmull-Clark do its job. Triangles are fine on rigid or
hidden areas (inside a mouth, under a sole) and expensive on elbows, knees, shoulders and hips.
N-gons cost more than triangles because they cannot be subdivided at all without a decision being
made about the topology.

`quad skew` (0 = perfectly square, 0.3+ = rhomboid) is reported with density, because a mesh can be
100% quads and still deform badly if every quad is a sliver.

### 2.2 Poles — 20 points

A **pole** is a vertex whose valence isn't 4. A regular quad grid has 4 edges at every vertex,
which is what lets a bend propagate evenly. A pole is where that stops: a 5-pole bulges, a 3-pole
pinches, and both ripple when the surface moves under them.

A closed quad shell *needs* poles (Euler characteristic: you cannot tile a sphere with pure quads).
So the question is never "are there poles", it's **where**. The scorer weights each pole by the
local curvature and by whether it sits inside a joint sphere. Poles on the belly, the scapula, the
back of the elbow — expensive. Poles on the sole of the foot, behind the ear, or on a
hidden boundary — free.

Vertices on an open boundary are excluded: their valence is whatever the cut happened to be, which
tells you nothing about flow.

### 2.3 Flow coherence — 20 points

This is the "topology flows along the muscles" part, made measurable.

At a well-flowed quad vertex the incident loop edges fall into **two perpendicular line families** —
a local grid. Directions are unsigned (a line, not an arrow), so the scorer compares them modulo
90° using a quadrupled-angle mean:

```
q = | mean( exp(4i·θ) ) |        θ = signed angle of each edge in the tangent plane
```

Four edges at 0°/90°/180°/270° give `4θ = 0/360/720/1080` → all +1, so **q = 1**. Random
directions cancel to **q ≈ 0**. A rigid quad torus measures 1.00; a triangulated soup measures 0.
Anything below ~0.6 means loops are crossing each other and the surface will shear at the crossing.

Only loops of 8+ edges are counted, because short loops are noise.

### 2.4 Loop length — 14 points

Traced by walking edge → opposite edge → next quad, which is the same walk the Edge Loop tool does.
A closed loop of 30 edges is a rib that can hold a bend; a loop that runs 4 edges and stops can't.
Both raw coverage and median length are scored.

### 2.5 Density — 12 points

Edge-length coefficient of variation, p95/p5 ratio, and quad skew. Uniform density deforms
uniformly. A region at 3× the average density next to one at 0.5× is where the seam tears, because
the two regions respond to the same rotation with different stiffness.

### 2.6 Joints — 12 points

The category that actually predicts candy-wrapper. For each joint you get:

- **rings crossing** — how many edge loops cross the bend. A loop counts as a ring if its plane
  normal is parallel to the limb axis (found by PCA of a neighbourhood 4× the joint radius). Under
  3 → the joint collapses when it bends past ~60°. Over ~14 → wasted density that will pinch.
- **poles inside** the joint sphere.
- **density ratio** — local mean edge length ÷ body average. Target 0.6–1.4.
- **quad purity inside** the joint.

Joints come from `--joints joints.json`:

```json
{"joints": [
  {"name": "elbow", "center": [0.0, 0.0, 0.72], "radius": 0.13}
]}
```

or `--joints auto`, which finds them by clustering high-dihedral-bend faces (armpit, inner elbow,
crotch, behind the knee) and fitting a sphere to each cluster. Auto is a convenience, not a
substitute for naming the real joints — it finds where the *surface* creases, not where the
*skeleton* bends.

---

## 3. Output

- **console** — score, grade, subscores as bars, caps
- **`--report r.md`** — full markdown with every number, the top-15 pole positions, and a
  "fix order" list sorted by how many points each fix is worth
- **`--heatmap map.png`** — two orthographic panels (front/side in the mesh's own axes) with the
  wireframe colour-coded: grey quads, orange tris/n-gons, yellow poles, red high-bend shading,
  cyan joint spheres
- **`--json`** — everything, for a pipeline

Example output, `arm_coarse`:

```
SCORE 77.7 / 100   grade B
  quads    100.0
  poles    100.0
  density    3.0     <- 13x edge-length spread
  flow     100.0
  loops     56.0
  joints    62.9     <- elbow has 2 rings, shoulder 1, wrist 1
```

---

## 4. What this does NOT measure

Said plainly, because a number invites over-trust:

1. **Shape.** A perfect quad grid over bad anatomy still deforms badly. The scorer never looks at
   whether the mesh actually resembles a human.
2. **Loop *placement*.** It counts rings crossing a joint, not whether they sit where the
   deformation happens. Two rings in the right place beat eight rings of uniform spacing.
3. **UV seams, weights, shape keys.** Unrelated to topology, all of them break the same shots.
4. **Self-intersection.** A dense armpit that folds through itself scores well here.
5. **The absolute score is a rubric, not physics.** The weights are defensible (they encode what
   production retopo guides and riggers agree on) but they are a choice. Treat the score as a
   ranking tool between two versions of a mesh, and the *subscores* as the actionable part.
6. **Triangulated meshes are judged differently.** A game/scan export with excellent triangle flow
   scores 94 under `--mode tri` and 13 under quad rules — because quad rules do not apply. The tool
   auto-detects this and says which lens it used; `--mode` forces it.

If you want the honest summary: **score alone is not the goal.** Use it to find which of the seven
properties is dragging, fix in the order the report prints, and stop when the remaining deductions
are in places nobody will see deform.

---

## 5. Files

| file | what |
|---|---|
| `topology_check.py` | the scorer (numpy only, `--selftest` needs no DCC) |
| `blender_topology_check.py` | Blender adapter — active object, evaluates modifiers, leaves poles in a vertex group |
| `maya_topology_check.py` | Maya adapter — copies the mesh, selects the poles |
| `make_examples.py` | builds the demo arms in `examples/` |
