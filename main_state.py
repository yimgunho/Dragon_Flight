import random
import json
import os

from pico2d import *
import game_framework
import game_world

import title_state
import pause_state
from Boss import Boss
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
boss = None
dragons = []
bullets = []


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def get_eru():
    return eru


def get_dragons():
    return dragons

def get_ground():
    return ground

def get_boss():
    return boss


def enter():
    global ground
    ground = Ground(0)
    game_world.add_object(ground, 0)

    global eru
    eru = Eru()
    game_world.add_object(eru, 1)

    global dragons
    dragons = [Dragon(i, eru.stage_level) for i in range(5)]
    game_world.add_objects(dragons, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and (event.key == SDLK_ESCAPE):
            game_framework.change_state(title_state)

        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)

        else:
            eru.handle_event(event)


def update():
    global dragons, boss
    for game_object in game_world.all_objects():
        game_object.update()

    if len(dragons) <= 0 and eru.stage_level < 4:
        dragons = [Dragon(i, eru.stage_level) for i in range(5)]
        game_world.add_objects(dragons, 1)

    elif eru.stage_level >= 4 and boss is None:
        boss = Boss()
        game_world.add_object(boss, 1)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
