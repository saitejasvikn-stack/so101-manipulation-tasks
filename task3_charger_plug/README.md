# Task 3: Plug in Charger

High-precision insertion task — pick up a charger plug and fully insert it
into a socket.

## Approach

Same imitation-learning pipeline as Tasks 1 and 2, using a Diffusion
Policy instead of ACT (better suited to contact-rich, high-precision
tasks). This task is documented as a **known, honest limitation** —
see `failure_analysis.md` for a full breakdown of why insertion tasks
are fundamentally harder than pick-and-place or pouring, and what would
be needed to solve them properly (primarily: force/torque feedback,
which this hardware setup doesn't have).

## Files

- `record_task.py` — records teleoperated insertion demonstrations
  (recommends 80+ episodes, more than Tasks 1/2, with slow deliberate
  final-approach motion).
- `train_task.py` — trains a Diffusion Policy (or ACT, as a fallback
  comparison) on the dataset.
- `staged_evaluate.py` — evaluates the trained policy with per-stage
  outcome tracking (approach / contact / insertion) instead of one
  binary success/fail, to make debugging tractable.
- `failure_analysis.md` — full writeup of why this task is hard, useful
  as presentation material regardless of live-demo outcome.

## Usage

```powershell
# 1. Record demonstrations (slow, deliberate final approach every time)
python record_task.py --hf_user your_username --episodes 80

# 2. Train (diffusion policy recommended)
python train_task.py --hf_user your_username --policy_type diffusion

# 3. Evaluate with staged outcome tracking
python staged_evaluate.py --checkpoint outputs/train/charger_plug/checkpoints/last/pretrained_model --robot_port COM3 --trials 10
```

## Expectation setting

This is a genuinely open research-difficulty task on hobbyist hardware.
Low first-attempt success rates are expected and normal — see
`failure_analysis.md` for the honest reasons why, and how to frame that
constructively if presenting live.
