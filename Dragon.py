from pico2d import *
import main_state

import game_framework
import game_world
from Eru import FRAMES_PER_ACTION, ACTION_PER_TIME

Dragon_Size = 150

class Dragon:
    images = None

    def __init__(self, x):
        if Dragon.images == None:
            Dragon.images = []
            Dragon.images += [load_image('dragon01.png')]
            Dragon.images += [load_image('dragon02.png')]
            Dragon.images += [load_image('dragon03.png')]
            Dragon.images += [load_image('dragon04.png')]


        self.x = x * 150 + 75
        self.frame = 0
        self.y = game_world.HEIGHT + Dragon_Size
        self.hp = 40
        self.stage = 1

    def get_bb(self):
        return self.x - Dragon_Size * 0.5, self.y - Dragon_Size * 0.5, self.x + Dragon_Size * 0.5, self.y + Dragon_Size * 0.5

    def update(self):
        dragons = main_state.get_dragons()
        self.y -= game_world.SPEED_PPS * 0.04
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.y < 0:
            game_world.remove_object(self)
            dragons.remove(self)

    def damage(self, atk):
        self.hp -= atk

    def draw(self):
        self.images[self.stage].clip_draw(int(self.frame) * 150, 0, 150, 150, self.x, self.y, Dragon_Size, Dragon_Size)
        draw_rectangle(*self.get_bb())

