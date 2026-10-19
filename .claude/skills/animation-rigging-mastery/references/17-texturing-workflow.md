# 17 — Texturing Workflow (the story on the surface)

Shading law lives in ref 16; click-level procedures in `11-blender-how-to.md` §H. This
file follows Owen Demers' *Digital Texturing and Painting* — its 15 chapters (verified
contents: `images/surf-01-demers-contents.jpg`) are still the industry workflow:
**see → dissect → decide → prepare → execute case by case → wrap up by re-examining.**

## 1. Owen Demers' method (do this before opening the Shader Editor)

- **Ch. 1 The Fine Art of Seeing and Dissecting.** For any surface ask: *What is it made
  of? What is its history and wear? Where is the light, and where can't you see?* Take
  the object apart visually into layers (substrate → coating → dirt → damage) — those
  layers become your node/map stack, in that order.
- **Ch. 2 Reference Materials.** Build a reference set *per material* (photos of the real
  thing at several distances and lights). Texture from memory = texture from clichés.
- **Ch. 5 Making Decisions — ask the right questions first**: What production materials
  are available? How close does the camera get (*at the time of the shot*)? What does
  the director want read? Which style (realism level) is the target? The answers set
  resolution, map list and effort *before* a single pixel is painted. (= the Pipeline
  Brief's surfacing scope, ref 14.)
- **Ch. 6 The Project: Technical Preparation** — mapping concepts decided up front:
  projection/UV strategy per asset class, which maps exist, naming, tileability needs.

## 2. UVs — the invisible foundation

- **Seams where the eye never goes**: garment seams, under jaw/arms, backs of props,
  inside creases. Every seam is a future paint problem; spend them like money.
- **Consistent texel density** (the PBR Guide treats "Resolution and Texel Density" in
  both workflows): one px-per-meter standard per production, checked with a checker
  texture. A face may *deliberately* get 2×. Mismatched density = sharp part, blurry
  neighbor = instant amateur tell.
- **UDIM tiles** for heroes that outgrow one 4K (face gets its own tile). Padding ≥16 px
  so mipmaps never bleed across islands. Straighten islands for manufactured things.

## 3. The PBR map set — what each map is FOR (metal/roughness workflow)

| Map | Job | Rules (values law in ref 16) |
|---|---|---|
| **Base Color** | Reflected color only | No AO/shadow baked in; 30–240 sRGB band; metals carry measured F0 tint here |
| **Metallic** | Metal yes/no per texel | Binary; rust/paint/dirt = 0 even on steel |
| **Roughness** | Microsurface variation | The hero map: fingerprints, smudges, polish on touch points, dust on up-faces |
| **Normal** (tangent) | Faked relief (pores, scratches, seams) | Blender = OpenGL (+Y); flip green for DirectX sources; Non-Color; strength ≈ 1 |
| **Height/Bump** | Micro-relief in shading only | Pair under normals (bump = grain, normal = sculpt) |
| **Displacement** | Real silhouette change (Owen Demers' Tire, ch. 9) | Needs subdivision density; mid-grey = 0; budget to close-ups |
| **Ambient Occlusion** | Micro-occlusion (PBR Guide: "maps common to both workflows") | Cycles computes real AO — baked AO is for pore detail & games; multiply subtly |
| **Curvature/Cavity** | Wear masks | Edges → chips & polish; cavities → dirt (bake, or live Pointiness) |
| **Thickness** | SSS/transmission control | Ears, fingers, leaves transmit more |

## 4. Baking (high-poly → low-poly) — principles, procedure in 11 H5

Cage/extrusion must fully enclose the high-poly or rays miss and bake black; margin
guards seams; bake **normals first** and inspect before anything else; wavy straight
lines mean low-poly shading is fighting the bake (add support loops / align hard edges
to UV seams). Never "fix it in the paint" — the next rebake resurrects it.

## 5. Procedural texturing (Ebert et al. → Blender nodes)

- **Texture spaces first** (Ebert ch. "Procedural Pattern Generation"; Owen Demers ch. 11,
  `images/surf-09-demers-procedural-goggles.jpg`): Owen Demers splits procedurals into
  **2D** — "defined by the object's textural coordinates (UVs)… cloth, fractals, and
  checkered patterns" — and **3D** — "a 'world' filled with a particular texture. They
  ignore the UVs of the object… granite, wood, leather, or cloud." In Blender: UV-space
  nodes for placed detail; Object/Generated space for volume-true materials (stone,
  rust creep — no seams, correct through cuts); box projection to skip UVs on rough
  props. And his combination law, verbatim: *"Using them verbatim… can result in an
  incomplete or unnatural textural expression. In combination with one another though,
  they can create some very realistic results."*
- **Layering and composition** is the whole game: substrate → variation → wear → dirt,
  each layer masked, exactly like Owen Demers' layered-shader dirt (his Goggles, ch. 11).
  One Noise node at one scale always reads "procedural" — stack **large / medium /
  micro** detail frequencies.
- **The noise families are the book's own chapters** ("Making Noises"): gradient noise
  (Perlin → Blender *Noise Texture*), cellular noise (Worley → *Voronoi Texture*),
  value noise, sparse convolution. Pick by structure: Voronoi = cells/cracks/scales,
  gradient noise = mottling/grime, stretched noise = brushed metal & rain streaks.
- **Aliasing** (Ebert's chapter of warnings): detail finer than a pixel shimmers —
  respect texture filtering/mipmaps, keep micro-contrast modest, check at final distance.
- **Geometry-driven masks**: Pointiness (edge wear), baked AO (crevice grime),
  world-normal Z (dust on up-faces). Gravity is an input: streaks run DOWN.

## 6. Owen Demers' case studies → production patterns

| Owen Demers chapter | The reusable pattern |
|---|---|
| Bandana (ch. 7) + Steel Braided Hoses (ch. 8) | **Tileable textures**: make it tillable, mask/render to hide the repeat, verify at 3×3 tiling |
| The Tire (ch. 9) | **Displacement for real relief** (treads): geometry-level detail only where silhouette shows it |
| Axle's Face (ch. 10) | **Character face on polygons**: prepare the mesh for texturing, create the color map from photo reference, fixed maps — and see his Final Maps audit below |
| The Goggles (ch. 11) | **Procedural + layered dirt**: shader layers with masks instead of giant painted maps |
| The Car Body (ch. 12) | **Complexity management**: many materials, one asset — plan map budget & shared trims |
| The Fin (ch. 13) | **Uneven surfaces + decals**: projecting logos/graphics onto curved forms without swimming |
| Aala's Chest (ch. 14) | **Sculpt → paint → project**: displacement sculpting feeding the texture, camera projections for cleanup |

## 7. Wear logic — four questions every texture answers

**What is it made of? How was it made? How old / who touched it? What weather hit it?**
Edges and touch points polish (roughness DOWN); crevices collect dirt (darker, roughness
UP, never shiny); paint chips on exposed edges down through primer to substrate; rust
starts at damage and streaks down; dust sits on up-faces; sun bleaches sky-facing sides.
Skin: roughness zones (oily T-zone smoother), color zones (redder nose/ears), pores
following wrinkle direction. *Uniform wear = no wear* — equal damage everywhere reads
as noise, not history.

## 8. Tools layout (industry reality, Blender-anchored)

- **Substance 3D Painter** is the standard texture painter (its rulebook is *The PBR
  Guide*): author there if available → export OpenGL normals → in Blender set data maps
  Non-Color, judge under AgX. Blender's Texture Paint covers stylized work and masks.
- **Scans/photogrammetry** (Megascans etc.) still need art direction: unify color
  temperature, re-grade roughness to your lighting, break tiling. Raw scan ≠ placed asset.

## 9. Budgets (fix in the Pipeline Brief, ref 14)

Hero face: UDIM 4K × tiles (pores must survive the ECU — Hooks ch. 7) · hero prop: 4K ·
midground: 2K + procedural variation · background: 1K or fully procedural. The camera
always finds the one asset that broke the texel-density standard.

## 10. Amateur tells (diagnose like ref 13)

Flat 0.5 roughness · metallic 0.5 · black albedo · sRGB data maps · crunchy over-strong
normals · visible tiling · wood grain at door scale on a spoon · shiny crevices and
dusty undersides · AO painted into color · materials approved under one pretty HDRI ·
detail invisible at shot distance (wasted) or missing in the ECU (fatal).
