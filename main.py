import cv2
import mediapipe as mp
import pyautogui
import time
import os
import numpy as np
from collections import deque
from mediapipe.tasks.python import vision

# ==========================
# MODEL SETUP
# ==========================

model_path = os.path.join(
    os.path.dirname(__file__),
    "models",
    "hand_landmarker.task"
)

if not os.path.exists(model_path):
    print(f"Model not found: {model_path}")
    exit(1)

base_options = mp.tasks.BaseOptions(model_asset_path=model_path)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

hand_landmarker = vision.HandLandmarker.create_from_options(options)

# ==========================
# CAMERA
# ==========================

cap = cv2.VideoCapture(0)

# ==========================
# VARIABLES
# ==========================

cooldown = 1.5
last_action_time = 0

gesture_history = deque(maxlen=5)

prev_time = time.time()

draw_mode = False
canvas = None

prev_x = 0
prev_y = 0

# ==========================
# HELPER FUNCTION
# ==========================

def fingers_up(hand_landmarks):

    fingers = []

    # Thumb
    if hand_landmarks[4].x > hand_landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Index
    fingers.append(
        1 if hand_landmarks[8].y < hand_landmarks[6].y else 0
    )

    # Middle
    fingers.append(
        1 if hand_landmarks[12].y < hand_landmarks[10].y else 0
    )

    # Ring
    fingers.append(
        1 if hand_landmarks[16].y < hand_landmarks[14].y else 0
    )

    # Pinky
    fingers.append(
        1 if hand_landmarks[20].y < hand_landmarks[18].y else 0
    )

    return fingers

# ==========================
# MAIN LOOP
# ==========================

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    detection_result = hand_landmarker.detect(mp_image)

    gesture_text = "Waiting..."
    finger_text = "-"
    confidence_text = "-"

    current_time = time.time()
    fps = int(1 / (current_time - prev_time))
    prev_time = current_time

    if detection_result.hand_landmarks:

        hand_landmarks = detection_result.hand_landmarks[0]

        for landmark in hand_landmarks:

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 255, 0),
                -1
            )

        connections = [
            (0,1),(1,2),(2,3),(3,4),
            (5,6),(6,7),(7,8),
            (9,10),(10,11),(11,12),
            (13,14),(14,15),(15,16),
            (17,18),(18,19),(19,20),
            (0,5),(5,9),(9,13),(13,17),(0,17)
        ]

        for start_idx, end_idx in connections:

            start = hand_landmarks[start_idx]
            end = hand_landmarks[end_idx]

            x1 = int(start.x * w)
            y1 = int(start.y * h)

            x2 = int(end.x * w)
            y2 = int(end.y * h)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

        # ==========================
        # LASER POINTER
        # ==========================

        index_tip = hand_landmarks[8]

        laser_x = int(index_tip.x * w)
        laser_y = int(index_tip.y * h)

        cv2.circle(
            frame,
            (laser_x, laser_y),
            12,
            (0, 0, 255),
            -1
        )

        # ==========================
        # FINGER COUNT
        # ==========================

        fingers = fingers_up(hand_landmarks)

        total = fingers.count(1)

        finger_text = str(total)

        gesture_history.append(total)

        stable = False

        if len(gesture_history) == 5:
            stable = all(
                g == gesture_history[0]
                for g in gesture_history
            )

        confidence_text = "High"

        # ==========================
        # DRAWING MODE
        # ==========================

        if draw_mode:

            if prev_x == 0 and prev_y == 0:
                prev_x = laser_x
                prev_y = laser_y

            cv2.line(
                canvas,
                (prev_x, prev_y),
                (laser_x, laser_y),
                (0, 0, 255),
                5
            )

            prev_x = laser_x
            prev_y = laser_y

        else:

            prev_x = 0
            prev_y = 0

        # ==========================
        # GESTURE ACTIONS
        # ==========================

        now = time.time()

        if stable and (now - last_action_time > cooldown):

            # 5 fingers = Toggle Drawing Mode
            if total == 5:

                draw_mode = not draw_mode

                if draw_mode:
                    gesture_text = "DRAW MODE ON"
                else:
                    gesture_text = "DRAW MODE OFF"

                last_action_time = now

            elif total == 4:

                pyautogui.press("right")

                gesture_text = "NEXT SLIDE"

                last_action_time = now

            elif total == 3:

                pyautogui.press("left")

                gesture_text = "PREVIOUS SLIDE"

                last_action_time = now

            elif total == 2:

                pyautogui.press("f5")

                gesture_text = "START SHOW"

                last_action_time = now

            elif total == 1:

                canvas = np.zeros((h, w, 3), dtype=np.uint8)

                gesture_text = "CANVAS CLEARED"

                last_action_time = now

            elif total == 0:

                pyautogui.press("esc")

                gesture_text = "EXIT SHOW"

                last_action_time = now

    frame = cv2.addWeighted(frame, 1, canvas, 1, 0)

    cv2.rectangle(frame, (10, 10), (450, 190), (0, 0, 0), -1)

    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Fingers: {finger_text}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Gesture: {gesture_text}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Draw Mode: {'ON' if draw_mode else 'OFF'}",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 165, 255),
        2
    )

    cv2.imshow(
        "Gesture Control Presenter",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()