import pygame.display


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
        self.window.fill(self.game.BG_COLOR)
        [self.window.blit(pygame.transform.scale(layer, self.res), (0, 0)) for layer in layers]
        pygame.display.flip()
