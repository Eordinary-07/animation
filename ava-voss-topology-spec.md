# AVA Voss — Quad Topology Specification (per mesh)

> Tripo generates triangles. Triangles deform badly (pinching, candy-wrapper
> twists) and will make a good rig look broken. This spec is the **retopology
> target** for each mesh — clean quad flow built for exactly the moves in the
> 24-second fight test (deep crouch, sweep, spin, back kick, roll).

## Universal rules (every mesh)

1. **100% quads.** No triangles/n-gons except end caps hidden inside joins.
2. **3 loops at every bending joint** — one loop on the joint line, one loop on
   each side. This is THE rule that makes elbows/knees/knuckles bend cleanly.
3. **Edge flow follows anatomy + deformation** — loops wrap *around* limbs and
   muscles; lengthwise edges run along the limb so twists distribute.
4. **Poles (3- or 5-edge vertices) only where nothing bends** — never on a joint
   bend line, never in the middle of the cheek/lid/lip loops.
5. **Density follows danger** — most quads where skin stretches most: armpits,
   hip crease, elbows, knees, neck, fingers, face. Fewest on skull, back, shins.
6. **Perfect mirror symmetry** left/right (needed for mirrored weights & poses).
7. **Even quad size within a region** — no sudden jumps from tiny to huge quads.

## 1) BODY — target ≈ 18,000–22,000 quads (head to toe, gear fused, no hands)

| Region | Quads | Topology requirements |
|---|---|---|
| Head + face | ~4,000 | **Concentric loops around eyes** (≥3 rings, 16–20 verts around the eye opening — the lids live on this mesh and must blink in S12), **3 rings around mouth** (~28 verts), brow loops, nose-bridge flow down to nostril wings, jawline loop, simple ear form. Loops must *circle* the features, never cut across them. |
| Neck | (in head/torso) | **16 around**, 4–5 horizontal rings so the head-snap (S02) and look-back (S10) twist spreads over the whole neck, not one ring. |
| Torso | ~4,500 | Horizontal rings following ribs → waist → pelvis **~28–32 around**; a ring every ~4–5 cm down the spine so the 180° spin (S09) twists gradually. Chest loops flow over the pecs into the deltoids. Waistband of the shorts = one clean ring; each shorts hem = one clean ring at mid-thigh (crisp cloth/skin border). |
| Shoulders / armpits | (in torso/arms) | The #1 danger zone. Loops fan from chest over the deltoid cap; the armpit gets a clean Y-flow with its pole buried in the armpit crease. Must survive guard (S01), downward block (S04) and full punch reach (S05). |
| Arms (each) | ~1,200 | **Upper arm 16 around, forearm 14 around.** Lengthwise rings every ~4 cm (forearm twist/pronation in the lip-wipe S13). **Elbow: 3 loops** (crease loop on the inside). Deltoid = cap of loops over the shoulder ball. |
| Wrist ends | — | Arm terminates in a flat ring of **exactly 16 vertices**, ellipse 5.4 × 4.0 cm (the WRIST_JOINT spec). Cap the hole with a simple fan — it's hidden inside the hand stub. |
| Hips / pelvis | (in torso/legs) | **Diagonal loops following the hip crease** front, and a fold loop under each glute — these two lines decide whether the deep crouch (S07) and knee-to-chest (S08) fold or tear. |
| Legs (each) | ~2,500 | **Thigh 16–18 around, calf 14, ankle 12.** **Knee: 3 loops** + a quad island flowing around the kneecap. |
| Feet | ~400 ea | Loops over the instep, a loop at the ankle crease, and **a bend loop at the ball of the foot** (metatarsals) — the front-foot pivot (S03) and sweep pivot (S07) physically rotate there. Toes may stay one fused mass for the clay pass; keep a toe-tip loop. |

Quad size guide: face ≈ 5–8 mm around eyes/lips · body ≈ 2–3 cm · limbs ≈ 2 cm.

## 2) HAND — target ≈ 1,800–2,500 quads each (make RIGHT, mirror for left)

- **Wrist stub:** starts with a flat ring of **exactly 16 vertices** — same count,
  same 5.4 × 4.0 cm ellipse as the body's arm end, vertex order starting at the
  thumb-forward point. (Matching counts = you can even weld them later if you
  ever want one mesh.) 3 rings along the 5 cm stub so the wrist can bend.
- **Wrap cuff:** simple band around the stub — **16 around × 3 rings** (~50 quads),
  slightly larger radius than the wrist; can be part of the same mesh.
- **Palm/back:** lengthwise grid flowing into the fingers; a loop row across the
  knuckle line; thumb mound (thenar) gets its own loop fan for thumb opposition.
- **Fingers:** **8 around** each finger (thumb 8–10). **3 loops at every knuckle**
  (base, middle, tip joints; thumb has 2 joints + its base). Fingertip closes in
  a rounded cap (pole at the very tip is fine). Nail = small inset quad patch
  (3 × 4) on top of each fingertip, or leave as smooth form for clay.
- **Webbing** between fingers: clean diamond quads — no stretched triangles
  (this is where Tripo fails most; check it first).

## 3) PONYTAIL — target ≈ 600–900 quads

- **Tube body:** **12 vertices around**, rings down the 38 cm length — every
  ~1.5 cm near the root (it bends most there when swinging, S09), every ~2.5 cm
  toward the tip → about 20 rings total. At least **3 rings per future bone**
  (plan 4–5 bones).
- **Taper:** radius shrinks smoothly ring by ring to a soft point; tip closes
  with a small fan (hidden pole OK).
- **Dome cap:** hemisphere of concentric rings (like half a UV sphere,
  12 around × 5–6 rings, ~70 quads) flowing into the tube's first ring.
- **Hair-tie ring:** plain band **12 around × 2–3 rings** at the dome base.
- Keep it a smooth mass — strand grooves are texture/sculpt detail for later,
  NOT topology (modeled strands would fight the bone bending).

## 4) EYES (made in Blender) — ~500 quads each

UV spheres **32 segments × 16 rings**, ⌀ 0.024 m, poles pointing back into the
head. That's all the clay pass needs.

---

## Join-matching summary (why the parts will fit)

| Join | Body side | Part side | Rule |
|---|---|---|---|
| Wrist | flat ring, **16 verts**, 5.4 × 4.0 cm ellipse | flat ring, **16 verts**, same ellipse | same count + same size = perfect plug |
| Ponytail | smooth skull (no ring needed) | dome base ring, 12 verts, ⌀ 5 cm | dome sinks 1 cm into skull, tie ring covers seam |

## Total budget

Body ~20k + hands ~4.5k + ponytail ~0.8k + eyes ~1k ≈ **26k quads** —
light enough for real-time playback while animating, dense enough that every
deformation failure you see in the test is the *rig's* fault, not the mesh's.

## Getting there from Tripo
Tripo exports triangles → retopologize to this spec (Tripo's quad retopo if
your plan has it, otherwise Quad Remesher in Blender with the counts above,
then hand-fix the face loops and webbing). Do NOT use voxel remesh — it makes
even quads but with random flow that still deforms badly at joints.
