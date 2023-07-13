#####################################
#   OpenCV and mediapipe functions  #
#####################################
import cv2

# Process the image and return the image and the results
def get_image(cap, hands):
    ret, frame = cap.read()
    # revert frame because it is mirrored
    frame = cv2.flip(frame, 1)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image, results


#####################################
#     OpenGL and GLFW functions     #
#####################################
import numpy as np
import glfw
from OpenGL.GL import *

# Callback function for keyboard input
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

# Initialize GLFW and return the window
def init_glfw():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(800, 600, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return

    # Set the window as the current OpenGL context
    glfw.make_context_current(window)

    # Set the callback function for keyboard input
    glfw.set_key_callback(window, key_callback)

    return window


class Line:
    def __init__(self, start, end, shader_program, color):
        self.start = start
        self.end = end
        self.shader_program = shader_program
        self.color = color
        self.linewidth = 5
        self.vao = 0
        self.vbo = 0

        self.create()

    def create(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vertices = [self.start, self.end]
        vertices = [coord for vertex in vertices for coord in vertex]
        vertices = np.array(vertices, dtype=np.float32)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def draw(self):
        glUseProgram(self.shader_program)

        glUniform3f(glGetUniformLocation(self.shader_program, "color"), *self.color)
        glLineWidth(self.linewidth)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0, 2)
        glBindVertexArray(0)


    def __del__(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])