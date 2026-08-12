"""
Task 1: Pick and Place — Data Recording
-----------------------------------------
Records teleoperated demonstrations for the pick-and-place task using
LeRobot's built-in recording pipeline. Requires LeRobot installed and
both arms calibrated first.

Usage:
    python record_task.py --hf_user your_username --episodes 40
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Record pick-and-place demonstrations")
    parser.add_argument("--hf_user", required=True, help="Your Hugging Face username")
    parser.add_argument("--robot_port", default="COM3", help="Follower arm COM port")
    parser.add_argument("--teleop_port", default="COM4", help="Leader arm COM port")
    parser.add_argument("--episodes", type=int, default=40, help="Number of demonstrations to record")
    parser.add_argument("--dataset_name", default="pick-place", help="Dataset repo name on Hugging Face Hub")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--episode_time_s", type=int, default=15, help="Max seconds per episode")
    parser.add_argument("--task_description", default="Pick up the object and place it in the target zone")
    args = parser.parse_args()

    repo_id = f"{args.hf_user}/{args.dataset_name}"

    cmd = [
        "lerobot-record",
        f"--robot.type=so101_follower",
        f"--robot.port={args.robot_port}",
        f"--teleop.type=so101_leader",
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
