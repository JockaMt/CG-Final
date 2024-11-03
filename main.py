import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

from objects import car, scene

camera_position = [0.0, 5.0, 15.0]
camera_distance = 10.0
camera_height = 5.0
camera_lag = 0.1

camera_top_view = False

carro = car.Carro()
cenario = scene.Scene()

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

def render_text(text, x_pos, y_pos):
    text_surface = font.render(text, True, (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    width, height = text_surface.get_size()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(x_pos, y_pos)
    glTexCoord2f(1, 1); glVertex2f(x_pos + width, y_pos)
    glTexCoord2f(1, 0); glVertex2f(x_pos + width, y_pos + height)
    glTexCoord2f(0, 0); glVertex2f(x_pos, y_pos + height)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glDeleteTextures([texture_id])

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 10.0, 0.0, 1.0])

def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect, 1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    global camera_position

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if camera_top_view:
        camera_position = [carro.position[0], 15.0, carro.position[2] + 10.0]
        gluLookAt(camera_position[0], camera_position[1], camera_position[2],
                  carro.position[0], carro.position[1], carro.position[2],
                  0, 1, 0)
    else:
        desired_cam_x = carro.position[0] - camera_distance * math.cos(math.radians(carro.angle))
        desired_cam_z = carro.position[2] + camera_distance * math.sin(math.radians(carro.angle))
        desired_cam_y = carro.position[1] + camera_height

        camera_position[0] += (desired_cam_x - camera_position[0]) * camera_lag
        camera_position[1] += (desired_cam_y - camera_position[1]) * camera_lag
        camera_position[2] += (desired_cam_z - camera_position[2]) * camera_lag

        gluLookAt(camera_position[0], camera_position[1], camera_position[2],
                  carro.position[0], carro.position[1], carro.position[2],
                  0, 1, 0)

    carro.draw()
    cenario.draw()

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    render_text("W, A, S, D para se mover", 10, 10)
    render_text("C para alterar a câmera", 10, 50)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glutSwapBuffers()

def keyboard(key, x, y):
    global camera_top_view
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
        camera_top_view = not camera_top_view
    glutPostRedisplay()

def keyboard_up(key, x, y):
    if key in (b'w', b's'):
        carro.running = False
        carro.move_speed = 0
    if key in (b'a', b'd'):
        carro.turning = 0

def update(value):
    carro.update(cenario.cones)
    collided = carro.check_collision(cenario.cones)
    if collided:
        carro.reset()
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("CG - Carros")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up) 
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()