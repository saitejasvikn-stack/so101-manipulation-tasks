"""
Task 2: Pouring 50ml — Policy Training
------------------------------------------
Trains an ACT policy on the pouring dataset. This learns the POUR MOTION
(approach, tilt, timing) — it does not learn the exact 50ml stop point.
That precision comes from pour_stop_detector.py at inference time.

Usage:
    python train_task.py --hf_user your_username
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Train ACT policy for pouring")
    parser.add_argument("--hf_user", required=True)
    parser.add_argument("--dataset_name", default="pouring-task")
    parser.add_argument("--output_dir", default="outputs/train/pouring")
    parser.add_argument("--job_name", default="pouring")
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
