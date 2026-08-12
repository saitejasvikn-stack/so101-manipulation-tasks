# Task 1: Pick and Place

Baseline imitation-learning task — pick up an object from a variable starting
position and place it in a fixed target zone.

## Approach

Standard LeRobot ACT (Action Chunking Transformer) workflow: collect teleoperated
demonstrations, train an ACT policy to imitate them, evaluate on the real robot.

## Prerequisites

- Both arms calibrated (`lerobot/scripts/calibrate.py`)
- Two cameras connected (overhead + wrist), correct indices set in `record_task.py`
- Logged in to Hugging Face: `huggingface-cli login`

## Usage

```powershell
# 1. Record ~40 demonstrations, varying the object's starting position each time
python record_task.py --hf_user your_username --episodes 40

# 2. Train the ACT policy
python train_task.py --hf_user your_username

# 3. Evaluate on the real robot
python evaluate_task.py --hf_user your_username
```

## Notes

- Vary the object's position across demos — a policy trained on one exact
  position will not generalize even a few cm off.
- 30–50 demonstrations is typically enough for a simple pick-and-place task.
- If grasp success is low, check whether failures cluster around specific
  object positions (data coverage gap) or are randomly distributed (needs
  more demos, or PD/actuator gain tuning at the hardware level).
