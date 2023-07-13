
import utils as ut

# OpenCV and mediapipe libraries
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import uuid
import os
import numpy as np


# OpenCV initialization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        image, results = ut.get_image(cap)

        if results.multi_hand_landmarks:
            for idx, hand in enumerate(results.multi_hand_landmarks):
                current_landmarks = []
               
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hand Tracking', image)

        # Detener el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
