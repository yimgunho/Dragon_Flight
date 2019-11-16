import game_framework
import pico2d
import os
import title_state

os.chdir('.//image')

WIDTH = 750
HEIGHT = 900

pico2d.open_canvas(WIDTH, HEIGHT)
game_framework.run(title_state)
pico2d.close_canvas()
