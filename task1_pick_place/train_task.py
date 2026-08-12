"""
Task 1: Pick and Place — Policy Training
-------------------------------------------
Trains an ACT (Action Chunking Transformer) policy on the recorded
pick-and-place dataset.

Usage:
    python train_task.py --hf_user your_username
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Train ACT policy for pick-and-place")
    parser.add_argument("--hf_user", required=True)
    parser.add_argument("--dataset_name", default="pick-place")
    parser.add_argument("--output_dir", default="outputs/train/pick_place")
    parser.add_argument("--job_name", default="pick_place")
    parser.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    parser.add_argument("--steps", type=int, default=20000)
    args = parser.parse_args()

    repo_id = f"{args.hf_user}/{args.dataset_name}"

    cmd = [
        "lerobot-train",
        f"--dataset.repo_id={repo_id}",
        "--policy.type=act",
        f"--output_dir={args.output_dir}",
        f"--job_name={args.job_name}",
        f"--policy.device={args.device}",
        f"--steps={args.steps}",
        "--wandb.enable=true",
    ]

    print("Running:\n", " ".join(cmd))
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
