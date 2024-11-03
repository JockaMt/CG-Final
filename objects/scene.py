from OpenGL.GL import *
from objects.cone import Cone  # Certifique-se de que este import esteja correto

def surface():
    # Define as propriedades do material do chão
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])

    glColor3f(0.5, 0.5, 0.5)  # Você ainda pode definir uma cor base para o chão
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, -50)
    glVertex3f(50, 0, -50)
    glVertex3f(50, 0, 50)
    glVertex3f(-50, 0, 50)
    glEnd()


class Scene:
    def __init__(self):
        # Cria uma lista de cones em diferentes posições
        self.cones = [
            Cone(2, 3), Cone(0, 3), Cone(-2, 3),
            Cone(2, 5), Cone(-2, 5), Cone(2, 7), Cone(-2, 7),
            Cone(2, 9), Cone(-2, 9), Cone(2, 11), Cone(-2, 11),
        ]

    def draw(self):
        # Desenha a superfície
        surface()
        # Desenha cada cone na cena
        for cone in self.cones:
            cone.draw()

    def update(self, box_position):
        # Verifica colisão para cada cone com a posição do carro
        for cone in self.cones:
            if cone.check_collision(box_position, 1.0):  # Supondo que o box_position seja a posição do carro
                print("Colisão detectada com o cone!")
