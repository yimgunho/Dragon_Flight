from pico2d import *

import game_world


def bullet_load():
    if EruBullet.bullet_image_01 == None:
        EruBullet.bullet_image_01 = load_image('Erubullet_01.png')
        EruBullet.bullet_image_02 = load_image('Erubullet_02.png')
        EruBullet.bullet_image_03 = load_image('Erubullet_03.png')
        EruBullet.bullet_image_04 = load_image('Erubullet_04.png')
        EruBullet.bullet_image_05 = load_image('Erubullet_05.png')


class EruBullet:
    bullet_image_01 = None
    bullet_image_02 = None
    bullet_image_03 = None
    bullet_image_04 = None
    bullet_image_05 = None

    def __init__(self, x, bullet_atk_upgrade, bullet_speed_upgrade):
        bullet_load()
        self.x = x
        self.y = 200
        self.bullet_atk_upgrade = bullet_atk_upgrade
        self.bullet_speed_upgrade = bullet_speed_upgrade

    def get_bb(self):
        return self.x - 20 - self.bullet_atk_upgrade * 10, self.y - 30 - self.bullet_atk_upgrade * 10, \
               self.x + 20 + self.bullet_atk_upgrade * 10, self.y + 30 + self.bullet_atk_upgrade * 10

    def update(self):
        self.y += game_world.SPEED_PPS * 0.015 + (self.bullet_speed_upgrade * 0.1)

        if self.y > game_world.HEIGHT:
            game_world.remove_object(self)

    def draw(self):
        if self.bullet_atk_upgrade == 1:
            self.bullet_image_01.draw(self.x, self.y, 40 + self.bullet_atk_upgrade * 20, 60 + self.bullet_atk_upgrade * 20)
        elif self.bullet_atk_upgrade == 2:
            self.bullet_image_02.draw(self.x, self.y, 40 + self.bullet_atk_upgrade * 20, 60 + self.bullet_atk_upgrade * 20)
        elif self.bullet_atk_upgrade == 3:
            self.bullet_image_03.draw(self.x, self.y, 40 + self.bullet_atk_upgrade * 20, 60 + self.bullet_atk_upgrade * 20)
        elif self.bullet_atk_upgrade == 4:
            self.bullet_image_04.draw(self.x, self.y, 40 + self.bullet_atk_upgrade * 20, 60 + self.bullet_atk_upgrade * 20)
        elif self.bullet_atk_upgrade == 5:
            self.bullet_image_05.draw(self.x, self.y, 40 + self.bullet_atk_upgrade * 20, 60 + self.bullet_atk_upgrade * 20)
        draw_rectangle(*self.get_bb())



