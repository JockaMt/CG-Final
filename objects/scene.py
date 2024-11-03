from OpenGL.GL import *
from objects.cone import Cone

def surface():
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, -50)
    glVertex3f(50, 0, -50)
    glVertex3f(50, 0, 50)
    glVertex3f(-50, 0, 50)
    glEnd()


class Scene:
    def __init__(self):
        self.cones = [
            Cone(2, 3), Cone(0, 3), Cone(-2, 3),
            Cone(2, 5), Cone(-2, 5), Cone(2, 7), Cone(-2, 7),
            Cone(2, 9), Cone(-2, 9), Cone(2, 11), Cone(-2, 11),
        ]

    def draw(self):
        surface()
        for cone in self.cones:
            cone.draw()

    def update(self, box_position):
        for cone in self.cones:
            if cone.check_collision(box_position, 1.0):
                print("Colisão detectada com o cone!")
