import random
import pygame


class Shrub:

    def __init__(self, game, parent, pos, sprites, id, solid=True, new=False, health=1, animated=False, animation_factor=15):
        self.game = game
        self.id = id

        from map_chunk import Chunk
        if type(parent) is Chunk:
            self.pos = pos + parent.pos
            self.parent_type = 'chunk'
        else:
            self.pos = pos
            self.parent_type = 'deep_level'

        if not new:
            self.pos = pos

        self.solid = solid
        self.parent = parent
        self.sprites = sprites
        self.active_sprite = 0
        self.frame = self.sprites[self.active_sprite]
        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())
        self.health = health
        self.animated = animated

        self.animation_index = 0
        self.animation_factor = animation_factor

    def get_bounding_rect(self):
        bounding_rect = self.frame.get_bounding_rect()
        if type(bounding_rect) is list:
            bounding_rect = bounding_rect[0]
        return pygame.Rect(
            bounding_rect.x + self.rect.topleft[0],
            bounding_rect.y + self.rect.topleft[1],
            bounding_rect.size[0],
            bounding_rect.size[1]
        )

    def interact(self):
        pass

    def update(self):
        self.frame = self.sprites[self.active_sprite]
        self.rect.update(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def active_update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.map.shrubs_colliding_with_player.append(self)
            if self.game.input.keys[pygame.K_e].pressed:
                self.interact()

        if self.health < 1:
            self.death()

        if self.animated:
            if self.animation_index // self.animation_factor >= len(self.sprites):
                self.animation_index = 0

            if self.animation_index == 0:
                self.frame = self.sprites[0]
            else:
                self.frame = self.sprites[self.animation_index // self.animation_factor]

            self.animation_index += round(self.game.delta_time * 100)

    def death(self):
        self.parent.shrubs.remove(self)

    def attacked(self, weapon_type, level, strength):
        pass

    def draw(self, surface):
        surface.blit(self.frame, self.rect.topleft - self.game.camera.offset)
