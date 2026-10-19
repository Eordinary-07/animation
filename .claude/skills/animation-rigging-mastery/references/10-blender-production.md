# Blender Production Practice — Scenes, Cuts, Render, Delivery

Practical conventions so the work in `02`-`09` is fast, organized, and deliverable.
Follow these on every project file.

## 1. Scene architecture

- One .blend per shot OR per sequence (shorts: per sequence; heavy scenes: per shot).
- Collections: `CHR` (characters), `SET`, `PROPS`, `CAMS`, `LIGHTS`, `WGT` (widgets),
  `REF` (reference empties/images), `RENDER` (hidden helpers).
- Naming: `CHR_name_rig`, `CAM_s010`, `SET_roomA`, actions `name_shot_action`.
  Prefix conventions from `02-rigging-blender.md` (ctrl_/def_/jnt_/wgt_) stay.
- Units: metric, 24 fps default (film/animation standard; 30 for broadcast NTSC if asked).
  1 unit = 1 meter; characters built to real-world scale (camera/lights/physics need it).

## 2. Cuts & cameras

- Timeline markers are the edit: `M` to add marker, rename it to the shot code
  (`s010`, `s020`…), select a camera → `Ctrl+B` binds it. Scrubbing plays the cut.
- Keep each camera's settings (lens/DOF) in the camera data — the lens choice IS shot
  design (`08-camera-cinematography.md`).
- Animate within shots in their own Actions (`shot_s010_walk`), combine in the **NLA**;
  retiming the edit = retiming NLA strips, not re-posing.

## 3. Reference & playblasts

- Import reference: Image empties (background images in cameras), or a reference plane;
  keep on a `REF` collection, never rendered.
- Playblast constantly: `View → Navigation → Fly/Walk` for camera feel tests; final
  playblasts via OpenGL render (`Render → OpenGL Render Image/Animation`, or
  `Ctrl+F12`), 24fps, with audio from the VSE.
- Scrub with sound ON for dialogue; check hook-ups across cuts in the VSE timeline.

## 4. The animatic in Blender

- Video Sequencer: add scene strips (each bound-camera scene) + audio + titles.
- Adjust strip lengths to lock pacing BEFORE the polish stages (Williams' Leica reel).
- The VSE timeline is the "bar sheet" (Whitaker): strip start/end = planned shot timing.

## 5. Lighting & rendering

- EEVEE: real-time lookdev + most final non-photoreal work; Cycles: refraction/true GI.
- Light for staging (principle #3): key light separates the subject; rim for silhouette;
  keep the darkest dark/lightest light on the acting point.
- Render settings: Filmic/AgX view transform for realistic punch; transparent film when
  compositing; 1920×1080 minimum, 24fps, motion blur ON for realism (shutter 0.5-1.0),
  OFF for crisp cartoon timing (or smear-frames instead).
- Output: FFMPEG → H.264 (MP4) for review, ProRes/MOV for final; **OpenEXR (multilayer)**
  image sequences for compositing (PNG only for quick stills).
- Compositor: subtle vignette/grain for "film feel" only if the style wants it.

## 6. Tooling habits

- Scripts in `tools/` in the repo (Python, bpy): batch playblasts, renames, marker binds,
  pose-library loaders. Keep them deterministic and documented in a comment header.
- Pose libraries: **Asset Browser pose assets** from a registered `POS_lib.blend` asset
  library (create/blend/flip workflow in `11-blender-how-to.md` B4); store every reusable
  golden pose and walk/run/emotion cycle there (`04-body-mechanics.md` recipes).
- Multi-shot work links characters and animates via **Library Overrides** — never animate
  in the source file (`11-blender-how-to.md` D4).
- Drivers/constraints named in English, one-liner expressions only (see `07`).
- Save incremental versions (`_v01`, `_v02`) before risky passes; Williams: "Making
  Changes" is part of the job.

## 7. Delivery checklist

1. All shots renderable from markers; cameras bound; no missing textures/linked data.
2. Frame rate/resolution/codec match the request.
3. Audio in sync; peaks normalized; no pop at head/tail.
4. Playblast of the FULL piece at speed, reviewed against
   `09-script-to-screen.md` Stage 6 checklist.
5. Files organized so a stranger could open the .blend and hit render.
