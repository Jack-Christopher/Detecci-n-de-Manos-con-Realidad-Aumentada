import utils as ut
import numpy as np

# OpenGL and GLFW libraries
import glfw
from hand import Hand
from OpenGL.GL import *

# OpenCV and mediapipe libraries
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import uuid
import os
import numpy as np

# OpenGL initialization
window = ut.init_glfw()
# Enable blending for transparency
# glEnable(GL_BLEND)
# glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# OpenCV initialization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

HANDS = []

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened() and not glfw.window_should_close(window):
        image, results = ut.get_image(cap, hands)

        if results.multi_hand_landmarks:
            for idx, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
                current_landmarks = [(landmark.x, landmark.y, landmark.z) for landmark in hand.landmark]

                if idx < len(HANDS):
                    HANDS[idx].set_landmarks(current_landmarks)
                else:
                    HANDS.append(Hand(current_landmarks))
            HANDS = HANDS[:len(results.multi_hand_landmarks)]
        else:
            HANDS = []

        cv2.imshow('Hand Tracking', image)

        # Clear the color buffer
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw the hands
        for hand in HANDS:
            hand.draw()

        # Swap buffers
        glfw.swap_buffers(window)
        # Poll events
        glfw.poll_events()

        # Detener el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release all resources
cap.release()
cv2.destroyAllWindows()
glfw.terminate()