window_height = 600
window_width = 600
window_title = "OpenGL Window"
hand_color = (0.6, 0.6, 0.6)
cube_color = (0.3, 0.3, 0.3)

# Define the vertex shader source
vertex_shader_source = """
    #version 330
    in vec2 position;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
    }
"""

# Define the fragment shader source
fragment_shader_source = """
    #version 330
    out vec4 fragColor;
    uniform vec3 color;
    void main()
    {
        fragColor = vec4(color, 1.0);
    }
"""
