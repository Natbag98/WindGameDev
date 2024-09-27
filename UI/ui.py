import pygame
from color import Color
from Inventory.item_desc import DESC
import inspect


class UI:

    def __init__(self, game):
        self.game = game

        from UI.screens import SCREENS
        import Inventory

        for name, obj in inspect.getmembers(Inventory.items):
            if inspect.isclass(obj):
                if not name in DESC.keys():
                    print(f'ERROR: Item {name} does not have a description')

        self.item_desc = {
            item: self.create_rendered_text(DESC[item], 35)
            for item in DESC
        }
        self.item_desc_name = {
            item: self.create_rendered_text(item, 35)
            for item in DESC
        }
        self.item_desc_display = None

        self.crafting_menu_open = None
        self.active_crafting_recipe = None
        self.screens = SCREENS
        [element.initialize(self.game) for screen in self.screens for element in self.screens[screen]]

    @staticmethod
    def create_rendered_text(text, text_size, text_color=Color('black').color, font=None):
        sys_font = pygame.font.SysFont(font, text_size)
        return sys_font.render(text, True, text_color)

    def update(self):
        self.item_desc_display = None
        [element.update() for element in self.screens[self.game.screen]]

    def draw(self, surface):
        [element.draw(surface) for element in self.screens[self.game.screen]]
