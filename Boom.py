from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Boom:
    def __init__(self, x, y):
        self.image = load_image('./image/boom.png')
        self.frame = 0
        self.x = x
        self.y = y
        game_world.add_object(self, 1)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if self.frame > 4:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(int(self.frame) * 120, 0, 120, 140, self.x, self.y)
