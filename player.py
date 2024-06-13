import pygame
from pygame import Vector2
from load import load_sprite_sheet_single


class Player:
    MOVE_SPEED = 100

    def __init__(self, game):
        self.game = game

        path = f'assets\\main_character'
        size = 1.5
        self.sprites = {
            'idle': {
                'up': load_sprite_sheet_single(path, '_up idle.png', 4, 2, size),
                'down': load_sprite_sheet_single(path, '_down idle.png', 4, 2, size),
                'left': load_sprite_sheet_single(path, '_side idle.png', 4, 2, size),
                'right': load_sprite_sheet_single(path, '_side idle.png', 4, 2, size, flip_x=True)
            },
            'moving': {
                'up': load_sprite_sheet_single(path, '_up walk.png', 4, 2, size),
                'down': load_sprite_sheet_single(path, '_down walk.png', 4, 2, size),
                'left': load_sprite_sheet_single(path, '_side walk.png', 4, 2, size),
                'right': load_sprite_sheet_single(path, '_side walk.png', 4, 2, size, flip_x=True)
            }
        }

        self.animation_factors = {
            'idle': 40,
            'moving': 15
        }

        self.pos = Vector2(0, 0)
        self.state = 'idle'
        self.animation_index = 0
        self.facing = 'down'
        self.frame = self.sprites[self.state][self.facing][0]

        self.rect = pygame.Rect(self.pos, self.frame.get_size())

    def update(self):
        velocity = Vector2(0, 0)

        if self.game.input.keys[pygame.K_a].held:
            self.facing = 'left'
            velocity.xy += (-1, 0)
        if self.game.input.keys[pygame.K_d].held:
            self.facing = 'right'
            velocity.xy += (1, 0)
        if self.game.input.keys[pygame.K_w].held:
            self.facing = 'up'
            velocity.xy += (0, -1)
        if self.game.input.keys[pygame.K_s].held:
            self.facing = 'down'
            velocity.xy += (0, 1)

        if velocity:
            self.state = 'moving'
            self.pos.xy += velocity.normalize() * self.MOVE_SPEED * self.game.delta_time
        else:
            self.state = 'idle'

        animation = self.sprites[self.state][self.facing]
        if self.animation_index // self.animation_factors[self.state] >= len(animation):
            self.animation_index = 0

        if self.animation_index == 0:
            self.frame = animation[0]
        else:
            self.frame = animation[self.animation_index // self.animation_factors[self.state]]

        self.animation_index += round(self.game.delta_time * 100)

        self.rect.update(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def draw(self, surface):
        surface.blit(self.frame, self.rect)
        pygame.draw.circle(surface, 'red', self.rect.center, 5)
        pygame.draw.rect(surface, 'red', self.rect, 5)
