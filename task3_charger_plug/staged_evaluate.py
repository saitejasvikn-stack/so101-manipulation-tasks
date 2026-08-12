"""
Task 3: Plug in Charger — Staged Evaluation
------------------------------------------------
Runs the trained policy but tracks success/failure at THREE separate
sub-stages instead of one binary "did it plug in" outcome. This makes it
much easier to diagnose exactly where the policy is failing:

    Stage 1: Approach       - did it reliably move toward and orient near the socket?
    Stage 2: Contact         - did it make contact with the socket face?
    Stage 3: Insertion       - did it complete full insertion?

Usage:
    python staged_evaluate.py --checkpoint outputs/train/charger_plug/checkpoints/last/pretrained_model --robot_port COM3 --trials 10
"""

import argparse
import time

try:
    from lerobot.common.robot_devices.robots.utils import make_robot
    from lerobot.common.policies.factory import make_policy
except ImportError:
    make_robot = None
    make_policy = None


def classify_stage_reached(robot, obs):
    """
    Placeholder stage classifier — replace with your actual logic based on
    end-effector position relative to the socket (from a marker, an
    overhead + wrist camera detection, or manual observation during
    live trials).

    Returns one of: "approach_failed", "contact_failed", "insertion_failed", "success"
    """
    # This needs real position/vision logic specific to your socket setup.
    # As a starting point during manual trials, you can run this script with
    # --manual_labeling to type in the outcome yourself after each trial.
    raise NotImplementedError(
        "Add your stage-classification logic here, or use --manual_labeling."
    )


def run_manual_trial(robot, policy, max_seconds):
    """Runs one policy rollout, then asks the human to label which stage failed."""
    print("\nRunning trial... press Ctrl+C to stop early if it's clearly failed.")
    start = time.time()
    try:
        while time.time() - start < max_seconds:
            obs = robot.capture_observation()
            action = policy.select_action(obs)
            robot.send_action(action)
    except KeyboardInterrupt:
        pass

    print("\nHow far did it get?")
    print("  1) Approach failed (never got near/oriented at the socket)")
    print("  2) Contact failed (got close but didn't make contact correctly)")
    print("  3) Insertion failed (made contact but didn't fully insert)")
    print("  4) Success (fully inserted)")
    choice = input("Enter 1-4: ").strip()
    return {"1": "approach_failed", "2": "contact_failed", "3": "insertion_failed", "4": "success"}.get(choice, "unlabeled")


def main():
    parser = argparse.ArgumentParser(description="Staged evaluation for charger-plugging policy")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--robot_port", default="COM3")
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--max_seconds", type=float, default=20.0)
    parser.add_argument("--manual_labeling", action="store_true", default=True,
                         help="Human labels each trial's outcome (recommended, since automatic stage detection needs custom setup)")
    args = parser.parse_args()

    if make_robot is None:
        raise ImportError("LeRobot is not installed in this environment.")

    robot = make_robot("so101_follower", port=args.robot_port)
    robot.connect()
    policy = make_policy(pretrained_path=args.checkpoint)

    results = []
    for i in range(args.trials):
        print(f"\n=== Trial {i + 1}/{args.trials} ===")
        outcome = run_manual_trial(robot, policy, args.max_seconds)
        results.append(outcome)
        robot.send_action(robot.capture_observation())  # reset/settle between trials as needed

    robot.disconnect()

    print("\n=== Summary ===")
    for stage in ["approach_failed", "contact_failed", "insertion_failed", "success"]:
        count = results.count(stage)
        print(f"{stage}: {count}/{len(results)}")


if __name__ == "__main__":
    main()
