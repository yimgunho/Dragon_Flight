import game_framework
import pico2d
import os
import title_state

os.chdir('.//image')

pico2d.open_canvas(700, 840)
game_framework.run(title_state)
pico2d.close_canvas()
