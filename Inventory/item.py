

class Item:

    def __init__(self, game, sprite, equipable='', placeable=False, consumable=False):
        self.game = game

        self.sprite = sprite
        self.equipable = equipable
        self.placeable = placeable
        self.consumable = consumable
