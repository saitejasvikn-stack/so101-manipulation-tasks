"""
Task 2: Pouring 50ml — Data Recording
----------------------------------------
Records teleoperated pouring demonstrations. Vary starting fill level and
pour angle slightly between demos so the policy learns the pouring MOTION,
not one exact fixed trajectory — the precise 50ml stop point is handled
separately at inference time by pour_stop_detector.py, not by this dataset.

Usage:
    python record_task.py --hf_user your_username --episodes 40
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Record pouring demonstrations")
    parser.add_argument("--hf_user", required=True)
    parser.add_argument("--robot_port", default="COM3")
    parser.add_argument("--teleop_port", default="COM4")
    parser.add_argument("--episodes", type=int, default=40)
    parser.add_argument("--dataset_name", default="pouring-task")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--episode_time_s", type=int, default=20)
    parser.add_argument(
        "--task_description",
        default="Pick up the source container and pour blue liquid into the beaker up to the red line",
    )
    args = parser.parse_args()

    repo_id = f"{args.hf_user}/{args.dataset_name}"

    cmd = [
        "lerobot-record",
        "--robot.type=so101_follower",
        f"--robot.port={args.robot_port}",
        "--teleop.type=so101_leader",
        f"--teleop.port={args.teleop_port}",
        f"--dataset.repo_id={repo_id}",
        f"--dataset.num_episodes={args.episodes}",
        f"--dataset.fps={args.fps}",
        f"--dataset.episode_time_s={args.episode_time_s}",
        f"--dataset.single_task={args.task_description}",
        "--robot.cameras={\"overhead\": {\"type\": \"opencv\", \"index_or_path\": 0, \"width\": 640, \"height\": 480, \"fps\": 30}, \"wrist\": {\"type\": \"opencv\", \"index_or_path\": 1, \"width\": 640, \"height\": 480, \"fps\": 30}}",
    ]

    print("Running:\n", " ".join(cmd))
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
