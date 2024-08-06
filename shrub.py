import random
import pygame


class Shrub:

    def __init__(self, game, parent, pos, sprites):
        self.game = game
        self.id = str(random.randbytes(20))

        from map_chunk import Chunk
        if type(parent) is Chunk:
            self.pos = pos + parent.pos
            self.parent_type = 'chunk'
        else:
            self.pos = pos
            self.parent_type = 'deep_level'

        self.parent = parent
        self.sprites = sprites
        self.active_sprite = 0
        self.frame = self.sprites[self.active_sprite]
        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def interact(self):
        pass

    def update(self):
        self.frame = self.sprites[self.active_sprite]
        self.rect.update(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def active_update(self):
        if self.rect.colliderect(self.game.player.rect) and self.game.input.keys[pygame.K_e].pressed:
            self.interact()

    def draw(self, surface):
        surface.blit(self.frame, self.rect.topleft - self.game.camera.offset)
        pygame.draw.circle(surface, 'red', self.pos - self.game.camera.offset, 5)
        pygame.draw.rect(surface, 'red', (self.rect.topleft - self.game.camera.offset, self.rect.size), 5)
