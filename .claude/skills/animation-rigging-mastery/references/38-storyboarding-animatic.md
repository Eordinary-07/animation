# 38 — Storyboarding & Animatic

> **Sources.**
> **Francis Glebas, *Directing the Story*** — **text-verified**: story beats, boarding process,
> anticipation, exaggeration, close-ups, "takes," delaying reveals, framing for the action.
> **Bruce Block, *The Visual Story*** — **text-verified**: visual structure — space, line,
> shape, tone, color, movement, rhythm as story elements.
> **Mateu Mestre, *Framed Ink*** — composition and framing for storyboards (visual reference
> for shot design; page numbers not quoted to avoid inventing citations from an art book).
> **Prerequisite:** the script/ref 09 script-to-screen must exist before boarding.

## 0. Why storyboarding is a discipline, not a sketch

A storyboard is not "rough drawings of the movie." It is a **blueprint for timing, camera,
and performance** — and a bad blueprint wastes weeks of animation. Glebas treats boarding as
the place where the story is actually solved: beats are broken, anticipation is designed,
reveals are delayed, and the camera is framed *before* a single frame is animated.

**The cost of skipping it:** you discover in animation that the beat doesn't work, the camera
angle reads wrong, or the timing is off — and you throw away animated work. Boarding is
cheap; re-animating is expensive.

## 1. The beat board — Glebas's method

Glebas breaks a scene into **beats** — the smallest units of story action. From his text
(p. 68, the wolf-and-pigs breakdown):

> *"Let's break down the story beats that we will need to show this action. First, we have
> to show the wolf eyeing the house of hay… We are not going to say it. We will show it."*

**The beat-board workflow:**

1. **Write the beats.** One line per beat: what happens, who wants what, what changes.
2. **Board each beat.** One panel per beat (or per camera change within a beat).
3. **Design the camera within the beat.** Close-up for the important action; long shot for
   context; tilt the frame to raise tension (Glebas: *"By keeping him in the shadows he is
   scarier. Just by tilting the image we have raised the tension level."*).
4. **Add anticipation.** *"Anticipation to an action tells the audience that something is
   about to happen."* Board the wind-up, not just the hit.
5. **Exaggerate.** *"If you are going to blow down a house, it is going to have to be a really
   big puff!"* Board the pushed pose, not the neutral one.
6. **Delay the reveal.** *"We delayed revealing what happened… If these actions were shown all
> in one shot, it wouldn't have been as funny."* Board the cutaway, the reaction, the
   delayed answer.

## 2. Boarding craft — panels, thumbnails, camera

From Glebas and Framed Ink (composition reference):

| Element | What it decides |
|---|---|
| **Panel size** | screen proportion (16:9, 2.39:1, 1:1 for social) |
| **Thumbnail** | the first, fastest read of the composition |
| **Camera angle** | eye level, low (powerful), high (vulnerable), Dutch (off-balance) |
| **Shot scale** | extreme close-up, close-up, medium, wide, extreme wide |
| **Movement** | pan, tilt, track, dolly, zoom — arrowed on the board |
| **Cut points** | where one panel ends and the next begins |
| **Takes** | *"a take is an animation term designating a broad reaction usually to seeing something.
> The pose is usually held for a beat"* (Glebas p. 75) |

**Rule:** every panel must answer "what is the audience looking at, and why?" If you cannot
answer that, the panel is not finished.

## 3. Story beats & pacing

Beats are not shots. A beat can be one panel or ten panels. The pacing comes from:

- **Beat length** — how many panels per beat. Fast action = short beats; emotion = longer.
- **Cut rhythm** — Bruce Block's *rhythm* element: the pattern of long and short shots.
- **Visual contrast** — Block's structure elements (space, line, shape, tone, color, movement,
  rhythm) applied across the board so adjacent shots feel different when they should.

**Bruce Block — visual structure as story:** each element is a story tool:

