from main import Game
from Inventory.item import Item
from load import load_sprites_from_dir

_inventory_items_path = 'assets\\inventory_items'
_inventory_items = {
    'BlueBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='purple_berries')[0],
    'OrangeBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='red_berries')[0],
    'OrangePotion': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='orange_potion')[0],
    'BluePotion': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='blue_potion')[0]
}


class OrangeBerries(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['OrangeBerries'])


class BlueBerries(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['BlueBerries'])


class OrangePotion(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['OrangePotion'])


class BluePotion(Item):

    def __init__(self, game):
        super().__init__(game, _inventory_items['BluePotion'])
