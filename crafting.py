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
        required_items = {item.__class__.__name__: 0 for item in self.input_items}
        for item in self.input_items:
            required_items[item.__class__.__name__] += 1

        for item in required_items:
            if not self.game.player.inventory.has_item(item, required_items[item]):
                return

        for item in required_items:
            self.game.player.inventory.remove_item(item, required_items[item])
        self.game.player.inventory.add_item(self.output_item)


CRAFTING_MENU = {
    BasicCraftingTable(None).sprite: [
        CraftingRecipe([Wood, Wood, Wood], BasicCraftingTable)
    ]
}
CRAFTING_MENUS = len(CRAFTING_MENU)
