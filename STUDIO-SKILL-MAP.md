# 🎬 THE COMPLETE STUDIO SKILL MAP — Everything That Constitutes Studio-Level Animation in Blender

> Every discipline that must exist (in a person or in this skill) to take an idea
> to a studio-level finished animation. Audited against the
> **animation-rigging-mastery** skill (34 refs, 25 books) on 2026-10-22.
> ✅ taught in the skill · ⚠️ present but thin · ❌ missing

---

## 1. STORY & PRE-PRODUCTION
| Skill | What it is | Status |
|---|---|---|
| Story structure & script intention | beats, gaps, controlling idea, audience feeling | ✅ refs 18, 25 |
| Directing & visual storytelling | staging, visual structure, attention control | ✅ ref 23 |
| Storyboarding & animatics | drawing the film first; timing boards to audio | ✅ **ref 38** — Glebas beats, Block visual structure, takes, board-to-animatic in Blender VSE |
| Production design & planning | pipeline design, asset lists, style cards | ✅ refs 14, 22 |

## 2. MODELING — *the category topology exposed*
| Skill | What it is | Status |
|---|---|---|
| **Topology & retopology** | edge flow, deformation loops, pole placement, quad discipline | ✅ **ref 27** — Vaughan's rule of three + O'Hailey's edgeloop laws, quad/n-gon discipline, pole placement, density budgets with measured numbers, printable PASS/FAIL Gate |
| Organic modeling & **sculpting** | building characters/props from form; digital clay | ❌ shape-key sculpting only (11 §A7) |
| **Anatomy** | skeleton, muscles, proportions, surface landmarks | ✅ **ref 35** — Zarins + Hogarth plates (rasterize method), anatomy-to-topology pipeline, sculpt workflow, retopo hand-off |
| Hard-surface modeling | props, vehicles, weapons, mechanical forms | ❌ |
| **UV unwrapping** | seams, islands, texel density, UDIMs | ✅ seam/island placement law (27 §5, Vaughan p.182) + texel density law (17 §2) |

## 3. RIGGING
| Skill | Status |
|---|---|
| Armatures, IK/FK, constraints, drivers | ✅ refs 02, 11 §A |
| Skinning & weight painting | ✅ 11 (procedures) + **ref 28** (bind methods, normalization trap, max influences = 3, 60/40 table, deformation battery) |
| Shape keys & corrective deformation | ✅ refs 02, 06, 11 + **28 §9** (never freeze, vertex-group masks, double-transform + combination targets) |
| Facial rig systems (Osipa) | ✅ refs 02, 06 |
| Rig math (vectors/matrices/constraints logic) | ✅ ref 07 |
| Control design, custom properties, rig UI | ✅ 11 §A5 |

## 4. ANIMATION
| Skill | Status |
|---|---|
| Principles, timing & spacing | ✅ ref 03 |
| Body mechanics & locomotion | ✅ ref 04 |
| Acting & performance | ✅ ref 05 (Hooks) |
| Facial animation & lip-sync | ✅ refs 06, 02 |
| Pose & gesture design | ✅ ref 24 (Stanchfield) |
| Polish: arcs, motion paths, graph craft | ✅ 11 §B7–B8 |
| Camera animation | ✅ 11 §C, ref 23 |
| **Motion-capture cleanup** | ⚠️ watchlist + bake procedures; no full cleanup workflow |

## 5. SURFACING (SHADING & TEXTURING)
| Skill | Status |
|---|---|
| PBR shading law (BSDF physics) | ✅ ref 16 |
| Texture painting & observation | ✅ ref 17 (Demers) |
| Procedural texturing (noise theory) | ✅ ref 17 (Ebert) |
| Substance 3D Painter pipeline | ✅ ref 21 |
| Baking (normal/AO/cavity) | ⚠️ present but thin |
| Lookdev (3-light test) | ✅ 16 §6 |

## 6. LIGHTING
| Skill | Status |
|---|---|
| Light design & qualities (Jeremy Birn) | ✅ refs 16–17 |
| Color & light observation (James Gurney) | ✅ refs 16–17 |
| HDRI/environment, volumetrics, light linking | ⚠️ scattered, no dedicated procedures |

## 7. CINEMATOGRAPHY
| Skill | Status |
|---|---|
| Shot design, lenses, composition (Block/Katz) | ✅ refs 08, 23 |
| Camera movement language & rigs | ✅ 11 §C |
| Continuity, editing theory (Walter Murch) | ✅ 23 §4 |

