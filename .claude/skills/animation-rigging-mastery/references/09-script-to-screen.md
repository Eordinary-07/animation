# Script → Screen — Directing Pipeline for Professional Animation

Sources: Whitaker & Halas (Storyboard, Slugging, Bar Sheets, Responsibility of the
Director), Williams (Directing: The Brief, The Leica Reel, Separate the Characters,
Best Foot Forward, Voice Recording, Hook-Ups, Research, Editing, Believe in Your Material),
Thomas & Johnston (Story; Character Development; How to Get It on the Screen),
Hooks (Given Circumstances, Objective), Parent (Animation Production, Digital Editing).

This is the master workflow: turn a **script or instruction** into a **professional-level
animation** in Blender. Follow the stages IN ORDER. Skipping to keyframes is how amateur
work happens.

## Stage 0 — Understand the assignment

- What is the story in ONE sentence? (If you can't say it, you don't understand it yet.)
- Who is the character and what do they WANT in this moment? (Hooks: objective.)
- What should the audience FEEL? (Every technical choice serves this.)
- Constraints: runtime, style (realistic/cartoon), shot count, delivery format.

## Stage 1 — Script analysis (before any 3D)

1. Mark **beats** — units of action where the thought/tactic changes. Number them.
2. Mark **the acting points** — the moments the scene exists for (Williams).
3. Mark **given circumstances** (Hooks): where/when/who/what just happened/what's at stake.
4. For each beat write: objective + obstacle + tactic (the VERB: to beg, to threaten).
5. Note props/sets/characters needed (production design list).

## Stage 2 — Shot design (the camera decides the story)

1. For each beat choose the shot that presents the idea most clearly
   (see `08-camera-cinematography.md`): size, angle, lens, movement.
2. Write the **shot list / slug lines**:
   `SCENE 1 - SHOT 2 - CU (85mm, static) - Maya realizes the door is locked - beat 3`
3. Check the whole sequence as a cut: variety of sizes, 180° rule, escalation of closeness,
   hook-ups. Whitaker: the storyboard (or its digital equivalent) is where timing is FIRST
   decided — design the shots so their DURATION serves the timing.
4. Slugging (Whitaker): break the sequence into shots with planned durations in seconds.

## Stage 3 — Storyboard & animatic ("the Leica reel", Williams)

- Thumbnails per shot (stick figures fine): composition + pose + screen direction.
- Cut them in order (Blender VSE or any editor) with scratch/voice audio → **animatic**.
- The animatic locks: order, shot durations, pacing. Williams: make the movie HERE,
  cheaply. Reason: re-timing an animatic costs minutes; re-timing an animation costs days.
- Decide timing per shot NOW (Whitaker: timing begins on the storyboard).

## Stage 4 — Layout & blocking in Blender

1. Scene assembly: sets/props only where the camera sees (fast iteration).
2. Place **cameras per shot**, bind to timeline markers (`Ctrl+B`).
3. Block characters: "best foot forward" (Williams) — start each shot with the clearest
   pose of the idea. Poses at beats only, Stepped interpolation.
4. Check silhouettes in each camera at each beat (solid drawing + staging).
5. Playblast the sequence — it must read SILENT FIRST (Williams: if it needs the dialogue
   to make sense, the staging failed).

## Stage 5 — Animation (the craft layers, in order)

1. **Reference**: act it out (Williams: "Steal It!" from life). Note real timing.
2. **Blocking**: extreme poses at beats (pose-to-pose). Attitude + staging.
3. **Breakdowns**: define paths/arcs and the tactic transitions (`03/04`).
4. **Spline + offsets**: overlap, stagger, drag (`03-timing-spacing.md`).
5. **Body mechanics pass**: weight, contacts, arcs — verify with `04-body-mechanics.md`.
6. **Face + dialogue pass** (if speaking): `06-facial-lip-sync.md` — mouth timing, then
   eyes/brows thinking, then offsets.
7. **Polish pass**: dents, accents, imperfections, asymmetry, breathing micro-motion,
   camera feel (handheld noise, ease on moves).
8. **Overlap layers** (Williams "The Procedure", p. 338 — animate in THIS order): the
   primary thing, then the secondary thing, then the third, fourth, and only then the
   "other bits" — drapery, hair, fat, tails. And keep testing at every stage (Leica/animatic
   → thumbnails → keys → extremes → passing positions — shoot a playblast of each).

## Stage 6 — Review like a director

Playblast at speed with sound. Williams' Directing checklist + professional bar:

1. Does the story read SILENT? (staging test)
2. Does each beat land? Are acting points clear? (contrast test)
3. Is the timing right emotionally — not just correct physically?
4. Weight, arcs, overlap present? Nothing floaty/even? (`03`)
5. Characters acting vs moving? Objective visible in behavior? (`05`)
6. Face: eyes thinking, sync tight, no robot simultaneity? (`06`)
7. Camera: motivated, continuous, cuts on beats? (`08`)
8. Appeal: is it *watchable*? Would you watch it twice? (Illusion of Life: appeal)
9. Hook-ups between shots work? Screen direction consistent?
10. "Believe in your material" (Williams) — if a beat is weak, fix the idea, not the polish.

## Stage 7 — Delivery

- Final render settings (`10-blender-production.md`): 24fps (or 30/60 if required),
  resolution, codec (ProRes/H.264), audio mix with picture-synced sound.
- Export variants: full shot sequence + individual shots + a "playblast" version.
- Keep the .blend organized for future edits (Williams: "Making Changes" WILL happen).

## Working from an instruction (not a full script)

When the user gives a brief like "a robot picks up a ball and looks sad":

1. Write the one-sentence story + the character's objective.
2. Invent given circumstances and a beat list (usually 2-4 beats for a short piece).
3. Propose the shot design in one short paragraph (size/angle/lens) — confirm only if
   the brief is ambiguous; otherwise commit and deliver.
4. Run Stages 3-6 condensed (animatic optional for 1-shot pieces).
5. Deliver at professional polish: this means **staging clarity + weight/timing +
   acting read + appeal** — never just "the rig moved".

## Professional level — the definition we hold

- Every frame is a good composition; every pose is a clear idea.
- Motion has weight, arcs, overlap, deliberate spacing (no default interpolation).
- The character *acts*: objective drives behavior; contrast reads; faces think.
- Camera grammar is invisible (correct) and motivated.
- The piece reads silent, lands its beats, and has appeal.
- Polish: asymmetry, offsets, micro-drift in holds, impacts with accents — details that
  prove decisions were made.
