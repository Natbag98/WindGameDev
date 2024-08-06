from pygame import Vector2
from main import CollideCircle
import pygame
import random


class Enemy:

    def __init__(
        self,
        game,
        chunk,
        sprites,
        animation_factors,
        move_speed,
        health,
        start_pos: Vector2,
        behaviour='patrol_radius',
        patrol_radius=100,
        stop_max=0,
        path=None,
        aggressive=False,
        aggressive_range=50,
        attacks=None,
        denied_biomes=(),
        bound_to_chunk=True,
        damage_amount=0,
        attack_cooldown=0,
    ):
        self.game = game
        self.chunk = chunk
        self.bound_to_chunk = bound_to_chunk
        self.start_pos_base = start_pos
        self.start_pos = start_pos + self.chunk.pos
        self.health = health

        self.sprites = sprites
        self.animation_factors = animation_factors

        self.behaviour = behaviour
        self.patrol_radius = patrol_radius
        self.stop_max = stop_max
        self.patrol_center = self.start_pos.xy
        self.path = path
        self.active_point = -1
        self.damage_amount = damage_amount
        self.attack_cooldown = attack_cooldown

        self.timer_name = str(self)
        self.attack_timer_name = f'{str(self)}_attack_timer'
        self.game.timers.add_timer(self.timer_name)
        self.game.timers.add_timer(self.attack_timer_name)
        self.collided_with_target_last_frame = False

        self.aggressive = aggressive
        self.aggressive_range = aggressive_range
        self.attacks = attacks

        self.move_speed = move_speed
        self.pos = self.start_pos
        self.state = 'idle'
        self.animation_index = 0
        self.facing_x = 'left'
        self.facing_y = 'down'
        self.frame = self.sprites[self.state][self.facing_y][self.facing_x][0]

        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

        self.target_pos = self.start_pos
        self.denied_biomes = denied_biomes
        self.valid_targets = self.get_valid_target_positions()
        self.hit = False
        self.dead = False
        self.attacking = False

    def get_valid_target_positions(self):
        valid_targets = []

        if self.behaviour == 'patrol_radius':
            for biome in self.chunk.biome_cells:
                if biome not in self.denied_biomes:
                    for cell in self.chunk.biome_cells[biome]:
                        if pygame.sprite.collide_circle(
                            CollideCircle(self.rect, self.patrol_radius),
                            CollideCircle(
                                (
                                        cell[0] + self.chunk.pos[0], cell[1] + self.chunk.pos[1],
                                        self.game.map.CELL_SIZE, self.game.map.CELL_SIZE
                                ),
                                self.game.map.CELL_SIZE // 2
                            )
                        ):
                            valid_targets.append(
                                (round(cell[0] + self.chunk.pos[0]), round(cell[1] + self.chunk.pos[1]))
                            )

        return valid_targets

    def get_target_pos(self):
        target_pos = Vector2(0, 0)
        if self.behaviour == 'patrol_radius':
            target_pos = Vector2(random.choice(self.valid_targets))

        if self.behaviour == 'patrol':
            if self.rect.collidepoint(self.path[self.active_point][0], self.path[self.active_point][1]):
                self.active_point += 1
                if self.active_point >= len(self.path):
                    self.active_point = 0
                    target_pos.update(round(self.path[self.active_point]))

        return target_pos

    def get_run_pos(self):
        return self.pos.move_towards(-self.game.player.pos, self.move_speed * self.game.delta_time) - self.pos

    def get_bounding_rect(self):
        bounding_rect = self.sprites[self.state][self.facing_y][self.facing_x][0].get_bounding_rect()
        if type(bounding_rect) is list:
            bounding_rect = bounding_rect[0]
        return pygame.Rect(
            bounding_rect.x + self.rect.topleft[0],
            bounding_rect.y + self.rect.topleft[1],
            bounding_rect.size[0],
            bounding_rect.size[1]
        )

    def damage(self, damage):
        self.hit = True
        self.health -= damage
        self.animation_index = 0

        if self.behaviour == 'patrol_radius' and not self.aggressive:
            self.target_pos = self.get_target_pos()

    def death_internal(self):
        self.dead = True
        self.animation_index = 0

    def death(self):
        self.chunk.enemies.remove(self)

    def attack(self):
        self.target_pos = self.get_target_pos()
        self.game.timers.add_timer(self.attack_timer_name, self.attack_cooldown)
        self.attacking = True
        self.animation_index = 0
        self.game.player.damage(self.damage_amount)

    def update(self):
        if self.rect.collidepoint(self.target_pos):
            if not self.collided_with_target_last_frame and self.stop_max:
                self.game.timers.add_timer(self.timer_name, random.randrange(0, self.stop_max))

            self.collided_with_target_last_frame = True

            if self.game.timers.check_max(self.timer_name):
                self.target_pos = self.get_target_pos()

        else:
            self.collided_with_target_last_frame = False

        if self.aggressive and self.game.timers.check_max(self.attack_timer_name):
            if pygame.sprite.collide_circle(
                    CollideCircle(self.game.player.rect, 2),
                    CollideCircle(self.rect, self.aggressive_range)
            ):
                self.target_pos.update(self.game.player.rect.center)

        if self.health <= 0 and not self.dead:
            self.death_internal()
            return

        self.state = 'idle'
        velocity = self.pos.move_towards(self.target_pos, self.move_speed * self.game.delta_time) - self.pos

        if self.dead or self.hit or self.attacking:
            velocity = Vector2(0, 0)

        if velocity.x < 0:
            self.facing_x = 'left'
        elif velocity.x > 0:
            self.facing_x = 'right'
        if velocity.y < 0:
            self.facing_y = 'up'
        elif velocity.y > 0:
            self.facing_y = 'down'

        if not velocity == Vector2(0, 0):
            self.state = 'moving'

        self.pos += velocity

        if self.get_bounding_rect().colliderect(
                self.game.player.get_bounding_rect()
        ) and self.target_pos == self.game.player.rect.center and not self.attacking:
            self.attack()

        if self.hit:
            self.state = 'hit'
        if self.dead:
            self.state = 'death'
        if self.attacking:
            self.state = 'attacking'

        animation = self.sprites[self.state][self.facing_y][self.facing_x]
        if self.animation_index // self.animation_factors[self.state] >= len(animation):
            self.animation_index = 0

            if self.state == 'death':
                self.death()
                return

            self.hit = False
            self.attacking = False
            if velocity:
                self.state = 'moving'
            else:
                self.state = 'idle'
            animation = self.sprites[self.state][self.facing_y][self.facing_x]

        if self.animation_index == 0:
            self.frame = animation[0]
        else:
            self.frame = animation[self.animation_index // self.animation_factors[self.state]]

        self.animation_index += round(self.game.delta_time * 100)

        self.rect.update(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

    def draw(self, surface):
        surface.blit(self.frame, self.rect.topleft - self.game.camera.offset)
        #pygame.draw.circle(surface, 'red', self.pos - self.game.camera.offset, 5)
        #pygame.draw.rect(surface, 'red', (self.rect.topleft - self.game.camera.offset, self.rect.size), 5)
        #pygame.draw.rect(surface, 'red', (self.get_bounding_rect().topleft - self.game.camera.offset, self.get_bounding_rect().size), 5)
