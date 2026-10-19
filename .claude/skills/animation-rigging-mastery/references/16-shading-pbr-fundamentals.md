# 16 — Shading & PBR Fundamentals (the physics law)

> **The surfacing canon** (6 books, all in this repo as PDFs): *The PBR Guide* — Wes
> Wes McDermott (Allegorithmic/Adobe; the metal/roughness rulebook — text-verified) ·
> *Digital Texturing and Painting* — Owen Demers (observation-based surface craft; contents
> verified, see `images/surf-01/02`) · *Digital Lighting & Rendering* — Jeremy Birn
> (1st-edition scan; ch. 9 "Materials and Rendering Algorithms") · *Physically Based
> Rendering* 4th ed. — Matt Pharr, Wenzel Jakob, Greg Humphreys (ch. 9 BSDFs, ch. 10 Textures and
> Materials — text-verified) · *Texturing and Modeling: A Procedural Approach* 3rd ed. —
> Ebert, F. Kenton Musgrave, Darwyn Peachey, Ken Perlin, Worley (noise/procedural theory —
> text-verified) · *Color and Light* — James Gurney (observed light on real materials;
> contents verified). Numbers quoted below are taken from the books' own text/charts;
> evidence pages are catalogued in `15-verified-page-images.md`.

## 1. Shading vs texturing — who does what

- **Shading** = the material *recipe*: how a surface answers light (metal or dielectric?
  rough or polished? does light scatter inside it?). In Blender: Principled BSDF settings.
  The rules are few, physical and absolute — learn them first.
- **Texturing** = maps that *vary the recipe across the surface* (ref 17). A flawless
  recipe left flat still looks CG; beautiful maps on a law-breaking recipe look wrong in
  a way nobody can name. Order of work: **shading law → textures → lighting to prove both.**

## 2. How light behaves (PBR Guide Part 1; PBRT ch. 9)

1. **Diffuse vs specular.** Light bounces off the surface (specular) or enters, scatters
   and re-emerges tinted (diffuse). **Metals have no diffuse** — their color lives
   entirely in the tinted reflection (gold looks gold because it absorbs blue light).
2. **Microfacet theory.** Surfaces are microscopic mirrors; *roughness* is how randomly
   they're angled. Low roughness → sharp bright highlights; high → wide dim sheen.
3. **Energy conservation.** Reflected + absorbed never exceeds what arrived — blurrier
   highlights are automatically dimmer. If a material glows brighter than its light
   source, a value is illegal somewhere.
4. **Fresnel.** Everything approaches a mirror at grazing angles. What differs is **F0**,
   the head-on reflectance — the single most important number in this file.
5. **Absorption & scattering.** Inside translucent matter (skin, wax, milk) light travels
   and changes color before exiting = subsurface scattering. No SSS → plastic people.

## 3. The verified numbers (The PBR Guide, quoted from the book)

- **Dielectric F0 = 0.02–0.05 linear (2–5%)**. The metal/roughness workflow *hardcodes
  dielectric F0 to 4%* (0.04 linear = 59 sRGB) — that is exactly what Blender's
  Principled BSDF assumes at Specular IOR Level 0.5. Chart: `images/surf-05-pbr-f0-range-chart.jpg`.
- **Conductors (metals): F0 = 0.5–1.0, and tinted.** Metal color comes from real-world
  *measured* reflectance values, "around 70–100%" brightness. Use measured F0 (linear):
  gold (1.00, 0.71, 0.29) · copper (0.95, 0.64, 0.54) · aluminium (0.91, 0.92, 0.92) ·
  silver (0.97, 0.96, 0.91) · iron (0.56, 0.57, 0.58) · titanium (0.54, 0.53, 0.51).
- **Base color brightness law**: *"For dark values, you should not go under 30–50 sRGB…
  For bright colors, you should not have any values that are higher than 240 sRGB."*
  Coal is the darkest reference and fresh white snow the brightest — and *"objects tend
  to be much lighter in tone than we remember them as being."*
