# Dance module: bachata basic step, counts 1 to 8 (stage mapping)

Status: plan only. Build after the guitar MVP, as a second module that reuses the beat grid, speed control, loop and mixer.
The footwork below is the standard side-to-side bachata basic, written from general knowledge. Have a dance teacher check it (especially the tap and hip timing) before it goes into lessons.

## The step in one line
Counts 1-2-3-tap move one way, counts 5-6-7-tap move back. Counts 4 and 8 are taps: the foot touches next to the standing foot, weight stays on the other foot, and the hip pops.

## Leader, side-to-side basic

| Count | Moving foot | Action | Weighted foot after | Travel |
|---|---|---|---|---|
| 1 | L | Step left | L | left |
| 2 | R | Close to L | R | none |
| 3 | L | Step left | L | left |
| 4 | R | Tap beside L, hip pop | L (R hollow) | none |
| 5 | R | Step right | R | right |
| 6 | L | Close to R | L | none |
| 7 | R | Step right | R | right |
| 8 | L | Tap beside R, hip pop | R (L hollow) | none |

After count 8 the dancer is back where they started, ready to repeat.
Follower is the mirror image: R on 1 and 3, L on 5 and 7, taps on 4 and 8 with the opposite foot.

## What changes on screen from counts 5 to 8
- **Beat counter:** a second row lights 5-6-7-TAP. Count 8 flashes like count 4 did, so both taps are marked.
- **Direction:** the glowing path line and ghost target flip from left to right. Counts 6 and 8 have no travel, so the ghost sits beside the standing foot.
- **Feet:** on 5 the solid (weighted) mark jumps from L to R. On 8 the L foot turns hollow and R stays solid. The weight bar slides to R at 5 and stays there.
- **Hips lane:** hip pops on 4 and 8, with the weight side shown.
- **Loop:** after 8 the stage glides back to the count 1 pose, so a 16-count loop plays cleanly.

## Stage coordinates (top-down, x in foot-widths, left is negative)
Start: L at -0.25, R at +0.25, both weighted.

| Count | L foot x | R foot x | Weight |
|---|---|---|---|
| 1 | -1.25 | +0.25 | L |
| 2 | -1.25 | -0.75 | R |
| 3 | -2.25 | -0.75 | L |
| 4 | -2.25 | -1.75 (tap) | L |
| 5 | -2.25 | -0.75 | R |
| 6 | -1.25 | -0.75 | L |
| 7 | -1.25 | +0.25 | R |
| 8 | -0.25 (tap) | +0.25 | R |

Check: count 8 ends with L at -0.25 and R at +0.25, the same as the start.

## Variation to add in lesson 2: forward and back basic
Counts 1-2-3-tap step forward (L, R, L, tap R), counts 5-6-7-tap step back (R, L, R, tap L). Same layout, but the path line runs up and down instead of sideways.

## Data the lesson engine needs
- Beat times from the song's beat tracker, plus which beat is count 1 (downbeat tracker, or a "tap on 1" button).
- One lesson file per move: 8 entries of {count, foot, x, weight, tap, hip}.
- Role flag (lead or follow) that mirrors the file at load time.
