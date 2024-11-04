from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Carro:
    def __init__(self):
        self.position = [0.0, 1.5, 0.0]
        self.angle = -90.0
        self.move_speed = 0.0
        self.turn_speed = 0.0
        self.max_move_speed = 0.1
        self.max_turn_speed = 2.0
        self.wheel_rotation = 0.0
        self.running = False
        self.direction = 0
        self.turning = 0
        self.move_acceleration = 0.01
        self.turn_acceleration = 0.1
        self.car_color = (0.0, 1.0, 0.0)
        self.size = 2
        self.target_position = [0.0, 1.5, -7.0]
        self.target_radius = 1.0

    def draw(self):

        # Configurar luzes para os faróis
        glLightfv(GL_LIGHT1, GL_POSITION, [
            self.position[0] + 1 * math.cos(math.radians(self.angle)),
            self.position[1] + 1,  # Levantar um pouco a luz
            self.position[2] - 1 * math.sin(math.radians(self.angle)),
            1.0
        ])  # Farol direito

        glLightfv(GL_LIGHT2, GL_POSITION, [
            self.position[0] - 1 * math.cos(math.radians(self.angle)),
            self.position[1] + 1,  # Levantar um pouco a luz
            self.position[2] + 1 * math.sin(math.radians(self.angle)),
            1.0
        ])  # Farol esquerdo

        # Configuração das luzes (cor e intensidade)
        light_color = [1.0, 1.0, 1.0, 1.0]  # Luz branca
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_color)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, light_color)

        # Habilitar as luzes
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)

        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.1, 0.1, 1.0])

        # Base do carro
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
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 0.2, 1, 1])
        glTranslatef(1, .55, 0)
        glScalef(0.01, 0.2, 0.6)
        glutSolidCube(3)
        glPopMatrix()
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 0, 0, 1.0])
        glTranslatef(-1, .55, 0)
        glScalef(0.01, 0.2, 0.6)
        glutSolidCube(3)
        glPopMatrix()
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 1, 1, 1.0])
        glTranslatef(1.8, -.2, 0.7)
        glScalef(0.05, 0.5, 0.5)
        glutSolidCube(1)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.8, -.2, -0.7)
        glScalef(0.05, 0.5, 0.5)
        glutSolidCube(1)
        glPopMatrix()
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0, 0, 1.0])
        glTranslatef(-1.8, 0, 0.7)
        glScalef(0.05, 0.1, 0.5)
        glutSolidCube(1)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-1.8, 0, -0.7)
        glScalef(0.05, 0.1, 0.5)
        glutSolidCube(1)
        glPopMatrix()

        # Pneus
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
        # A esfera foi a melhor forma que achei para detectar colisões, tentei cubos, mas não girava com o carro
        car_collision_radius = 1.0

        for cone in cones:
            cone_collision_radius = cone.size
            distance_x = self.position[0] - cone.x
            distance_z = self.position[2] - cone.y
            distance = math.sqrt(distance_x ** 2 + distance_z ** 2)

            if distance < (car_collision_radius + cone_collision_radius):
                return True

        return False

    def reset(self):
        self.position = [0.0, 1.5, 0.0]
        self.angle = -90.0

    def update(self, cones):
        # Atualiza a posição do carro
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

        if self.direction == 0:
            self.position[0] += self.move_speed * math.cos(math.radians(self.angle))
            self.position[2] -= self.move_speed * math.sin(math.radians(self.angle))
        elif self.direction == 1:
            self.position[0] -= self.move_speed * math.cos(math.radians(self.angle))
            self.position[2] += self.move_speed * math.sin(math.radians(self.angle))

        if self.turning != 0 and self.running:
            angle_adjustment = self.turn_speed * self.turning * (-1 if self.direction == 1 else 1)
            self.angle += angle_adjustment

            self.wheel_rotation += self.turn_speed * self.turning
            self.wheel_rotation = max(-20, min(self.wheel_rotation, 20))
        else:
            if self.wheel_rotation != 0:
                if self.wheel_rotation > 0:
                    self.wheel_rotation -= 2
                else:
                    self.wheel_rotation += 2
                if abs(self.wheel_rotation) < 0.1:
                    self.wheel_rotation = 0

        # Verificar colisão com cones
        if self.check_collision(cones):
            print("Colisão detectada com um cone!")

    def check_proximity_to_target(self):
        # Calcular a distância até a posição alvo
        distance_x = self.position[0] - self.target_position[0]
        distance_z = self.position[2] - self.target_position[2]
        distance = math.sqrt(distance_x ** 2 + distance_z ** 2)

        # Verificar se a distância está dentro do raio de proximidade
        return distance < self.target_radius