- **Base color carries no lighting**: it "should be devoid of lighting information such
  as ambient occlusion" (a micro-occlusion exception exists, still governed by the
  brightness range). AO painted into color = double-shaded, muddy renders.
- **Corrosion/dirt on metal is a dielectric layer** (F0 4%): in the metallic map rust is
  black (0) even on a steel object. Correct/incorrect reference:
  `images/surf-06-pbr-correct-incorrect.jpg`.

## 4. Principled BSDF decoded (Blender 4.x socket names)

| Input | The law | Amateur tell |
|---|---|---|
| **Base Color** | Dielectric: albedo in the 30–240 sRGB band, no baked light. Metal: the measured F0 tint above | Pure black/white albedo; grey "metal" |
| **Metallic** | **0 or 1 — nothing between** (transitions live only inside a map: rust over steel) | 0.5 "semi-metal" sludge |
| **Roughness** | The realism channel: real range ≈ 0.05–0.95 and it must *vary* (fingerprints, polish, dust) | One flat value for a whole asset |
| **Specular IOR Level** | 0.5 default = F0 0.04 — correct for nearly all dielectrics; touch only for gemstones/water films | Cranked to fake "shininess" |
| **IOR** | Water 1.33 · skin ≈ 1.4 · glass 1.5 · diamond 2.42 | Glass left on defaults |
| **Subsurface Weight / Radius** | Skin, wax, milk, marble, leaves. Radius = RGB travel distance (skin: red ≫ blue). **Demands real-world scale** | SSS on a character modeled 100 units tall |
| **Sheen Weight** | Cloth/velvet retro-reflective rim | Hard CG fabric edges |
| **Coat Weight / Roughness** | Clear second layer: car paint, varnish, lacquer; Coat 1 over a rough base = the "wet look" | Faking lacquer with low base roughness |
| **Transmission Weight** | Glass/water/ice — needs IOR + genuine thickness (solid mesh or Thickness) and samples | Alpha-blend "glass" in final renders |
| **Anisotropy** | Brushed metal, satin, CDs (needs a Tangent) | — |
| **Emission** | Only true light sources (screens, bulbs, lava) | Emission used to brighten dim materials |

## 5. Linear-workflow commandments

1. **Color maps → sRGB. ALL data maps → Non-Color** (roughness, metallic, normal, bump,
   displacement, AO). The PBR Guide's "Linear Space Rendering" chapter exists because
   this one mistake quietly wrecks more materials than any other.
2. Judge under **AgX** (Blender 4.x default view transform) — it rolls highlights off
   like film. Never approve a material under Standard.
3. **Model at true scale (meters).** SSS radius, transmission, light falloff and depth
   of field all assume it.

## 6. Judging the result (Jeremy Birn + James Gurney)

- Jeremy Birn's discipline (*Lighting Workflow*, *Qualities of Light*): a material is only
  proven when it survives different lights. Test every hero material under **three**:
  neutral studio HDRI → hard sun → dim interior. If it only works in one, the *values*
  are wrong, not the light. (Lighting itself: refs 08/10; Jeremy Birn ch. 9 for shader models.)
- James Gurney's observation layer (*Sources of Light*, *Light and Form*, *Surfaces and
  Effects*): before texturing, name the light logic of the reference — where is the
  specular core, where does diffuse wrap, what does the grazing rim do? If you can't
  describe the real surface's light behavior in one sentence, you're not ready to shade it.

## 7. Six-point realism check (every material, before more detail)

1. Base color in the legal band, zero baked lighting? 2. Metallic strictly 0/1 (map
blends only for corrosion layers)? 3. Roughness *varies* with readable wear logic?
4. Fresnel intact (specular not killed to fake matte)? 5. True scale, SSS/transmission
sane at that scale? 6. Survives the 3-light test at the final camera distance?
Any "no" → fix the recipe before touching textures (Williams' test-first discipline,
applied to surfaces).
