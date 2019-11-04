from pico2d import *

WIDTH = 700
HEIGHT = 840


class Background:

    def __init__(self, a):
        self.image = load_image('background.jpg')
        self.frame = a
        self.first = HEIGHT // 2
        self.second = HEIGHT // 2 + HEIGHT

    def update(self):
        if self.first <= -(HEIGHT // 2):
            self.first = HEIGHT // 2 + HEIGHT
        elif self.second <= -(HEIGHT // 2):
            self.second = HEIGHT // 2 + HEIGHT

        self.first -= 10
        self.second -= 10

    def draw(self):
        self.image.clip_draw(720 * self.frame, 0, 720, 1280, WIDTH // 2, self.first, WIDTH, HEIGHT)
        self.image.clip_draw(720 * self.frame, 0, 720, 1280, WIDTH // 2, self.second, WIDTH, HEIGHT)
