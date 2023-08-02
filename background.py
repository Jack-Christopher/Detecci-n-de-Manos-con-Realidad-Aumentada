import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
from PIL import Image


def compile_shader(shader_type, source_code):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source_code)
    glCompileShader(shader)

    # Verificar si hubo errores de compilación
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise Exception('Error de compilación del shader: {}'.format(glGetShaderInfoLog(shader)))

    return shader


class Background:
    def __init__(self, texture_path):
        # Definir los vértices del cuadrado
        self.vertices = [
            -1, -1, 0.0,  # Vértice inferior izquierdo
            1, -1, 0.0,   # Vértice inferior derecho
            1, 1, 0.0,    # Vértice superior derecho
            -1, 1, 0.0     # Vértice superior izquierdo
        ]

        # Coordenadas de textura correspondientes a los vértices del cuadrado
        self.tex_coords = [
            0.0, 0.0,  # Coordenada de textura para el vértice inferior izquierdo
            1.0, 0.0,  # Coordenada de textura para el vértice inferior derecho
            1.0, 1.0,  # Coordenada de textura para el vértice superior derecho
            0.0, 1.0   # Coordenada de textura para el vértice superior izquierdo
        ]

        # Índices de los vértices para definir los triángulos del cuadrado
        self.indices = [0, 1, 2, 0, 2, 3]

        # Crear la textura y cargar la imagen
        self.texture_id = self.create_texture(texture_path)

        # Compilar shaders y crear el programa de shader
        self.shader_program = self.create_shader_program()

        # Obtener la ubicación de los atributos y uniformes
        self.position_attr = glGetAttribLocation(self.shader_program, "position")
        self.tex_coord_attr = glGetAttribLocation(self.shader_program, "texCoord")
        self.texture_sampler_uniform = glGetUniformLocation(self.shader_program, "textureSampler")

        # Crear el VAO (Vertex Array Object) y configurarlo
        self.vao = self.create_vao()


    def create_texture(self, image_path):
        # Cargar la imagen utilizando PIL
        image = Image.open(image_path)
        image_data = image.convert("RGBA").tobytes()

        # Obtener las dimensiones de la imagen
        width, height = image.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Configurar parámetros de la textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Cargar la imagen de la textura
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        return texture_id

    def create_shader_program(self):
        vertex_shader_source = """
            #version 330
            layout(location = 0) in vec3 position;
            layout(location = 1) in vec2 texCoord;
            out vec2 texCoord0;

            void main()
            {
                gl_Position = vec4(position, 1.0);
                texCoord0 = texCoord;
            }
        """

        fragment_shader_source = """
            #version 330
            in vec2 texCoord0;
            out vec4 fragColor;
            uniform sampler2D textureSampler;

            void main()
            {
                fragColor = texture(textureSampler, texCoord0);
            }
        """

        vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_source)
        fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_source)

        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)

        # Verificar si hubo errores de enlace
        if not glGetProgramiv(shader_program, GL_LINK_STATUS):
            raise Exception('Error de enlace del programa de shader: {}'.format(glGetProgramInfoLog(shader_program)))

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return shader_program

    def create_vao(self):
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        # Crear el VBO (Vertex Buffer Object) de los vértices y cargar los datos
        vbo_vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(self.vertices), (GLfloat * len(self.vertices))(*self.vertices),
                     GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.position_attr)
        glVertexAttribPointer(self.position_attr, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Crear el VBO de las coordenadas de textura y cargar los datos
        vbo_tex_coords = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_tex_coords)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(self.tex_coords), (GLfloat * len(self.tex_coords))(*self.tex_coords),
                     GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.tex_coord_attr)
        glVertexAttribPointer(self.tex_coord_attr, 2, GL_FLOAT, GL_FALSE, 0, None)

        # Crear el EBO (Element Buffer Object) de los índices y cargar los datos
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(self.indices), (GLuint * len(self.indices))(*self.indices),
                     GL_STATIC_DRAW)

        return vao

    def draw(self):
        # Usar el programa de shaders
        glUseProgram(self.shader_program)

        # Establecer la textura activa en la unidad de textura 0
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.texture_sampler_uniform, 0)

        # Dibujar el cuadrado
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)