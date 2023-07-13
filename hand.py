import glm
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import utils as ut
from constants import *

class Hand:
    def __init__(self, landmarks):
        self.color = hand_color
        self.lines = []
        self.movement = 0
        self.landmarks = landmarks
        self.shader_program = compileProgram(
            compileShader(vertex_shader_source, GL_VERTEX_SHADER),
            compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        )
        self.landmark_indices = [
            # Fingers
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20],
            # Thumb
            [1, 2, 3, 4],
            # Palm
            [1, 0, 5, 9, 13, 17, 0],
        ]
        self.set_landmarks(landmarks)
        self.update()

    def set_landmarks(self, landmarks):
        landmarks = np.array(landmarks)
        landmarks[:, 1] *= -1
        # convert to OpenGL coordinates
        landmarks[:, 0] = (landmarks[:, 0] * 2) - 1
        landmarks[:, 1] = (landmarks[:, 1] * 2) + 1
        landmarks[:, 2] = (landmarks[:, 2] * 20000) -0.5
        landmarks[:, 2] = (landmarks[:, 2] * 2) - 1
        
        self.movement = landmarks[0] - self.landmarks[0]
        self.landmarks = landmarks
        self.update()

        # print(self.landmarks)

    def update(self):
        self.clean()

        for indices in self.landmark_indices:
            vertices = self.landmarks[indices]
            for i in range(len(vertices) - 1):
                self.lines.append(ut.Line(vertices[i], vertices[i + 1], self.shader_program, self.color))


    def draw(self):
        for line in self.lines:
            line.draw()


    def clean(self):
        for line in self.lines:
            del line
        self.lines = []


    def collides(self, vertices):
        # print("Checking collision in hand")
        # print(vertices)

        for idx, line in enumerate(self.lines):
            # print(idx, end=" ")
            if line.collides(vertices):
                return True
        return False