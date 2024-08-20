

class Item:

    def __init__(
        self,
        game,
        sprite,
        equipable='',
        placeable=False,
        shrub_to_place=None,
        consumable=False,
        floor_sprite=None,
        inventory_sprite=None
    ):
        self.game = game

        self.sprite = sprite
        self.equipable = equipable
        self.placeable = placeable
        self.shrub_to_place = shrub_to_place
        self.consumable = consumable
        self.floor_sprite = floor_sprite
        if not floor_sprite:
            self.floor_sprite = sprite
        self.inventory_sprite = inventory_sprite
