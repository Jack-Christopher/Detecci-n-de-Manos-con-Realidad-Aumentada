import utils as ut
import numpy as np

# OpenGL and GLFW libraries
import glm
import glfw
from hand import Hand
from OpenGL.GL import *
from cube import Cube
from background import Background

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

# OpenCV initialization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

HANDS = []
cube = Cube(glm.vec3(0, 0, 0), 0.4, cube_color=(0, 0, 1))
cube2 = Cube(glm.vec3(0.5, 0.5, 0.5), 0.2, cube_color=(0, 1, 0))

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened() and not glfw.window_should_close(window):

        #OPEN CV

        image, results = ut.get_image(cap, hands)
        image2 = cv2.flip(image, 0)
        cv2. imwrite('frame.jpg', image2)

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

        #OPEN GL

        # Clear the color buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Draw the background
        background = Background("frame.jpg")

        background.draw()



        # detect collisions
        for hand in HANDS:
            # reshape the vertices to be a list of points in 3d
            if hand.collides((cube.vertices).reshape(-1, 3)):
                # print("collision")
                cube.move(hand.movement)
                cube.zoom()
                # print("("+str(hand.movement[0])+", "+str(hand.movement[1])+", "+str(hand.movement[2])+")")

        # Draw the hands
        for hand in HANDS:
            # print("("+str(hand.landmarks[0][0])+", "+str(hand.landmarks[0][1])+", "+str(hand.landmarks[0][2])+")")
            hand.draw()

        cube.update()
        cube.draw()
        cube2.update()
        cube2.draw()

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

os.remove("frame.jpg")