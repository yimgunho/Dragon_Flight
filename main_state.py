import random
import json
import os

from pico2d import *
import game_framework
import game_world

import title_state
import pause_state
from Ground import Ground
from Eru import Eru
from EruBullet import EruBullet
from Dragon import Dragon
from Boom import Boom
from HPGauge import HPGauge

game_name = "MainState"

ground = None
eru = None
heart_point = None
ctrl_dir = 0


def enter():
    global ground, eru, heart_point
    ground = Ground(0)
    eru = Eru()
    game_world.add_object(ground, 0)
    game_world.add_object(eru, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global ctrl_dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and (event.key == SDLK_ESCAPE):
            game_framework.change_state(title_state)

        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)

        elif event.type == SDL_KEYDOWN and event.key == SDLK_LCTRL:
            ctrl_dir += 1

        elif event.type == SDL_KEYDOWN and ctrl_dir > 0 and event.key == SDLK_2:
            eru.atk_upgrade += 1

        elif event.type == SDL_KEYUP and event.key == SDLK_LCTRL:
            ctrl_dir -= 1

        else:
            eru.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
