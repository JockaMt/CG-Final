from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


class Cone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0.5  # Define o tamanho do cone para colisão (raio da base do cilindro)

    def draw(self):

        # Base do cone
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glColor3f(1, 1, 1)  # Cor branco para a plataforma
        glPushMatrix()
        glTranslatef(self.x, 0, self.y)
        glRotatef(-90, 1, 0, 0)
        glutSolidCylinder(0.5, 0.1, 10, 10)  # Plataforma do cilindro
        glPopMatrix()

        # Cone
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.25, 0.0, 1.0])
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(self.x, 0.1, self.y)
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(0.4, 1, 10, 10)
        glPopMatrix()

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glTranslatef(self.x, 0.55, self.y)
        glRotatef(-90, 1, 0, 0)
        glLineWidth(2)
        gluCylinder(gluNewQuadric(), 0.02, 0.02, 0.5, 10, 10)
        glPopMatrix()

    def check_collision(self, box_position, box_size):
        car_min_x = box_position[0] - box_size
        car_max_x = box_position[0] + box_size
        car_min_z = box_position[2] - box_size
        car_max_z = box_position[2] + box_size

        cone_min_x = self.x - self.size
        cone_max_x = self.x + self.size
        cone_min_z = self.y - self.size
        cone_max_z = self.y + self.size

        if (car_min_x <= cone_max_x and car_max_x >= cone_min_x and
            car_min_z <= cone_max_z and car_max_z >= cone_min_z):
            return True
        return False
