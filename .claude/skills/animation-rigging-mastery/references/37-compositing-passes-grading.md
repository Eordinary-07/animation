# 37 — Compositing, Passes & Grading

> **Sources.**
> **Compositing Visual Effects (Essentials)** — **text-verified**: multipass compositing (diffuse,
> specular, occlusion, shadow, reflection passes), EXR file format, alpha and premultiplied
> alpha, keyers/despill, holdout mattes, garbage mattes, motion vectors / optical flow.
> **Color Correction Handbook, 2nd ed. (Alexis Van Hurkman)** — **text-verified**: grading,
> LUTs, waveform monitor, parade scope, vectorscope, ACES vs display-referred color,
> BT.709, color space for delivery.
> **Bruce Block, *The Visual Story*** — color and tone as elements of visual structure.
> **Prerequisites:** ref 10/14 (render setup), ref 33/34/36 (the renders being composited).

## 0. Why compositing is the "final 10%" that reads as studio

Compositing is where separate render passes become a single image. It is also where a shot
either looks like a render or looks like a film. The studio difference is in the passes:
rendering one beauty pass and calling it done is amateur; rendering AOVs and reassembling
them with control is studio.

**Compositing Visual Effects (Essentials)**, on multipass:

> *"Multipass Compositing… Diffuse and Specular Passes… Occlusion and Shadow Passes…
> Reflection Pass…"*

Each pass is a separate layer you control in comp — you can darken the shadows without
touching the diffuse, boost the specular on the eyes only, grade the reflection pass
separately. That control is the whole point.

## 1. The multipass render — what to output

Render to **EXR** (OpenEXR) — floating-point, multi-layer, the production standard. The
compositing book lists EXR as the file format for CGI compositing.

**Minimum pass set for every shot:**

| Pass | What it gives you in comp |
|---|---|
| **Combined / Beauty** | the full image, for reference and quick comps |
| **Diffuse** | base surface color, no lighting |
| **Specular** | highlights — control their intensity separately |
| **Shadow / Occlusion** | darken contact areas without affecting color |
| **Reflection** | reflectivity, graded independently |
| **Z / Depth** | depth-of-field, fog, atmospheric falloff |
| **Normal** | relighting, fake highlights in comp |
| **Motion Vector** | motion blur, speed changes, optical flow |
| **Cryptomatte / ID matte** | per-object or per-material selection for regrading |
| **Alpha** | the matte that separates foreground from background |

**Alpha rule (verbatim principle from the compositing book):** know whether your alpha is
**straight** or **premultiplied**. Premultiplied alpha has the background color baked into the
edges; straight alpha does not. Mixing them in comp creates dark or light halos around edges.
Blender's default — check it, match it across all passes, and never assume.

## 2. Pass assembly — rebuilding the beauty in comp

**Compositing Visual Effects (Essentials)**, the core moves:

- **Scaling the background** — match the CG element to the plate.
- **Summing the layers** — diffuse + specular + reflection + shadow = beauty, but with each
  layer controllable.
- **Holdout mattes** — hold out (mask) parts of a layer so they don't double up.
- **Garbage mattes** — rough masks to hide problem areas; *garbage in the matte is fine,
  garbage in the key is not* (the book's emphasis: keyers need clean edges, garbage mattes
  can be rough).

**Blender Compositor:** Use the **Compositor** workspace (`Ctrl+Left` / workspace tab).
Nodes: `Render Layers` → separate the passes → `Mix`, `Add`, `Multiply`, `Color Balance`,
`Hue/Sat/Value` → `Composite` viewer → output.

**The stack order that works:** diffuse first, then specular (screen or add), then reflection,
then shadow/occlusion (multiply), then grade the whole thing.

## 3. Color grading & correction

**Color Correction Handbook (Van Hurkman)** — the professional vocabulary:

- **Grading** is not "making it look cool." It is making every shot in a sequence match, then
  giving it the intended look.
- **LUTs (Look-Up Tables)** — convert one color space to another, or apply a look. A LUT is a
  starting point, not a finish.
- **Waveform monitor** — shows brightness (luma) across the frame. Use it to check exposure,
  not your eye.
- **Parade scope** — shows R, G, B channels side by side. Use it to check color balance.
- **Vectorscope** — shows hue and saturation. Use it to check skin tones and saturation
  levels.

**Color space rules (Van Hurkman, text-verified):**

> *"Televisions will be generally the BT.709 specification for color, and display gamma will
> be set to somewhere between 2.2 and 2.4."*

