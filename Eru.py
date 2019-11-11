from pico2d import *
import game_world

from EruHP import EruHP

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
            eru.velocity += 1
        elif event == LEFT_DOWN:
            eru.velocity -= 1
        elif event == RIGHT_UP:
            eru.velocity -= 1
        elif event == LEFT_UP:
            eru.velocity += 1

    @staticmethod
    def exit(eru, event):
        pass

    @staticmethod
    def do(eru):
        eru.frame = (eru.frame + 1) % 6
        eru.eruHP()

    @staticmethod
    def draw(eru):
        eru.image.clip_draw(eru.frame * 128, 0, 128, 128, eru.x, eru.y, 140, 140)


class MoveState:

    @staticmethod
    def enter(eru, event):
        if event == RIGHT_DOWN:
            eru.velocity += 1
        elif event == LEFT_DOWN:
            eru.velocity -= 1
        elif event == RIGHT_UP:
            eru.velocity -= 1
        elif event == LEFT_UP:
            eru.velocity += 1

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(eru):
        eru.frame = (eru.frame + 1) % 6
        eru.x += eru.velocity * eru.speed
        eru.x = clamp(65, eru.x, 700 - 65)
        eru.eruHP()

    @staticmethod
    def draw(eru):
        eru.image.clip_draw(eru.frame * 128, 0, 128, 128, eru.x, eru.y, 140, 140)


next_state_table = {
    IdleState: {RIGHT_UP: MoveState, LEFT_UP: MoveState,
                RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState},
    MoveState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState}
}


class Eru:

    def __init__(self):
        self.image = load_image('cha.png')
        self.damage = load_image('damage.png')
        self.hit_effect = load_image('hit_effect.png')
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

    def eruHP(self):
        HP = EruHP(self.hp)
        game_world.add_object(HP, 1)

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





