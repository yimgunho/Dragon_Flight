from pico2d import *


class HPGauge:

    def __init__(self, x, y):
        self.image = load_image('hp_gauge.png')
        self.x = x
        self.y = y - 100
        self.hp = None

    def update(self, hp):
        self.y -= 10
        self.hp = hp

    def draw(self):
        self.image.clip_draw(0, 0, 100, 12, self.x, self.y, self.hp, 12)
