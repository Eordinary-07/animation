# 📤 CGBoost "Character Sculpting in Blender" P1 C1-10 — EXACT UPLOAD LIST

> You have 45.87 GB. **I only need ~790 MB (21 files) + the caption text files.**
> Rule I used: I can parse **.blend files** (node trees, modifiers, mesh stats)
> and read **text** — I **cannot watch the videos**. So: files + captions, no videos.

---

## 🥇 TIER A — GEOMETRY NODES (upload first) — 7 files, **431.7 MB**
These are real production node trees. I extract the exact node graph (nodes,
sockets, links, defaults) → **ref 32 Geometry Nodes**.

| File (in `Project Files/`) | Size |
|---|---|
| `05_sculpting_shirt_project_files/05_09_modeling_zipper_geometry_nodes_final.blend` | 26.91 MB |
| `06_sculpting_trousers_project_files/06_09_modeling_stitching_geonodes_final.blend` | 59.44 MB |
| `06_sculpting_trousers_project_files/06_10_geonodes_organization_final.blend` | 59.99 MB |
| `07_sculpting_boots_project_files/07_17_modeling_stitches_geometry_nodes_final.blend` | 63.61 MB |
| `09_sculpting_sweater_project_files/09_08_geonodes_smoothing_vertex_groups_final.blend` | 68.24 MB |
| `10_modeling_jetpack_project_files/10_12_geonodes_panel_bolts_final.blend` | 76.21 MB |
| `10_modeling_jetpack_project_files/10_19_geonodes_wing_bolts_final.blend` | 77.32 MB |

*Upload the `_final` versions — they contain the finished graph. Skip the `_start` ones.*

## 🥈 TIER B — CLOTH & FOLD CRAFT — 6 files, **248.2 MB**
Fold logic is the art half of cloth → **ref 33**. (Start with the two tiny
exercise files — 3 MB total, pure fold study.)

| File | Size |
|---|---|
| `05_sculpting_shirt_project_files/05_04_exercise_1.blend` | 1.23 MB |
| `05_sculpting_shirt_project_files/05_04_exercise_2.blend` | 1.66 MB |
| `05_sculpting_shirt_project_files/05_08_sculpting_shirt_part_4_final.blend` | 26.70 MB |
| `06_sculpting_trousers_project_files/06_17_sculpting_knee_fabric_final.blend` | 58.42 MB |
| `09_sculpting_sweater_project_files/09_04_sculpting_cloth_brush_final.blend` | 69.81 MB |
| `10_modeling_jetpack_project_files/10_26_sculpting_sweater__final.blend` | 90.39 MB |

## 🥉 TIER C — HAIR + ANATOMY — 8 files, **112.6 MB**
Sculpted hair (silhouette/flow craft) + finished body parts → **ref 31** and the
anatomy half of **ref 27** (topology follows form).

| File | Size |
|---|---|
| `03_sculpting_body_project_files/03_24_sculpting_the_hair_final.blend` | 22.29 MB |
| `03_sculpting_body_project_files/03_09_refining_the_head_part_2_final.blend` | 10.88 MB |
| `03_sculpting_body_project_files/03_11_sculpting_the_torso_part_1_final.blend` | 13.54 MB |
| `03_sculpting_body_project_files/03_16_sculpting_the_arms_final.blend` | 14.70 MB |
| `03_sculpting_body_project_files/03_20_sculpting_the_hands_part_2_final.blend` | 15.10 MB |
| `03_sculpting_body_project_files/03_21_sculpting_the_legs_final.blend` | 18.35 MB |
| `03_sculpting_body_project_files/03_23_sculpting_the_feet_part_2_final.blend` | 17.72 MB |
| *(`03_05` head, if you have room)* | 8.79 MB |

## 🆓 TIER D — CAPTIONS (**free, tiny, highest value per byte**)
CG Boost ships **English captions for every lesson**. Export/download the
`.srt`/`.vtt` for these lessons and paste or upload them — the *teaching* is in
the narration, and text is the one form of video content I can actually use:

`05_03 anatomy of folds` · `05_04 folds exercise` · `09_03 sculpting sweater` ·
`09_04 sculpting cloth brush` · `05_09 zipper GeoNodes` · `06_09 stitching
GeoNodes` · `06_10 GeoNodes organization` · `03_24 sculpting the hair` ·
`02_03 analyzing concept art`.

(Not needed: 02_04, or any hard-surface/jetpack lessons.)

---

## ⛔ SKIP (saves ~45 GB)
* **All `*_videos_1440p` folders** — I can't watch them.
* **All `*_reference_board.pur`** (Pureref binaries, ~1 GB total) — I can't open
  them; you open them in Pureref and study them yourself.
* **`02_04_id_and_references/Reference Sheet.pur`** (193 MB) — same reason.
* **`03_02_brush_textures` + `03_02_matcaps`** (29 MB) — install them in your own
  Blender (they're great sculpting brushes for folds); they're useless to me.
* **All `_start.blend`** files — the `_final` ones contain the result.
* **Hard-surface jetpack modeling** (10_07–10_24) — not your Ava pipeline.
  (Keep only the two GeoNodes ones listed in Tier A.)

---

## 📦 HOW TO UPLOAD
1. Zip each tier separately: `cgboost-A-geonodes.zip` (432 MB),
   `cgboost-B-cloth-folds.zip` (248 MB), `cgboost-C-hair-anatomy.zip` (113 MB).
   Every single `.blend` is **under 100 MB** ✅ so no size problem.
2. Upload to the **GitHub release** (your usual route) — release assets allow
   much bigger files than the repo itself. **Don't `git add` them into the repo.**
3. Paste/upload the caption files (or just paste the text into chat).

**Short on space/time?** Upload **Tier A + the Tier D captions** — that alone
gives me Geometry Nodes (exact graphs) + the fold teaching.

**Optional bonus (tiny, very precise):** open each Tier A `.blend` in Blender and
run the dump script from `WHAT-TO-GIVE-HAIR-GEONODES-CLOTH.md` → a ~1 MB JSON with
every node and setting. That's the most precise thing you can hand me.
