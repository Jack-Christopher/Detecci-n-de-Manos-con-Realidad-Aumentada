import glm
import numpy as np
from constants import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Cube:
    def __init__(self, coordinates, side, cube_color=(1, 1, 1)):
        self.side = side
        self.color = cube_color
        self.vertices = []
        self.coordinates = None
        self.shader_program = compileProgram(
            compileShader(vertex_shader_source, GL_VERTEX_SHADER),
            compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        )
        self.rotation_angle = 0
        self.set_coordinates(coordinates)
        self.update()

    def update(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vertices = [
            # front 
            self.coordinates[0] + self.side/2, self.coordinates[1] + self.side/2, self.coordinates[2] + self.side/2,
            self.coordinates[0] + self.side/2, self.coordinates[1] - self.side/2, self.coordinates[2] + self.side/2,
            self.coordinates[0] - self.side/2, self.coordinates[1] - self.side/2, self.coordinates[2] + self.side/2,
            self.coordinates[0] - self.side/2, self.coordinates[1] + self.side/2, self.coordinates[2] + self.side/2,
            # back
            self.coordinates[0] + self.side/2, self.coordinates[1] + self.side/2, self.coordinates[2] - self.side/2,
            self.coordinates[0] + self.side/2, self.coordinates[1] - self.side/2, self.coordinates[2] - self.side/2,
            self.coordinates[0] - self.side/2, self.coordinates[1] - self.side/2, self.coordinates[2] - self.side/2,
            self.coordinates[0] - self.side/2, self.coordinates[1] + self.side/2, self.coordinates[2] - self.side/2,
        ]
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.rotation_angle += 0.1
        # rotate all vertices around the z axis
        z_rotation_matrix = np.array([
            [np.cos(self.rotation_angle), -np.sin(self.rotation_angle), 0],
            [np.sin(self.rotation_angle), np.cos(self.rotation_angle), 0],
            [0, 0, 1]
        ])
        for i in range(8):
            self.vertices[i*3:i*3+3] = z_rotation_matrix @ self.vertices[i*3:i*3+3]
        # rotate all vertices around the y axis
        y_rotation_matrix = np.array([
            [np.cos(self.rotation_angle), 0, np.sin(self.rotation_angle)],
            [0, 1, 0],
            [-np.sin(self.rotation_angle), 0, np.cos(self.rotation_angle)]
        ])
        for i in range(8):
            self.vertices[i*3:i*3+3] = y_rotation_matrix @ self.vertices[i*3:i*3+3]
      


        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * self.vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)


    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
        self.update()
        
    # def zoom(z):
    # """Zooms the 3D object by the given amount."""
    # cube.scale(1 / (z + 1))
    
    def zoom(self):
        z = self.coordinates[2]
        self.side = self.side * (1 / (z + 1))
        self.update()

    def draw(self):
        glUseProgram(self.shader_program)

        glUniform3f(glGetUniformLocation(self.shader_program, "color"), *self.color)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 24)
        glBindVertexArray(0)

    def move(self, movement):
        self.coordinates += movement
        # for i in range(len(self.coordinates)):
        #     self.vertices[i] += movement[i]
        self.update()
