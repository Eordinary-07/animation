# Facial Animation & Lip Sync — Osipa, *Stop Staring*

Source: Jason Osipa, *Stop Staring: Facial Modeling and Animation Done Right* (2nd ed).
Sections: Basics of Lip Sync (ch. 1), Eyes and Brows (ch. 2), Landmarking (ch. 3),
Visemes & Technique (ch. 4), Mouth/Nose construction (ch. 5), Mouth Keys (ch. 6),
Eyes (ch. 7-9), Connecting Features (ch. 10), Skeletal Setup/Weighting/Rigging (ch. 11),
Interfaces (ch. 12), Squash/Stretch/Squoosh (ch. 13), A Shot in Production (ch. 14).

Core truth of the book: **the mouth speaks, but the eyes and brows think.** Lip sync gets
you noticed; eyes/brows get you believed.

## 1. The viseme set (Osipa's mouth shapes) — our shape-key targets

| Viseme | Sound(s) | Shape |
|---|---|---|
| **AI** | "ah", "eye", "cat" | jaw open, corners neutral-down, widest open vowel |
| **E** | "ee", "eh", "bit" | wide, corners pulled back, teeth close |
| **O** | "oh", "boat" | rounded, jaw mid-open |
| **U** | "oo", "boot", "you" | tight small round, pushed forward |
| **MBP** | "m", "b", "p" | lips pressed closed (rest face is fine) |
| **FV** | "f", "v" | lower lip under upper teeth |
| **L** | "l", "th", "n", "d", "t" | tongue up behind teeth; jaw slightly open |
| **W** | "w", "wh", "qu" | small round, corners in |
| **Q** | "q", "g", "k", "y" | slight open, back-of-mouth constriction (use with jaw) |

Rules: vowels carry the openness, consonants carry the *shape changes* (the read lives in
consonants — MBP closures and FV/L are what make speech legible).

## 2. Lip sync technique (ch. 1 + 4)

1. **Listen first**: understand the *words and the phrasing* — meaning before mouths.
2. **Rough pass**: pose the mouth shapes at the RIGHT TIME (timing of shapes > detail of
   shapes). Sync the closures (MBP) precisely; vowels can be approximate.
3. **Phrase it**: break the line into phrases; mouth goes to a neutral/rest between phrases
   (Osipa: the mouth doesn't stay in continuous motion — it *returns*).
4. **Accent with shape, not just timing**: the emphasized word gets a bigger shape.
5. **Simplify**: cartoon lines need FEWER shapes, bigger contrast; realistic lines need
   more, subtler transitions.
6. Jaw is a driver: jawOpen blends with every shape; never make a shape that can't sit on
   a moving jaw.

## 3. Eyes and brows (ch. 2, 7-9) — where the acting lives

- **Brows**: the strongest emotion signal. Sets: brow raise (inner = sadness/worry,
  outer = surprise), brow furrow (anger/concentration), brow cock (skepticism).
- **Eyes**: lids + focus + timing. The **squint** (lower lid up) is the secret of life —
  smiles are in the lower lids; anger is in the inner brows + lower lids.
- **Focus**: eyes look AT something specific; darts (saccades) between points; blinks at
  thought changes (and after eye darts).
- Blink rules: blinks are fast (2-4 frames close, 2-3 open); double-blink = confusion or
  innocence; NO blink = stare = intensity or dead.
- **Eye/brow keys** (ch. 9): build the standard sets as shape keys or bone poses:
  lids half/quarter/closed, brows up2/up1/flat/down1/down2, squint_L/R, wide_L/R.

## 4. Connecting the features (ch. 10) — the anti-robot chapter

- **Offset the parts**: brows move first, then eyes, then lids, then cheeks, then mouth
  (1-3 frame staggers). Simultaneous = robotic.
- **Dependencies**: smile raises cheeks → cheeks squint eyes slightly → brow softens.
  Wire these as drivers at low influence so emotion *propagates*.
- **Asymmetry**: one corner higher, one brow faster. Perfect symmetry reads as CG.
- Instant reads (Williams' "profiles for readability"): check the silhouette of the
  expression in profile and 3/4 — it must read instantly.

## 5. Rig & interface (ch. 11-12)

- Hybrid rig: shape keys for the surface, bones for jaw/eyes/head, drivers to connect.
  (Osipa's "skeletal setup, weighting and rigging" — his joint face = our bone option.)
- **Interfaces** (ch. 12): one clean animator panel: sliders grouped by region
  (phonemes / brows / eyes / emotion presets). Presets (happy/angry/sad/surprise) = macros
  driving groups of keys at partial values (Osipa: emotion shapes are COMBINATIONS).
- **Squash, stretch and squoosh** (ch. 13): global face squash/stretch sells extreme
  emotion and impact; "squoosh" = the soft redistribution of flesh (cheeks bulge when the
  jaw opens wide). Implement: face-scale bone or lattice + corrective keys.

## 6. A dialogue shot in production (ch. 14 + Williams' dialogue)

1. Audio first: transcribe, mark phonemes AND phrase accents on the timeline.
2. Body acts the scene (`05-acting-performance.md`) — the shot is acting, the lip sync is
   delivery.
3. Mouth pass: closures + vowels at right times (rough shapes).
4. Eyes/brows pass: thought changes, focus, blinks at phrase boundaries.
5. Connect: offsets, squints, cheek drivers; asymmetry.
6. Polish: accents on stressed words, settle jaw at phrase ends, final playblast WITH sound.

## 7. Blender implementation notes

- Shape keys: `vis_AI`, `vis_E`, `vis_O`, `vis_U`, `vis_MBP`, `vis_FV`, `vis_L`, `vis_W`,
  `vis_Q` + emotion keys + corrective keys. Drive with a "mouth controller" or audio
  markers; combine visemes by slider summing (drivers) since keys add linearly.
- Jaw: bone driven by `jawOpen`; shapes built on an open-jaw Basis so combinations work.
- Eyes: `Track To` constraints on eyeball bones toward a target empty (target moves = gaze);
  lids as bones or keys driven by `blink_L/R` and `lid_follow`.
- Audio sync: load sound in the Video Sequencer or as a channel; use timeline markers for
  phoneme accents; scrub at speed constantly.
