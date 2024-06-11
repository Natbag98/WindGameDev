import pygame
from pygame import Vector2
from color import Color


class Player:
    MOVE_SPEED = 100

    def __init__(self, game):
        self.game = game

        self.pos = Vector2(0, 0)
        self.size = 30
        self.state = 'idle'
        self.rect = pygame.Rect((1, 1, 1, 1))

    def update(self):
        velocity = Vector2(0, 0)

        if self.game.input.keys[pygame.K_w].held:
            velocity.xy += (0, -1)
        if self.game.input.keys[pygame.K_s].held:
            velocity.xy += (0, 1)
        if self.game.input.keys[pygame.K_a].held:
            velocity.xy += (-1, 0)
        if self.game.input.keys[pygame.K_d].held:
            velocity.xy += (1, 0)

        if velocity:
            self.state = 'moving'
            self.pos.xy += velocity.normalize() * self.MOVE_SPEED * self.game.delta_time
        else:
            self.state = 'idle'

        self.rect.update(self.pos, (self.size, self.size))

    def draw(self, surface):
        pygame.draw.rect(surface, Color('white').color, self.rect)
