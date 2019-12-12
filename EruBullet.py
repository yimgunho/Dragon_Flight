from math import radians
from random import randint

from pico2d import *
import main_state

import game_world

PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
BULLET_SPEED_KMPH = 10.0  # Km / Hour
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


class EruBullet:
    images = None

    def __init__(self):
        eru = main_state.get_eru()
        if EruBullet.images == None:
            EruBullet.images = []
            EruBullet.images += [load_image('./image/Erubullet1.png')]
            EruBullet.images += [load_image('./image/Erubullet2.png')]
            EruBullet.images += [load_image('./image/Erubullet3.png')]
            EruBullet.images += [load_image('./image/Erubullet4.png')]
            EruBullet.images += [load_image('./image/Erubullet5.png')]

        self.x = eru.x
        self.attack_upgrade_value = eru.attack_upgrade_value
        self.speed_upgrade_value = eru.speed_upgrade_value
        self.attack_damage = (eru.attack_upgrade_value + 1) * 20
        self.y = 150 + bullet_level[self.attack_upgrade_value][1] / 2
        game_world.add_object(self, 1)
        self.crush_count = 0

    def get_bb(self):
        return self.x - bullet_level[self.attack_upgrade_value][0] / 2, \
               self.y - bullet_level[self.attack_upgrade_value][1] / 2, \
               self.x + bullet_level[self.attack_upgrade_value][0] / 2, \
               self.y + bullet_level[self.attack_upgrade_value][1] / 2

    def update(self):
        dragons = main_state.get_dragons()
        boss = main_state.get_boss()
        eru = main_state.get_eru()
        bg = main_state.get_ground()

        self.y += BULLET_SPEED_PPS

        if eru.stage_level < 4:
            for dragon in reversed(dragons):
                if collide(dragon, self):
                    dragon.hp -= self.attack_damage / (dragon.stage_level + 1)
                    if dragon.hp <= 0:
                        dragon.eraser()
                        bg.monster_death += 1
                        if randint(0, 4) == 2:
                            eru.gold += 1
                    self.crush_count += 1

        if self.y > game_world.HEIGHT or self.crush_count is not 0:
            self.eraser()

        elif eru.stage_level == 4 and boss is not None:
            if collide(boss, self):
                boss.hp -= self.attack_damage / 30
                self.eraser()

    def draw(self):
        self.images[self.attack_upgrade_value].rotate_draw(radians(90.0),
                                                           self.x, self.y,
                                                           bullet_level[self.attack_upgrade_value][1],
                                                           bullet_level[self.attack_upgrade_value][0])
        #draw_rectangle(*self.get_bb())

    def eraser(self):
        bullets = main_state.get_bullets()
        bullets.remove(self)
        game_world.remove_object(self)
