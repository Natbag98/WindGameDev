from UI.screens import SCREENS, INVENTORY_ITEMS


class UI:

    def __init__(self, game):
        self.game = game

        self.screens = SCREENS
        for element in INVENTORY_ITEMS:
            self.screens['game'].append(element)
        [element.initialize(self.game) for screen in self.screens for element in self.screens[screen]]

    def update(self):
        [element.update() for element in self.screens[self.game.screen]]

    def draw(self, surface):
        [element.draw(surface) for element in self.screens[self.game.screen]]
