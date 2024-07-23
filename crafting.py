from Inventory.items import *


class CraftingRecipe:

    def __init__(self, input, output):
        self.game = None

        self.input_items = input
        self.output_item = output

    def initialize(self, game):
        self.game = game
        self.input_items = [item(game) for item in self.input_items]
        self.output_item = self.output_item(game)

    def craft(self):
        items = {item.__class__.__name__: 0 for item in self.input_items}
        for item in self.input_items:
            items[item.__class__.__name__] += 1

        for item in items:
            if not self.game.player.inventory.has_item(item, items[item]):
                return

        for item in items:
            self.game.player.inventory.remove_item(item)
        self.game.player.inventory.add_item(self.output_item)


CRAFTING_MENU = {
    'placeholder_image_1': [
        CraftingRecipe([BlueBerries], BluePotion),
        CraftingRecipe([OrangeBerries], OrangePotion)
    ]
}
CRAFTING_MENUS = len(CRAFTING_MENU)
