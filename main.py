import sys
sys.path.append('..')

import pygame
from window import Window
from color import Color
from input import Input
from player import Player


class Game:
    RES = WIDTH, HEIGHT = 500, 500

    LAYER_COUNT = 2
    FPS = 60

    FILL_COLOR = Color('black', a=0).color
    BG_COLOR = Color('green', a=255).color

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.layers = [pygame.Surface(self.RES, pygame.SRCALPHA) for _ in range(self.LAYER_COUNT)]
        self.delta_time = 1

        self.window = Window(self)
        self.input = Input()

        self.player = Player(self)

    @staticmethod
    def get_centered_position(pos, size):
        return pos[0] - size[0] // 2, pos[1] - size[1] // 2

    def update(self):
        self.delta_time = self.clock.tick(self.FPS)
        self.delta_time /= 1000

        frame_rate = 1 / self.delta_time
        pygame.display.set_caption(str(frame_rate))

        self.input.update()

        self.player.update()

    def draw(self):
        [layer.fill(self.FILL_COLOR) for layer in self.layers]

        self.player.draw(self.layers[0])

    def run(self):
        while self.running:
            self.update()
            self.draw()

            self.window.update()
            self.window.render(self.layers)

        self.quit()

    def quit(self):
        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Game()
    game.run()
