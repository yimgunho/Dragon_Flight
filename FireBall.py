from pico2d import *
import main_state

import game_world

PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
Fire_SPEED_KMPH = 7.0  # Km / Hour
Fire_SPEED_MPM = (Fire_SPEED_KMPH * 1000.0 / 60.0)
Fire_SPEED_MPS = (Fire_SPEED_MPM / 60.0)
Fire_SPEED_PPS = (Fire_SPEED_MPS * PIXEL_PER_METER)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class FireBall:
    image = None

    def __init__(self):
        eru = main_state.get_eru()
        if FireBall.image == None:
            FireBall.image = load_image('./image/fireball.png')

        self.x = eru.x
        self.y = game_world.HEIGHT + 160
        self.timer = 0

    def get_bb(self):
        return self.x - 55, self.y - 80, self.x + 55, self.y + 80

    def update(self):
        eru = main_state.get_eru()

        self.y -= Fire_SPEED_PPS * eru.stage_level * 0.2 + Fire_SPEED_PPS

        if collide(eru, self):
            eru.remain_hp -= 1
            eru.crash_effect_timer = 1
            self.eraser()

        elif self.y <= -100:
            self.eraser()


    def draw(self):
        self.image.draw(self.x, self.y, 100, 160)
        #draw_rectangle(*self.get_bb())

    def eraser(self):
        game_world.remove_object(self)
        del self
