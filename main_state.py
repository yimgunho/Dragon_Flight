import random
import json
import os

from pico2d import *

import game_framework
import title_state
import pause_state
from Background import Background
from Character import Character
from Bullet import Bullet
from Dragon import Dragon
from Boom import Boom
from HPGauge import HPGauge

name = "MainState"

background = None
character = None
dragon = []
bullet = []
count = 0
hit_count = 0
boom = []
hp_gauge = []


def enter():
    global background, character, dragon, boom, count, bullet, hp_gauge, hit_count
    background = Background(0)
    character = Character()
    dragon = []
    bullet = []
    count = 0
    boom = []
    hp_gauge = []


def exit():
    pass


#    global background, character, dragon, boom, count, bullet
#    del background, character, dragon, boom, count, bullet


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_p:
                game_framework.push_state(pause_state)

            elif event.key == SDLK_RIGHT:
                character.change_x += 1
            elif event.key == SDLK_LEFT:
                character.change_x -= 1

        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                character.change_x -= 1
            elif event.key == SDLK_LEFT:
                character.change_x += 1


def update():
    global bullet, count, dragon, boom, hp_gauge, hit_count
    background.update()
    character.update()

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
        if dragon[d].x - 110 < character.x < dragon[d].x + 110 and \
                dragon[d].y - 110 < character.y < dragon[d].y + 110:
            character.hp -= 1
            dra = [d]
            character.hit += 1
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

    if character.hit > 0:
        hit_count += 1
        if hit_count > 50:
            character.hit = 0
            hit_count = 0

    if count == 0:
        bullet += [Bullet(character.x)]

    if character.hp == 0:
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
    background.draw()
    character.draw(character.hit)
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
