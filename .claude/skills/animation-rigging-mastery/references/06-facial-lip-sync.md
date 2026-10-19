# Facial Animation & Lip Sync — Osipa, *Stop Staring*

Source: Jason Osipa, *Stop Staring: Facial Modeling and Animation Done Right* (2nd ed).
Sections: Basics of Lip Sync (ch. 1), Eyes and Brows (ch. 2), Landmarking (ch. 3),
Visemes & Technique (ch. 4), Mouth/Nose construction (ch. 5), Mouth Keys (ch. 6),
Eyes (ch. 7-9), Connecting Features (ch. 10), Skeletal Setup/Weighting/Rigging (ch. 11),
Interfaces (ch. 12), Squash/Stretch/Squoosh (ch. 13), A Shot in Production (ch. 14).

Core truth of the book: **the mouth speaks, but the eyes and brows think.** Lip sync gets
you noticed; eyes/brows get you believed.

## 1. The visime set (Osipa Table 1.1) — our shape-key targets

Osipa's terms: *"Phonemes are sounds; visimes are shapes."* English has ~38 phonemes but
only **7 visimes to build** — everything else funnels to the closest shape. (Osipa spells it
"visime"; the industry also writes "viseme".)

| Visime | Example sounds | Rule / shape |
|---|---|---|
| **B, M, P / Closed** | murder, plantation, cherub | lips closed |
| **EE / Wide** | cheese, me, charity | mouth wide |
| **F, V** | fire, fight, Virginia | lower lip rolled in under upper teeth |
| **OO / Narrow** | dude, use, fool | mouth narrow |
| **IH** | trip, snip | sometimes taller or wider than surrounding shapes |
| **R** | car, road | sometimes narrower than surrounding shapes |
| **T, S** | beat, traffic | sometimes taller or wider than surrounding shapes |

**Open / jaw sounds** (UH, AW, "ah"…) are NOT separate visimes — they are the *jaw opening*
on its own; Osipa "kicked the jaw out of the visime club" so the set doesn't explode back
into phonemes. Funnel near-misses (OH → OO, L/TH → nearest) to the closest shape.

Rules: the read lives in the **lips-made consonants** — Closed (B/M/P) closures and F/V are
what make speech legible; vowels can be approximate. The classic traditional-animation
mouth chart (AI, E, O, U, MBP, FV, L, W, Q) is a valid alternative key set from the TV
animation tradition, but it is NOT Osipa's book — if you use it, use it consistently.

## 2. Lip sync technique (ch. 1 + 4)

1. **Listen first**: understand the *words and the phrasing* — meaning before mouths.
2. **Rough pass**: pose the mouth shapes at the RIGHT TIME (timing of shapes > detail of
   shapes). Sync the closures (B/M/P Closed) precisely; vowels can be approximate.
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
- **Eyes**: lids + focus + timing. The **Squint** (Osipa's name for the lower lids — really
  the whole orbicularis-oculi squeeze zone: upper cheeks, outer brow edges) is the great
  communicator: "The Value of a Good Squint" (ch. 2) is that it makes *think* read; smiles
  live in the lower lids; anger is inner brows + lower lids. Never treat cheeks as an
  independent emoting area — that's the leading cause of bad facial animation (Osipa).
- **Focus**: eyes look AT something specific; darts (saccades) between points; blinks at
  thought changes (and after eye darts).
- Blink rules (Osipa, ch. 7): blink **during big motions of the eyes**; stay away from
  *groups* of blinks for functional reasons — blink groups read as **disbelief, shock,
  confusion** (great for emotion, wrong for ordinary speech). Conversational subtext: a
  blink after a statement signals "your turn to talk"; no blink = no message = dead air.
  Blinks are fast (industry default ≈ 2-4 frames close, 2-3 open — tune to your frame rate).
  Eyes and lids animate on **linear** f-curves during motions and holds (Osipa's rule).
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

- Shape keys: `vis_BMP` (closed), `vis_EE` (wide), `vis_FV`, `vis_OO` (narrow), `vis_IH`,
  `vis_R`, `vis_TS`, `jaw_open` + emotion keys + corrective keys (Osipa's 7 visimes + jaw;
  or the classic traditional 9-chart AI/E/O/U/MBP/FV/L/W/Q — pick ONE set and stay
  consistent). Drive with a "mouth controller" or audio
  markers; combine visimes by slider summing (drivers) since keys add linearly.
- Jaw: bone driven by `jawOpen`; shapes built on an open-jaw Basis so combinations work.
- Eyes: `Track To` constraints on eyeball bones toward a target empty (target moves = gaze);
  lids as bones or keys driven by `blink_L/R` and `lid_follow`.
- Audio sync: load sound in the Video Sequencer or as a channel; use timeline markers for
  phoneme accents; scrub at speed constantly.
