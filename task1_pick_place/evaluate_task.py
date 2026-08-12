"""
Task 1: Pick and Place — Policy Evaluation
---------------------------------------------
Runs the trained policy on the real robot and records evaluation episodes
for review.

Usage:
    python evaluate_task.py --hf_user your_username
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Evaluate trained pick-and-place policy")
    parser.add_argument("--hf_user", required=True)
    parser.add_argument("--robot_port", default="COM3")
    parser.add_argument("--checkpoint", default="outputs/train/pick_place/checkpoints/last/pretrained_model")
    parser.add_argument("--eval_dataset_name", default="eval-pick-place")
    parser.add_argument("--episodes", type=int, default=10)
    args = parser.parse_args()

    repo_id = f"{args.hf_user}/{args.eval_dataset_name}"

    cmd = [
        "lerobot-record",
        "--robot.type=so101_follower",
        f"--robot.port={args.robot_port}",
        f"--dataset.repo_id={repo_id}",
        f"--dataset.num_episodes={args.episodes}",
        f"--policy.path={args.checkpoint}",
    ]

    print("Running:\n", " ".join(cmd))
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
