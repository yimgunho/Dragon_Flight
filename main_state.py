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

name = "MainState"

ground = None
eru = None
dragon = []
bullet = []
count = 0
hit_count = 0
boom = []
hp_gauge = []
ctrl_dir = 0


def enter():
    global ground, eru, dragon, boom, count, bullet, hp_gauge, hit_count
    ground = Ground(0)
    eru = Eru()
    dragon = []
    bullet = []
    count = 0
    boom = []
    hp_gauge = []
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
    global bullet, count, dragon, boom, hp_gauge, hit_count
    for game_object in game_world.all_objects():
        game_object.update()

    if len(dragon) == 0:
        dragon = [Dragon(n * 140 - 70) for n in range(1, 6)]
        for d in range(len(dragon)):
            hp_gauge += [HPGauge(dragon[d].x, dragon[d].y)]

    dra = []
    bul = []
    bo = []

    for d in range(len(dragon)):
        dragon[d].update()
        hp_gauge[d].update(dragon[d].hp)
        for b in range(len(bullet)):
            if dragon[d].x - 110 < bullet[b].x < dragon[d].x + 110 \
                    and dragon[d].y - 110 < bullet[b].y < dragon[d].y + 110:
                dragon[d].damage(bullet[b].atk)
                if dragon[d].hp <= 0:
                    dra = [d]
                bul = [b]
                break
        if dragon[d].x - 110 < eru.x < dragon[d].x + 110 and \
                dragon[d].y - 110 < eru.y < dragon[d].y + 110:
            eru.hp -= 1
            dra = [d]
            eru.hit += 1
            break

        if dragon[d].y <= -100:
            dra = [d]

    for d in dra:
        boom = [Boom(dragon[d].x, dragon[d].y)]
        del dragon[d]
        del hp_gauge[d]

    for o in range(len(boom)):
        boom[o].update()
        if boom[o].frame >= 6:
            bo = [o]

    for o in bo:
        del boom[o]

    count = (count + 1) % 10

    if eru.hit > 0:
        hit_count += 1
        if hit_count > 50:
            eru.hit = 0
            hit_count = 0

    if count == 0:
        bullet += [EruBullet(eru.x, eru.atk_upgrade)]

    if eru.hp == 0:
        game_framework.push_state(title_state)

    for b in range(len(bullet)):
        bullet[b].update()
        if bullet[b].y >= 900:
            bul = [b]

    for i in bul:
        del bullet[i]


def draw():
    global bullet
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for bul in bullet:
        bul.draw()
    for dra in dragon:
        dra.draw()
    for bo in boom:
        bo.draw()
    for hp in hp_gauge:
        hp.draw()

    delay(0.02)
    update_canvas()
