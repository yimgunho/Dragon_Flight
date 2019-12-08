from pico2d import *
import game_framework
from game_world import HEIGHT, WIDTH
import main_state

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
SPEED_KMPH = 10.0  # Km / Hour
SPEED_MPM = (SPEED_KMPH * 1000.0 / 60.0)
SPEED_MPS = (SPEED_MPM / 60.0)
SPEED_PPS = (SPEED_MPS * PIXEL_PER_METER)

class Ground:
    images = None

    def __init__(self, a):
        if Ground.images == None:
            Ground.images = []
            Ground.images += [load_image('stage1.jpg')]
            Ground.images += [load_image('stage2.jpg')]
            Ground.images += [load_image('stage3.jpg')]
            Ground.images += [load_image('stage4.jpg')]
            Ground.images += [load_image('stage5.jpg')]

        self.frame = a
        self.first = HEIGHT * 0.5
        self.second = HEIGHT * 0.5 + HEIGHT
        self.timer = 0
        self.stage_level = 0

    def update(self):
        if self.first <= -(HEIGHT * 0.5):
            self.first = HEIGHT * 0.5 + HEIGHT
        elif self.second <= -(HEIGHT * 0.5):
            self.second = HEIGHT * 0.5 + HEIGHT

        self.first -= int(SPEED_PPS * 0.04)
        self.second -= int(SPEED_PPS * 0.04)
        self.timer += SPEED_PPS * 0.01

    def draw(self):
        self.images[self.stage_level].clip_draw(720 * self.frame, 0, 720, 1280, WIDTH * 0.5, self.first, WIDTH, HEIGHT)
        self.images[self.stage_level].clip_draw(720 * self.frame, 0, 720, 1280, WIDTH * 0.5, self.second, WIDTH, HEIGHT)


