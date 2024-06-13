import  pygame
from pygame import Vector2
from main import Game


class Camera:

    def __init__(self, game):
        self.game = game

        self.offset = Vector2(0, 0)
        self.rect = pygame.Rect(self.offset, Game.RES)

    def update(self):
        self.offset.update(self.game.get_centered_position(self.game.player.pos, Game.RES))
        self.rect = pygame.Rect(self.offset, Game.RES)
