from pygame import Vector2
from main import Game
import pygame


class FloorItem:

    def __init__(self, game, chunk, pos, item):
        self.game = game
        self.chunk = chunk

        self.pos = Vector2(pos)
        self.item = item
        self.rect = pygame.Rect(
            Game.get_centered_position(self.pos, self.item.floor_sprite.get_size()),
            self.item.floor_sprite.get_size()
        )

    def active_update(self):
        if self.rect.colliderect(self.game.player.rect) and self.game.input.keys[pygame.K_e].pressed:
            self.game.player.inventory.add_item(self.item)
            self.chunk.floor_items.remove(self)

    def draw(self, surface):
        surface.blit(self.item.floor_sprite, self.rect.topleft - self.game.camera.offset)
