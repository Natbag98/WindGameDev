from main import Game
from UI.ui_element import Element
from color import Color
from load import load_sprites_from_dir

CRAFTING_BACK_SIZE = (Game.INVENTORY_ITEM_SIZE[0] * 1.1, Game.INVENTORY_ITEM_SIZE[1] * 1.1)

_ui_path = 'assets\\ui'
_ui_assets = {
    'home_button': load_sprites_from_dir(_ui_path, 2, prefix='home_button')[0],
    'inventory_frame_1': load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    'inventory_back': load_sprites_from_dir(f'{_ui_path}\\inventory_back', CRAFTING_BACK_SIZE)
}

_inventory_items_path = 'assets\\inventory_items'
_inventory_items = {
    'BlueBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='purple_berries')[0],
    'OrangeBerries': load_sprites_from_dir(_inventory_items_path, Game.INVENTORY_ITEM_SIZE, prefix='red_berries')[0]
}


def _home_button_pressed(game: Game):
    game.paused = not game.paused


def _exit_button_clicked(game: Game):
    game.running = False


def _start_button_clicked(game: Game):
    game.setup()


def _inventory_item_update(game: Game, element: Element, index):
    item = game.player.inventory.items[index]
    if item:
        element.sprites[1] = _inventory_items[item.__name__]
    else:
        element.sprites[1] = None


def _loading_text_update(game: Game, element: Element):
    element.text = f'{game.chunk_progress} \\ {game.total_chunks}'
    element.render_text()


def _crafting_menu_update(game: Game, element: Element, index):
    if game.input.mouse['left'].interact(element.rect, 'clicked'):
        if game.ui.crafting_menu_open == index:
            game.ui.crafting_menu_open = None
            return
        game.ui.crafting_menu_open = index


def crafting_menu_bg_update(game: Game, element: Element, index):
    element.hidden = True
    if game.ui.crafting_menu_open == index:
        element.hidden = False


CRAFTING_MENU_BG = []
for i in range(Game.CRAFTING_MENUS):
    back = 4
    if i == 0:
        back = 3
    elif i == Game.CRAFTING_MENUS - 1:
        back = 2
    CRAFTING_MENU_BG.append(
        Element(
            (
                0,
                (Game.HEIGHT // 2 - (CRAFTING_BACK_SIZE[1] * Game.CRAFTING_MENUS) // 2) + i * CRAFTING_BACK_SIZE[1],
            ),
            pos_position='top_left',
            sprites=[_ui_assets['inventory_back'][back]]
        )
    )

CRAFTING_ITEM_MENUS_BG = []
for i in range(Game.CRAFTING_MENUS):
    for j in range(len(list(Game.CRAFTING_MENU.values())[i])):
        back = 4
        if j == 0:
            back = 3
        elif j == Game.CRAFTING_MENUS - 1:
            back = 2
        CRAFTING_ITEM_MENUS_BG.append(
            Element(
                (
                    CRAFTING_BACK_SIZE[0],
                    (Game.HEIGHT // 2 - (CRAFTING_BACK_SIZE[1] * Game.CRAFTING_MENUS) // 2) + j * CRAFTING_BACK_SIZE[1],
                ),
                pos_position='top_left',
                sprites=[_ui_assets['inventory_back'][back]],
                update_func=crafting_menu_bg_update,
                update_func_args=(i,),
                hidden=True
            )
        )

CRAFTING_ITEMS = []
for i in range(Game.CRAFTING_MENUS):
    for j, crafting_item in enumerate(list(Game.CRAFTING_MENU.values())[i]):
        CRAFTING_ITEMS.append(
            Element(
                (
                    Game.CRAFTING_ITEM_SIZE[0],
                    (Game.HEIGHT // 2 - (Game.CRAFTING_ITEM_SIZE[0] * Game.CRAFTING_MENUS) // 2) + j * Game.CRAFTING_ITEM_SIZE[0],
                ),
                pos_position='top_left',
                sprites=[_ui_assets['inventory_frame_1']],
                update_func=crafting_menu_bg_update,
                update_func_args=(i,),
                hidden=True
            )
        )


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
        ),
        *[
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
        ],
        *CRAFTING_MENU_BG,
        *CRAFTING_ITEM_MENUS_BG,
        *[
            Element(
                (
                    0,
                    (Game.HEIGHT // 2 - (Game.CRAFTING_ITEM_SIZE[0] * Game.CRAFTING_MENUS) // 2) + i * Game.CRAFTING_ITEM_SIZE[0],
                ),
                pos_position='top_left',
                sprites=[_ui_assets['inventory_frame_1']],
                update_func=_crafting_menu_update,
                update_func_args=(i,)
            )
            for i in range(Game.CRAFTING_MENUS)
        ],
        *CRAFTING_ITEMS
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
    ],
    'loading': [
        Element(
            (0, 0),
            bg_color=Color('black').color,
            size=Game.RES,
            pos_position='top_left'
        ),
        Element(
            (0, 0),
            pos_position='top_left',
            text='None',
            text_size=80,
            update_func=_loading_text_update
        ),
    ]
}
