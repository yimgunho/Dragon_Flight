from pico2d import *
import main_state

import game_world

PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
BULLET_SPEED_KMPH = 10.0  # Km / Hour
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)


class EruBullet:
    images = None

    def __init__(self):
        eru = main_state.get_eru()
        if EruBullet.images == None:
            EruBullet.images = []
            EruBullet.images += [load_image('Erubullet_01.png')]
            EruBullet.images += [load_image('Erubullet_02.png')]
            EruBullet.images += [load_image('Erubullet_03.png')]
            EruBullet.images += [load_image('Erubullet_04.png')]
            EruBullet.images += [load_image('Erubullet_05.png')]

        self.x = eru.x
        self.y = 200
        self.bullet_atk_upgrade = eru.bullet_atk_upgrade
        self.bullet_speed_upgrade = eru.bullet_speed_upgrade
        game_world.add_object(self, 1)

    def get_bb(self):
        return self.x - 20 - self.bullet_atk_upgrade * 10, self.y - 30 - self.bullet_atk_upgrade * 10, \
               self.x + 20 + self.bullet_atk_upgrade * 10, self.y + 30 + self.bullet_atk_upgrade * 10

    def update(self):
        eru = main_state.get_eru()
        self.y += BULLET_SPEED_PPS

        if self.y > game_world.HEIGHT:
            game_world.remove_object(self)
            eru.bullets.remove(self)


    def draw(self):
        self.images[self.bullet_atk_upgrade].draw(self.x, self.y, 40 + self.bullet_atk_upgrade * 20, 60 + self.bullet_atk_upgrade * 20)

        draw_rectangle(*self.get_bb())



