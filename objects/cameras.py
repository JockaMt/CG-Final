from OpenGL.GLU import *
import math

class Camera:
    def __init__(self, target):
        self.target = target
        self.position = [0.0, 5.0, 15.0]

    def update(self):
        pass


class TopViewCamera(Camera):
    def __init__(self, target):
        super().__init__(target)

    def update(self):
        self.position = [self.target.position[0], 15.0, self.target.position[2] + 10.0]
        gluLookAt(self.position[0], self.position[1], self.position[2], self.target.position[0], self.target.position[1], self.target.position[2], 0, 1, 0)


class FollowCamera(Camera):
    def __init__(self, target, distance=10.0, height=5.0, lag=0.1):
        super().__init__(target)
        self.distance = distance
        self.height = height
        self.lag = lag

    def update(self):
        desired_cam_x = self.target.position[0] - self.distance * math.cos(math.radians(self.target.angle))
        desired_cam_z = self.target.position[2] + self.distance * math.sin(math.radians(self.target.angle))
        desired_cam_y = self.target.position[1] + self.height

        self.position[0] += (desired_cam_x - self.position[0]) * self.lag
        self.position[1] += (desired_cam_y - self.position[1]) * self.lag
        self.position[2] += (desired_cam_z - self.position[2]) * self.lag

        gluLookAt(self.position[0], self.position[1], self.position[2], self.target.position[0], self.target.position[1], self.target.position[2], 0, 1, 0)

class FrontViewCamera(Camera):
    def __init__(self, target, height_offset=0.1, forward_offset=1.0):
        super().__init__(target)
        self.height_offset = height_offset
        self.forward_offset = forward_offset

    def update(self):
        self.position[0] = self.target.position[0] + self.forward_offset * math.cos(math.radians(self.target.angle))
        self.position[1] = self.target.position[1] + self.height_offset
        self.position[2] = self.target.position[2] - self.forward_offset * math.sin(math.radians(self.target.angle))

        look_at_x = self.position[0] + math.cos(math.radians(self.target.angle))
        look_at_z = self.position[2] - math.sin(math.radians(self.target.angle))

        gluLookAt(self.position[0], self.position[1], self.position[2], look_at_x, self.position[1], look_at_z, 0, 1, 0)