| Element | Story use |
|---|---|
| **Space** | deep (epic, lonely) vs flat (claustrophobic, graphic) |
| **Line** | horizontal (calm), vertical (stable), diagonal (dynamic/tense) |
| **Shape** | round (friendly), angular (dangerous), square (stable) |
| **Tone** | light (comic, safe), dark (threatening, serious) |
| **Color** | warm (intimate, energetic), cool (distant, melancholy) |
| **Movement** | static (stately) vs kinetic (urgent) |
| **Rhythm** | fast cuts (panic) vs long holds (dread, awe) |

Board with intent: pick the elements that serve *this* beat's emotion.

## 4. From board to animatic

**The animatic** is the storyboard timed to sound (scratch dialogue, temp music, sfx). It is
the first version of the film that actually plays in time.

**Workflow:**
1. Import boards into Blender's **Video Sequence Editor (VSE)** or the **Animation** timeline
   as image strips.
2. Time each strip to the beat length (seconds, not frames, at this stage).
3. Add scratch audio — dialogue, temp score, sfx placeholders.
4. Play it back. Does the story work? Does the timing breathe? Cut boards, re-time, add
   hold panels where the audience needs a beat to process.
5. **Lock the animatic.** Once locked, it is the reference for layout, animation, and
   editorial. Changes after this point cost animation time.

**Blender:** VSE → `Add → Image/Sequence` → select board panels → strip length = beat
duration → `Add → Sound` → scratch audio → play (`Spacebar`).

## 5. The Gate — printable checklist

```
BEFORE BOARDING
[ ] Script or beat list exists (ref 09 script-to-screen)
[ ] Aspect ratio decided (16:9 / 2.39:1 / 1:1)
[ ] Visual tone decided (Block elements: space, line, tone, color, movement, rhythm)

BEAT BOARD
[ ] Every scene broken into beats (one line per beat: what happens, what changes)
[ ] One panel per beat minimum; more for camera changes within a beat
[ ] Anticipation boarded before every major action
[ ] Exaggerated poses boarded (not neutral poses)
[ ] Reveals delayed — cutaways and reactions boarded separately
[ ] Every panel answers: what is the audience looking at, and why?

CAMERA & COMPOSITION
[ ] Camera angle chosen per panel (eye level / low / high / Dutch)
[ ] Shot scale chosen (ECU / CU / medium / wide / XWS)
[ ] Movement arrows drawn where the camera or subject moves
[ ] Cut points marked between panels

TAKES & REACTIONS
[ ] Reaction shots boarded (takes held for a beat)
[ ] Close-ups on the important action (Glebas: "frame what is important")

ANIMATIC
[ ] Boards imported to VSE/timeline as image strips
[ ] Each strip timed to beat duration (seconds)
[ ] Scratch audio added (dialogue, temp music, sfx)
[ ] Played back end-to-end; story and timing work
[ ] Animatic locked — reference for layout and animation

VERIFY
[ ] Hide the drawings: does the beat order still tell the story?
[ ] Show to someone fresh: do they understand what happens without explanation?
```

## 6. Blender 5.x quick procedure index

| Task | Path |
|---|---|
| Import board panels | VSE → `Add → Image/Sequence` → select panels |
| Set strip duration | Select strip → `S` (scale) or Properties → strip length |
| Add scratch audio | VSE → `Add → Sound` |
| Play animatic | `Spacebar` in VSE or Animation timeline |
| Add camera move notes | Grease Pencil on board panels, or text strip in VSE |
| Mark cut points | Strip boundaries in VSE |
| Lock animatic | Freeze strip order/length; note as reference for layout |
| Send to layout | Animatic + camera notes → Layout artist → 3D blockout |

## 7. The rule

Board the story before you animate it. Beats, not pretty drawings. Anticipation, exaggeration,
delayed reveals — designed on paper where they cost nothing, not in 3D where they cost
everything. The animatic is the contract; everything after it is fulfillment.
