from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Variáveis de posição e orientação da caixa
box_position = [0.0, 1.5, 0.0]
box_angle = 90.0  # Ângulo de rotação da caixa em relação ao eixo Y
running = False
direction = 0
turning = 0
show_collisions = 0.1

# Variáveis de aceleração e velocidade máxima
move_speed = 0.0
turn_speed = 0.0
move_acceleration = 0.01
turn_acceleration = 0.2
max_move_speed = 0.1
max_turn_speed = 2.0

wheel_rotation = 0.0
original_wheel_rotation = 0.0

# Variáveis da câmera
camera_position = [0.0, 5.0, 15.0]
camera_distance = 10.0
camera_height = 5.0
camera_lag = 0.1
cone_positions = [(2, 2), (0, 2), (-2, 2), (2, 4), (-2, 4), (2, 6), (-2, 6)]

# Configurações iniciais da janela
def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def draw_car():
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(*box_position)
    glRotatef(box_angle, 0, 1, 0)
    glutSolidCube(2)
    glPushMatrix()
    glColor3f(0.0, 1.0, 0.0)
    glScalef(1.2, 0.4, 1)
    glScalef(1, 1, 0.66)
    glTranslatef(0, -1, 0)
    glutSolidCube(3)
    glPopMatrix()
    # Pneus dianteiros
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(1,-1,.7)
    glRotatef(wheel_rotation, 0, 1, 0)
    glutSolidCylinder(0.5, 0.4, 12, 12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(1,-1,-1.1)
    glRotatef(wheel_rotation, 0, 1, 0) 
    glutSolidCylinder(0.5, 0.4, 12, 12)
    glPopMatrix()
    # Pneus traseiros
    glPushMatrix()
    glTranslatef(-1,-1,-1.1)
    glutSolidCylinder(0.5, 0.4, 12, 12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-1,-1,0.7)
    glutSolidCylinder(0.5, 0.4, 12, 12)
    glPopMatrix()
    glPopMatrix()  # Reabilita culling após desenhar a caixa


def draw_cone(x, y):
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(x, 0, y)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(0.4, 1, 10, 10)
    glPopMatrix()

# Função de redimensionamento da janela
def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect, 1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Função para desenhar a plataforma, o cone e a caixa
def display():
    global camera_position

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Cálculo da posição desejada da câmera
    desired_cam_x = box_position[0] - camera_distance * math.cos(math.radians(box_angle))
    desired_cam_z = box_position[2] + camera_distance * math.sin(math.radians(box_angle))
    desired_cam_y = box_position[1] + camera_height

    # Interpolação para o efeito de atraso
    camera_position[0] += (desired_cam_x - camera_position[0]) * camera_lag
    camera_position[1] += (desired_cam_y - camera_position[1]) * camera_lag
    camera_position[2] += (desired_cam_z - camera_position[2]) * camera_lag

    gluLookAt(camera_position[0], camera_position[1], camera_position[2],
              box_position[0], box_position[1], box_position[2],
              0, 1, 0)

    # Desenha os cones primeiro (não transparentes)
    for i in cone_positions:
        draw_cone(i[0], i[1])

    # Agora desenha a caixa (transparente)
    draw_car()

    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, -50)
    glVertex3f(50, 0, -50)
    glVertex3f(50, 0, 50)
    glVertex3f(-50, 0, 50)
    glEnd()

    glutSwapBuffers()

# Função de teclado para mover e rotacionar a caixa
def keyboard(key, x, y):
    global running, direction, turning

    if key == b'a':
        turning = 1
    if key == b'd':
        turning = -1

    if key == b'w':
        direction = 0
        running = True
    elif key == b's':
        direction = 1
        running = True

    glutPostRedisplay()

def keyboard_up(key, x, y):
    global running, turning, move_speed, turn_speed
    if key in (b'w', b's'):
        running = False
        move_speed = 0
    if key in (b'a', b'd'):
        turning = 0

# Função de atualização para mover a caixa continuamente
def update(value):
    global box_position, box_angle, move_speed, turn_speed, running, direction, wheel_rotation

    # Aceleração linear
    if running:
        if move_speed < max_move_speed:
            move_speed += move_acceleration
    else:
        if move_speed > 0:
            move_speed -= move_acceleration
            move_speed = max(0, move_speed)

    # Aceleração de rotação
    if turning != 0:
        if turn_speed < max_turn_speed:
            turn_speed += turn_acceleration
    else:
        if turn_speed > 0:
            turn_speed -= turn_acceleration
            turn_speed = max(0, turn_speed)

    # Atualiza a posição e o ângulo da caixa
    if direction == 0:
        box_position[0] += move_speed * math.cos(math.radians(box_angle))
        box_position[2] -= move_speed * math.sin(math.radians(box_angle))
    elif direction == 1:
        box_position[0] -= move_speed * math.cos(math.radians(box_angle))
        box_position[2] += move_speed * math.sin(math.radians(box_angle))

    # Atualiza a rotação da caixa
    # Simplificando a rotação do ângulo
    if turning != 0 and running:
        # Ajusta o fator de rotação com base na direção e no sentido do giro
        angle_adjustment = turn_speed * turning * (-1 if direction == 1 else 1)
        box_angle += angle_adjustment
        
        # Atualiza a rotação dos pneus
        wheel_rotation += turn_speed * turning
        wheel_rotation = max(-20, min(wheel_rotation, 20))
    else:
        # Retorna a rotação dos pneus para a rotação original quando as teclas não estão pressionadas
        if wheel_rotation != 0:
            if wheel_rotation > 0:
                wheel_rotation -= turn_acceleration  # Suaviza a rotação negativa
            else:
                wheel_rotation += turn_acceleration  # Suaviza a rotação positiva
            if abs(wheel_rotation) < 0.1:  # Para a rotação se muito pequena
                wheel_rotation = 0

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Função principal
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("GTA 7")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up) 
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
