from Inventory.items import *


class CraftingRecipe:

    def __init__(self, input, output):
        self.game = None

        self.input_items = input
        self.output_item = output

    def initialize(self, game):
        self.input_items = [item(game) for item in self.input_items]
        self.output_item = self.output_item(game)


CRAFTING_MENU = {
    'placeholder_image_1': [
        CraftingRecipe([BlueBerries], BluePotion),
        CraftingRecipe([OrangeBerries], OrangePotion)
    ]
}
CRAFTING_MENUS = len(CRAFTING_MENU)
