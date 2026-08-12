"""
Task 2: Pouring 50ml — Inference with Vision-Based Stop Condition
----------------------------------------------------------------------
This is the key script for Task 2: it runs the trained ACT policy to
execute the pouring MOTION, but overrides the stop point using live
camera detection of the blue liquid crossing a red reference line —
because the learned policy alone cannot measure volume, only imitate
motion patterns.

Setup required before running:
    1. Mark the beaker with a red line at the exact 50ml height.
    2. Have the trained policy checkpoint ready (from train_task.py).
    3. Camera must have a clear, unobstructed view of the beaker.

Usage:
    python run_policy_with_stop_condition.py --checkpoint outputs/train/pouring/checkpoints/last/pretrained_model --robot_port COM3
"""

import argparse
import time

import cv2
import numpy as np

from pour_stop_detector import find_red_line_row, liquid_has_reached_line

try:
    from lerobot.common.robot_devices.robots.utils import make_robot
    from lerobot.common.policies.factory import make_policy
except ImportError:
    make_robot = None
    make_policy = None


def calibrate_red_line(cap):
    """Show the live feed until the user confirms the empty beaker + red
    line are visible, then lock in the red line's pixel row."""
    print("Position the empty beaker with its red line visible.")
    print("Press 'c' to calibrate, 'q' to abort.")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Calibration - press 'c' when ready", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            row = find_red_line_row(frame)
            if row is None:
                print("Could not detect red line — adjust lighting/angle and try again.")
                continue
            print(f"Red line calibrated at pixel row: {row}")
            cv2.destroyAllWindows()
            return row
        if key == ord('q'):
            cv2.destroyAllWindows()
            raise SystemExit("Calibration aborted.")


def main():
    parser = argparse.ArgumentParser(description="Run pouring policy with vision-based stop condition")
    parser.add_argument("--checkpoint", required=True, help="Path to trained ACT policy checkpoint")
    parser.add_argument("--robot_port", default="COM3")
    parser.add_argument("--camera_index", type=int, default=0, help="Overhead camera index")
    parser.add_argument("--max_seconds", type=float, default=15.0, help="Safety timeout for the pour")
    args = parser.parse_args()

    if make_robot is None:
        raise ImportError(
            "LeRobot is not installed in this environment. "
            "Run this script from within your LeRobot virtual environment."
        )

    cap = cv2.VideoCapture(args.camera_index)
    red_line_row = calibrate_red_line(cap)

    print("Loading robot and policy...")
    robot = make_robot("so101_follower", port=args.robot_port)
    robot.connect()
    policy = make_policy(pretrained_path=args.checkpoint)

    print("Starting pour. Watching for liquid to reach the red line...")
    start_time = time.time()
    stopped = False

    try:
        while not stopped:
            obs = robot.capture_observation()
            action = policy.select_action(obs)
            robot.send_action(action)

            ret, frame = cap.read()
            if ret and liquid_has_reached_line(frame, red_line_row):
                print("Liquid reached the 50ml line — stopping pour.")
                stopped = True
                break

            if time.time() - start_time > args.max_seconds:
                print("Safety timeout reached — stopping pour regardless of fill level.")
                stopped = True
                break

    finally:
        # Return the source container to an upright/safe position.
        # Replace this with your actual "upright" joint configuration.
        upright_action = np.zeros_like(action) if 'action' in locals() else None
        if upright_action is not None:
            robot.send_action(upright_action)
        robot.disconnect()
        cap.release()
        cv2.destroyAllWindows()
        print("Done.")


if __name__ == "__main__":
    main()
