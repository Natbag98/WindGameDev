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


# TODO : Finish crafting menu ui placement and sprite display
CRAFTING_MENU = {
    'placeholder0': [
        CraftingRecipe([Wood, Wood, Wood], BasicCraftingTable),
        CraftingRecipe([Wood, StonesSmall, StonesSmall], SwordBasic),
        CraftingRecipe([Wood, StonesSmall, StonesSmall], AxeBasic),
        CraftingRecipe([Wood, StonesSmall, StonesSmall], PickBasic),
        CraftingRecipe([StonesSmall, Rock], Firestarter),
        CraftingRecipe([Wood, Wood, Firestarter], Campfire)
    ],
    'placeholder1': [
        CraftingRecipe([BlueBerries, BluePowder], BluePotion),
        CraftingRecipe([OrangeBerries, OrangePowder], OrangePotion),
        CraftingRecipe([Wood, Wood], Plank),
        CraftingRecipe([SmallStonesBlue, RockBlue], BluePowder),
        CraftingRecipe([SmallStonesOrange, RockOrange], OrangePowder),
        CraftingRecipe([Rock, Rock, StonesSmall], Brick),
        CraftingRecipe([RockOrange, RockOrange, SmallStonesOrange], OrangeBrick),
        CraftingRecipe([RockBlue, RockBlue, SmallStonesBlue], BlueBrick),
    ]
}
CRAFTING_MENUS = len(CRAFTING_MENU)
