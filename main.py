import pygame
from window import Window
from color import Color


class Game:
    RES = WIDTH, HEIGHT = 500, 500

    LAYER_COUNT = 5
    FPS = 60

    BG_COLOR = Color('black', a=0).color

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.layers = [pygame.Surface(self.RES, pygame.SRCALPHA) for _ in range(self.LAYER_COUNT)]
        self.delta_time = 1

        self.window = Window(self)

    def update(self):
        self.delta_time = self.clock.tick(self.FPS)
        self.delta_time /= 1000

        frame_rate = 1 / self.delta_time
        pygame.display.set_caption(str(frame_rate))

    def draw(self):
        [layer.fill(self.BG_COLOR) for layer in self.layers]

        pygame.draw.rect(self.layers[0], Color('white', a=100).color, (0, 0, 100, 100))
        pygame.draw.rect(self.layers[1], Color('white', a=150).color, (50, 50, 100, 100))

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
