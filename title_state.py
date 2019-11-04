import game_framework
from pico2d import *
import main_state
from Background import Background

name = "TitleState"
ti_background = None
character = None
name = None
start = None
feeling = None
character_move = 0
character_up = True
count = 0
start_time = 0.0
start_draw = True


def enter():
    global character, ti_background, name, start, feeling
    ti_background = Background(0)
    character = load_image('title_character.png')
    name = load_image('title_name.png')
    start = load_image('title_start.png')
    feeling = load_image('title_feeling.png')


def exit():
    global character, ti_background, name, start, feeling
    del character, ti_background, name, start, feeling


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    ti_background.draw()
    character.draw(500, 250 + character_move, 450, 490)
    if start_draw:
        start.draw(350, 150, 600, 100)
    name.draw(350, 620, 500, 300)
    feeling.draw(350, 420, 700, 840)
    delay(0.02)
    update_canvas()


def update():
    global character_move, character_up, count, start_time, start_draw
    ti_background.update()

    count = (count + 1) % 2

    if count == 0:
        if character_move > 20:
            character_up = 1
        elif character_move < 0:
            character_up = 0

        if character_up == 0:
            character_move += 1
        elif character_up == 1:
            character_move -= 1

    if start_time > 0.2:
        start_time = 0
        if start_draw:
            start_draw = False
        else:
            start_draw = True

    start_time += 0.01


def pause():
    pass


def resume():
    pass
