from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos

class Sign:
    def __init__(self, x, y, color=(1.0, 1.0, 0.0)):
        self.x = x
        self.y = y
        self.color = color  # RGB color for the sign background
        self.angle = 0  # Initial rotation angle in degrees

    def draw_curve_symbol(self):
        """Draw a simple curve symbol on the sign."""
        glColor3f(0.0, 0.0, 0.0)  # Black color for the symbol

        glBegin(GL_LINE_STRIP)
        for angle in range(0, 180, 10):
            rad = angle * 3.14159 / 180
            glVertex3f(0.2 * cos(rad), 0.2 * sin(rad) + 0.5, 0.01)  # Offset in z to avoid z-fighting
        glEnd()

        # Arrowhead for the curve
        glBegin(GL_TRIANGLES)
        glVertex3f(0.18, 0.7, 0.01)
        glVertex3f(0.3, 0.6, 0.01)
        glVertex3f(0.15, 0.5, 0.01)
        glEnd()

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.y)
        glRotatef(self.angle, 0, 1, 0)  # Rotate around the Y-axis

        # Draw the sign background
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0.0, 0.0)
        glVertex3f(0.5, 0.0, 0.0)
        glVertex3f(0.5, 1.0, 0.0)
        glVertex3f(-0.5, 1.0, 0.0)
        glEnd()

        # Draw the curve symbol
        self.draw_curve_symbol()

        glPopMatrix()

    def set_rotation(self, angle):
        """Set the rotation angle of the sign."""
        self.angle = angle
