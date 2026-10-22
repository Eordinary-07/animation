# Topology report — arm_good

**Score 97.8 / 100 — grade A**

| | |
|---|---|
| vertices | 640 |
| faces | 624 (624 quads / 0 tris / 0 ngons) |
| edges | 1,264 |

## Subscores

| category | score | weight | what it measures |
|---|---|---|---|
| quads | **100** | 22 | quad purity — tris fan, ngons crease |
| poles | **100** | 20 | valence-4 breaks, weighted by how much the surface bends there |
| density | **100** | 12 | edge-length balance and quad squareness |
| flow | **100** | 20 | edge loops run in coherent directions and don't die out |
| loops | **84** | 14 | loop length — short loops can't store a bend |
| joints | **100** | 12 | loops crossing each joint, poles inside it, local density |

## 1. Quad purity

quads 100.0% · tris 0.0% · ngons 0.0% · quad skew 0.006 (0 = square)

- Quad coverage is production-grade.

## 2. Poles (vertices with valence != 4)

0 poles, 0.0 per 1000 vertices, by valence: {}

A regular quad grid bends smoothly because every vertex has 4 neighbours. A pole is a pinch point: it ripples, dents, or catches light wrong when the surface deforms. Poles are unavoidable (a closed shell needs some), but they belong on **flat, rigid, or hidden** surfaces — never on the belly of a deformation zone.

## 3. Edge flow

loops traced 55 (39 closed) · median length 16 edges · longest 40

loop coverage 100% (edges that belong to a loop of 8+ edges) · long-loop coverage 100%

grid coherence 1.00  (1.0 = every vertex sits in a clean orthogonal grid of loops, 0 = directions are random)

Edge loops are the mesh's memory of a bend: a loop that runs the length of a limb distributes the rotation across every quad in it. A loop that turns back on itself, branches, or runs out after three edges concentrates the whole bend into one quad.

## 4. Density and shape balance

edge length CV 0.26 · p95/p5 ratio 2.40 · median edge 0.0304

## 5. Joints

| joint | loops crossing | poles inside | density ratio | quad purity | score |
|---|---|---|---|---|---|
| shoulder | 4 | 0 | 1.08 | 100% | **100** |
| elbow | 8 | 0 | 0.99 | 100% | **100** |
| wrist | 4 | 0 | 0.82 | 100% | **100** |

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

1. **loops** — 84/100, worth 2.2 points. Extend short loops, or add loops across the joint (edge loop tool / insert loop).
