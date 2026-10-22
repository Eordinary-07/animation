# 34 — Hair Grooming

> **Sources.**
> **William Vaughan, *Digital Modeling*** — p. 53 *hair fibers*, p. 63 *topology +
> communication*, p. 155–156 *texture displacement for hair details*, p. 157 *hair as soft-body
> dynamics*, index entry “head model, 213–237”.
> **Blender 5.2 LTS (docs.blender.org)** — *Braid Hair Curves*, *Attach Hair Curves to Surface*,
> hair system modifier, groom workflow.
> **Visual reference:** `studio-reference/hair/` — three braided-hair close-up plates
> (Ava's signature look; Next Gen style target).
> **Honest note:** there is no dedicated hair book in the repo's 34 PDFs, and Zarins is
> image-only for hair/scalp (0 text hits). Where a page number is given it is read from the
> book; where none is given the step comes from Blender 5.2 docs or from the craft convention.
> **Prerequisite:** ref 27 Mesh & Topology Readiness must PASS — hair sits on the head mesh,
> and a bad scalp topology ruins the groom no matter how good the curves are.

## 0. Why hair is its own chapter — and its own discipline

Vaughan p. 53, index entry “hair fibers,” lists hair under **effects**:

> *"An effects artist creates all the non-model elements in an animation. These include things
> like hair fibers; elemental effects like water, fire, and smoke; as well as fabric dynamics."*

And p. 63 places the modeler's responsibility:

> *"TDs and programmers will also have a say in a model's creation; they will be handling things
> like dynamic cloth, hair, muscles, liquids, fur, particles, and lighting."*

**The practical consequence:** hair touches three departments — modeling (the scalp mesh),
grooming (the curves/cards), and simulation (how it moves). A decision in one breaks the
others if they aren't aligned. This chapter covers the modeling + grooming side; simulation is
ref 33's cloth half and ref 44's hair-sim half (still open).

## 1. Choose the hair representation before you draw a single strand

There are three ways to put hair on a head, and the choice is a **production decision**, not
an aesthetic one:

| Representation | Best for | Cost | Blender reality |
|---|---|---|---|
| **Hair cards** | real-time / games / stylized film | cheap to render, author once, reuse | planes with hair texture + alpha |
| **Curves / strands** | hero close-ups, braids, Ava's look | expensive, per-strand control | Blender 5.2 Hair Curves system |
| **Simulated (soft body)** | hair that must react to motion | sim + cache per shot | Cloth/soft body on hair curves |

**The deciding question, same as cloth (§1 of ref 33):** does the hair have to *react* in this
shot? For a beauty shot or a held pose, strands or cards are better — art-directed, cheap,
predictable. Reach for simulation when hair swings in a run cycle, whips in a head turn, or
gets grabbed.

**Vaughan p. 157** classifies hair under dynamics:

> *"dynamics collectively refers to any physics-based simulations… soft deformable objects
> (soft body), like hair and cloth."*

That is the entire theoretical basis for simulated hair: treat it as soft body, not as a
separate magic system.

## 2. Ava's look — braids, from the reference plates

`studio-reference/hair/` holds three braided-hair close-ups. Ava's signature is a **braid
down the back of the head** — which, in Blender 5.2, is not "modeled hair"; it is **curves
with a hair system applied**, or a braid mesh with hair cards fanning from it.

**The trap to avoid:** do not model each braid strand as geometry. The braid is the *shape*;
the hair is the *detail on the shape*. Build the braid form once (mesh or curve), then attach
the groom to it.

**Blender 5.2 path (docs.blender.org):** `Add → Curve → Braid Hair Curves` generates a braided
curve primitive; `Attach Hair Curves to Surface` binds groom curves to a mesh surface so the
hair sticks to the scalp and follows it when the head deforms. Those two operators are the
start and the anchor of every groom in this skill.

## 3. The scalp mesh — topology first

ref 27's gate applies to the head *before* any groom touches it. Specifics for hair:

- **Edge loops around the hairline** (ref 27 §1.2 — rule of three: one segment deforms, two
  support). The forehead/temple boundary is a high-deformation zone; it needs the same loop
  discipline as an eye or mouth.
- **Poles on the crown** (ref 27 §1.5 — poles in low-deformation zones). The crown is
  relatively static in most poses; that is where a 5+ pole belongs, not at the hairline where
  the groom fans out.
- **No n-gons on the scalp** (ref 27 §1.6) — n-gons triangulate unpredictably under
  subdivision, and hair cards or curves seeded from a triangulated surface splay in random
  directions.
- **Watertight head mesh** (ref 27 §2) — the groom seeds from surface points; a hole in the
  scalp is a hole where hair can spawn inside the head.

**Blender:** the scalp is part of the hero head mesh. Apply all transforms (`Ctrl+A → All
Transforms`) before attaching hair, or the groom offsets from the mesh when you move the
character.

## 4. Groom workflow — guides, clumps, and the braid

The groom happens in **Particle Edit / Hair mode** (Blender 5.x). Working order:

1. **Block the shape with guides.** Draw a sparse set of guide curves that define the
   *direction and mass* of the hair — not individual strands. A braid needs maybe a dozen
   guides following the plait, not hundreds.
2. **Clump the guides.** Hair does not hang as single strands; it hangs in clumps. Blend
   neighboring guides so they separate into strands only at the tips.
3. **Add children / interpolation.** Let Blender generate the dense strand count from the
   sparse guides. Children multiply; guides direct.
4. **Attach to surface.** `Attach Hair Curves to Surface` locks the groom to the scalp mesh so
   it deforms with the head (and so you do not get hairs floating above the forehead when the
   character turns).
5. **Comb and length.** Shape with the comb tools; set length per guide group, not globally —
   bangs shorter than the back, shorter at the temples than at the crown.

**Why guides first:** a groom with 5,000 hand-placed strands is uneditable. A groom with 60
guides and generated children is revised by moving 60 curves. This is the same “build once,
instance many” discipline as ref 32's Geometry Nodes groups.

## 5. Hair cards vs strands — when to switch

| Situation | Use | Why |
|---|---|---|
| Background characters | hair cards | 1–2 planes per clump, alpha texture, renders in EEVEE |
| Hero close-up (Ava's face) | strands | braids read as individual plaits at camera distance |
| Hair under a hat/helmet | cards or nothing | hidden detail wastes render time |
| Hair that moves in shot | simulated strands | cards cannot simulate; strands can (soft body) |
| Braid ends / flyaways | a few stray strands | adds life without full groom cost |

**Vaughan p. 155–156** describes the hybrid that sits between the two: **texture displacement
for hair details**:

> *"I recently used this technique to create details in a character's hair for the FunGoPlay
> virtual world. A procedural texture was used to displace a simple hair mesh, producing the
> hairstyle the art director was looking for and making light work of what could have been a
> more challenging task to model traditionally."*

And the production benefit:

> *"it allows animators to work with a low-resolution mesh when animating and then increase the
> object's polygon density before applying the displacement at render time."*

**Translation:** for hair, model the low-res shape, displace the detail at render. The base
mesh stays light for animation; the detail appears only when it is needed.

## 6. Simulated hair — soft body, same rules as cloth

If the hair must react, it is a soft-body sim (Vaughan p. 157). The constraints from ref 33
apply unchanged:

- **Pin group** — the roots pinned to the scalp; the rest free to swing.
- **Collision enabled** on the head/shoulders so hair does not pass through the body.
- **Quality steps** raised until hair stops tunneling through the shoulders (start 5–8).
- **Cache baked** before rendering; re-baked after any groom or geometry change.
- **Self-collision** only when hair folds onto itself (long hair in a braid).

**Blender:** the hair curves carry a **Cloth** physics modifier; pin via a vertex group
(painted on the scalp, blurred first via ref 32's `Blur Vertex Group` — the same
sculpt→sim bridge).

## 7. Groom-to-head integration checklist

```
BEFORE THE GROOM
[ ] ref 27 Gate passed on the head mesh (topology frozen)
[ ] Scalp edge loops around hairline and crown (rule of three)
[ ] Poles placed on the crown, never at the hairline
[ ] All Transforms applied (Ctrl+A) on head and any braid mesh
[ ] Hair representation chosen: cards / strands / simulated

GROOM
[ ] Guides block the shape first; density generated from guides
[ ] Hair clumps, not single strands
[ ] Attach Hair Curves to Surface used (groom locked to scalp)
[ ] Braid built as a form, groom attached to it (not modeled strand-by-strand)
[ ] Length varies by region (bangs < back < crown)

SIMULATION (only if hair reacts)
[ ] Pin group painted on scalp, blurred (Blur Vertex Group)
[ ] Collision on head and shoulders
[ ] Quality steps raised until no tunneling
[ ] Cache baked; re-bake rule posted at the rig file

VERIFY
[ ] Hide the groom: head reads correctly on its own
[ ] Turn the head 180°: no hairs floating inside or through the scalp
[ ] Braid holds its plait shape; flyaways read as intentional, not broken
[ ] Compare against studio-reference/hair/ plates
```

## 8. Blender 5.x quick procedure index — hair

| Task | Path |
|---|---|
| Create braided curve primitive | `Add → Curve → Braid Hair Curves` |
| Attach groom to scalp mesh | `Attach Hair Curves to Surface` (binds curves to surface) |
| Enter groom editing | Particle Edit mode → Hair |
| Add/position guides | Hair mode → draw guides along hair flow |
| Generate children from guides | Hair settings → Children → Interpolation |
| Pin hair roots to scalp | Vertex group painted on scalp → Cloth modifier → Pin Group |
| Blur a pin mask | ref 32 §3 `Blur Vertex Group` |
| Enable hair collision | Cloth modifier → Collision (on head/shoulders) |
| Bake hair cache | Physics → Cache → Bake |
| Hair cards (real-time) | Plane + hair alpha texture, plane per clump |
| Texture-displaced hair detail | Displace modifier with procedural texture (Vaughan p.155–156) |
| Apply transforms before groom | `Ctrl+A → All Transforms` on head + braid mesh |

## 9. The rule

Vaughan p. 53 and p. 63, read together: **hair is an effects element created by people who are
not the modeler, on a mesh the modeler built, for a rigger who has to make it deform.** The
groom does not start with curves. It starts with a scalp that passes the topology gate, with
departments agreed on representation (cards vs strands vs sim), and with the braid planned as
a form before a single strand is drawn.

Get the mesh right, get the representation right, and the hair follows. Get either wrong and
you will re-groom it every time the head turns.
