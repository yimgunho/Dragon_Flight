from pico2d import *


class Dragon:

    def __init__(self, x):
        self.image = load_image('green_dragon.png')
        self.frame = 0
        self.x = x
        self.y = 1000
        self.hp = 40

    def update(self):
        self.y -= 10
        self.frame = (self.frame + 1) % 9

    def damage(self, atk):
        self.hp -= atk

    def draw(self):
        if self.hp > 0:
            self.image.clip_draw(self.frame * 200, 0, 200, 200, self.x, self.y, 130, 130)