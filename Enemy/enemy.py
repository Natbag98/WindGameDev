from pygame import Vector2
from main import CollideCircle
from main import Game
import pygame
import random
import math


class Enemy:

    def __init__(
        self,
        game,
        chunk,
        sprites,
        animation_factors,
        move_speed,
        start_pos: Vector2,
        behaviour='patrol_radius',
        patrol_radius=100,
        stop_max=0,
        path=None,
        aggressive=False,
        aggressive_range=50,
        attacks=None
    ):
        self.game = game
        self.chunk = chunk

        self.sprites = sprites
        self.animation_factors = animation_factors

        self.behaviour = behaviour
        self.patrol_radius = patrol_radius
        self.stop_max = stop_max
        self.patrol_center = start_pos.xy
        self.path = path
        self.active_point = -1

        self.timer_name = str(self)
        self.game.timers.add_timer(self.timer_name)
        self.collided_with_target_last_frame = False

        self.aggressive = aggressive
        self.aggressive_range = aggressive_range
        self.attacks = attacks

        self.move_speed = move_speed
        self.pos = start_pos
        self.state = 'idle'
        self.animation_index = 0
        self.facing_x = 'left'
        self.facing_y = 'down'
        self.frame = self.sprites[self.state][self.facing_y][self.facing_x][0]

        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.frame.get_size()), self.frame.get_size())

        self.target_pos = start_pos

    def update(self):
        if self.rect.collidepoint(self.target_pos):
            if not self.collided_with_target_last_frame and self.stop_max:
                self.game.timers.add_timer(self.timer_name, random.randrange(0, self.stop_max))

            self.collided_with_target_last_frame = True

            if self.game.timers.check_max(self.timer_name):
                if self.behaviour == 'patrol_radius':
                    radius = self.patrol_radius * math.sqrt(random.random())
                    theta = 2 * math.pi * random.random()
                    self.target_pos = Vector2(
                        (self.patrol_center[0] + radius * math.cos(theta), self.patrol_center[1] + radius * math.sin(theta))
                    )
                if self.behaviour == 'patrol':
                    if self.rect.collidepoint(self.path[self.active_point][0], self.path[self.active_point][1]):
                        self.active_point += 1
                        if self.active_point >= len(self.path):
                            self.active_point = 0
                        self.target_pos.update(self.path[self.active_point])
        else:
            self.collided_with_target_last_frame = False

        if self.aggressive:
            if pygame.sprite.collide_circle(
                    CollideCircle(self.game.player.rect, 2),
                    CollideCircle(self.rect, self.aggressive_range)
            ):
                self.target_pos.update(self.game.player.rect.center)

        self.state = 'idle'
        velocity = self.pos.move_towards(self.target_pos, self.move_speed * self.game.delta_time) - self.pos

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

        animation = self.sprites[self.state][self.facing_y][self.facing_x]
        if self.animation_index // self.animation_factors[self.state] >= len(animation):
            self.animation_index = 0

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
