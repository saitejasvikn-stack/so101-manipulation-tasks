"""
Pour-to-50ml stop detector
---------------------------
Watches a webcam feed for a BLUE liquid rising toward a RED reference line
marked on the beaker at the 50ml height. Returns True the moment the blue
liquid's top edge reaches (or crosses) the red line.

Usage:
    Run this standalone to test/tune your color ranges with a live camera
    preview. Then import `liquid_has_reached_line()` into your robot
    control loop and call it every frame instead of reading a scale.
"""

import cv2
import numpy as np

# ── COLOR RANGES (tune these to your exact liquid + marker) ────────────────
# HSV is used instead of BGR because it separates "color" from "brightness",
# making detection much more stable under changing light.
BLUE_LOWER = np.array([100, 150, 50])
BLUE_UPPER = np.array([130, 255, 255])

RED_LOWER_1 = np.array([0, 120, 70])     # red wraps around the HSV hue wheel,
RED_UPPER_1 = np.array([10, 255, 255])   # so we need two ranges to catch it
RED_LOWER_2 = np.array([170, 120, 70])
RED_UPPER_2 = np.array([180, 255, 255])

MIN_BLOB_AREA = 200  # ignore tiny noisy specks of "blue" or "red"


def _topmost_row(mask, min_area=MIN_BLOB_AREA):
    """Return the topmost (smallest) pixel row containing enough of the
    target color, or None if nothing found. Smaller row number = higher
    up in the image = higher liquid level."""
    if cv2.countNonZero(mask) < min_area:
        return None
    ys, xs = np.where(mask > 0)
    return int(ys.min())


def find_red_line_row(frame):
    """Locate the red reference line once (call this at setup, or every
    frame if the camera/beaker could shift)."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1)
    mask2 = cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    return _topmost_row(red_mask)


def find_blue_liquid_row(frame):
    """Locate the current top edge of the blue liquid."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
    return _topmost_row(blue_mask)


def liquid_has_reached_line(frame, red_line_row, tolerance_px=3):
    """
    Core check for your control loop.
    Returns True once the blue liquid's top edge is at or above
    (i.e. numerically <=) the red line's row, within a small tolerance.
    """
    blue_row = find_blue_liquid_row(frame)
    if blue_row is None or red_line_row is None:
        return False
    return blue_row <= (red_line_row + tolerance_px)


# ── STANDALONE TEST / TUNING MODE ───────────────────────────────────────────
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    print("Show the empty beaker with red line visible, then press 'c' to calibrate the line.")
    print("Press 'q' to quit.")

    red_line_row = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            red_line_row = find_red_line_row(frame)
            print(f"Red line calibrated at pixel row: {red_line_row}")

        if red_line_row is not None:
            reached = liquid_has_reached_line(frame, red_line_row)
            cv2.line(frame, (0, red_line_row), (frame.shape[1], red_line_row), (0, 0, 255), 2)
            status = "STOP - 50ml REACHED" if reached else "pouring..."
            color = (0, 0, 255) if reached else (0, 255, 0)
            cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Pour Detector", frame)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
