import contextlib, sys
from OpenGL import GL as gl
import glfw
# https://www.glfw.org/docs/latest/quick.html
# https://www.glfw.org/docs/latest/  
#read://https_www.metamost.com/?url=https%3A%2F%2Fwww.metamost.com%2Fopengl-with-python%2F%23%3A~%3Atext%3DModern%2520OpenGL%2520with%2520shaders%2520is%2520used%2520with%2520Python%2CGoetz%252010%2520May%25202019%2520%25E2%2580%25A2%25205%2520min%2520read

@contextlib.contextmanager
def create_main_window():
    if not glfw.init():
        sys.exit(1)
    try:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        title = 'Tutorial 2: First Triangle'
        window = glfw.create_window(500, 400, title, None, None)
        if not window:
            sys.exit(2)
        glfw.make_context_current(window)

        glfw.set_input_mode(window, glfw.STICKY_KEYS, True)
        gl.glClearColor(0, 0, 0.4, 0)

        yield window

    finally:
        glfw.terminate()

if __name__ == '__main__':
    with create_main_window() as window:
        while (
            glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
            not glfw.window_should_close(window)
        ):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(window)
            glfw.poll_events()