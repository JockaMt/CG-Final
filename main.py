from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Variáveis de posição e orientação da caixa
box_position = [0.0, 1.5, 0.0]
box_angle = 0.0  # Ângulo de rotação da caixa em relação ao eixo Y
running = False
direction = 0
turning = 0

# Configurações iniciais da janela
def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Fundo branco
    glEnable(GL_DEPTH_TEST)            # Habilita teste de profundidade para 3D

def car():
    glColor4f(0.0, 0.0, 0.0, 0.1)
    glPushMatrix()
    glTranslatef(*box_position)  # Posiciona a caixa na posição calculada
    glRotatef(box_angle, 0, 1, 0)  # Rotaciona a caixa em torno do eixo Y
    glutSolidCube(2)
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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 5, 15, 0, 0, 0, 0, 1, 0)

    # Desenha a plataforma cinza
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(-5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glEnd()

    car()

    # Desenha o cone vermelho no centro
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(1, 3, 50, 50)
    glPopMatrix()

    # Desenha a caixa azul com movimento e rotação controlados
    glutSwapBuffers()

# Função de teclado para mover e rotacionar a caixa
def keyboard(key, x, y):
    global running, direction, turning

    if key == b'a':  # Rotaciona a caixa para a esquerda
        turning = 1
    elif key == b'd':  # Rotaciona a caixa para a direita
        turning = -1

    if key == b'w':  # Ativa o movimento para frente
        direction = 0
        running = True
    elif key == b's':  # Ativa o movimento para trás
        direction = 1
        running = True

    glutPostRedisplay()  # Redesenha a tela com a nova posição e orientação

def keyboard_up(key, x, y):
    global running, turning
    if key in (b'w', b's'):
        running = False
    if key in (b'a', b'd'):
        turning = 0

# Função de atualização para mover a caixa continuamente enquanto `running` é True
def update(value):
    global box_position, box_angle, running, direction
    move_step = 0.1  # Passo de movimento contínuo\
    turn_step = 2

    if turning == 1 and running:
        box_angle += turn_step
    elif turning == -1 and running:
        box_angle -= turn_step

    if running:
        if direction == 0:  # Movendo para frente
            box_position[0] += move_step * math.cos(math.radians(box_angle))
            box_position[2] -= move_step * math.sin(math.radians(box_angle))
        elif direction == 1:  # Movendo para trás
            box_position[0] -= move_step * math.cos(math.radians(box_angle))
            box_position[2] += move_step * math.sin(math.radians(box_angle))
    
    glutPostRedisplay()  # Redesenha a tela com a nova posição
    glutTimerFunc(16, update, 0)  # Chama `update` a cada 16 ms (~60 fps)

# Função principal
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Plataforma com Cone e Caixa Móvel")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)  # Registra a função do teclado
    glutKeyboardUpFunc(keyboard_up) 
    glutTimerFunc(0, update, 0)  # Inicia o loop de atualização
    glutMainLoop()

if __name__ == "__main__":
    main()
