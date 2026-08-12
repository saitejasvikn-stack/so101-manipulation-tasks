"""
Task 3: Plug in Charger — Data Recording
--------------------------------------------
Records teleoperated charger-insertion demonstrations. This task needs
MORE demonstrations than pick-and-place or pouring, with the final
approach/insertion phase performed slowly and deliberately in every demo —
a rushed teleoperated demo teaches a rushed, imprecise policy.

Usage:
    python record_task.py --hf_user your_username --episodes 80
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Record charger-plugging demonstrations")
    parser.add_argument("--hf_user", required=True)
    parser.add_argument("--robot_port", default="COM3")
    parser.add_argument("--teleop_port", default="COM4")
    parser.add_argument("--episodes", type=int, default=80, help="Insertion tasks need more demos than pick-and-place")
    parser.add_argument("--dataset_name", default="charger-plug-task")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--episode_time_s", type=int, default=20)
    parser.add_argument(
        "--task_description",
        default="Pick up the charger plug and insert it fully into the socket",
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
        # Wrist camera is close to mandatory here — the gripper occludes the
        # socket from an overhead view during the critical final approach.
        "--robot.cameras={\"overhead\": {\"type\": \"opencv\", \"index_or_path\": 0, \"width\": 640, \"height\": 480, \"fps\": 30}, \"wrist\": {\"type\": \"opencv\", \"index_or_path\": 1, \"width\": 640, \"height\": 480, \"fps\": 30}}",
    ]

    print("Running:\n", " ".join(cmd))
    print("\nReminder: perform the final approach/insertion SLOWLY in every demo.")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
