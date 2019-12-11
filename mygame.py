import game_framework
import pico2d
import title_state

WIDTH = 750
HEIGHT = 900

pico2d.open_canvas(WIDTH, HEIGHT, sync=True)
game_framework.run(title_state)
pico2d.close_canvas()
