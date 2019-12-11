from pico2d import *

import game_framework
import game_world
import ranking_state
from EruBullet import EruBullet
import title_state
import main_state

Eru_Size = 200

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
SPEED_KMPH = 10.0  # Km / Hour
SPEED_MPM = (SPEED_KMPH * 1000.0 / 60.0)
SPEED_MPS = (SPEED_MPM / 60.0)
SPEED_PPS = (SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

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
            eru.velocity += SPEED_PPS * 5
        elif event == LEFT_DOWN:
            eru.velocity -= SPEED_PPS * 5
        elif event == RIGHT_UP:
            eru.velocity -= SPEED_PPS * 5
        elif event == LEFT_UP:
            eru.velocity += SPEED_PPS * 5

    @staticmethod
    def exit(eru, event):
        if event == ONE:
            if eru.attack_upgrade_value < 4 and eru.gold >= (eru.attack_upgrade_value + 1) * 10:
                eru.gold -= (eru.attack_upgrade_value + 1) * 10
                eru.attack_upgrade_value += 1

        if event == TWO and eru.gold >= (eru.speed_upgrade_value + 1) * 10:
            if eru.speed_upgrade_value < 4:
                eru.gold -= (eru.speed_upgrade_value + 1) * 10
                eru.speed_upgrade_value += 1

        if event == THREE and eru.remain_hp < 3 and eru.gold >= (eru.hp_upgrade_value + 1) * 10:
            eru.gold -= (eru.hp_upgrade_value + 1) * 10
            eru.hp_upgrade_value += 1
            eru.remain_hp += 1

        if event == ZERO:
            eru.distance += 5000

        if event == NINE:
            eru.gold += 100

    @staticmethod
    def do(eru):
        eru.frame = (eru.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) \
                    % FRAMES_PER_ACTION
        eru.x += eru.velocity * game_framework.frame_time
        eru.x = clamp(Eru_Size * 0.25, eru.x, game_world.WIDTH - Eru_Size * 0.25)
        eru.distance += game_framework.frame_time * SPEED_PPS

        eru.bullet_timer += game_framework.frame_time * 10

        if int(eru.bullet_timer) >= 3 - eru.speed_upgrade_value * 0.5:
            eru.bullet_shoot()
            eru.bullet_timer = 0

        if eru.crash_effect_timer > 0:
            eru.crash_effect_timer -= game_framework.frame_time

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
        eru.distance_draw()
        eru.gold_draw()
        eru.upgrade_draw()
        eru.crash_draw()

        draw_rectangle(*eru.get_bb())


next_state_table = {
    MoveState: {RIGHT_UP: MoveState, LEFT_UP: MoveState,
                LEFT_DOWN: MoveState, RIGHT_DOWN: MoveState,
                ONE: MoveState, TWO: MoveState, THREE: MoveState,
                ZERO: MoveState, NINE: MoveState}
}


class Eru:
    # eru 관련
    image = None
    gold_image = None

    # eru 업그레이드 관련
    attack_upgrade_image = None
    speed_upgrade_image = None
    hp_upgrade_image = None

    # hp 관련
    Full_image = None
    Empty_image = None

    # 피격 관련
    eru_crash_image = None
    background_crash_image = None

    def __init__(self):
        if Eru.image == None:
            # eru 관련
            Eru.image = load_image('./image/Eru.png')
            Eru.gold_image = load_image('./image/gold.png')

            # eru 업그레이드 관련
            Eru.attack_upgrade_image = load_image('./image/attack_upgrade.png')
            Eru.speed_upgrade_image = load_image('./image/speed_upgrade.png')
            Eru.hp_upgrade_image = load_image('./image/hp_upgrade.png')

            # hp 관련
            Eru.Full_image = load_image('./image/full_hp.png')
            Eru.Empty_image = load_image('./image/empty_hp.png')

            # 피격 관련
            Eru.eru_crash_image = load_image('./image/eru_crush.png')
            Eru.background_crash_image = load_image('./image/background_crush.png')

        # eru 위치 관련
        self.x = game_world.WIDTH * 0.5
        self.y = 100
        self.velocity = 0
        self.frame = 0

        # eru 공격 관련
        self.bullet_timer = 0
        self.attack_upgrade_value = 0
        self.speed_upgrade_value = 0
        self.hp_upgrade_value = 0

        # eru HP 관련
        self.remain_hp = 3
        self.crash_effect_timer = 0

        # eru 스테이지 관련
        self.distance = 0
        self.gold = 0
        self.stage_level = 0

        # 그 외
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.font = load_font('./image/NanumGothicExtraBold.TTF', 30)

    def get_bb(self):
        return self.x - Eru_Size * 0.2, self.y - Eru_Size * 0.25, self.x + Eru_Size * 0.2, self.y + Eru_Size * 0.25

    def bullet_shoot(self):
        bullets = main_state.get_bullets()
        bullets += [EruBullet()]

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
        [self.Full_image.draw(325 + 50 * i, game_world.HEIGHT - 50) for i in range(self.remain_hp)]
        [self.Empty_image.draw(325 + 50 * i, game_world.HEIGHT - 50) for i in range(self.remain_hp, 3)]

    def gold_draw(self):
        self.gold_image.draw(game_world.WIDTH * 0.05, game_world.HEIGHT - 50, 40, 40)
        self.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 50, ': %1.0f' % (self.gold), (255, 255, 0))

    def upgrade_draw(self):
        self.attack_upgrade_image.draw(game_world.WIDTH * 0.05, game_world.HEIGHT - 100, 40, 40)
        self.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 100,
                       ': %1.0f' % self.attack_upgrade_value, (255, 255, 0))

        self.speed_upgrade_image.draw(game_world.WIDTH * 0.05, game_world.HEIGHT - 150, 40, 40)
        self.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 150,
                       ': %1.0f' % self.speed_upgrade_value, (255, 255, 0))

        self.hp_upgrade_image.clip_draw(120, 0, 128, 128, game_world.WIDTH * 0.05 + 7, game_world.HEIGHT - 200, 50, 50)
        self.font.draw(game_world.WIDTH * 0.1, game_world.HEIGHT - 200,
                       ': %1.0f' % self.hp_upgrade_value, (255, 255, 0))

    def distance_draw(self):
        self.font.draw(game_world.WIDTH * 0.7, game_world.HEIGHT - 50,
                       '%10.0f M' % (self.distance - (self.distance % 10)), (255, 255, 0))

    def crash_draw(self):
        if 0.4 <= self.crash_effect_timer <= 0.6 or 0.8 <= self.crash_effect_timer <= 1:
            self.eru_crash_image.draw(self.x + 50, self.y + 70)
            self.background_crash_image.draw(game_world.WIDTH * 0.5, game_world.HEIGHT * 0.5,
                                             game_world.WIDTH, game_world.HEIGHT)
