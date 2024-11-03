from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Carro:
    def __init__(self):
        self.position = [0.0, 1.5, 0.0]
        self.angle = 90.0
        self.move_speed = 0.0
        self.turn_speed = 0.0
        self.max_move_speed = 0.1
        self.max_turn_speed = 2.0
        self.wheel_rotation = 0.0
        self.running = False
        self.direction = 0
        self.turning = 0
        self.move_acceleration = 0.01
        self.turn_acceleration = 0.2
        self.car_color = (0.0, 1.0, 0.0)  # Cor inicial do carro
        self.size = 2  # Tamanho do cubo do carro

    def draw(self):
        # Definindo propriedades do material do carro
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.1, 0.1, 1.0])

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.angle, 0, 1, 0)
        glutSolidCube(2)
        glPushMatrix()
        glColor4f(0.0, 1.0, 0.0, 0.0)
        glScalef(1.2, 0.4, 1)
        glScalef(1, 1, 0.66)
        glTranslatef(0, -1, 0)
        glutSolidCube(3)
        glPopMatrix()

        # Desenho dos pneus
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.05, 0.05, 0.05, 1.0])
        self.draw_front_wheel(0.7)
        self.draw_front_wheel(-1.1)
        self.draw_back_wheel(-1.1)
        self.draw_back_wheel(0.7)

        glPopMatrix()

    def draw_front_wheel(self, z):
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(1, -1, z)
        glRotatef(self.wheel_rotation, 0, 1, 0)
        glutSolidCylinder(0.5, 0.4, 12, 12)
        glPopMatrix()

    def draw_back_wheel(self, z):
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(-1, -1, z)
        glutSolidCylinder(0.5, 0.4, 12, 12)
        glPopMatrix()

    def check_collision(self, cones):
        # Raio da esfera de colisão do carro
        car_collision_radius = 1.0  # Ajuste este valor conforme necessário para o tamanho do carro

        for cone in cones:
            # Raio da esfera de colisão do cone
            cone_collision_radius = cone.size  # Usando o atributo `size` como raio

            # Calcula a distância entre o centro do carro e o cone
            distance_x = self.position[0] - cone.x
            distance_z = self.position[2] - cone.y
            distance = math.sqrt(distance_x ** 2 + distance_z ** 2)

            # Verifica se a distância é menor que a soma dos raios das esferas
            if distance < (car_collision_radius + cone_collision_radius):
                return True  # Colisão detectada
        return False  # Nenhuma colisão

    def reset(self):
        self.position = [0.0, 1.5, 0.0]
        self.angle = 90.0

    def update(self, cones):
        # Atualiza a velocidade e a rotação do carro
        if self.running:
            if self.move_speed < self.max_move_speed:
                self.move_speed += self.move_acceleration
        else:
            if self.move_speed > 0:
                self.move_speed -= self.move_acceleration
                self.move_speed = max(0, self.move_speed)

        if self.turning != 0:
            if self.turn_speed < self.max_turn_speed:
                self.turn_speed += self.turn_acceleration
        else:
            if self.turn_speed > 0:
                self.turn_speed -= self.turn_acceleration
                self.turn_speed = max(0, self.turn_speed)

        # Atualiza a posição e a rotação do carro
        if self.direction == 0:
            self.position[0] += self.move_speed * math.cos(math.radians(self.angle))
            self.position[2] -= self.move_speed * math.sin(math.radians(self.angle))
        elif self.direction == 1:
            self.position[0] -= self.move_speed * math.cos(math.radians(self.angle))
            self.position[2] += self.move_speed * math.sin(math.radians(self.angle))

        if self.turning != 0 and self.running:
            angle_adjustment = self.turn_speed * self.turning * (-1 if self.direction == 1 else 1)
            self.angle += angle_adjustment
            
            # Atualiza a rotação dos pneus
            self.wheel_rotation += self.turn_speed * self.turning
            self.wheel_rotation = max(-20, min(self.wheel_rotation, 20))
        else:
            if self.wheel_rotation != 0:
                if self.wheel_rotation > 0:
                    self.wheel_rotation -= 2  # Suaviza a rotação negativa
                else:
                    self.wheel_rotation += 2  # Suaviza a rotação positiva
                if abs(self.wheel_rotation) < 0.1:  # Para a rotação se muito pequena
                    self.wheel_rotation = 0
        self.check_collision(cones)