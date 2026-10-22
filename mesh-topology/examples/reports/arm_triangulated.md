# Topology report — arm_triangulated

**Score 78.3 / 100 — grade B**

| | |
|---|---|
| vertices | 640 |
| faces | 1,248 (0 quads / 1,248 tris / 0 ngons) |
| edges | 1,888 |

## Subscores

| category | score | weight | what it measures |
|---|---|---|---|
| quads | **84** | 22 | quad purity — tris fan, ngons crease |
| poles | **100** | 20 | valence-4 breaks, weighted by how much the surface bends there |
| density | **100** | 12 | edge-length balance and quad squareness |
| joints | **10** | 12 | loops crossing each joint, poles inside it, local density |

## 1. Quad purity

quads 0.0% · tris 100.0% · ngons 0.0% · quad skew 0.000 (0 = square)

- Triangles on a deforming surface fan into a starburst when bent. Fine on flat, rigid or hidden areas; expensive on elbows, knees, shoulders, hips.

## 2. Poles (vertices with valence != 4)

608 poles, 950.0 per 1000 vertices, by valence: {6: 608}

A regular quad grid bends smoothly because every vertex has 4 neighbours. A pole is a pinch point: it ripples, dents, or catches light wrong when the surface deforms. Poles are unavoidable (a closed shell needs some), but they belong on **flat, rigid, or hidden** surfaces — never on the belly of a deformation zone.

| pole | valence | position (x, y, z) |
|---|---|---|
| v16 | 6 | (0.077, 0.000, 0.036) |
| v17 | 6 | (0.071, 0.029, 0.036) |
| v18 | 6 | (0.054, 0.054, 0.036) |
| v19 | 6 | (0.029, 0.071, 0.036) |
| v20 | 6 | (0.000, 0.077, 0.036) |
| v21 | 6 | (-0.029, 0.071, 0.036) |
| v22 | 6 | (-0.054, 0.054, 0.036) |
| v23 | 6 | (-0.071, 0.029, 0.036) |
| v24 | 6 | (-0.077, 0.000, 0.036) |
| v25 | 6 | (-0.071, -0.029, 0.036) |
| v26 | 6 | (-0.054, -0.054, 0.036) |
| v27 | 6 | (-0.029, -0.071, 0.036) |
| v28 | 6 | (-0.000, -0.077, 0.036) |
| v29 | 6 | (0.029, -0.071, 0.036) |
| v30 | 6 | (0.054, -0.054, 0.036) |
| … | | 593 more |

## 3. Edge flow

loops traced 0 (0 closed) · median length 0 edges · longest 0

loop coverage 0% (edges that belong to a loop of 8+ edges) · long-loop coverage 0%

grid coherence 0.00  (1.0 = every vertex sits in a clean orthogonal grid of loops, 0 = directions are random)

Edge loops are the mesh's memory of a bend: a loop that runs the length of a limb distributes the rotation across every quad in it. A loop that turns back on itself, branches, or runs out after three edges concentrates the whole bend into one quad.

## 4. Density and shape balance

edge length CV 0.27 · p95/p5 ratio 2.87 · median edge 0.0359

## 5. Joints

| joint | loops crossing | poles inside | density ratio | quad purity | score |
|---|---|---|---|---|---|
| shoulder | 0 | 48 | 1.04 | 0% | **10** |
| elbow | 0 | 112 | 0.96 | 0% | **10** |
| wrist | 0 | 48 | 0.82 | 0% | **10** |

`loops crossing` is the number of edge loops that pass through the joint. Under 3, the joint will candy-wrapper when it bends past ~60°. `density ratio` is the local mean edge length divided by the body average — above ~1.5 the joint smears, below ~0.5 it pinches.

## 6. Hygiene

| check | count |
|---|---|
| non manifold edges | 0 |
| non manifold verts | 0 |
| boundary edges | 32 |
| degenerate faces | 0 |
| duplicate vert faces | 0 |
| isolated verts | 0 |

## Fix order (highest score impact first)

1. **joints** — 10/100, worth 10.8 points. Add 1-2 loops across the joint and push poles out of it; the bend needs 3+ loops.
2. **quads** — 84/100, worth 3.5 points. Triangulate only rigid/hidden islands; rebuild ngons as quads.
