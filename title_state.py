import game_framework
from pico2d import *
import main_state
from Ground import Ground, WIDTH, HEIGHT

title_name = "TitleState"
ti_background = None
eru = None
title_name = None
start = None
feeling = None
character_move = 0
character_up = True
count = 0
start_time = 0.0
start_draw = True
velocity = 100


def enter():
    global eru, ti_background, title_name, start, feeling
    ti_background = Ground(0)
    eru = load_image('title_character.png')
    title_name = load_image('title_name.png')
    start = load_image('title_start.png')
    feeling = load_image('title_feeling.png')


def exit():
    global eru, ti_background, title_name, start, feeling
    del eru, ti_background, title_name, start, feeling


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
    eru.draw(500, 250 + character_move, 450, 490)
    if start_draw:
        start.draw(WIDTH * 0.5, HEIGHT * 0.15, WIDTH * 0.9, HEIGHT * 0.15)
    title_name.draw(WIDTH * 0.5, HEIGHT * 0.7, WIDTH * 0.8, HEIGHT * 0.3)
    feeling.draw(WIDTH * 0.5, HEIGHT * 0.5, WIDTH, HEIGHT)
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
            character_move += velocity * game_framework.frame_time
        elif character_up == 1:
            character_move -= velocity * game_framework.frame_time

    if start_time > 50:
        start_time = 0
        if start_draw:
            start_draw = False
        else:
            start_draw = True

    start_time += velocity * game_framework.frame_time


def pause():
    pass


def resume():
    pass
