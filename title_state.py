import game_framework
from pico2d import *

import game_world
import main_state
from Ground import Ground
from Title import Eru_Illustration, Game_Name, Game_Start

game_name = "TitleState"
background = None
eru_illustration = None
name = None
game_start = None


def enter():
    global eru_illustration, background, name, game_start
    background = Ground(0)
    game_world.add_object(background, 0)

    eru_illustration = Eru_Illustration()
    game_world.add_object(eru_illustration, 1)

    name = Game_Name()
    game_world.add_object(name, 1)

    game_start = Game_Start()
    game_world.add_object(game_start, 1)


def exit():
    game_world.clear()


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
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def pause():
    pass


def resume():
    pass