> *"In the case of web video, it is more likely that users have their computer displays set
> to use sRGB color, with a gamma of 2.2."*

**ACES vs display-referred (Van Hurkman):** at the time of writing, ACES is an important new
development but most workflows are still **display-referred** — color fidelity is judged by
what the image looks like on the display, not by an embedded scene profile. For Blender: set
**Color Management** view transform to match your delivery target (Filmic or AgX for Blender
5.x, sRGB for web, BT.709 for broadcast), and grade on a calibrated display.

**Bruce Block, *The Visual Story*:** color, tone, and contrast are **visual structure
elements** — they carry story information, not just prettiness. A warm grade reads
differently from a cold grade. Grade for the scene's emotional intent, not just for "nice."

## 4. Motion vectors & speed changes

**Compositing Visual Effects (Essentials)**, on optical flow / motion vectors:

> *"Optical flow… the computer compares two adjacent frames, and then creates a list describing
> how small groups of pixels have moved from the first to the second frame."*

Motion vectors (a render pass) enable:
- **Motion blur** applied in comp (cheaper than re-rendering)
- **Speed changes / retiming** without the "strobey" look of simple frame blending
- **Optical flow interpolation** — synthesizing honest in-between frames for slow motion

**Blender:** the **Motion Vectors** pass + the **Speed Change** or **Vector Blur** node in the
Compositor. Render motion vectors with the scene; apply blur in comp.

## 5. Cryptomatte & selection

**Cryptomatte** gives you automatic per-object/per-material mattes without painting them by
hand. In comp, you click a pixel and get a clean matte for that object — regrade the character's
shirt without affecting anything else. This is the modern replacement for hand-painted holdout
mattes on complex shots.

**Honest status:** Cryptomatte support and deep compositing (multi-sample, voxel data) are
Blender-version dependent. Verify the version you render with supports the Cryptomatte pass
you need.

## 6. The Gate — printable checklist

```
RENDER SETUP
[ ] Every shot renders EXR multi-layer, not a single beauty PNG/JPEG
[ ] Minimum pass set: Combined, Diffuse, Specular, Shadow/Occlusion, Reflection,
    Z/Depth, Normal, Motion Vector, Alpha
[ ] Cryptomatte / ID matte enabled for shots with regrading needs
[ ] Alpha type confirmed (straight vs premultiplied) and consistent across passes

COMPOSITING
[ ] Beauty rebuilt in comp from passes, not just the Combined pass used raw
[ ] Specular and reflection controllable independently of diffuse
[ ] Shadow/occlusion layered with Multiply, not painted on
[ ] Holdout mattes used for overlap; garbage mattes rough but keys clean
[ ] Motion blur applied from Motion Vector pass, not re-rendered

GRADING
[ ] Waveform used to check exposure (not just the eye)
[ ] Parade used to check color balance across R/G/B
[ ] Vectorscope used for skin tones and saturation
[ ] LUT applied as starting point, not final look
[ ] Grade matches the shot's emotional intent (Block: color carries story)
[ ] Delivery color space set (sRGB web / BT.709 broadcast / ACES if pipeline uses it)

OUTPUT
[ ] View transform matches delivery target
[ ] Test frame rendered at final resolution before full comp
[ ] Cryptomatte pass verified (if used) — click-select produces clean matte
```

## 7. Blender 5.x quick procedure index

| Task | Path |
|---|---|
| Open Compositor | Workspace tab → Compositing (`Ctrl+Left`) |
| Enable use nodes | Compositor header → **Use Nodes** |
| Add Render Layers node | `Add → Input → Render Layers` |
| Separate a pass | Render Layers node → socket → `Mix`/`Add`/`Multiply` node → Composite |
| Diffuse + Specular | Diffuse → `Add` → Specular → Composite |
| Shadow layer | Shadow/Occlusion → `Multiply` factor → over beauty |
| Color grade | `Color Balance` → `Hue/Saturation/Value` → `Composite` |
| Motion blur from vectors | `Vector Blur` node, feed Motion Vectors pass |
| Speed change / retime | `Speed Change` node or Optical Flow with Motion Vectors |
| Cryptomatte matte | `Cryptomatte` node → pick pixel → matte output |
| Set color management | `Render Properties → Color Management` → View Transform / Look |
| Output EXR | `Output Properties → File Format: OpenEXR` → multi-layer |

## 8. The rule

Render in passes, composite with control, grade with scopes, deliver in the right color
space. The beauty pass is a reference, not the shot. The shot is what you build in the
Compositor — and what the audience actually sees.
