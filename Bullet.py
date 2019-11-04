from pico2d import *


class Bullet:

    def __init__(self, x):
        self.image = load_image('bullet.png')
        self.x = x
        self.y = 100
        self.speed = 10
        self.atk = 20

    def update(self):
        self.y += self.speed

    def draw(self):
        self.image.draw(self.x, self.y, 105, 105)
