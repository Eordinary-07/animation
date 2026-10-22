#!/usr/bin/env bash
# generate_all.sh — drive Kimodo over the 10-minute taekwondo practice sequence.
#
#   ./generate_all.sh --dry-run              # print every kimodo_gen command, run nothing
#   ./generate_all.sh                        # full pass, 2 samples per segment
#   ./generate_all.sh --block B4 --samples 4 # hero pass on the kicking block only
#   ./generate_all.sh --resume               # skip segments already on disk
#
# Every segment is <= 10 s (Kimodo's per-prompt maximum, verified by validate.py).
# Segments sharing a "chain" id are emitted as ONE kimodo_gen call with multiple
# prompts, so Kimodo conditions each prompt on the last frames of the previous one
# and the poomsae lines stay continuous.
#
# Outputs land in $OUT as <segment id>.npz (+ .bvh with --bvh), and manifest.csv
# is written for the edit.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SEGMENTS="$HERE/segments.json"

MODEL="Kimodo-SOMA-RP-v1.2"
OUT="$HERE/output"
SAMPLES=2
SEED=1000
STEPS=100
BLOCK=""
DRY_RUN=0
RESUME=0
BVH=1
EXTRA=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)  DRY_RUN=1; shift ;;
    --resume)   RESUME=1; shift ;;
    --block)    BLOCK="$2"; shift 2 ;;
    --samples)  SAMPLES="$2"; shift 2 ;;
    --seed)     SEED="$2"; shift 2 ;;
    --model)    MODEL="$2"; shift 2 ;;
    --steps)    STEPS="$2"; shift 2 ;;
    --out)      OUT="$2"; shift 2 ;;
    --no-bvh)   BVH=0; shift ;;
    --no-postprocess) EXTRA+=(--no-postprocess); shift ;;
    -h|--help)  sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

mkdir -p "$OUT"

# ---- build the plan -------------------------------------------------------
# One tab-separated record per kimodo_gen call:
#   group_id  output_stem  durations  prompt  first_segment_id
PLAN="$OUT/.plan.tsv"
python3 - "$SEGMENTS" "$BLOCK" > "$PLAN" <<'PY'
import json, sys

path, block = sys.argv[1], sys.argv[2]
data = json.load(open(path))
segs = [s for s in data["segments"] if not block or s["block"] == block]

groups, order = {}, []
for s in segs:
    key = s.get("chain") or s["id"]
    if key not in groups:
        groups[key] = []
        order.append(key)
    groups[key].append(s)

for key in order:
    members = groups[key]
    durations = " ".join(str(m["dur"]) for m in members)
    prompt = " ".join(m["prompt"] for m in members)
    # output stem: first id, plus "-chain" when several prompts are fused
    stem = members[0]["id"] if len(members) == 1 else f"{members[0]['id']}-chain{len(members)}"
    print("\t".join([key, stem, durations, prompt, members[0]["id"]]))
PY

TOTAL=$(wc -l < "$PLAN" | tr -d ' ')
echo "plan: $TOTAL generation call(s) -> $OUT"
echo "model: $MODEL   samples: $SAMPLES   seed base: $SEED   steps: $STEPS"
echo

n=0
while IFS=$'\t' read -r key stem durations prompt sid; do
  n=$((n + 1))
  seed=$((SEED + n))
  printf '[%2d/%2d] %-16s %ss  %s\n' "$n" "$TOTAL" "$stem" "${durations// /+}" "${prompt:0:64}..."

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "        kimodo_gen \"$prompt\" --model $MODEL --duration \"$durations\" --num_samples $SAMPLES --seed $seed --diffusion_steps $STEPS --output $OUT/$stem"
    continue
  fi

  if [[ $RESUME -eq 1 ]] && { [[ -f "$OUT/$stem.npz" ]] || [[ -d "$OUT/$stem" ]]; }; then
    echo "        skipped (already exists)"
    continue
  fi

  args=(--model "$MODEL" --duration "$durations" --num_samples "$SAMPLES"
        --seed "$seed" --diffusion_steps "$STEPS" --output "$OUT/$stem")
  [[ $BVH -eq 1 ]] && args+=(--bvh --bvh_standard_tpose)
  [[ ${#EXTRA[@]} -gt 0 ]] && args+=("${EXTRA[@]}")

  kimodo_gen "$prompt" "${args[@]}"
done < "$PLAN"

rm -f "$PLAN"

# ---- edit manifest --------------------------------------------------------
python3 - "$SEGMENTS" "$OUT" "$BVH" <<'PY'
import csv, json, sys
from pathlib import Path

path, out, bvh = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
data = json.load(open(path))
fps = data["fps"]

def tc(sec: float) -> str:
    return f"{int(sec // 60):02d}:{sec % 60:06.3f}"

# chained segments live inside one clip: point the editor at that clip and give
# the in-clip frame range instead of pretending each segment has its own file.
groups = {}
for s in data["segments"]:
    groups.setdefault(s.get("chain") or s["id"], []).append(s)

offsets = {}
for key, members in groups.items():
    stem = members[0]["id"] if len(members) == 1 else f"{members[0]['id']}-chain{len(members)}"
    cursor = 0
    for m in members:
        offsets[m["id"]] = (stem, cursor, cursor + int(float(m["dur"]) * fps))
        cursor += int(float(m["dur"]) * fps)

manifest = Path(out) / "manifest.csv"
with manifest.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["segment", "block", "tc_in", "tc_out", "frames_in", "frames_out",
                "dur_sec", "beat", "clip", "clip_frame_in", "clip_frame_out", "prompt"])
    for s in data["segments"]:
        start, dur = float(s["start"]), float(s["dur"])
        stem, cin, cout = offsets[s["id"]]
        w.writerow([s["id"], s["block"], tc(start), tc(start + dur),
                    int(start * fps), int((start + dur) * fps), f"{dur:g}",
                    s["beat"], f"{stem}.npz", cin, cout, s["prompt"]])
print(f"\nmanifest: {manifest}")
PY
