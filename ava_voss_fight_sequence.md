# AVA VOSS: SOLO FIGHT SEQUENCE

**Character:** AVA VOSS, female fighter, athletic build, fitted dark training gear, hair tied back.
**Duration:** 24 seconds (24 fps, so one second = 24 frames)
**Space:** Empty. No background, no opponents, no props.

---

## Part 1: Moves (Second by Second)

| Time | Action |
|---|---|
| 00:00 | Neutral stance, standing still. Arms relaxed at her sides. |
| 00:01 | She raises both fists into a guard in front of her face. Weight on her back foot. |
| 00:02 | She rolls her shoulders back, then tilts her head left and settles it. |
| 00:03 | She exhales and bends her knees slightly. Her chest drops. |
| 00:04 | She snaps her head to the right, as if reacting to something. |
| 00:05 | She pivots on the ball of her front foot. Her hips rotate about 45 degrees. |
| 00:06 | Her right hand sweeps down in a block. Her left fist stays tight at her chin. |
| 00:07 | A short right cross shoots out from her hip. The punch fully extends at 00:07.5. |
| 00:08 | She pulls the punch back into a ready stance. |
| 00:09 | She drops low into a crouch. |
| 00:10 | She sweeps her left leg in a low arc, pivoting on her right foot. The leg extends horizontally at hip height. |
| 00:11 | She rises out of the sweep and pulls her left knee up toward her chest. |
| 00:12 | She drives the knee forward. Her upper body leans back for balance. |
| 00:13 | She spins 180 degrees on her feet. |
| 00:14 | Mid-spin. Her arms stay tight to her body. Her ponytail swings out. |
| 00:15 | She extends a back kick. Her right heel fires straight out at chest height. |
| 00:16 | She lands on her front foot and holds her balance. Her guard comes back up. |
| 00:17 | SLOW MOTION (50% speed for 1 second). Her movement slows, and she holds a controlled stance. |
| 00:18 | Normal speed resumes. She wipes her lip with the back of her wrist. |
| 00:19 | She crouches low. Her fingertips touch the floor. |
| 00:20 | She explodes forward into a rolling motion across the floor. |
| 00:21 | The roll ends in a standing slide. She comes up with one foot forward. |
| 00:22 | A jab shoots out, fully extended, and holds. |
| 00:23 | She lowers her guard slowly and returns to a neutral stance. |
| 00:24 | She holds still in neutral stance. END. |

---

## Part 2: Camera Direction

**Setup:** Empty space with a plain neutral backdrop and a flat floor.
**Character origin:** Center of the floor, at her feet. She faces the camera.
**Character height:** about 1.7 m (adjust to your rig).
**Lens:** 50 mm standard. Use 35 mm for wide shots and 85 mm for close-ups.

| Time | Shot | Angle | Movement | Notes |
|---|---|---|---|---|
| 00:00 | Black | (none) | (none) | Hold black, no visible subject |
| 00:01 | Medium wide (full body) | Eye level, straight on | Slow dolly in | Ease-in, ends at 00:03 |
| 00:02 | Same | Same | Same | Frame head to toe with room to move |
| 00:03 | Medium (waist up) | Eye level | Dolly stops | Hold for the guard |
| 00:04 | Medium | Eye level | Static | Head snap should stay in frame |
| 00:05 | Full body | Slightly low (knee height) | Static | Shows the hip pivot clearly |
| 00:06 | Medium close (chest up) | Eye level | Slight push in | Camera ends 00:06.5 |
| 00:07 | Close-up on arm and shoulder | Eye level, slightly side-on | Quick push in | Snap zoom on punch |
| 00:07.5 | Hold | Same | Static | Lock on full extension |
| 00:08 | Medium | Eye level | Pull back | Reset to medium |
| 00:09 | Full body | Eye level | Static | Show the crouch |
| 00:10 | Full body, low | Low, 0.5 m height | Track sideways | Follow the sweep |
| 00:11 | Full body | Eye level | Static | Show rise |
| 00:12 | Medium | Eye level | Slow push in | Knee strike |
| 00:13 | Full body | Eye level | Orbit 180° around her | Camera orbits with the spin |
| 00:14 | Full body | Eye level | Continue orbit | Ponytail visible |
| 00:15 | Full body, slightly low | Low angle, 0.7 m height | Static | Show back kick at chest height |
| 00:16 | Medium | Eye level | Pull back | Settle |
| 00:17 | Medium close (face and shoulders) | Eye level | Very slow push in | Slow-motion beat, camera moves at half speed |
| 00:18 | Medium | Eye level | Static | Wipe of the lip |
| 00:19 | Full body | High angle, about 2.5 m height | Slow crane down | Show the crouch from above |
| 00:20 | Full body | Eye level | Static, quick shake | Roll starts |
| 00:21 | Full body | Eye level | Track | Slide, follow her motion |
| 00:22 | Medium close (arm and head) | Eye level | Slight push in | Hold on the jab |
| 00:23 | Medium wide | Eye level | Slow pull back | Lowering guard |
| 00:24 | Full body | Eye level | Static | Final hold, fade to black |

### Camera Coordinates for Code

Positions are relative to Ava's feet. Z is up. The camera looks at her center (about 0.9 m height).

| Shot | Distance from Ava (m) | Camera height (m) |
|---|---|---|
| Full body | 4.0 | 1.2 |
| Medium wide | 3.0 | 1.2 |
| Medium | 2.2 | 1.3 |
| Medium close | 1.4 | 1.4 |
| Close-up | 0.9 | 1.5 |
| Low angle (kick) | 3.5 | 0.7 |
| High angle (crouch) | 4.0 | 2.5 |

---

## Part 3: Animation Notes

- **Frame numbers:** Use frame numbers, not seconds. For example, 00:07.5 is frame 180 at 24 fps.
- **Motion hierarchy:** Drive each move from the pelvis first, then the spine, then the arms and legs.
- **Easing:** Use ease-in for wind-ups and pushes. Use ease-out for impacts, holds, and pull-backs.
- **Overshoot:** Add a small overshoot to the punch and kick endings for a snappy feel.
- **Slow motion (00:17):** Use a time-scale of 0.5 for the character and the camera during this segment only.
- **Camera shake:** Add a 2 to 3 frame shake at 00:07.5, 00:15, and 00:20.
- **Orbit (00:13 to 00:14):** Keep the look-at target on her chest (about 1.2 m) during the orbit.
- **Breathing:** Add a subtle chest-expansion loop (about 0.3 seconds per breath) during idle frames at 00:02, 00:03, and 00:17.
- **Frame margin:** Keep at least 0.3 m of empty space around her limbs in full-body shots so kicks and sweeps aren't cut off.
