import os

from main import Game
from Inventory.item import Item
from load import load_sprites_from_dir, load_sprite_sheet_single


_inventory_items_path = 'assets\\inventory_items'
_inventory_items = {
    ''.join([word.capitalize() for word in item.split('.')[0].split('_')]):
    load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix=item)[0]
    for item in os.listdir(_inventory_items_path)
}

_inventory_items_floor = {
    'StonesSmall': load_sprites_from_dir(_inventory_items_path, 0.6, prefix='stones_small')[0]
}


class SmallStonesOrange(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['SmallStonesOrange'])


class SmallStonesBlue(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['SmallStonesBlue'])


class RockOrange(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['RockOrange'])


class RockBlue(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['RockBlue'])


class Rock(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['Rock'])


class OrangeBrick(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['OrangeBrick'])


class Brick(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['Brick'])


class OrangePowder(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['OrangePowder'])


class BluePowder(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['BluePowder'])


class BlueBrick(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['BlueBrick'])


class Plank(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['Plank'])


class SwordBasic(Item):

    def __init__(self, game):
        self.attack_strength = 3
        super().__init__(game, _inventory_items['SwordBasic'], hand=True)


class PickBasic(Item):

    def __init__(self, game):
        self.attack_strength = 1
        super().__init__(game, _inventory_items['PickBasic'], hand=True)


class AxeBasic(Item):

    def __init__(self, game):
        self.attack_strength = 2
        super().__init__(game, _inventory_items['AxeBasic'], hand=True)


class StonesSmall(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['StonesSmall'], floor_sprite=_inventory_items_floor['StonesSmall'])


class BasicCraftingTable(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['BasicCraftingTable'], placeable=True)


class Wood(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['Wood'])


class OrangeBerries(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['OrangeBerries'])


class BlueBerries(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['BlueBerries'])


class SquirrelCarcass(Item):

    def __init__(self, game, squirrel, new=True):
        from Enemy.enemies import _SPRITES
        if new:
            anim = _SPRITES['squirrel'][squirrel.state][squirrel.facing_y][squirrel.facing_x]
        else:
            anim = [_inventory_items['SquirrelCarcass']]
        super().__init__(game, anim[len(anim) - 1], inventory_sprite=_inventory_items['SquirrelCarcass'])


class HedgehogCarcass(Item):

    def __init__(self, game, hedgehog, new=False):
        from Enemy.enemies import _SPRITES
        if new:
            anim = _SPRITES['hedgehog'][hedgehog.state][hedgehog.facing_y][hedgehog.facing_x]
        else:
            anim = [_inventory_items['HedgehogCarcass']]
        super().__init__(game, anim[len(anim) - 1], inventory_sprite=_inventory_items['HedgehogCarcass'])


class OrangePotion(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['OrangePotion'])


class BluePotion(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['BluePotion'])


_INVENTORY_ITEMS = {
    'OrangeBerries': OrangeBerries,
    'BlueBerries': BlueBerries,
    'OrangePotion': OrangePotion,
    'BluePotion': BluePotion,
    'SquirrelCarcass': SquirrelCarcass,
    'HedgehogCarcass': HedgehogCarcass
}
