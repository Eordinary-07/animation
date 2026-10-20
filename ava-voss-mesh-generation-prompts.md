# AVA Voss — Mesh Generation Prompts (Body · Hand · Ponytail)
### Separate parts, designed to join with NO gaps

**The no-gap secret (read first):** never butt two flat ends exactly together —
that always shows a crack. Instead: **overlap** (push one part 2–3 cm *inside*
the other; the seam hides inside the mesh) and put a **cover** over every seam
line (wrist-wrap cuff at the wrist, hair-tie ring at the ponytail root). All
three prompts below are engineered for this. Same words for proportions, clay
material, background and lighting are repeated in every prompt on purpose — that
sameness is what makes the parts match.

**Workflow:** generate the IMAGE with each prompt → check the image (5 clean
fingers? clean wrist cut?) → regenerate the *image* until correct (cheap) →
feed image to Tripo → assemble in Blender using the coordinate card at the end.

---

## PROMPT 1 — BODY ONLY (no hands, no ponytail)

```
Ava Voss, athletic adult woman, 170 cm tall, full body head to toe, standing in
a neutral A-pose: arms angled about 40 degrees away from the body with a clear
gap between arms and torso, legs shoulder-width apart, feet flat and pointing
forward. IMPORTANT: the arms END at the wrists — there are NO hands and NO
fingers; each arm finishes in a smooth flat circular cross-section cap at the
wrist, like an artist mannequin with its detachable hands removed. Hair is
slicked back tight and smooth against the skull like a swim cap, gathered at
the back of the head, NO ponytail, NO loose hair. Fitted athletic training top
and fitted training pants tight to the body, no loose cloth, no flowing fabric,
simple smooth feet with no shoe details. Neutral relaxed face, eyes open
looking forward, mouth closed. Realistic human proportions, athletic build,
perfectly symmetrical, one single continuous body mesh. Untextured plain matte
grey clay material, 3D sculpt render look, no color, no accessories, no props.
Single character centered, full body fully visible from head to toe, front
orthographic view, plain solid light-grey background, soft even studio
lighting, no harsh shadows.
```

## PROMPT 2 — ONE HAND (generate the RIGHT hand only — mirror it in Blender for the left)

```
Single right hand of an athletic adult woman, 170 cm tall, shown alone as a
separate detachable part, like an artist mannequin hand. The piece includes
the complete hand plus about 5 cm of wrist and lower forearm, ending in a
clean flat circular cross-section cut. Around the wrist is a simple smooth
cloth hand-wrap band (a boxer's wrist wrap) forming a short cuff that is
slightly wider than the wrist. The hand is open and relaxed, back of the hand
facing the camera, fingers pointing up, thumb on the left side, all five
fingers clearly separated with small visible gaps between them, natural slight
relaxed curl, short clean fingernails. Hand length is 18.5 cm from wrist
crease to middle fingertip, realistic feminine athletic proportions.
Untextured plain matte grey clay material, 3D sculpt render look, no color.
Single object centered, the whole hand and wrist stub fully visible, plain
solid light-grey background, soft even studio lighting, no harsh shadows.
```

## PROMPT 3 — PONYTAIL ONLY

```
Single women's ponytail hair piece shown alone as a separate detachable part,
for an athletic adult woman 170 cm tall, total length about 38 cm. At the top
it begins as a smooth rounded dome cap, like a half-sphere about 5 cm wide,
with a simple hair-tie band ring around its base — the dome is designed to sit
flush against the back of a head. From the dome, one thick smooth ponytail
flows straight down with a gentle natural curve, gradually tapering to a soft
pointed tip at the bottom. Sleek tight hair surface with subtle strand
grooves, no loose flying strands, no braid, no waves. Untextured plain matte
dark-grey clay material, 3D sculpt render look, no color. Single object
centered and fully visible from dome to tip, side profile view, plain solid
light-grey background, soft even studio lighting, no harsh shadows.
```

---

## 📐 ASSEMBLY COORDINATE CARD (Blender — origin at her feet, Z = up, meters)

**Step 0 — fix scales first (Tripo scale is random).** Resize each part to its
ruler size before placing anything: body = **1.70 m** tall · hand = **0.185 m**
(wrist crease → middle fingertip) · ponytail = **0.38 m** (dome top → tip).

**HANDS (each side):**
1. Move the hand so the center of its flat cut sits exactly on the center of
   the body's wrist cap, pointing along the forearm's direction.
2. Push the hand **0.025 m (2.5 cm) INTO the arm** along that direction — the
   stub disappears inside the forearm, the wrap cuff covers the seam circle
   outside. This overlap is why there can never be a gap.
3. Rotate around the forearm axis until the **palm faces the thigh** (inward)
   and the thumb points forward.
4. Sanity check in the 40° A-pose: wrist joint ≈ **Z 1.02–1.05 m**, **X ±0.53 m**
   from center; fingertips land around mid-thigh, **Z ≈ 0.83–0.87 m**.
5. Left hand = mirror of the right (select hand → Object → Mirror → X Global,
   cursor at world center). Mirroring guarantees both wrists identical size.

**PONYTAIL:**
1. Place the dome center on the back-of-head centerline at **Z ≈ 1.62 m**,
   about **0.095 m behind the head's center**.
2. Sink the dome **~0.01 m (1 cm) into the skull** so the hair-tie ring rests
   exactly on the scalp surface — the ring covers the seam circle.
3. Hang it straight down along the back; the tip should reach **Z ≈ 1.22–1.26 m**
   (mid-back). It gets its own 3+ bone chain when rigging (per the test script).

**EYES (added in Blender, per plan):** two spheres, diameter **0.024 m**,
centers at **Z ≈ 1.595 m**, **X ±0.0315 m**, sitting in the sockets — separate
objects so they can lead the head snap (test script S02) while lids (on the
face mesh) handle the S12 blink.

**Materials (same clay everywhere = joins read as one sculpt):** body + hands
**#8B8E93**, ponytail **#55575C**, roughness 0.65 (from the production script,
Part 5).

### ✅ No-gap checklist
☐ Every join OVERLAPS 2–3 cm (nothing is butt-joined flat-to-flat)
☐ Wrist-wrap cuff fully covers the wrist seam circle, both sides
☐ Hair-tie ring sits on the scalp, covering the ponytail seam circle
☐ Orbit 360° around each join at close zoom — no crack visible from any angle
☐ Ruler sizes verified (1.70 / 0.185 / 0.38 m) before judging proportions
☐ If Tripo still gives mitten hands: open choice ⑤ — finger checks in the
  test script adapt to a mitten curl; placement method stays identical
