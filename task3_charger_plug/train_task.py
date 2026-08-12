"""
Task 3: Plug in Charger — Policy Training
----------------------------------------------
Trains a Diffusion Policy (rather than ACT) on the charger-plugging
dataset. Diffusion policies tend to handle contact-rich, high-precision
insertion tasks more robustly than ACT, at the cost of slower inference.

Usage:
    python train_task.py --hf_user your_username
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Train diffusion policy for charger plugging")
    parser.add_argument("--hf_user", required=True)
    parser.add_argument("--dataset_name", default="charger-plug-task")
    parser.add_argument("--output_dir", default="outputs/train/charger_plug")
    parser.add_argument("--job_name", default="charger_plug")
    parser.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    parser.add_argument("--steps", type=int, default=30000, help="Insertion tasks often need more training steps")
    parser.add_argument(
        "--policy_type", default="diffusion", choices=["diffusion", "act"],
        help="diffusion is recommended for this task; act is available as a fallback comparison"
    )
    args = parser.parse_args()

    repo_id = f"{args.hf_user}/{args.dataset_name}"

    cmd = [
        "lerobot-train",
        f"--dataset.repo_id={repo_id}",
        f"--policy.type={args.policy_type}",
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
