
https://github.com/user-attachments/assets/0ce0dd72-75e3-4a14-a07d-2d10f61534a5

https://github.com/user-attachments/assets/37d218ac-c78f-478f-ab40-d7c474a80f14

<img width="1600" height="1000" alt="robo interface" src="https://github.com/user-attachments/assets/92dec4d0-f78b-4aac-8d98-65f2d68324f3" />

<img width="1280" height="960" alt="training" src="https://github.com/user-attachments/assets/5283d9c7-1996-491b-b510-de234c7db27b" /># SO-101 Manipulation Tasks

Three imitation-learning manipulation tasks trained on a Hugging Face LeRobot SO-101 arm, built as part of a Physical AI / Robotics session.

## Tasks

| Task | Policy | Status | Notes |
|---|---|---|---|
| 1. Pick and Place | ACT | ✅ Working | Baseline imitation learning task |
| 2. Pour 50ml of blue liquid | ACT + CV stopping condition | ⚙️ In progress | Uses a red reference line + OpenCV color detection instead of a scale |
| 3. Plug in charger | ACT / Diffusion Policy | ❌ Known limitation | High-precision insertion task — see `task3_charger_plug/notes.md` for failure analysis |

## Hardware

- SO-101 leader + follower arm pair
- 2x USB webcams (overhead + wrist), 720p, different models to avoid USB path collisions
- Windows 11, Python 3.11, RTX 4050 Laptop GPU

## Software stack

- [LeRobot](https://github.com/huggingface/lerobot) — Hugging Face's robotics framework (calibration, teleoperation, recording, training)
- OpenCV — custom vision logic for Task 2's stopping condition
- ACT (Action Chunking Transformer) policy for Tasks 1 & 2

## Setup

```powershell
git clone https://github.com/huggingface/lerobot.git
cd lerobot
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[feetech]"
pip install -e ".[core_scripts,training]"
```

See each task folder for task-specific recording/training commands.

## Repo structure

```
task1_pick_place/    - baseline pick-and-place, standard LeRobot workflow
task2_pouring/        - pouring task with custom CV-based volume detection
task3_charger_plug/   - high-precision insertion task (documented limitations)
calibration/          - saved calibration files (red line position, etc.)
notes/                - general project notes (camera setup, lessons learned)
```
