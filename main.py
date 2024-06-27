import sys
sys.path.append('..')

import pygame
pygame.init()
from color import Color
import profilehooks


class Game:
    RES = WIDTH, HEIGHT = 1600, 900

    LAYER_COUNT = 3
    FPS = 60
    CHUNK_SIZE = 400
    CHUNK_COUNT = 4

    FILL_COLOR = Color('black', a=0).color
    BG_COLOR = Color('black', random_=False).color

    PLAYER_INVENTORY_SIZE = 12
    INVENTORY_ITEM_SIZE = (64, 64)

    @profilehooks.profile
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.layers = [pygame.Surface(self.RES, pygame.SRCALPHA) for _ in range(self.LAYER_COUNT)]
        self.delta_time = 1
        self.screen = 'main_menu'

        self.total_chunks = self.CHUNK_COUNT * self.CHUNK_COUNT
        self.chunk_progress = 0

        from window import Window
        from input import Input
        from camera import Camera

        self.window = Window(self)
        self.input = Input(self)
        self.camera = Camera(self)

        from UI.ui import UI
        from player import Player
        from map import Map

        self.ui = UI(self)
        self.player = Player(self)
        self.map = Map(self)

    @staticmethod
    def get_centered_position(pos, size):
        return pos[0] - size[0] // 2, pos[1] - size[1] // 2

    @staticmethod
    def div(a, b, default=None):
        if not b:
            if not default:
                return a
            else:
                return default
        return a / b

    @staticmethod
    def draw_transparent_rect(surface, size, pos, color):
        temp_surf = pygame.Surface(size, pygame.SRCALPHA)
        temp_surf.fill(color)
        surface.blit(temp_surf, pos)

    def setup(self):
        self.map.generate()

    def update(self):
        self.delta_time = self.clock.tick(self.FPS)
        self.delta_time /= 1000

        frame_rate = 1 / self.delta_time
        pygame.display.set_caption(str(frame_rate))

        self.input.update()

        if self.screen == 'game':
            self.game_update()

        self.camera.update()
        self.ui.update()

    def game_update(self):
        self.player.update()
        self.map.update()

    def draw(self):
        [layer.fill(self.FILL_COLOR) for layer in self.layers]

        if self.screen == 'game':
            self.game_draw()

        self.ui.draw(self.layers[2])
        self.input.draw(self.layers[2])

    def game_draw(self):
        self.player.draw(self.layers[1])
        self.map.draw(self.layers[0], self.layers[1])

    @profilehooks.profile
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
