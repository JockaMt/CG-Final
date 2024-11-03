from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

from objects import car, scene

# Variáveis da câmera
camera_position = [0.0, 5.0, 15.0]
camera_distance = 10.0
camera_height = 5.0
camera_lag = 0.1

camera_top_view = False  # Adicione esta variável

carro = car.Carro()
cenario = scene.Scene()

# Configurações iniciais da janela
def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    # Configuração da iluminação
    # Habilita a iluminação
    glEnable(GL_LIGHTING)

    # Habilita a luz 0
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 10.0, 0.0, 1.0])  # Luz pontual acima do centro da cena




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

# Função para desenhar a plataforma, o cone e o carro
def display():
    global camera_position

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if camera_top_view:
        # Câmera fixa em visão superior
        camera_position = [carro.position[0], 15.0, carro.position[2] + 10.0]  # Posição fixa da câmera
        gluLookAt(camera_position[0], camera_position[1], camera_position[2],
                  carro.position[0], carro.position[1], carro.position[2],
                  0, 1, 0)
    else:
        # Cálculo da posição desejada da câmera
        desired_cam_x = carro.position[0] - camera_distance * math.cos(math.radians(carro.angle))
        desired_cam_z = carro.position[2] + camera_distance * math.sin(math.radians(carro.angle))
        desired_cam_y = carro.position[1] + camera_height

        # Interpolação para o efeito de atraso
        camera_position[0] += (desired_cam_x - camera_position[0]) * camera_lag
        camera_position[1] += (desired_cam_y - camera_position[1]) * camera_lag
        camera_position[2] += (desired_cam_z - camera_position[2]) * camera_lag

        gluLookAt(camera_position[0], camera_position[1], camera_position[2],
                  carro.position[0], carro.position[1], carro.position[2],
                  0, 1, 0)

    # Agora desenha o carro (transparente)
    carro.draw()
    cenario.draw()

    glutSwapBuffers()


# Função de teclado para mover e rotacionar o carro
def keyboard(key, x, y):
    global camera_top_view  # Certifique-se de usar a variável global
    if key == b'a':
        carro.turning = 1
    if key == b'd':
        carro.turning = -1

    if key == b'w':
        carro.direction = 0
        carro.running = True
    elif key == b's':
        carro.direction = 1
        carro.running = True

    if key == b'c':
        camera_top_view = not camera_top_view  # Alterna a visão da câmera

    glutPostRedisplay()


def keyboard_up(key, x, y):
    if key in (b'w', b's'):
        carro.running = False
        carro.move_speed = 0
    if key in (b'a', b'd'):
        carro.turning = 0

# Função de atualização para mover o carro continuamente
def update(value):
    carro.update(cenario.cones)
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Função principal
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Plataforma com Cone e Carro Móvel")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up) 
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
