import pygame.display
from color import Color


class Window:

    def __init__(self, game):
        self.game = game
        self.res = game.RES

        self.window = pygame.display.set_mode(self.res, pygame.SRCALPHA)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def render(self, layers):
        self.window.fill(Color('black').color)
        [self.window.blit(pygame.transform.scale(layer, self.res), (0, 0)) for layer in layers]
        pygame.display.flip()
