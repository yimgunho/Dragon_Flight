import game_framework
from pico2d import *
import main_state
import title_state

name = "PauseState"
image = None
pause_time = 0.0
pause_draw = True


def enter():
    global image
    image = load_image('pause.png')


def exit():
    global image
    del image


def update():
    global pause_time, pause_draw

    if pause_time > 0.1:
        pause_time = 0
        if pause_draw:
            pause_draw = False
        else:
            pause_draw = True

    delay(0.01)
    pause_time += 0.01


def draw():
    global image
    clear_canvas()
    main_state.draw()
    if pause_draw:
        image.draw(350, 420, 200, 200)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()


def pause(): pass


def resume(): pass