## 8. SIMULATION, HAIR & FX
| Skill | Status |
|---|---|
| FX design language (fire/water/magic behavior) | ✅ ref 24 (Gilland) |
| Cloth/fluid/particle **simulation technique** | ✅ **ref 36** — cloth/sim decision framework, soft body/hair sim, rigid body, Mantaflow workflow-level (deep fluid params still absent — flagged missing) |
| **Hair grooming** (curves, guides, clumping) | ✅ **ref 34** — cards vs strands vs sim, scalp topology, braids, Blender 5.2 hair operators, soft-body sim |
| **Geometry Nodes** systems | ✅ **ref 32** — 646-node census from production files, 5 reusable groups, 2 verbatim recipes |

## 9. ENVIRONMENTS & LAYOUT
| Skill | Status |
|---|---|
| Set/world design intent | ⚠️ via directing refs |
| Layout, set dressing, scene assembly, library overrides | ⚠️ refs 10/14 touch it; no dedicated craft chapter |

## 10. RENDERING
| Skill | Status |
|---|---|
| Cycles/EEVEE craft, sampling, denoising | ✅ refs 10, 20 |
| Color management (AgX/ACES) | ✅ 16 §5, 11 §0 |
| Optimization without quality loss | ✅ ref 20 |
| **Render passes / AOVs** | ❌ 1 mention — thin |

## 11. COMPOSITING, GRADING, EDIT, SOUND
| Skill | Status |
|---|---|
| Compositing (pass recombination, glare, fixes) | ✅ **ref 37** — multipass EXR, alpha/premultiplied, pass assembly, LUTs/scopes, motion vectors, Cryptomatte |
| Color grading (final look) | ⚠️ via script-template Part 5; Blender-side thin |
| Editing craft & rhythm | ✅ theory (Walter Murch); VSE practice ⚠️ |
| Sound design awareness | ⚠️ planning level (template Part 8) |

## 12. PRODUCTION & STUDIO OPERATING SYSTEM
| Skill | Status |
|---|---|
| Per-request pipeline design + style cards | ✅ ref 22 |
| Self-critique gates, tolerances, Lessons Ledger | ✅ ref 19 |
| Scripting/automation (bpy) | ✅ 11 §G |
| Add-on judgment & tool intelligence | ✅ refs 21, 26 |
| Intake/briefing discipline | ✅ ref 25 |

---

## ❌ THE GAP LIST (priority order for YOUR current path)

1. ~~**Topology & retopology**~~ — ✅ **CLOSED 2026-10-22 by ref 27** (mesh & topology
   readiness gate; Vaughan + O'Hailey, text-verified).
2. ~~**Modeling, sculpting & anatomy**~~ — ✅ **CLOSED 2026-10-22 by ref 35** (Zarins +
   Hogarth plates, anatomy-to-topology pipeline, sculpt workflow, retopo hand-off).
3. ~~**Hair**~~ — ✅ **CLOSED 2026-10-22 by ref 34** (grooming + hair-card/chain craft;
   Ava's braided look covered).
4. ~~**Simulation technique**~~ — ✅ **CLOSED 2026-10-22 by ref 36** (cloth/sim decision
   framework, soft body/hair sim, rigid body, Mantaflow workflow-level).
5. ~~**Geometry Nodes**~~ — ✅ **CLOSED 2026-10-22 by ref 32** (646-node census,
   5 reusable groups, 2 verbatim production recipes).
6. ~~**Compositing, passes & grading**~~ — ✅ **CLOSED 2026-10-22 by ref 37** (multipass EXR,
   alpha/premultiplied, LUTs/scopes, motion vectors, Cryptomatte).
7. ~~**Storyboarding workflow**~~ — ✅ **CLOSED 2026-10-22 by ref 38** (Glebas beats, Block
   visual structure, board-to-animatic in Blender VSE).

**All studio-map gaps now closed.** The skill is complete across the core studio
disciplines: modeling/sculpting/anatomy (ref 35), simulation (ref 36), compositing/passes/
grading (ref 37), and storyboarding (ref 38) join topology (27), skinning (28), Geometry
Nodes (32), cloth (33), and hair (34).

Deep fluid-simulation parameter reference (Mantaflow specifics) remains the one flagged
honest gap — add a fluid-sim book to the library when that depth is needed.
