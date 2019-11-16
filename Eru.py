from pico2d import *

import game_framework
import game_world
from EruBullet import EruBullet

Eru_Size = 200

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
FLY_SPEED_KMPH = 100.0  # Km / Hour
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}


class IdleState:

    @staticmethod
    def enter(eru, event):
        if event == RIGHT_DOWN:
            eru.velocity += FLY_SPEED_PPS
        elif event == LEFT_DOWN:
            eru.velocity -= FLY_SPEED_PPS
        elif event == RIGHT_UP:
            eru.velocity -= FLY_SPEED_PPS
        elif event == LEFT_UP:
            eru.velocity += FLY_SPEED_PPS

    @staticmethod
    def exit(eru, event):
        pass

    @staticmethod
    def do(eru):
        eru.frame = (eru.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) \
                    % FRAMES_PER_ACTION
        if int(eru.frame) == 0:
            eru.bullet_shoot()


    @staticmethod
    def draw(eru):
        eru.image.clip_draw(int(eru.frame) * 150, 0, 150, 150, eru.x, eru.y, Eru_Size, Eru_Size)
        eru.hp_draw()


class MoveState:

    @staticmethod
    def enter(eru, event):
        if event == RIGHT_DOWN:
            eru.velocity += FLY_SPEED_PPS
        elif event == LEFT_DOWN:
            eru.velocity -= FLY_SPEED_PPS
        elif event == RIGHT_UP:
            eru.velocity -= FLY_SPEED_PPS
        elif event == LEFT_UP:
            eru.velocity += FLY_SPEED_PPS

    @staticmethod
    def exit(eru, event):
        pass

    @staticmethod
    def do(eru):
        eru.frame = (eru.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) \
                    % FRAMES_PER_ACTION
        eru.x += eru.velocity * game_framework.frame_time
        eru.x = clamp(Eru_Size * 0.5, eru.x, game_world.WIDTH - Eru_Size * 0.5)
        if int(eru.frame) == 0:
            eru.bullet_shoot()

    @staticmethod
    def draw(eru):
        eru.image.clip_draw(int(eru.frame) * 150, 0, 150, 150, eru.x, eru.y, Eru_Size, Eru_Size)
        eru.hp_draw()


next_state_table = {
    IdleState: {RIGHT_UP: MoveState, LEFT_UP: MoveState,
                RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState},
    MoveState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState}
}


class Eru:
    image = None
    Full_image = None
    Empty_image = None

    def __init__(self):
        if Eru.image == None:
            Eru.image = load_image('Eru.png')

        self.damage = load_image('damage.png')
        self.hit_effect = load_image('hit_effect.png')

        if Eru.Full_image is None:
            self.Full_image = load_image('hp_heart_01.png')
        if Eru.Empty_image is None:
            self.Empty_image = load_image('hp_heart_02.png')

        self.velocity = 0
        self.timer = 0
        self.frame = 0
        self.x = 350
        self.y = 100
        self.speed = 10
        self.hp = 3
        self.hit = 0
        self.atk_upgrade = 1
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def bullet_shoot(self):
        bullet = EruBullet(self.x, self.atk_upgrade)
        game_world.add_object(bullet, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        if self.hit > 0:
            self.damage.draw(self.x + 50, self.y + 50, 100, 100)
            self.timer = (self.timer + 1) % 20
            if self.timer < 10:
                self.hit_effect.draw(350, 420, 700, 840)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def hp_draw(self):
        if self.hp == 3:
            self.Full_image.draw(300, game_world.HEIGHT - 50)
            self.Full_image.draw(350, game_world.HEIGHT - 50)
            self.Full_image.draw(400, game_world.HEIGHT - 50)

        elif self.hp == 2:
            self.Full_image.draw(300, game_world.HEIGHT - 50)
            self.Full_image.draw(350, game_world.HEIGHT - 50)
            self.Empty_image.draw(400, game_world.HEIGHT - 50)

        elif self.hp == 1:
            self.Full_image.draw(300, game_world.HEIGHT - 50)
            self.Empty_image.draw(350, game_world.HEIGHT - 50)
            self.Empty_image.draw(400, game_world.HEIGHT - 50)

