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
        # Define os limites da caixa delimitadora do carro
        car_min_x = box_position[0] - box_size
        car_max_x = box_position[0] + box_size
        car_min_z = box_position[2] - box_size
        car_max_z = box_position[2] + box_size

        # Define os limites da caixa delimitadora do cone (com base no centro e no raio da base)
        cone_min_x = self.x - self.size
        cone_max_x = self.x + self.size
        cone_min_z = self.y - self.size
        cone_max_z = self.y + self.size

        # Verifica se as caixas delimitadoras se sobrepõem
        if (car_min_x <= cone_max_x and car_max_x >= cone_min_x and
            car_min_z <= cone_max_z and car_max_z >= cone_min_z):
            return True
        return False
