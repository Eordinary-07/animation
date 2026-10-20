# 26 — Tool Intelligence: Staying Current Without Chasing Hype

> **The books are the constitution; tools are applicants for citizenship.**
> This skill was authored in the Blender 5.2 era. Better tools for smoother motion
> and richer texturing exist that it doesn't name, and more will ship after it.
> The solution is not a longer tool list — it is this system: define quality by
> **measurable outcomes from the books**, keep a **living registry** of candidate
> tools, and make every new tool **pass the same exams** before it touches a shot.

## 1. The outcome contract (why unknown tools can't obsolete this skill)

Every production capability in this skill is specified by **outcome + measurable
criteria**, never by tool name. The named tool in each reference is merely the
*current champion*. Any tool — built-in, add-on, external app, AI system, future
Blender feature — may challenge the champion at any time; it wins only by beating
the criteria on the golden tests (§4). Examples of the contract:

| Capability | Outcome criteria (the law) | Current champion (replaceable) |
|---|---|---|
| Smooth arcs & spacing | Zero unintended kinks; spacing accelerates monotonically; planted contacts don't crawl (11 §B8, ref 19) | Motion Paths edit-on-path + Graph Editor |
| In-betweens/breakdowns | Eccentric, intention-serving breakdowns; no spacing jumps (refs 03/05) | Breakdowner + hand keys |
| Secondary motion (cloth/hair/flesh) | Believable overlap at target fps; bakeable; art-directable | Blender sims + hand offsets |
| Retarget/cleanup of captured motion | Contacts preserved (zero slide), accents survive | Manual cleanup (11 §B7) |
| Surface detail | PBR ranges legal (ref 16 §3), no baked light in base color, texel-density standard (ref 17) | Substance 3D Painter (ref 21) |
| Fast texture iteration | Same legality checks pass in 3-light test (ref 16 §6) | Principled + texture cache (ref 20) |

When you (the model) know of a newer tool than this text does — from training, from
the user's machine, or from the user naming it — **nominate it against the contract**
instead of ignoring it or blindly trusting it.

## 2. The evaluation scorecard (every candidate, no exceptions)

Run all five gates; a tool must pass each to be adopted:

1. **Outcome proof** — run the golden test (§4) with champion and challenger on the
   SAME input. Challenger must measurably beat the champion (smoother path, less
   slide, faster iteration at equal quality) — "feels better" is not proof.
2. **Book-law compliance** — the output still obeys the craft laws: spacing/arc law
   (refs 03/11 B8) for motion tools; PBR value law + no baked light (ref 16) for
   texturing tools; intention law (ref 18) for anything AI-generative. **A tool
   that is fast but breaks the law is rejected, however impressive the demo.**
3. **No-hostage test** (ref 21) — the .blend must remain fully workable if the tool
   vanishes tomorrow: bake/export path exists, standard formats out, no proprietary
   runtime required to open the file.
4. **Version & machine fit** — explicitly supports the user's Blender version
   (5.x law, ref 21) and runs acceptably on the user's recorded PC budget
   (refs 20/25).
5. **Reversibility & cost** — non-destructive or cleanly bakeable; price/learning
   curve justified by the measured win; a 10-minute trial on a throwaway copy
   precedes any verdict.

**Verdicts** (record in the registry, §3): **ADOPT** (new champion, update the
pipeline defaults) · **TRIAL** (this project only, re-judge at wrap) · **PARK**
(promising but immature/incompatible — recheck at next version bump) · **REJECT**
(record *why*, so it is never re-evaluated from zero).

## 3. TOOLS.md — the living registry (memory across sessions)

Maintain `TOOLS.md` in the project root, next to `LESSONS.md` (ref 19 §4); read both
at session start. One block per tool:

```
## [Tool name] — [capability it challenges]
- Version tested / Blender version: …  · Date: …
- Golden-test result vs champion: … (numbers, not adjectives)
- Book-law check: pass/fail + evidence
- Hostage/version/cost notes: …
- VERDICT: ADOPT / TRIAL / PARK / REJECT — because …
```

Rules: *tested* and *merely heard-of* entries are labeled as such — never blur
them. The user's owned tools (e.g., Substance 3D Painter + add-on, ref 21) get
priority trials but the **same scorecard** — ownership is not evidence.

## 4. Golden tests (fixed, so results stay comparable forever)

Keep these small scenes; every challenger runs the same battery:
- **Walk cycle, 24 frames** — contact slide (frames/mm of drift), head-path wave
  smoothness, playback fps on the user's PC.
- **Head-turn close-up** — path dip integrity, blink/eye-lead timing preserved.
- **Hand gesture arc** — fingertip path kinks/spacing (11 §B8 readout).
- **Hero material** (rusty painted metal) — PBR legal ranges, 3-light test
  (ref 16 §6), texture memory + render time at fixed samples.
- **Night interior still** — noise/render-time at equal quality (denoiser/engine
  challengers).
Changing a golden test requires re-baselining the champion on it first.

## 5. The `toolcheck` ritual (how the toolbox stays fresh)

Trigger: user types **toolcheck**, names a new tool, upgrades Blender, or a fresh
pipeline is being designed (ref 22 §B). Steps:
1. **Version delta-check**: if the user's Blender is newer than this skill's
   baseline, identify changes in the areas the pipeline actually uses (animation
   editors, rigging, shading, render) from official release notes where
   available; log UI/API deltas in TOOLS.md — the same procedure that moved this
   skill from 4.x to 5.x, now a habit instead of a rescue (11 §0 is the template).
2. **Registry sweep**: re-examine PARKed tools against the new version/landscape.
3. **Nominate challengers** per capability from your current knowledge; scorecard
   the credible ones (§2); log verdicts (§3).
4. **Report in five lines max**: what changed, what's adopted, what's parked, what
   it means for the current project. Update Pipeline Brief tool assumptions only
   on ADOPT.

## 6. Watchlist — categories that will keep evolving (and their traps)

- **AI in-betweening / motion generation** — trap: plausible-but-lawless spacing;
  must pass motion-path readout + accent survival, and serve the shot's intention
  (ref 18), not generic "smoothness" (smooth ≠ even, 11 §B8).
- **Mocap & video-pose estimation** — trap: foot slide, contact mush, lost accents
  in cleanup; contacts and extremes are re-authored by hand regardless.
- **Muscle/cloth/hair simulation** — trap: slow iteration killing the stage gates;
  require caching + low-res proxy workflow; believability judged at final camera.
- **AI texture generation / photo→PBR capture** — trap: baked lighting, illegal
  values, tiling seams, scale-free detail; must pass ref 16 ranges + ref 17
  observation checks (Demers) before lookdev.
- **Denoisers / new render paths / texture streaming** — trap: look drift between
  test and final; re-approve hero materials under the 3-light test after any swap.
- **Rig automation / full-body IK solvers** — trap: animator-hostile controls;
  judged by whether a pose from the Story Card is reachable in ≤3 control moves.

## 7. Honesty rules

- Never claim a tool is better without the golden-test comparison; if you cannot
  test it this session, output **"unverified — trial plan: …"** and log it as such.
- If a capability has no worthy challenger, say so; silence about novelty is a
  professional answer (Robert McKee: principles, not fashion).
- When the user's Blender/tools are newer than your knowledge, ask them to name
  what's installed — the registry grows from their real machine, not from hype.
