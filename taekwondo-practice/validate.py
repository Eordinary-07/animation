#!/usr/bin/env python3
"""Validate the taekwondo practice sequence against Kimodo's documented limits.

Checks:
  * every segment is <= 10 s (Kimodo's hard per-prompt maximum)
  * segments are contiguous (start == previous start + previous dur)
  * total duration matches the declared scene length
  * ids unique, prompts non-empty and in the "A person ..." style
  * chained groups respect the <= 10 s per prompt rule (total may exceed 10 s)
  * prompt length is in Kimodo's recommended "medium detail" band

Exit code 1 on any error. Warnings do not fail the build.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MAX_PROMPT_SEC = 10.0
MIN_WORDS = 6
MAX_WORDS = 32


def main(path: str) -> int:
    data = json.loads(Path(path).read_text())
    segs = data["segments"]
    fps = data.get("fps", 30)
    total = data.get("total_duration_sec")

    errors: list[str] = []
    warnings: list[str] = []

    seen: set[str] = set()
    clock = 0.0
    chains: dict[str, list[dict]] = {}

    for i, s in enumerate(segs):
        sid = s["id"]
        dur = float(s["dur"])
        start = float(s["start"])

        if sid in seen:
            errors.append(f"{sid}: duplicate id")
        seen.add(sid)

        if abs(start - clock) > 1e-6:
            errors.append(f"{sid}: starts at {start:g}s, expected {clock:g}s (gap or overlap)")
        clock = start + dur

        if dur <= 0:
            errors.append(f"{sid}: non-positive duration")
        if dur > MAX_PROMPT_SEC:
            errors.append(f"{sid}: {dur:g}s exceeds Kimodo's {MAX_PROMPT_SEC:g}s per-prompt limit")

        prompt = s.get("prompt", "").strip()
        if not prompt:
            errors.append(f"{sid}: empty prompt")
            continue
        if not (prompt.startswith("A ") or prompt.startswith("An ")):
            warnings.append(f"{sid}: prompt should open with 'A person ...' / 'An old person ...'")
        words = len(prompt.split())
        if words < MIN_WORDS:
            warnings.append(f"{sid}: prompt is very short ({words} words) — may be too vague")
        if words > MAX_WORDS:
            warnings.append(f"{sid}: prompt is very long ({words} words) — Kimodo prefers medium detail")
        if prompt.count(".") > 2:
            errors.append(f"{sid}: {prompt.count('.')} sentences — max 2 behaviours per prompt")

        if s.get("chain"):
            chains.setdefault(s["chain"], []).append(s)

    if total is not None and abs(clock - float(total)) > 1e-6:
        errors.append(f"scene ends at {clock:g}s but total_duration_sec is {total:g}s")

    for name, members in chains.items():
        span = sum(float(m["dur"]) for m in members)
        ids = ", ".join(m["id"] for m in members)
        if span > 30:
            warnings.append(f"chain {name} ({ids}) is {span:g}s — long chains drift; consider splitting")
        print(f"  chain {name}: {span:g}s over {len(members)} prompts -> {ids}")

    frames = int(round(clock * fps))
    print(f"\n  segments : {len(segs)}")
    print(f"  duration : {clock:g}s  ({int(clock // 60)}:{int(clock % 60):02d})  at {fps} fps = {frames} frames")
    print(f"  chains   : {len(chains)}")
    print(f"  prompts  : {sum(1 for s in segs if s.get('prompt'))}")
    print()

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")

    if errors:
        print(f"\n{len(errors)} error(s).")
        return 1
    print(f"OK — {len(warnings)} warning(s), 0 errors.")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "segments.json"
    raise SystemExit(main(target))
