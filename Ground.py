from pico2d import *
import game_framework

WIDTH = 750
HEIGHT = 900


class Ground:

    def __init__(self, a):
        self.image = load_image('background.jpg')
        self.frame = a
        self.first = HEIGHT * 0.5
        self.second = HEIGHT * 0.5 + HEIGHT
        self.velocity = 500

    def update(self):
        if self.first <= -(HEIGHT * 0.5):
            self.first = HEIGHT * 0.5 + HEIGHT
        elif self.second <= -(HEIGHT * 0.5):
            self.second = HEIGHT * 0.5 + HEIGHT

        self.first -= self.velocity * game_framework.frame_time
        self.second -= self.velocity * game_framework.frame_time

    def draw(self):
        self.image.clip_draw(720 * self.frame, 0, 720, 1280, WIDTH * 0.5, self.first, WIDTH, HEIGHT)
        self.image.clip_draw(720 * self.frame, 0, 720, 1280, WIDTH * 0.5, self.second, WIDTH, HEIGHT)
