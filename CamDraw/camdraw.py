import cv2
import mediapipe as mp
import numpy as np
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cv2.namedWindow("Hand Paint", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Paint", 1920, 1080)

canvas = None
prev_x, prev_y = None, None

colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 0)]
color_names = ["Red", "Green", "Blue", "Yellow", "Eraser"]
selected_color = colors[0]

draw_thickness = 6
eraser_thickness = 50

pinch_threshold = 40  # pixels: adjust to tune sensitivity

drawing_mode = False      # toggles when a pinch is detected (rising edge)
prev_pinched = False      # previous frame pinch state

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    button_width = 120
    button_height = 100
    top_area_bottom = 10 + button_height
    for i, color in enumerate(colors):
        cv2.rectangle(frame, (10 + i * button_width, 10), (10 + (i + 1) * button_width, 10 + button_height), color, -1)
        cv2.putText(frame, color_names[i], (15 + i * button_width, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            index_y = int(hand_landmarks.landmark[8].y * frame.shape[0])
            thumb_x = int(hand_landmarks.landmark[4].x * frame.shape[1])
            thumb_y = int(hand_landmarks.landmark[4].y * frame.shape[0])

            # select color buttons by touching top area (no toggle when selecting)
            if index_y < top_area_bottom:
                for i in range(len(colors)):
                    if 10 + i * button_width < index_x < 10 + (i + 1) * button_width:
                        selected_color = colors[i]
                        prev_x, prev_y = None, None

            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # detect pinch (current)
            is_pinched = distance < pinch_threshold

            # toggle drawing mode on pinch rising edge (but don't toggle if finger is in top button area)
            if is_pinched and not prev_pinched and index_y >= top_area_bottom:
                drawing_mode = not drawing_mode
                if drawing_mode:
                    prev_x, prev_y = index_x, index_y
                else:
                    prev_x, prev_y = None, None

            prev_pinched = is_pinched

            # If drawing mode is on, draw following the index finger continuously
            if drawing_mode:
                if prev_x is None or prev_y is None:
                    prev_x, prev_y = index_x, index_y
                thickness = eraser_thickness if selected_color == colors[4] else draw_thickness
                cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), selected_color, thickness)
                prev_x, prev_y = index_x, index_y
                # visual feedback for drawing mode
                cv2.circle(frame, (index_x, index_y), 8, selected_color, -1)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        # no hand detected; stop drawing continuity until hand returns
        prev_x, prev_y = None, None
        prev_pinched = False

    # show drawing status
    status_text = "Drawing: ON" if drawing_mode else "Drawing: OFF"
    cv2.putText(frame, status_text, (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    frame = cv2.add(frame, canvas)

    key = cv2.waitKey(1) & 0xFF
    cv2.imshow("Hand Paint", frame)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
