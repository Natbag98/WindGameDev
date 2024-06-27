from main import Game
from UI.ui_element import Element
from color import Color
from load import load_sprites_from_dir

_ui_path = 'assets\\ui'
_ui_assets = {
    'home_button': load_sprites_from_dir(_ui_path, 2, prefix='home_button')[0],
    'inventory_frame_1': load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0]
}

_inventory_items_path = 'assets\\inventory_items'
_inventory_items = {
    'BlueBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='purple_berries')[0],
    'OrangeBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='red_berries')[0]
}


def _home_button_pressed(game: Game):
    game.screen = 'main_menu'


def _exit_button_clicked(game: Game):
    game.running = False


def _start_button_clicked(game: Game):
    game.setup()
    game.screen = 'game'


def _inventory_item_update(game: Game, element: Element, index):
    item = game.player.inventory.items[index]
    if item:
        element.sprites[1] = _inventory_items[item.__name__]
    else:
        element.sprites[1] = None


INVENTORY_ITEMS = [
    Element(
        (
            (Game.WIDTH // 2 - (Game.INVENTORY_ITEM_SIZE[0] * Game.PLAYER_INVENTORY_SIZE) // 2) + i * Game.INVENTORY_ITEM_SIZE[0],
            (Game.HEIGHT - Game.INVENTORY_ITEM_SIZE[1])
        ),
        pos_position='top_left',
        sprites=[_ui_assets['inventory_frame_1'], None],
        update_func=_inventory_item_update,
        update_func_args=(i,)
    )
    for i in range(Game.PLAYER_INVENTORY_SIZE)
]


SCREENS = {
    'game': [
        Element(
            (Game.WIDTH - 20, 20),
            hover_color=Color('white', a=50).color,
            sprites=[_ui_assets['home_button']],
            clicked_func=_home_button_pressed
        ),
        Element(
            (Game.WIDTH // 2, Game.HEIGHT),
            pos_position='bottom_center',
            bg_color=Color('black').color,
            hover_color=Color('black').color,
            size=(Game.INVENTORY_ITEM_SIZE[0] * Game.PLAYER_INVENTORY_SIZE, Game.INVENTORY_ITEM_SIZE[1] * 1.2)
        )
    ],
    'main_menu': [
        Element(
            (0, 0),
            bg_color=Color('black').color,
            size=Game.RES,
            pos_position='top_left'
        ),
        Element(
            (Game.WIDTH // 2, Game.HEIGHT // 2 - 50),
            text='Start New',
            text_size=80,
            clicked_func=_start_button_clicked
        ),
        Element(
            (Game.WIDTH // 2, Game.HEIGHT // 2 + 50),
            bg_color=Color('green').color,
            size=(150, 40),
            clicked_func=_exit_button_clicked
        )
    ]
}
