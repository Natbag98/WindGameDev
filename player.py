import pygame
from pygame import Vector2
from load import load_sprite_sheet_single
from Inventory.inventory import Inventory


class Player:
    MOVE_SPEED = 500
    BASE_DAMAGE = 2

    def __init__(self, game):
        self.game = game

        path = f'assets\\main_character'
        size = 2
        self.sprites = {
            'idle': {
                'up': load_sprite_sheet_single(path, '_up idle.png', 4, 2, size, read_axis='y'),
                'down': load_sprite_sheet_single(path, '_down idle.png', 4, 2, size, read_axis='y'),
                'left': load_sprite_sheet_single(path, '_side idle.png', 4, 2, size, read_axis='y'),
                'right': load_sprite_sheet_single(path, '_side idle.png', 4, 2, size, flip_x=True, read_axis='y')
            },
            'moving': {
                'up': load_sprite_sheet_single(path, '_up walk.png', 4, 2, size, read_axis='y'),
                'down': load_sprite_sheet_single(path, '_down walk.png', 4, 2, size, read_axis='y'),
                'left': load_sprite_sheet_single(path, '_side walk.png', 4, 2, size, read_axis='y'),
                'right': load_sprite_sheet_single(path, '_side walk.png', 4, 2, size, flip_x=True, read_axis='y')
            },
            'attacking': {
                'up': load_sprite_sheet_single(path, '_up attack.png', 2, 2, size, read_axis='y'),
                'down': load_sprite_sheet_single(path, '_down attack.png', 2, 2, size, read_axis='y'),
                'left': load_sprite_sheet_single(path, '_side attack.png', 2, 2, size, read_axis='y'),
                'right': load_sprite_sheet_single(path, '_side attack.png', 2, 2, size, flip_x=True, read_axis='y')
            },
            'hit': {
                'up': load_sprite_sheet_single(path, 'hit_up.png', 4, 2, size * 3, read_axis='y'),
                'down': load_sprite_sheet_single(path, 'hit_down.png', 4, 2, size * 3, read_axis='y'),
                'left': load_sprite_sheet_single(path, 'hit_side.png', 4, 2, size * 3, read_axis='y'),
                'right': load_sprite_sheet_single(path, 'hit_side.png', 4, 2, size * 3, flip_x=True, read_axis='y')
            },
            'death': {
                'up': load_sprite_sheet_single(path, 'hit_up.png', 4, 2, size * 3, read_axis='y'),
                'down': load_sprite_sheet_single(path, 'hit_down.png', 4, 2, size * 3, read_axis='y'),
                'left': load_sprite_sheet_single(path, 'hit_side.png', 4, 2, size * 3, read_axis='y'),
                'right': load_sprite_sheet_single(path, 'hit_side.png', 4, 2, size * 3, flip_x=True, read_axis='y')
            },
            'pickup': {
                'left': load_sprite_sheet_single(path, '_pick up.png', 4, 2, size, read_axis='y'),
                'right': load_sprite_sheet_single(path, '_pick up.png', 4, 2, size, flip_x=True, read_axis='y')
            }
        }

        self.animation_factors = {
            'idle': 15,
            'moving': 15,
            'attacking': 15,
            'hit': 5,
            'pickup': 5
        }

        self.inventory = Inventory(self.game, self)

        self.pos = Vector2(0, 0)
        self.state = 'idle'
        self.animation_index = 0
        self.facing = 'down'
        self.frame = self.sprites[self.state][self.facing][0]
        self.health = 10

        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

        self.attacking = False
        self.hit = False
        self.death = False
        self.pickup = False

    def get_bounding_rect(self, animation=None):
        bounding_rect = self.sprites[self.state][self.facing][0].get_bounding_rect()
        if animation:
            bounding_rect = animation[0].get_bounding_rect()
        if type(bounding_rect) == list:
            bounding_rect = bounding_rect[0]

        return pygame.Rect(
            bounding_rect.x + self.rect.topleft[0],
            bounding_rect.y + self.rect.topleft[1],
            bounding_rect.size[0],
            bounding_rect.size[1]
        )

    def basic_attack(self):
        self.game.active_map.basic_damage(self.get_bounding_rect(self.sprites['attacking'][self.facing]), self.BASE_DAMAGE)

    def damage(self, damage):
        self.health -= damage
        self.hit = True
        self.animation_index = 0

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

        if self.game.input.keys[pygame.K_e].pressed:
            self.pickup = True

        if self.hit or self.attacking:
            velocity = Vector2(0, 0)

        if velocity:
            self.state = 'moving'
            self.pos.xy += velocity.normalize() * self.MOVE_SPEED * self.game.delta_time
        else:
            self.state = 'idle'

        if self.game.input.keys[pygame.K_SPACE].pressed and not self.attacking:
            self.attacking = True
            self.animation_index = 0
            self.basic_attack()

        if self.pickup:
            self.state = 'pickup'
            if self.facing in ['up', 'down']:
                self.facing = 'left'
        elif self.attacking:
            self.state = 'attacking'
        elif self.hit:
            self.state = 'hit'

        animation = self.sprites[self.state][self.facing]
        if self.animation_index // self.animation_factors[self.state] >= len(animation):
            self.animation_index = 0

            self.attacking = False
            self.hit = False
            self.pickup = False
            if velocity:
                self.state = 'moving'
            else:
                self.state = 'idle'
            animation = self.sprites[self.state][self.facing]

        if self.animation_index == 0:
            self.frame = animation[0]
        else:
            self.frame = animation[self.animation_index // self.animation_factors[self.state]]

        self.animation_index += round(self.game.delta_time * 100)

        self.rect.update(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def draw(self, surface):
        surface.blit(self.frame, self.rect.topleft - self.game.camera.offset)
        pygame.draw.circle(surface, 'red', self.pos - self.game.camera.offset, 5)
        pygame.draw.rect(surface, 'red', (self.rect.topleft - self.game.camera.offset, self.rect.size), 5)
        pygame.draw.rect(surface, 'red', (self.get_bounding_rect().topleft - self.game.camera.offset, self.get_bounding_rect().size), 5)
