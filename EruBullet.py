from pico2d import *


def bullet_load():
    if EruBullet.bullet_image_01 == None:
        EruBullet.bullet_image_01 = load_image('Erubullet_01.png')
        EruBullet.bullet_image_02 = load_image('Erubullet_02.png')
        EruBullet.bullet_image_03 = load_image('Erubullet_03.png')
        EruBullet.bullet_image_04 = load_image('Erubullet_04.png')
        EruBullet.bullet_image_05 = load_image('Erubullet_05.png')
        EruBullet.bullet_image_06 = load_image('Erubullet_06.png')
        EruBullet.bullet_image_07 = load_image('Erubullet_07.png')


class EruBullet:
    bullet_image_01 = None
    bullet_image_02 = None
    bullet_image_03 = None
    bullet_image_04 = None
    bullet_image_05 = None
    bullet_image_06 = None
    bullet_image_07 = None

    def __init__(self, x, atk_upgrade):
        bullet_load()
        self.x = x
        self.y = 200
        self.speed = 10
        self.atk = 20
        self.upgrade = atk_upgrade

    def update(self):
        self.y += self.speed

    def draw(self):
        if self.upgrade == 1:
            self.bullet_image_01.draw(self.x, self.y, 34, 74)
        elif self.upgrade == 2:
            self.bullet_image_02.draw(self.x, self.y, 49, 105)
        elif self.upgrade == 3:
            self.bullet_image_03.draw(self.x, self.y, 71, 122)
        elif self.upgrade == 4:
            self.bullet_image_04.draw(self.x, self.y, 71, 122)
        elif self.upgrade == 5:
            self.bullet_image_05.draw(self.x, self.y, 128, 128)
        elif self.upgrade == 6:
            self.bullet_image_06.draw(self.x, self.y, 128, 128)
        elif self.upgrade == 7:
            self.bullet_image_07.draw(self.x, self.y, 128, 128)



