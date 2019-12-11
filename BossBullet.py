from math import radians

from pico2d import *
import main_state

import game_world

PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
BULLET_SPEED_KMPH = 5.0  # Km / Hour
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


bullet_level = {0: (79, 182), 1: (90, 182), 2: (101, 151), 3: (144, 148), 4: (169, 199)}


class BossBullet:
    image = None

    def __init__(self, trans_x):
        boss = main_state.get_boss()
        eru = main_state.get_eru()
        if BossBullet.image == None:
            BossBullet.image = load_image('./image/boss_bullet.png')

        self.x = boss.x
        self.trans_x = trans_x * BULLET_SPEED_PPS * 0.001
        self.trans_y = BULLET_SPEED_PPS
        self.count = 0

        self.y = boss.y - game_world.HEIGHT * 0.15
        game_world.add_object(self, 1)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def update(self):
        dragons = main_state.get_dragons()
        boss = main_state.get_boss()
        eru = main_state.get_eru()

        self.x += self.trans_x
        self.y -= self.trans_y

        if self.x <= 0:
            self.trans_x = -self.trans_x
            self.count += 1

        if self.x >= game_world.WIDTH:
            self.trans_x = -self.trans_x
            self.count += 1

        if self.y <= 0:
            self.trans_y = -self.trans_y
            self.count += 1

        if self.y >= game_world.WIDTH:
            self.trans_y = -self.trans_y
            self.count += 1

        if self.count >= 5:
            self.eraser()

        if collide(eru, self):
            eru.remain_hp -= 1
            eru.crash_effect_timer = 1
            self.eraser()

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def eraser(self):
        bossbullets = main_state.get_bossbullets()
        bossbullets.remove(self)
        game_world.remove_object(self)
