from pico2d import *
import game_world


class EruHP:
    Full_image = None
    Empty_image = None

    def __init__(self, eruHP):
        if EruHP.Full_image is None:
            self.Full_image = load_image('hp_heart_01.png')
        if EruHP.Empty_image is None:
            self.Empty_image = load_image('hp_heart_02.png')

        self.eruHP = eruHP

    def draw(self):
        if self.eruHP == 3:
            self.Full_image.draw(300, 800)
            self.Full_image.draw(350, 800)
            self.Full_image.draw(400, 800)

        elif self.eruHP == 2:
            self.Full_image.draw(300, 800)
            self.Full_image.draw(350, 800)
            self.Empty_image.draw(400, 800)

        elif self.eruHP == 1:
            self.Full_image.draw(300, 800)
            self.Empty_image.draw(350, 800)
            self.Empty_image.draw(400, 800)

    def update(self):
        pass
