# Animation notes

Reference PDFs plus working documents for Kimodo (NVIDIA text-to-motion) production.

| Document | What's in it |
|---|---|
| [`kimodo-fist-prompt.md`](kimodo-fist-prompt.md) | Prompt pack for "making a fist" on Kimodo, plus the frame-by-frame finger-keying table (Kimodo predicts on a 30-joint skeleton with no finger detail). |
| [`kimodo-leg-martial-5s.md`](kimodo-leg-martial-5s.md) | Leg-only martial arts (Taekkyon / Savate / Taekwondo), their US popularity, and a 5-second three-kick volley with frame timing. |
| [`TAEKWONDO_10MIN_SCRIPT.md`](TAEKWONDO_10MIN_SCRIPT.md) | **10-minute taekwondo class sequence, whole script in one file** — 30 fps / 18,000 frames, 66 scored prompts, camera plan, generation plan, assembly notes. |
| [`rest-pose/REST_POSE_DIAGNOSIS.md`](rest-pose/REST_POSE_DIAGNOSIS.md) | Why the character isn't in a T-pose — measured diagnosis, Maya/Blender fix, and why it matters for retargeting. |
| [`rest-pose/fix_rest_pose.py`](rest-pose/fix_rest_pose.py) | Audits and repairs a rest pose in Maya or Blender (`--audit`, `--zero`, `--tpose`, `--apose`, `--bake-rest`); `--selftest` runs without a DCC. |
| [`taekwondo-practice/segments.json`](taekwondo-practice/segments.json) | Machine-readable source of truth for the 10-minute sequence. |
| [`taekwondo-practice/build_doc.py`](taekwondo-practice/build_doc.py) | Regenerates `TAEKWONDO_10MIN_SCRIPT.md` from `segments.json`. |
| [`taekwondo-practice/generate_all.sh`](taekwondo-practice/generate_all.sh) | Drives `kimodo_gen` across the sequence (`--dry-run`, `--block`, `--resume`). |
| [`taekwondo-practice/validate.py`](taekwondo-practice/validate.py) | Checks every prompt against Kimodo's limits (≤10 s, contiguity, 2-behaviour cap). |

Books in the repo root: *The Animator's Survival Kit*, *The Illusion of Life*, *Timing for Animation*,
*Acting for Animators*, *Stop Staring*, *3D Math Primer*, Rick Parent's *Computer Animation*,
and an introduction to Maya character rigging.
