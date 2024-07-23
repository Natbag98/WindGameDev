import pygame
from color import Color


class UI:

    def __init__(self, game):
        self.game = game

        from UI.screens import SCREENS

        self.crafting_menu_open = None
        self.active_crafting_recipe = None
        self.screens = SCREENS
        [element.initialize(self.game) for screen in self.screens for element in self.screens[screen]]

    @staticmethod
    def create_rendered_text(text, text_size, text_color=Color('black').color, font=None):
        sys_font = pygame.font.SysFont(font, text_size)
        return sys_font.render(text, True, text_color)

    def update(self):
        [element.update() for element in self.screens[self.game.screen]]

    def draw(self, surface):
        [element.draw(surface) for element in self.screens[self.game.screen]]
