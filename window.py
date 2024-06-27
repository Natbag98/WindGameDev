import pygame.display
import math


class Window:

    def __init__(self, game):
        self.game = game
        self.res = (960 * 1.2, 540 * 1.2)
        self.res_scale = (self.res[0] / self.game.RES[0], self.res[1] / self.game.RES[1])

        self.window = pygame.display.set_mode(self.res, pygame.SRCALPHA)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def render(self, layers):
        self.window.fill(self.game.BG_COLOR)
        [self.window.blit(pygame.transform.scale(layer, self.res), (0, 0)) for layer in layers]
        pygame.display.flip()
