from pico2d import *
import main_state

import game_framework
import game_world
from Boom import Boom
from Eru import FRAMES_PER_ACTION, ACTION_PER_TIME
from Gold import Gold

Dragon_Size = 150

PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
DRAGON_SPEED_KMPH = 5.0  # Km / Hour
DRAGON_SPEED_MPM = (DRAGON_SPEED_KMPH * 1000.0 / 60.0)
DRAGON_SPEED_MPS = (DRAGON_SPEED_MPM / 60.0)
DRAGON_SPEED_PPS = (DRAGON_SPEED_MPS * PIXEL_PER_METER)


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

    def __init__(self, x):
        if Dragon.images == None:
            Dragon.images = []
            Dragon.images += [load_image('dragon01.png')]
            Dragon.images += [load_image('dragon02.png')]
            Dragon.images += [load_image('dragon03.png')]
            Dragon.images += [load_image('dragon04.png')]
            Dragon.HPimage = load_image('hp_gauge.png')

        self.x = x * 150 + 75
        self.frame = 0
        self.y = game_world.HEIGHT + Dragon_Size
        self.hp = 40
        self.stage = 1
        self.boom = None
        self.gold = None

    def get_bb(self):
        return self.x - Dragon_Size * 0.5, self.y - Dragon_Size * 0.5, self.x + Dragon_Size * 0.5, self.y + Dragon_Size * 0.5

    def update(self):
        dragons = main_state.get_dragons()
        eru = main_state.get_eru()
        self.y -= DRAGON_SPEED_PPS
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.y < -Dragon_Size or self.hp <= 0:
            dragons.remove(self)
            game_world.remove_object(self)
            self.boom = Boom(self.x, self.y)
            self.gold = Gold(self.x, self.y)

        if collide(eru, self):
            eru.hp -= 1
            eru.hptimer = 1
            dragons.remove(self)
            game_world.remove_object(self)
            self.boom = Boom(self.x, self.y)
            self.gold = Gold(self.x, self.y)


    def damage(self, atk):
        self.hp -= atk

    def draw(self):
        self.images[self.stage].clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y, Dragon_Size, Dragon_Size)
        draw_rectangle(*self.get_bb())
        self.HPimage.clip_draw(0, 0, 100, 12, self.x, self.y - 100, self.hp, 12)

