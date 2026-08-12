# Task 2: Pouring Exactly 50ml of Blue Liquid

Pours blue liquid from a source container into a beaker, stopping precisely
at 50ml — without a scale.

## Approach

An ACT policy learns the pouring MOTION (approach, tilt, timing) from
teleoperated demonstrations, the same way as Task 1. But volume precision
isn't something a vision+motion policy can reliably measure on its own, so
the exact 50ml stop point is handled by a **separate, deterministic vision
check**: a red line is marked on the beaker at the 50ml height, and a
lightweight OpenCV script watches for the blue liquid's surface to reach
that line, then signals the robot to stop — regardless of what the policy
itself "thinks."

This keeps the two concerns cleanly separated: the neural network handles
*how to pour smoothly*, the vision check handles *when to stop precisely*.

## Files

- `pour_stop_detector.py` — standalone/importable vision module. Detects the
  red reference line and checks whether the blue liquid has reached it.
  Run it directly for a live calibration/testing preview.
- `record_task.py` — records teleoperated pouring demonstrations.
- `train_task.py` — trains the ACT policy on those demonstrations.
- `run_policy_with_stop_condition.py` — runs the trained policy live,
  combined with the vision-based stop condition. This is the actual
  demo-ready script.

## Setup

1. Mark a red line on the beaker at the exact 50ml height (measure once
   with a standard measuring cup beforehand).
2. Use a transparent beaker/container — the camera needs to see the liquid.
3. Test detection first:
   ```powershell
   python pour_stop_detector.py
   ```
   Press `c` once the empty beaker (with the red line) is in frame to
   calibrate, then pour and watch the on-screen status flip to
   "STOP - 50ml REACHED". Tune `BLUE_LOWER`/`BLUE_UPPER` in the script if
   detection is unreliable under your lighting.

## Usage

```powershell
# 1. Record ~40 pouring demonstrations, varying start fill level and angle
python record_task.py --hf_user your_username --episodes 40

# 2. Train the ACT policy
python train_task.py --hf_user your_username

# 3. Run the trained policy with the live vision stop condition
python run_policy_with_stop_condition.py --checkpoint outputs/train/pouring/checkpoints/last/pretrained_model --robot_port COM3
```

## Known limitations

- Pixel-based detection assumes the camera and beaker don't move between
  calibration and the live run — recalibrate (`c`) if either shifts.
- Tolerance is set via `tolerance_px` in `pour_stop_detector.py` — perfect
  precision isn't realistic given reaction latency; a few ml of error is
  expected and acceptable.
- No scale/load-cell is used — this is a fully vision-based approach.
