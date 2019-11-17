from pico2d import *

import game_framework
import game_world
from Eru import FRAMES_PER_ACTION, ACTION_PER_TIME


Dragon_Size = 150

class IdleState:

    @staticmethod
    def enter(eru, event):
        pass

    @staticmethod
    def exit(eru, event):
        pass

    @staticmethod
    def do(eru):
        eru.frame = (eru.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) \
                    % FRAMES_PER_ACTION
        eru.distance += game_framework.frame_time * game_world.SPEED_PPS
        eru.bullet_timer += game_framework.frame_time * 10

        if int(eru.bullet_timer) >= 3 - eru.bullet_speed_upgrade * 0.5:
            eru.bullet_shoot()
            eru.bullet_timer = 0


    @staticmethod
    def draw(dragon):
        dragon.image.clip_draw(int(dragon.frame) * 150, 0, 150, 150, dragon.x, dragon.y, Dragon_Size, Dragon_Size)


class Dragon:

    def __init__(self, x):
        self.image = load_image('green_dragon.png')
        self.frame = 0
        self.x = x * 150 + 150
        self.y = game_world.HEIGHT
        self.hp = 40

    def update(self):
        self.y -= 10
        self.frame = (self.frame + 1) % 9

    def damage(self, atk):
        self.hp -= atk

    def draw(self):
        if self.hp > 0:
            self.image.clip_draw(self.frame * 200, 0, 200, 200, self.x, self.y, 130, 130)