from pico2d import *
import main_state
import game_framework
import game_world

PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
GOLD_SPEED_KMPH = 8.0  # Km / Hour
GOLD_SPEED_MPM = (GOLD_SPEED_KMPH * 1000.0 / 60.0)
GOLD_SPEED_MPS = (GOLD_SPEED_MPM / 60.0)
GOLD_SPEED_PPS = (GOLD_SPEED_MPS * PIXEL_PER_METER)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class Gold:
    image = None

    def __init__(self, x, y):
        if Gold.image == None:
            Gold.image = load_image('./image/gold.png')

        self.x = x
        self.y = y
        game_world.add_object(self, 1)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def update(self):
        global GOLD_SPEED_PPS
        eru = main_state.get_eru()

        self.y -= GOLD_SPEED_PPS

        if collide(eru, self):
            game_world.remove_object(self)
            eru.gold += 1

        if self.y < -20:
            game_world.remove_object(self)
            del self


    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())
