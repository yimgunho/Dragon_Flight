import game_framework
from pico2d import *
import game_world


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
SPEED_KMPH = 5.0  # Km / Hour
SPEED_MPM = (SPEED_KMPH * 1000.0 / 60.0)
SPEED_MPS = (SPEED_MPM / 60.0)
SPEED_PPS = (SPEED_MPS * PIXEL_PER_METER)


class Eru_Illustration:
    image = None

    def __init__(self):
        if Eru_Illustration.image == None:
            Eru_Illustration.image = load_image('Eru_Illustration.png')
        self.x = game_world.WIDTH * 0.7
        self.y = game_world.HEIGHT * 0.37
        self.dir = 0

    def update(self):
        if self.dir == 0:
            self.y += SPEED_PPS * game_framework.frame_time
            clamp(game_world.HEIGHT * 0.35, self.y, game_world.HEIGHT * 0.39)
            if self.y >= game_world.HEIGHT * 0.39:
                self.dir = 1

        elif self.dir == 1:
            self.y -= SPEED_PPS * game_framework.frame_time
            clamp(game_world.HEIGHT * 0.35, self.y, game_world.HEIGHT * 0.39)
            if self.y <= game_world.HEIGHT * 0.35:
                self.dir = 0

    def draw(self):
        self.image.draw(self.x, self.y, 450, 490)


class Game_Name:
    image = None

    def __init__(self):
        if Game_Name.image == None:
            Game_Name.image = load_image('title_name.png')
        self.x = game_world.WIDTH * 0.5
        self.y = game_world.HEIGHT * 0.75

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 483, 288)