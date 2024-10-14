import pygame
from pygame import Vector2
from load import load_sprite_sheet_single
from Inventory.inventory import Inventory


class Player:
    MOVE_SPEED = 200
    COLL_PADDING = 25
    BASE_ATTACK_STRENGTH = 1

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
                'right': load_sprite_sheet_single(path, '_pick up.png', 4, 2, size, flip_x=True, read_axis='y'),
                'up': load_sprite_sheet_single(path, '_pick up.png', 4, 2, size, flip_x=True, read_axis='y'),
                'down': load_sprite_sheet_single(path, '_pick up.png', 4, 2, size, flip_x=True, read_axis='y')
            }
        }

        self.animation_factors = {
            'idle': 15,
            'moving': 15,
            'attacking': 15,
            'hit': 5,
            'pickup': 15
        }

        self.inventory = Inventory(self.game, self)
        self.basic_crafting = False
        self.advanced_crafting = False
        self.food_crafting = False

        self.pos = Vector2(0, 0)
        self.state = 'idle'
        self.animation_index = 0
        self.facing = 'down'
        self.frame = self.sprites[self.state][self.facing][0]
        self.attack_strength = self.BASE_ATTACK_STRENGTH

        self.max_health = 100
        self.health = 100
        self.max_hunger = 100
        self.hunger = 80
        self._hunger = self.hunger
        self.max_sanity = 100
        self.sanity = 80
        self._sanity = self.sanity
        self.max_air = 100
        self.air = 100
        self._air = self.air

        self.food_decay = 0.3
        self.sanity_decay = 0.5
        self.air_decay = 0

        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

        self.attacking = False
        self.hit = False
        self.death = False
        self.pickup = False

        self.death_reason = False

        self.damage_increase_timer_name = f'{self}_damage_timer'
        self.damage_increase_timer_time = 600
        self.damage_increase = 2
        self.game.timers.add_timer(self.damage_increase_timer_name, 0)

    def increase_hunger(self, amount):
        self._hunger += amount

    def increase_damage(self):
        self.game.timers.add_timer(self.damage_increase_timer_name, self.damage_increase_timer_time)

    def increase_health(self, amount):
        self.health += amount

    def get_bounding_rect(self, animation=None, coll=False):
        bounding_rect = self.sprites[self.state][self.facing][0].get_bounding_rect()
        if animation:
            bounding_rect = animation[0].get_bounding_rect()
        if type(bounding_rect) == list:
            bounding_rect = bounding_rect[0]

        if coll:
            return pygame.Rect(
                self.pos,
                (3, 3)
            )
        else:
            return pygame.Rect(
                bounding_rect.x + self.rect.topleft[0],
                bounding_rect.y + self.rect.topleft[1],
                bounding_rect.size[0],
                bounding_rect.size[1]
            )

    def basic_attack(self):
        attack_strength = self.attack_strength
        if not self.game.timers.check_max(self.damage_increase_timer_name):
            attack_strength += self.damage_increase
        self.game.active_map.basic_damage(
            self.get_bounding_rect(self.sprites['attacking'][self.facing]),
            attack_strength
        )

    def damage(self, damage):
        self.health -= damage
        self.hit = True
        self.animation_index = 0

    def check_col_axis_x(self, rect_left: pygame.Rect, rect_right: pygame.Rect):
        if rect_right.x < rect_left.x < rect_right.x + rect_right.size[0]:
            return True

    def check_col(self, velocity, rect):
        collided = False
        temp_velocity = Vector2(round(velocity.x * self.COLL_PADDING), round(velocity.y * self.COLL_PADDING))

        temp_x = self.pos.x
        self.pos.x += temp_velocity.x
        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())
        if self.get_bounding_rect(coll=True).colliderect(rect):
            velocity.x = 0
            collided = True
        self.pos.x = temp_x
        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

        temp_y = self.pos.y
        self.pos.y += temp_velocity.y
        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())
        if self.get_bounding_rect(coll=True).colliderect(rect):
            velocity.y = 0
            collided = True
        self.pos.y = temp_y

        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())
        return velocity, collided

    def update(self):
        if self.game.map.ocean_mask:
            from main import CollideRect
            if pygame.sprite.collide_rect(
                CollideRect(self.get_bounding_rect()),
                CollideRect(pygame.Rect((0, 0), self.game.map.DIMENSIONS))
            ) and self.game.collide_mask_rect(
                self.game.map.ocean_mask,
                CollideRect(self.get_bounding_rect())
            ):
                self.air_decay = -30
            else:
                self.air_decay = 15

        self._hunger -= self.food_decay * self.game.delta_time
        self._sanity -= self.sanity_decay * self.game.delta_time * (self.game.darkness / 255)
        self._air -= self.air_decay * self.game.delta_time

        if self.health < 0:
            self.health = 0
        if self._hunger < 0:
            self._hunger = 0
        if self._sanity < 0:
            self._sanity = 0
        if self._air < 0:
            self._air = 0

        if self.health > self.max_health:
            self.health = self.max_health
        if self._hunger > self.max_hunger:
            self._hunger = self.max_hunger
        if self._sanity > self.max_sanity:
            self._sanity = self.max_sanity
        if self._air > self.max_air:
            self._air = self.max_air

        self.hunger = round(self._hunger)
        self.sanity = round(self._sanity)
        self.air = round(self._air)

        if self.health == 0:
            self.death_reason = 1
        elif self.hunger == 0:
            self.death_reason = 2
        elif self.sanity == 0:
            self.death_reason = 3
        elif self.air == 0:
            self.death_reason = 4

        if self.death_reason:
            self.game.screen = f'death_{self.death_reason}'

        self.attack_strength = self.BASE_ATTACK_STRENGTH
        if self.inventory.hand_item:
            self.attack_strength = self.inventory.hand_item.attack_strength

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

        if self.hit or self.attacking or self.pickup:
            velocity = Vector2(0, 0)

        self.basic_crafting = False
        self.advanced_crafting = False
        self.food_crafting = False
        for shrub in self.game.map.shrubs_colliding_with_player:
            if shrub.solid:
                velocity, collided = self.check_col(velocity, shrub.get_bounding_rect())

            if shrub.__class__.__name__ == 'BasicCraftingTable':
                self.basic_crafting = True

            if shrub.__class__.__name__ == 'Campfire':
                self.food_crafting = True

        if velocity:
            self.state = 'moving'
            self.pos.xy += velocity.normalize() * self.MOVE_SPEED * self.game.delta_time
        else:
            self.state = 'idle'

        if self.game.input.keys[pygame.K_SPACE].pressed and not self.attacking:
            self.attacking = True
            self.animation_index = 0
            self.basic_attack()

            if self.inventory.hand_item:
                hand_item_name = re.findall('[A-Z][^A-Z]*', self.inventory.hand_item.__class__.__name__)
                for shrub in self.game.map.shrubs_colliding_with_player:
                    shrub.attacked(hand_item_name[0], hand_item_name[1], self.inventory.hand_item.attack_strength)

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
        # pygame.draw.circle(surface, 'red', self.pos - self.game.camera.offset, 5)
        # pygame.draw.rect(surface, 'red', (self.rect.topleft - self.game.camera.offset, self.rect.size), 5)
        # pygame.draw.rect(surface, 'red', (self.get_bounding_rect().topleft - self.game.camera.offset, self.get_bounding_rect().size), 5)
