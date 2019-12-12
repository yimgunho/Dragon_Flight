import pickle

import game_framework
from pico2d import *

import game_world
import main_state

import title_state

name = "RankingState"
font = None
records = []


def get_ranking_data():
    global records

    with open('record_data.json', 'r') as f:
        data_str = f.read()
        data = json.loads(data_str)
        records = data
        print(records)


def enter():
    global font
    bg = main_state.get_ground()
    bg.bgm.pause()
    font = load_font('./image/NanumGothicExtraBold.TTF', 30)
    get_ranking_data()
    hide_cursor()
    hide_lattice()
    print('ranking')


def exit():
    bg = main_state.get_ground()
    bg.bgm.resume()

def update(): pass


def draw():
    clear_canvas()
    record = main_state.get_record()
    font.draw(game_world.WIDTH * 0.35, game_world.HEIGHT * 0.8, '[Total Ranking]', (0, 0, 0))
    i = 1
    for recorded in records:
        font.draw(game_world.WIDTH * 0.35, game_world.HEIGHT * 0.8 - i * 50, '#%d %2.2f M' % (i, recorded), (0, 0, 0))
        i += 1
    font.draw(game_world.WIDTH * 0.3, game_world.HEIGHT * 0.75 - i * 50, 'My Score : %2.2f M' % record, (0, 0, 0))
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)


def pause(): pass


def resume(): pass
