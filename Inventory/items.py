from main import Game
from Inventory.item import Item
from load import load_sprites_from_dir, load_sprite_sheet_single

_inventory_items_path = 'assets\\inventory_items'
_inventory_items = {
    'BlueBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='purple_berries')[0],
    'OrangeBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='red_berries')[0],
    'OrangePotion': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='orange_potion')[0],
    'BluePotion': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='blue_potion')[0],
    'SquirrelCarcass': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='squirrel_carcass')[0],
    'HedgehogCarcass': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='hedgehog_carcass')[0],
    'Wood': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='wood')[0],
    'BasicCraftingTable': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='basic_crafting_table')[0]
}


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
