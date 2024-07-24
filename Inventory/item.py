

class Item:

    def __init__(self, game, sprite, equipable='', placeable=False, consumable=False, floor_sprite=None):
        self.game = game

        self.sprite = sprite
        self.equipable = equipable
        self.placeable = placeable
        self.consumable = consumable
        self.floor_sprite = floor_sprite
        if not floor_sprite:
            self.floor_sprite = sprite
