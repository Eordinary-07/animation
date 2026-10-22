# Topology report — arm_ngon_caps

**Score 75.2 / 100 — grade B**

| | |
|---|---|
| vertices | 640 |
| faces | 626 (624 quads / 0 tris / 2 ngons) |
| edges | 1,264 |

## Subscores

| category | score | weight | what it measures |
|---|---|---|---|
| quads | **99** | 22 | quad purity — tris fan, ngons crease |
| poles | **0** | 20 | valence-4 breaks, weighted by how much the surface bends there |
| density | **100** | 12 | edge-length balance and quad squareness |
| flow | **100** | 20 | edge loops run in coherent directions and don't die out |
| loops | **84** | 14 | loop length — short loops can't store a bend |
| joints | **80** | 12 | loops crossing each joint, poles inside it, local density |

## 1. Quad purity

quads 99.7% · tris 0.0% · ngons 0.3% · quad skew 0.006 (0 = square)

- Quad coverage is production-grade.

## 2. Poles (vertices with valence != 4)

32 poles, 50.0 per 1000 vertices, by valence: {3: 32}

A regular quad grid bends smoothly because every vertex has 4 neighbours. A pole is a pinch point: it ripples, dents, or catches light wrong when the surface deforms. Poles are unavoidable (a closed shell needs some), but they belong on **flat, rigid, or hidden** surfaces — never on the belly of a deformation zone.

| pole | valence | position (x, y, z) |
|---|---|---|
| v0 | 3 | (0.078, 0.000, 0.000) |
| v1 | 3 | (0.072, 0.030, 0.000) |
| v2 | 3 | (0.055, 0.055, 0.000) |
| v3 | 3 | (0.030, 0.072, 0.000) |
| v4 | 3 | (0.000, 0.078, 0.000) |
| v5 | 3 | (-0.030, 0.072, 0.000) |
| v6 | 3 | (-0.055, 0.055, 0.000) |
| v7 | 3 | (-0.072, 0.030, 0.000) |
| v8 | 3 | (-0.078, 0.000, 0.000) |
| v9 | 3 | (-0.072, -0.030, 0.000) |
| v10 | 3 | (-0.055, -0.055, 0.000) |
| v11 | 3 | (-0.030, -0.072, 0.000) |
| v12 | 3 | (-0.000, -0.078, 0.000) |
| v13 | 3 | (0.030, -0.072, 0.000) |
| v14 | 3 | (0.055, -0.055, 0.000) |
| … | | 17 more |

## 3. Edge flow

loops traced 55 (39 closed) · median length 16 edges · longest 40

loop coverage 100% (edges that belong to a loop of 8+ edges) · long-loop coverage 100%

grid coherence 0.99  (1.0 = every vertex sits in a clean orthogonal grid of loops, 0 = directions are random)

Edge loops are the mesh's memory of a bend: a loop that runs the length of a limb distributes the rotation across every quad in it. A loop that turns back on itself, branches, or runs out after three edges concentrates the whole bend into one quad.

## 4. Density and shape balance

edge length CV 0.26 · p95/p5 ratio 2.40 · median edge 0.0304

## 5. Joints

| joint | loops crossing | poles inside | density ratio | quad purity | score |
|---|---|---|---|---|---|
| shoulder | 4 | 16 | 1.08 | 98% | **70** |
| elbow | 8 | 0 | 0.99 | 100% | **100** |
| wrist | 4 | 16 | 0.82 | 98% | **70** |

`loops crossing` is the number of edge loops that pass through the joint. Under 3, the joint will candy-wrapper when it bends past ~60°. `density ratio` is the local mean edge length divided by the body average — above ~1.5 the joint smears, below ~0.5 it pinches.

## 6. Hygiene

| check | count |
|---|---|
| non manifold edges | 0 |
| non manifold verts | 0 |
| boundary edges | 0 |
| degenerate faces | 0 |
| duplicate vert faces | 0 |
| isolated verts | 0 |

## Fix order (highest score impact first)

1. **poles** — 0/100, worth 20.0 points. Move poles off deforming surfaces — slide them toward the nearest flat or hidden boundary.
2. **joints** — 80/100, worth 2.4 points. Add 1-2 loops across the joint and push poles out of it; the bend needs 3+ loops.
3. **loops** — 84/100, worth 2.2 points. Extend short loops, or add loops across the joint (edge loop tool / insert loop).
