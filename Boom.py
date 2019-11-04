from pico2d import *


class Boom:
    def __init__(self, x, y):
        self.image = load_image('boom.png')
        self.frame = 0
        self.x = x
        self.y = y

    def update(self):
        self.frame = self.frame + 1

    def draw(self):
        self.image.clip_draw(self.frame * 120, 0, 120, 140, self.x, self.y)