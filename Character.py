from pico2d import *


class Character:

    def __init__(self):
        self.image = load_image('cha.png')
        self.full_hp = load_image('hp_heart_01.png')
        self.no_hp = load_image('hp_heart_02.png')
        self.damage = load_image('damage.png')
        self.hit_effect = load_image('hit_effect.png')
        self.timer = 0
        self.frame = 0
        self.x = 350
        self.y = 100
        self.change_x = 0
        self.speed = 10
        self.hp = 3
        self.hit = 0

    def update(self):
        if 65 <= self.x and self.change_x < 0:
            self.x -= self.speed
        elif self.x <= 635 and self.change_x > 0:
            self.x += self.speed

        self.frame = (self.frame + 1) % 6

    def draw(self, hit):
        self.image.clip_draw(128 * self.frame, 0, 128, 128, self.x, self.y, 140, 140)
        self.draw_hp()
        if hit > 0:
            self.damage.draw(self.x + 50, self.y + 50, 100, 100)
            self.timer = (self.timer + 1) % 20
            if self.timer < 10:
                self.hit_effect.draw(350, 420, 700, 840)

    def draw_hp(self):
        if self.hp == 3:
            self.full_hp.draw(300, 800)
            self.full_hp.draw(350, 800)
            self.full_hp.draw(400, 800)
        elif self.hp == 2:
            self.full_hp.draw(300, 800)
            self.full_hp.draw(350, 800)
            self.no_hp.draw(400, 800)
        elif self.hp == 1:
            self.full_hp.draw(300, 800)
            self.no_hp.draw(350, 800)
            self.no_hp.draw(400, 800)




