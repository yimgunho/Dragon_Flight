from pico2d import *
import main_state

import game_framework
import game_world
import title_state

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class Boss:
    image = None
    HPimage = None
    bullet_image = None
    game_clear = None

    def __init__(self):
        if Boss.image == None:
            Boss.image = load_image('boss.png')
            Boss.HPimage = load_image('hp_gauge.png')
            Boss.bullet_image = load_image('boss_bullet.png')
            Boss.game_clear = load_image('game_clear.png')

        self.x = game_world.WIDTH * 0.5
        self.frame = 0
        self.y = game_world.HEIGHT * 0.75
        self.hp = 500
        self.boom = None

    def get_bb(self):
        return self.x - game_world.WIDTH * 0.2, self.y - game_world.HEIGHT * 0.15, \
               self.x + game_world.WIDTH * 0.2, self.y + game_world.HEIGHT * 0.15

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2



    def draw(self):
        self.image.clip_draw(0, int(self.frame) * 250, 350, 250, self.x, self.y, game_world.WIDTH * 0.8, game_world.HEIGHT * 0.3)
        draw_rectangle(*self.get_bb())
        self.HPimage.clip_draw(0, 0, 100, 12, self.x, self.y - 100, self.hp, 12)

        if self.hp <= 0:
            self.image.clip_draw(0, 0, 485, 100, game_world.WIDTH * 0.5, game_world.HEIGHT * 0.5,
                                 game_world.WIDTH * 0.8, game_world.HEIGHT * 0.3)

