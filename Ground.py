from pico2d import *
import game_framework
from game_world import HEIGHT, WIDTH, SPEED_PPS


class Ground:

    def __init__(self, a):
        self.image = load_image('background.jpg')
        self.frame = a
        self.first = HEIGHT * 0.5
        self.second = HEIGHT * 0.5 + HEIGHT
        self.timer = 0

    def update(self):
        if self.first <= -(HEIGHT * 0.5):
            self.first = HEIGHT * 0.5 + HEIGHT
        elif self.second <= -(HEIGHT * 0.5):
            self.second = HEIGHT * 0.5 + HEIGHT

        self.first -= int(SPEED_PPS * 0.04)
        self.second -= int(SPEED_PPS * 0.04)
        self.timer += SPEED_PPS * 0.01

    def draw(self):
        self.image.clip_draw(720 * self.frame, 0, 720, 1280, WIDTH * 0.5, self.first, WIDTH, HEIGHT)
        self.image.clip_draw(720 * self.frame, 0, 720, 1280, WIDTH * 0.5, self.second, WIDTH, HEIGHT)
