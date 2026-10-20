# AVA Voss — Mesh Prompts for CHATGPT WEB APP (Body · Hand · Ponytail)
### XML-tag format · one chat · parts engineered to join perfectly

## How to use (important — this is what makes the parts fit)

1. Open **one new ChatGPT chat** and paste **MESSAGE 0 (setup)** first. It teaches
   ChatGPT the shared engineering spec: exact wrist-joint ellipse, exact ponytail
   root, exact ruler lengths, locked style.
2. Then paste **PART 1**, check the image, then **PART 2**, check, then **PART 3** —
   all in the SAME chat, so ChatGPT keeps the same character and measurements.
3. If a part comes out wrong, don't start over — reply with a correction from the
   cheat-sheet at the bottom ("Regenerate PART 2. Exactly five separated
   fingers. Keep everything else identical.").
4. Download the 3 PNGs → Tripo (image-to-3D) → assemble in Blender with the
   coordinate card in `ava-voss-mesh-generation-prompts.md`.

**Why the tags?** ChatGPT follows `<tag>` blocks like labeled boxes — the shared
`<joint_interfaces>` block is the contract every part is built against: same
wrist ellipse (5.4 × 4.0 cm) on body AND hand, same 5 cm ponytail dome — that's
what makes them plug together in Blender with no gaps.

---

## MESSAGE 0 — SETUP (paste this FIRST)

```
<project>
You will generate THREE separate reference images of ONE character's body parts,
in this same chat, one at a time. The images will be converted to 3D meshes and
assembled together, so the parts MUST fit each other perfectly. Follow this
specification EXACTLY in every image. Do not improvise proportions, style or
measurements. Precision beats beauty.
</project>

<character_spec>
- Ava Voss, athletic adult woman, exact total height 170 cm
- Realistic human proportions, athletic build, perfectly symmetrical
- Neutral relaxed face, eyes open looking forward, mouth closed
</character_spec>

<joint_interfaces>
These connection points are IDENTICAL in every part. Never change them.
1. WRIST_JOINT: the arm-to-hand connection is a clean flat cut, perpendicular
   to the forearm. Cross-section = flat ellipse, 5.4 cm wide x 4.0 cm deep.
   The thumb side of the wrist always faces FORWARD (toward camera).
2. PONYTAIL_ROOT: a smooth rounded dome cap, diameter 5.0 cm, sitting on the
   centerline at the back of the head, 162 cm above the floor, 9.5 cm behind
   the head's center. A plain hair-tie ring (0.8 cm tall) wraps its base.
3. RULER LENGTHS: body = 170 cm tall. Hand = 18.5 cm (wrist crease to middle
   fingertip) plus a 5 cm wrist stub. Ponytail = 38 cm (dome top to tip).
</joint_interfaces>

<style_lock>
- Untextured plain matte GREY CLAY, 3D sculpt render look (like a ZBrush clay render)
- Body and hand: medium grey clay. Ponytail: slightly darker grey clay
- Background: plain solid light grey (#D9D9D9), nothing else in frame
- Lighting: soft even studio lighting, no harsh shadows, no dramatic light
- Camera: orthographic-style, dead level, no perspective distortion
- NO text, NO labels, NO watermark, NO color anywhere
- Object centered and FULLY visible, never cropped
</style_lock>

Reply "Ready" only. I will then ask for PART 1, PART 2 and PART 3, one at a time.
```

## PART 1 — BODY ONLY

```
Generate PART 1 of 3 now: BODY ONLY.

<subject>
Full body of the character in <character_spec>, head to toe, FRONT view,
standing in a neutral A-pose:
- Arms angled 40 degrees away from the torso, clear visible gap between arms and torso
- Legs shoulder-width apart, feet flat, toes pointing forward
</subject>

<critical_joint_rules>
- The arms END at the WRIST_JOINT from <joint_interfaces>: NO hands, NO fingers.
  Each arm finishes with the exact flat elliptical cut face (5.4 x 4.0 cm),
  thumb side facing forward — like an artist mannequin with detachable hands removed.
- Hair: slicked back tight and smooth against the skull like a swim cap.
  NO ponytail, NO loose hair. The ponytail is a separate part later.
</critical_joint_rules>

<clothing>
Fitted athletic training top and SHORT tight athletic shorts ending at
mid-thigh, both skin-tight and fused to the body, no loose or flowing fabric.
Legs bare from mid-thigh down. Simple smooth feet, no shoe details.
</clothing>

<render>
Front orthographic view, whole body visible head to toe. Apply <style_lock>
exactly. One image only.
</render>
```

## PART 2 — ONE RIGHT HAND (mirror it in Blender for the left)

```
Generate PART 2 of 3 now: ONE RIGHT HAND.
This hand belongs to the exact character in PART 1 — same clay, same proportions.

<subject>
A single RIGHT hand shown alone as a detachable part, BACK of the hand facing
camera, fingers pointing UP, thumb on the LEFT side:
- Open and relaxed, natural slight curl
- All FIVE fingers clearly separated, small visible gaps between them
- Short clean fingernails
</subject>

<critical_joint_rules>
- Below the hand, include a straight wrist/forearm STUB exactly 5 cm long.
- The stub ENDS in the exact flat elliptical cut face of WRIST_JOINT from
  <joint_interfaces> (5.4 x 4.0 cm) — the matching plug for the arm ends in PART 1.
- Around the wrist, add a smooth boxer's hand-wrap CUFF: a plain band 6 cm long,
  slightly wider than the wrist (about 6.5 cm across), same grey clay.
- Hand length: 18.5 cm from wrist crease to middle fingertip.
</critical_joint_rules>

<render>
Orthographic front view. Whole hand AND the full stub visible, nothing cropped.
Apply <style_lock> exactly. One image only.
</render>
```

## PART 3 — PONYTAIL ONLY

```
Generate PART 3 of 3 now: PONYTAIL ONLY.
It belongs to the exact character in PART 1 — same head size, darker grey clay.

<subject>
A single women's ponytail hair piece alone, SIDE profile view, hanging vertically:
- Total length 38 cm (would reach mid-back on the character)
- One thick smooth tail flowing straight down with a gentle natural curve
- Gradually tapers to a soft pointed tip
- Sleek tight surface with subtle strand grooves. NO braid, NO waves, NO loose strands
</subject>

<critical_joint_rules>
- The TOP is the exact PONYTAIL_ROOT from <joint_interfaces>: a smooth rounded
  dome cap, diameter 5.0 cm, like a half-sphere that sits flush against the
  back of a head.
- A plain hair-tie ring (0.8 cm tall) wraps the base of the dome where the tail exits.
</critical_joint_rules>

<render>
Orthographic side view. Entire piece from dome to tip visible, nothing cropped.
Apply <style_lock> exactly, ponytail clay slightly darker grey. One image only.
</render>
```

---

## 🔧 Correction cheat-sheet (reply in the same chat if a part is wrong)

| Problem in image | Reply exactly this |
|---|---|
| Body has hands/fingers | "Regenerate PART 1. Arms must END at the wrists with flat elliptical cut faces. Zero hands, zero fingers. Keep everything else identical." |
| Fingers merged/missing | "Regenerate PART 2. Exactly FIVE fingers, clearly separated with visible gaps. Keep everything else identical." |
| Hand wrong side | "Regenerate PART 2 as a RIGHT hand: back of hand to camera, thumb on the LEFT. Keep everything else identical." |
| Ponytail has no dome | "Regenerate PART 3. The top MUST be a smooth rounded dome cap, 5 cm diameter, with a hair-tie ring at its base. Keep everything else identical." |
| Style/color drifted | "Regenerate. Apply <style_lock> exactly: matte grey clay, plain #D9D9D9 background, even light, no color, no text." |
| Part cropped | "Regenerate with the ENTIRE part inside the frame, small margin on all sides, nothing cropped." |

## After Tripo — 60-second Blender join recap
Scale to rulers (body 1.70 m · hand 0.185 m · ponytail 0.38 m) → hand cut-center
onto wrist cap-center, push **2.5 cm inside** the arm (cuff hides the seam) →
mirror for left hand → ponytail dome center at **Z 1.62 m, 0.095 m behind head
center**, sink **1 cm** into skull (ring hides the seam). Full card:
`ava-voss-mesh-generation-prompts.md`.
