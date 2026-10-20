# 25 — Briefing the Skill (what to give, and how it's understood)

> The user is the director; this file is the **front desk**. It defines the five input
> levels the user can brief at, what to infer vs ask at each level, and how every input
> field lands in the intention engine (ref 18) and Pipeline Brief (ref 14). The user
> never needs technical vocabulary — translating their words into production terms is
> the skill's job (Hooks: ask the right questions; Robert McKee: respect for the audience
> starts with respect for the briefer).

## 1. The five input levels (accept ALL of them gracefully)

| Level | User gives | Skill does first |
|---|---|---|
| **L0 — Spark** | One line ("a robot learns to dance") | Generate a Story Card (below) + Style Card proposal → **confirm before building** |
| **L1 — Mini Brief** | The 6 fields (§2) | Story Card → Pipeline Brief → proceed |
| **L2 — Director's Brief** | Mini Brief + scene list/dialogue/wishes | Map scenes to beats/shots → Brief → proceed |
| **L3 — Full Script** | Screenplay or prose script | Ref 18 extraction protocol → Brief (no Story Card needed unless gaps) |
| **L4 — Production Pack** | Script + boards/audio/.blend files | Inventory assets first (what exists rules scope) → Brief |

**Classify the level silently; never complain about a low level.** A spark is a valid
brief — it just means the skill proposes more and confirms once.

## 2. The 6-field Mini Brief (the recommended minimum)

1. **Idea** — what happens, 1–3 lines, plain words.
2. **Who** — characters/objects + one line each (age, nature, look if known).
3. **Feeling** — what the audience should feel (one word is enough: "wonder").
4. **Style** — a ref 22 preset name, or "like *this film/clip/image*", or "you choose".
5. **Length & destination** — seconds/minutes + where it plays (YouTube, reel, film).
6. **What exists** — models/rigs/.blend/audio/images you already have (or "nothing").

Optional power-ups: must-have moments · must-avoid · dialogue lines · deadline ·
your PC (GPU/RAM — ask once per user, store in LESSONS.md header; feeds ref 20).

## 3. The Story Card (how the skill proves it understood)

For L0–L2, before any production output, return this card for a one-word approval:

```
STORY CARD — [working title]
Logline: [who] wants [what] but [obstacle]
Hero: wants ___ · needs ___ · flaw/habit ___
Inciting incident: the moment balance breaks: ___
Beats: B1 tries ___ → gap: ___ · B2 tries ___ → gap: ___ · B3 ...
Crisis (hardest choice): ___   Climax (final answer): ___
Ending feeling / controlling idea: "[life becomes ___ when ___]"
Style: [preset/custom] · Length: [s] · Format: [type]
Open questions (max 3, each with my recommended default): ...
```

Story structure behind the card (teach it when the user wants to write their own):
**Setup** (balanced world) → **Inciting Incident** (balance breaks) → **Struggle**
(attempt → *gap* between expectation and result → stronger attempt, escalating) →
**Crisis** (the dilemma choice) → **Climax** (the answer, biggest value swing) →
**Resolution** (new balance). Every beat runs the same loop in miniature:
*goal → attempt → gap → new tactic* (Robert McKee, ref 18 §8; Francis Glebas' narrative questions,
ref 23 §2 — each beat opens the question the next beat answers sideways).

## 4. Writing formats the skill accepts (tell the user: all are fine)

- **Plain story paragraph** — "first this happens, then…" (skill extracts beats).
- **Beat list** — numbered moments; gaps marked by the user or inferred.
- **Shot list** — # | seconds | what's seen | camera (wide/close/moving) | sound/lines.
  For users who think in camera; the skill still runs the intention pass per shot.
- **Screenplay-ish** — `INT. KITCHEN – DAY` headings, action in present tense,
  dialogue under names. Rough is fine; formatting perfection is not required.
- **References only** — images/clips/links + "like this but with my character" →
  treated as L0 with a custom Style Card derivation (ref 22 §A2).

## 5. Missing-information protocol

- **Infer** all mechanics (rig scope, maps, fps, samples — refs 14/20 decide).
- **Assume + declare** story mechanics that have professional defaults (state them in
  the Story Card so silence = approval).
- **Ask at most 3 questions**, only where *intention branches* (is she angry or
  protecting him?), each with your recommended default first ("I'd play her as
  protecting him — say 'ok' or tell me otherwise").
- If the user answers "you decide", decide by the feeling field; log the choice as a
  standing preference (ref 19 §4) so it's never asked twice.

## 6. How briefs map downstream (so nothing the user said gets lost)

| User gave | Lands in |
|---|---|
| Feeling field / ending feeling | Pipeline Brief line 0 (audience feeling), ref 18 arc peak |
| Hero want/obstacle | Story Card → beat map objectives/tactics (ref 18 §2) |
| Style words/reference | Style Card (ref 22 §A) — proven by a 2-second test |
| Must-haves / must-avoids | Brief constraints + Gate checklists (ref 19) |
| Existing assets/files | Stage inclusion in pipeline design (ref 22 §B); reuse rules (ref 14 §D) |
| PC specs / deadline | Optimization budget (ref 20, Brief line 9) |
| Corrections during work | LESSONS.md as standing rules (ref 19 §4) |

## 7. How to give feedback (teach this once, it compounds)

Most useful note format: **[shot/time] + [what you see] + [what you wanted to feel]** —
"S03, when he turns: he looks angry; I wanted sad." Feeling-words beat technical words;
the skill translates. Every note becomes a fix + a ledger rule, so the same note is
never needed twice (ref 19). If the user can only say "feels wrong", run the
self-critique battery and present the top-3 candidate causes as choices.

## 8. The Production Script Package (external template → perfect docking)

The user may paste a **Production Script Package** generated by another AI from the
companion master template (`STORY-TEMPLATE-FOR-ANY-AI.md`). Recognize it by its
**Parts 0–10** structure (Project Card · Story Structure · Character/World Bibles ·
Cinematography Bible · Color Script & Grading · Style Card · Shot-by-Shot Script ·
Sound Plan · FX · Production Handover). Treat as **L4** and dock it:

1. **Validate before building** (report pass/fail in 5 lines): every beat has a gap
   (Part 1) · every shot has a ★ FEELING JOB (Part 7) · shot durations sum to the
   Part 0 total · color arc mirrors the feeling arc (Part 5 vs Part 0) · hero asset
   list matches shot list (Part 10 vs Part 7). Fix small holes by inference and say so.
2. **Convert, don't re-interview**: Part 0 → Pipeline Brief header; Part 6 → Style
   Card (ref 22 §A); Part 5 → lookdev/grade targets (refs 16–17); Part 7 → the shot
   plan is law unless it violates a gate tolerance. Skip the Story Card.
3. **Conflicts** (e.g., a lens that can't frame the described action, a beat with no
   gap): raise at most 3, each with your fix as the recommended default.
4. Parts marked "Open choices" are yours to decide during pipeline design — decide,
   declare, proceed.
