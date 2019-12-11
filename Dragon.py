from pico2d import *
import main_state

import game_framework
import game_world
from Boom import Boom
from Gold import Gold

PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
DRAGON_SPEED_KMPH = 5.0  # Km / Hour
DRAGON_SPEED_MPM = (DRAGON_SPEED_KMPH * 1000.0 / 60.0)
DRAGON_SPEED_MPS = (DRAGON_SPEED_MPM / 60.0)
DRAGON_SPEED_PPS = (DRAGON_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class Dragon:
    images = None
    HPimage = None

    def __init__(self, x, stage):
        if Dragon.images == None:
            Dragon.images = []
            Dragon.images += [load_image('./image/dragon01.png')]
            Dragon.images += [load_image('./image/dragon02.png')]
            Dragon.images += [load_image('./image/dragon03.png')]
            Dragon.images += [load_image('./image/dragon04.png')]
            Dragon.HPimage = load_image('./image/hp_gauge.png')

        self.x = x * 150 + 75
        self.frame = 0
        self.size = 150
        self.y = game_world.HEIGHT + self.size
        self.hp = 40 + stage * 40
        self.stage_level = stage

    def get_bb(self):
        return self.x - (self.size * 0.5), self.y - (self.size * 0.5), \
               self.x + (self.size * 0.5), self.y + (self.size * 0.5)

    def update(self):
        eru = main_state.get_eru()

        self.y -= DRAGON_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.stage_level >= 4 or self.y < -self.size:
            self.delite()

        elif collide(eru, self):
            eru.remain_hp -= 1
            eru.crash_effect_timer = 1
            self.eraser()

    def eru_attack_dragon(self):
        eru = main_state.get_eru()

        self.hp -= eru.atk / self.stage_level

    def draw(self):
        if self.stage_level < 4:
            self.images[self.stage_level].clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y, self.size, self.size)
            draw_rectangle(*self.get_bb())
            self.HPimage.clip_draw(0, 0, 100, 12, self.x, self.y - 100, self.hp, 12)

    def eraser(self):
        dragons = main_state.get_dragons()
        dragons.remove(self)
        game_world.remove_object(self)
        self.boom = Boom(self.x, self.y)
        self.gold = Gold(self.x, self.y)

    def delite(self):
        dragons = main_state.get_dragons()
        dragons.remove(self)
        game_world.remove_object(self)



