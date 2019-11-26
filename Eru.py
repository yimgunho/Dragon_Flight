from pico2d import *

import game_framework
import game_world
from EruBullet import EruBullet
import title_state
import main_state

Eru_Size = 200

WIDTH = 750
HEIGHT = 900

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

bullet = []

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, ONE, TWO, THREE, ZERO, NINE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_1): ONE,
    (SDL_KEYDOWN, SDLK_2): TWO,
    (SDL_KEYDOWN, SDLK_3): THREE,
    (SDL_KEYDOWN, SDLK_0): ZERO,
    (SDL_KEYDOWN, SDLK_9): NINE
}


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False


class MoveState:

    @staticmethod
    def enter(eru, event):
        if event == RIGHT_DOWN:
            eru.velocity += game_world.SPEED_PPS * 5
        elif event == LEFT_DOWN:
            eru.velocity -= game_world.SPEED_PPS * 5
        elif event == RIGHT_UP:
            eru.velocity -= game_world.SPEED_PPS * 5
        elif event == LEFT_UP:
            eru.velocity += game_world.SPEED_PPS * 5

    @staticmethod
    def exit(eru, event):
        if event == ONE:
            if eru.bullet_atk_upgrade < 4 and eru.gold >= eru.bullet_atk_upgrade * 10:
                eru.gold -= eru.bullet_atk_upgrade * 10
                eru.bullet_atk_upgrade += 1

        if event == TWO and eru.gold >= eru.bullet_speed_upgrade * 10:
            if eru.bullet_speed_upgrade < 4:
                eru.gold -= eru.bullet_speed_upgrade * 10
                eru.bullet_speed_upgrade += 1

        if event == THREE and eru.hp < 3 and eru.gold >= eru.heart_upgrade * 10:
            eru.gold -= eru.heart_upgrade * 10
            eru.heart_upgrade += 1
            eru.hp += 1

        if event == ZERO:
            dragons = main_state.get_dragons()
            ground = main_state.get_ground()
            if eru.stage_level < 4:
                ground.stage_level += 1
                eru.stage_level += 1
                for dragon in dragons:
                    if dragon.stage_level < 4:
                        dragon.stage_level = ground.stage_level

        if event == NINE:
            eru.gold += 100

    @staticmethod
    def do(eru):
        eru.frame = (eru.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) \
                    % FRAMES_PER_ACTION
        eru.x += eru.velocity * game_framework.frame_time
        eru.x = clamp(Eru_Size * 0.25, eru.x, game_world.WIDTH - Eru_Size * 0.25)
        eru.distance += game_framework.frame_time * game_world.SPEED_PPS

        eru.bullet_timer += game_framework.frame_time * 10

        if int(eru.bullet_timer) >= 3 - eru.bullet_speed_upgrade * 0.5:
            eru.bullet_shoot()
            eru.bullet_timer = 0

        if eru.hptimer > 0:
            eru.hptimer -= game_framework.frame_time

        if eru.hp <= 0:
            game_framework.change_state(title_state)

        dragons = main_state.get_dragons()
        ground = main_state.get_ground()
        if eru.distance >= eru.stage_level * 5000 + 5000 and eru.stage_level < 4:
            ground.stage_level += 1
            eru.stage_level += 1
            for dragon in dragons:
                if dragon.stage_level < 4:
                    dragon.stage_level = ground.stage_level

    @staticmethod
    def draw(eru):
        eru.image.clip_draw(int(eru.frame) * 150, 0, 150, 150, eru.x, eru.y, Eru_Size, Eru_Size)
        eru.hp_draw()
        eru.font.draw(game_world.WIDTH * 0.7, game_world.HEIGHT - 50,
                      '%10.0f M' % (eru.distance - (eru.distance % 10)), (255, 255, 0))

        eru.gold_image.draw(game_world.WIDTH * 0.05, game_world.HEIGHT - 50, 40, 40)
        eru.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 50,
                      ': %1.0f' % (eru.gold), (255, 255, 0))

        eru.atk_image.draw(game_world.WIDTH * 0.05, game_world.HEIGHT - 100, 40, 40)
        eru.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 100,
                      ': %1.0f' % (eru.bullet_atk_upgrade), (255, 255, 0))

        eru.speed_image.draw(game_world.WIDTH * 0.05, game_world.HEIGHT - 150, 40, 40)
        eru.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 150,
                      ': %1.0f' % (eru.bullet_speed_upgrade), (255, 255, 0))

        eru.heart_image.clip_draw(120, 0, 128, 128, game_world.WIDTH * 0.05 + 7, game_world.HEIGHT - 200, 50, 50)
        eru.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 200,
                      ': %1.0f' % (eru.heart_upgrade), (255, 255, 0))

        draw_rectangle(*eru.get_bb())

        if 0.4 <= eru.hptimer <= 0.6 or 0.8 <= eru.hptimer <= 1:
            eru.damage_image.draw(eru.x + 50, eru.y + 70)
            eru.damage_image2.draw(game_world.WIDTH * 0.5, game_world.HEIGHT * 0.5, game_world.WIDTH, game_world.HEIGHT)


next_state_table = {
    MoveState: {RIGHT_UP: MoveState, LEFT_UP: MoveState,
                LEFT_DOWN: MoveState, RIGHT_DOWN: MoveState,
                ONE: MoveState, TWO: MoveState, THREE: MoveState,
                ZERO: MoveState, NINE: MoveState}
}


class Eru:
    image = None
    Full_image = None
    Empty_image = None
    damage_image = None
    damage_image2 = None
    gold_image = None
    atk_image = None
    speed_image = None
    heart_image = None

    def __init__(self):
        if Eru.image == None:
            Eru.image = load_image('Eru.png')
            Eru.Full_image = load_image('hp_heart_01.png')
            Eru.Empty_image = load_image('hp_heart_02.png')
            Eru.damage_image = load_image('damage.png')
            Eru.damage_image2 = load_image('damage2.png')
            Eru.gold_image = load_image('gold.png')
            Eru.atk_image = load_image('atk.png')
            Eru.speed_image = load_image('speed.png')
            Eru.heart_image = load_image('heart.png')

        self.velocity = 0
        self.frame = 0
        self.bullet_timer = 0
        self.x = WIDTH * 0.5
        self.y = 100
        self.hp = 3
        self.hptimer = 0
        self.distance = 0
        self.gold = 0

        self.stage_level = 0

        self.bullets = []
        self.bullets_number = 0
        self.bullet_atk_upgrade = 1
        self.bullet_speed_upgrade = 1
        self.heart_upgrade = 1

        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.font = load_font('NanumGothicExtraBold.TTF', 30)

    def get_bb(self):
        return self.x - Eru_Size * 0.2, self.y - Eru_Size * 0.25, self.x + Eru_Size * 0.2, self.y + Eru_Size * 0.25

    def bullet_shoot(self):
        self.bullets += [EruBullet()]

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

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def hp_draw(self):
        [self.Full_image.draw(325 + 50 * i, game_world.HEIGHT - 50) for i in range(self.hp)]
        [self.Empty_image.draw(325 + 50 * i, game_world.HEIGHT - 50) for i in range(self.hp, 3)]

    def get_bullets(self):
        return self.bullets
