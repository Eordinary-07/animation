# 22 — Animation Styles & Per-Request Pipeline Design

> Two guarantees. **(1) Every request gets its own style card and its own freshly
> designed pipeline** — nothing generic is reused blindly. **(2) Every pipeline is
> explained back in plain words**, so using this skill teaches production, not just
> produces it. Style parameters scale the books' constants (refs 03–06, 16–17); pipeline
> design runs on ref 14's method with ref 19's gates.

## A. The style system (choose per request, lock in the brief)

Declare ONE preset (or derive a custom card, §A2) in the Pipeline Brief. The dials that
change: **frame density** (on 1s/2s/mixed), **squash ceiling**, **anticipation scale**,
**spacing snap** (how extreme ease contrasts get), **smears**, **physics obedience**,
**camera energy**, **surfacing finish** (refs 16–17 tier), **renderer/motion blur**.

| Preset | Frame density | Squash | Signature settings |
|---|---|---|---|
| **Feature Realistic** (film CG) | on 1s | ≤5% (flesh only) | True physics & timing; subtle overlap; full PBR law; Cycles; true motion blur; micro-movement over gesture |
| **Stylized Feature** (Pixar-class) | on 1s | ≤15% | Anticipation ×1.5; snappy spacing contrasts; caricatured silhouettes; longer moving holds; art-directed light |
| **TV / Streaming Cartoon** | mixed 1s–2s | ≤30% | Smears & multiples allowed; strong holds; physics negotiable for the gag; EEVEE Next viable; flatter surfacing |
| **Anime-influenced 3D** | limited (2s–3s, held) | pose-driven | Snap-then-hold; stepped accents kept (constant interp. hits); timing owns truth, not physics; graphic light |
| **Stop-Motion Feel** | on 2s | physical | Tiny per-frame pose jitter ("boiling"); motion blur OFF/minimal; practical light; micro-imperfections in surfacing (ref 17) |
| **Game Cutscene** | on 1s | ≤8% | Cleaned naturalism (mocap-adjacent + principles polish); gameplay-grammar camera; budgets hard (ref 20) |
| **Product / Brand** | on 1s | n/a | The object is the actor; ultra-smooth eases; macro surfacing hero tier (Substance, ref 21B); slow premium timing |
| **Motion Design / Explainer** | rhythm-locked | graphic | Shape language over anatomy; flat/stylized materials; cuts and moves on the beat grid (ref 18 §4) |

**§A1 Style-lock rules.** One style per production unless the *story* demands contrast
(dream, flashback, screen-within-screen). The card is recorded in the brief and
LESSONS.md; every gate (ref 19) includes a style-consistency check — a realistic shot
inside a cartoon piece fails Gate P even if beautifully made.

**§A2 Deriving a custom style (from any reference).** When the user names/shows a
reference (film, clip, stills, "like X but calmer"):
1. Extract the dials: frame density, exaggeration scale, timing contrast (holds vs
   snaps), pose language (silhouette strength), camera energy, surfacing finish,
   palette/light character.
2. Write a one-page **Style Card** (preset name, every dial value, 2–3 "we always…"
   and "we never…" rules — e.g. "we never smear; we always hold reactions 12+ frames").
3. **Prove it with a 2-second test** before production (Williams' test-first): one
   gesture, one material, one light. Adjust dials from evidence, not adjectives.
4. Name it and reuse it across the production's shots; log refinements as rules
   (ref 19 §4) so the style sharpens instead of drifting.

## B. Designing a fresh pipeline per request

**The stage menu** (include only what this request needs — ref 14 §F: *nothing is built
that the story doesn't need*):

| Stage | Purpose in one sentence | Skip when |
|---|---|---|
| 1. Intention (ref 18) | Know what the audience must feel before making anything | never |
| 2. Pipeline Brief (ref 14) | Turn intention into scope, budgets, and this plan | never |
| 3. Style test (§A2) | Prove the look/movement in 2 seconds instead of discovering problems at shot 40 | style already proven on this production |
| 4. Asset build (model) | Geometry the story needs at the quality the camera needs | assets exist/reused (ref 14 §D) |
| 5. Rig (ref 02) | Controls that make the required performances possible | static/product pieces |
| 6. Surfacing (refs 16–17, 21B) | Materials/textures that survive light and close-ups | previz-only deliverables |
| 7. Layout (Gate L) | Camera + staging: the film exists as readable stills | single locked product shot (merge into 8) |
| 8. Blocking (Gate B) | Story poses on beats, stepped — cheap to change, impossible to fake later | never for character work |
| 9. Spline (Gate S) | Weight, arcs, mechanics between the poses | limited-animation styles keep stepped accents intentionally |
| 10. Polish (Gate P) | Face, overlap, texture of motion — where "professional" is decided | never (scope it, don't skip it) |
| 11. Lighting/lookdev (ref 16 §6) | Light that serves intention and proves materials | lighting locked by style test (then verify only) |
| 12. FX / simulation | Fire, water, cloth, crowds — baked before render (ref 20) | no FX in story |
| 13. Render (refs 10, 20) | Frames at the shot's budget, passes for control | playblast deliverables |
| 14. Comp / delivery | Final image assembly + formats | in-engine finals |
| 15. Review & ledger (ref 19) | Battery, fixes, lessons recorded — the learning stage | never |

**Design rules.** Work backwards from the deliverable and deadline. Solo production
merges stages but **keeps the gates**; team production adds hand-off artifacts (the
brief, style card, gate checklists ARE the hand-offs). Tools are chosen per stage
(Substance for stage 6 heroes; add-ons per ref 21 §A) and frozen in the brief.

## C. The Pipeline Explainer (always printed, always plain)

After every Pipeline Brief, output **"Your pipeline in simple words"**: one short
paragraph per included stage — *what happens, why it exists, what you (the user) will
see at that stage, and what decision is yours*. Example:

> **Blocking** — I'll pose only the important moments (like comic-book panels) with no
> smoothness yet. This is where the *acting* is decided, and it's cheap to change.
> You'll see a rough stepped video; your job is only to say whether the feeling is
> right — ignore the stiffness, that's fixed in the next stage.

This is non-negotiable: the user should understand production better after every
project. Jargon gets a 5-word translation the first time it appears. If the user asks
"why this stage?", answer from the stage menu's purpose column, not with authority.

## D. Mini worked example

Request: *"30-second product film for a steel watch, premium feel."*
→ Style: **Product/Brand** (object-as-actor; macro surfacing; slow eases).
→ Pipeline: intention (feeling: engineered calm) → brief → style test (one macro
rotating hero frame, brushed-steel anisotropy check) → model (CAD-clean) → surfacing
(Substance, measured steel F0, ref 21B) → layout (3 camera moves) → spline-only
animation (no character blocking needed — stage 8 skipped *with the reason stated*) →
lighting (strip-light studio, ref 16) → render budget: threshold 0.005, 4K macro
textures justified by screen coverage (ref 20) → comp → review/ledger.
→ Explainer printed in simple words under the brief. Same request next month =
**re-derived**, not copy-pasted — the intention may be "sporty energy" next time, and
the whole design follows that.

## E. Fresh-eyes tool check (part of every pipeline design)

Before locking a pipeline, spend one beat on the toolbox (ref 26): read the
project's `TOOLS.md`; if the user's Blender is newer than the skill baseline, run
the version delta-check for the areas this pipeline uses; nominate any challenger
that could beat a champion on *this* project's hardest capability (motion
smoothness, hero texturing, render budget) and either scorecard it or log it as
"unverified — trial plan". Pipeline tool assumptions change only on an ADOPT
verdict — novelty never silently enters a locked pipeline.
