from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


class Cone:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw(self):
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.25, 0.0, 1.0])

        # Desenhar a plataforma (cilindro)
        glColor3f(1, 1, 1)  # Cor branco para a plataforma
        glPushMatrix()
        glTranslatef(self.x, 0, self.y)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 0.5, 0.5, 0.1, 10, 10)  # Plataforma do cilindro
        glPopMatrix()

        # Desenhar o cone
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(self.x, 0.1, self.y)  # Levanta o cone para cima da plataforma
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(0.4, 1, 10, 10)
        glPopMatrix()

        # Desenhar a linha branca no meio
        glColor3f(1.0, 1.0, 1.0)  # Cor branca para a linha
        glPushMatrix()
        glTranslatef(self.x, 0.55, self.y)  # Posição da linha em relação ao cone
        glRotatef(-90, 1, 0, 0)
        glLineWidth(2)  # Largura da linha
        gluCylinder(gluNewQuadric(), 0.02, 0.02, 0.5, 10, 10)  # Linha em cima do cone
        glPopMatrix()

    def check_collision(self, box_position, box_size):
        # Calcular a distância entre o carro e a posição do cone
        cone_distance = math.sqrt((self.x - box_position[0]) ** 2 + (self.y - box_position[2]) ** 2)

        # Verifica se a distância é menor que um determinado valor (ex. raio da colisão)
        if cone_distance < (box_size + 0.5):  # Supondo box_size como a largura do carro
            print("Colisão com o cone detectada!")
