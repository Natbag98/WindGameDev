import pygame.display
from concurrent.futures import ThreadPoolExecutor, as_completed


class Window:
    BASE_RES = (1920 // 2, 1080 // 2)

    def __init__(self, game):
        self.game = game
        self.set_res(self.BASE_RES)

    def set_res(self, res):
        self.res = res
        self.res_scale = (self.res[0] / self.game.RES[0], self.res[1] / self.game.RES[1])

        self.window = pygame.display.set_mode(self.res, pygame.SRCALPHA)
        pygame.display.set_caption('Wind')

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def scale_surf(self, layer, surface, size):
        return pygame.transform.scale(surface, size), layer

    def render(self, layers):
        self.window.fill(self.game.BG_COLOR)

        layers_to_draw = [pygame.Surface((0, 0)) for _ in range(len(layers))]
        with ThreadPoolExecutor() as executor:
            results = []
            for i, layer in enumerate(layers):
                results.append(executor.submit(self.scale_surf, i, layer, self.res))

            for result in as_completed(results):
                surface, layer = result.result()
                layers_to_draw[layer] = surface

        [self.window.blit(layer, (0, 0)) for layer in layers_to_draw]
        pygame.display.flip()
