import pygame


class Shrub:

    def __init__(self, game, chunk, pos, sprites):
        self.game = game
        self.chunk = chunk

        self.pos = pos + self.chunk.pos
        self.sprites = sprites
        self.active_sprite = 0
        self.frame = self.sprites[self.active_sprite]
        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def update(self):
        self.frame = self.sprites[self.active_sprite]
        self.rect.update(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def draw(self, surface):
        surface.blit(self.frame, self.rect.topleft - self.game.camera.offset)
        #pygame.draw.circle(surface, 'red', self.pos - self.game.camera.offset, 5)
        #pygame.draw.rect(surface, 'red', (self.rect.topleft - self.game.camera.offset, self.rect.size), 5)