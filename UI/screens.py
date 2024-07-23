from main import Game
from UI.ui_element import Element
from color import Color
from load import load_sprites_from_dir
from crafting import CRAFTING_MENU, CRAFTING_MENUS
from UI.ui import UI

CRAFTING_BACK_SIZE = (Game.INVENTORY_ITEM_SIZE[0] * 1.1, Game.INVENTORY_ITEM_SIZE[1] * 1.1)

INFO_TILES_COUNT = (6, 5)
INFO_HORIZONTAL_PADDING = 15
INFO_VERTICAL_PADDING = 15

_ui_path = 'assets\\ui'
_ui_assets = {
    'home_button': load_sprites_from_dir(_ui_path, 2, prefix='home_button')[0],
    'inventory_frame_1': load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    'inventory_back': load_sprites_from_dir(f'{_ui_path}\\inventory_back', CRAFTING_BACK_SIZE)
}


def _home_button_pressed(game: Game, element: Element):
    game.paused = not game.paused


def _exit_button_clicked(game: Game, element: Element):
    game.running = False


def _start_button_clicked(game: Game, element: Element):
    game.setup()


def _crafting_button_clicked(game: Game, element: Element):
    if game.ui.active_crafting_recipe:
        game.ui.active_crafting_recipe.craft()


def _inventory_item_update(game: Game, element: Element, index):
    item = game.player.inventory.items[index]
    if item:
        element.sprites[1] = item.sprite
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


def _crafting_menu_bg_update(game: Game, element: Element, index):
    element.hidden = True
    if game.ui.crafting_menu_open == index:
        element.hidden = False


def _crafting_item_update(game: Game, element: Element, index, crafting_item):
    _crafting_menu_bg_update(game, element, index)
    if game.input.mouse['left'].interact(element.rect, 'clicked'):
        if game.ui.active_crafting_recipe == crafting_item:
            game.ui.active_crafting_recipe = None
        else:
            game.ui.active_crafting_recipe = crafting_item


def _crafting_info_input_update(game: Game, element: Element, index):
    element.sprites[1] = None
    if game.ui.active_crafting_recipe:
        if len(game.ui.active_crafting_recipe.input_items) >= index + 1:
            element.sprites[1] = game.ui.active_crafting_recipe.input_items[index].sprite


def _crafting_info_output_update(game: Game, element: Element):
    element.sprites[1] = None
    if game.ui.active_crafting_recipe:
        element.sprites[1] = game.ui.active_crafting_recipe.output_item.sprite


CRAFTING_MENU_BG = []
for i in range(CRAFTING_MENUS):
    back = 4
    if i == 0:
        back = 4
    elif i == CRAFTING_MENUS - 1:
        back = 3
    CRAFTING_MENU_BG.append(
        Element(
            (
                0,
                (Game.HEIGHT // 2 - (CRAFTING_BACK_SIZE[1] * CRAFTING_MENUS) // 2) + i * CRAFTING_BACK_SIZE[1],
            ),
            pos_position='top_left',
            sprites=[_ui_assets['inventory_back'][back]]
        )
    )

CRAFTING_ITEM_MENUS_BG = []
for i in range(CRAFTING_MENUS):
    for j in range(len(list(CRAFTING_MENU.values())[i])):
        back = 4
        if j == 0:
            back = 4
        elif j == len(list(CRAFTING_MENU.values())[i]) - 1:
            back = 3
        CRAFTING_ITEM_MENUS_BG.append(
            Element(
                (
                    CRAFTING_BACK_SIZE[0],
                    (Game.HEIGHT // 2 - (CRAFTING_BACK_SIZE[1] * CRAFTING_MENUS) // 2) + j * CRAFTING_BACK_SIZE[1],
                ),
                pos_position='top_left',
                sprites=[_ui_assets['inventory_back'][back]],
                update_func=_crafting_menu_bg_update,
                update_func_args=(i,),
                hidden=True
            )
        )

CRAFTING_ITEMS = []
for i in range(CRAFTING_MENUS):
    for j, crafting_item in enumerate(list(CRAFTING_MENU.values())[i]):
        CRAFTING_ITEMS.append(
            Element(
                (
                    Game.CRAFTING_ITEM_SIZE[0],
                    (Game.HEIGHT // 2 - (Game.CRAFTING_ITEM_SIZE[0] * CRAFTING_MENUS) // 2) + j * Game.CRAFTING_ITEM_SIZE[0],
                ),
                pos_position='top_left',
                sprites=[_ui_assets['inventory_frame_1'], crafting_item.output_item.sprite],
                update_func=_crafting_item_update,
                update_func_args=(i, crafting_item),
                hidden=True
            )
        )

INFO_TILES_BACK = []
for x in range(INFO_TILES_COUNT[0]):
    for y in range(INFO_TILES_COUNT[1]):
        back = 0
        if y == INFO_TILES_COUNT[1] - 1 and x == INFO_TILES_COUNT[0] - 1:
            back = 4
        elif y == INFO_TILES_COUNT[1] - 1:
            back = 1
        elif x == INFO_TILES_COUNT[0] - 1:
            back = 5
        INFO_TILES_BACK.append(
            Element(
                (
                    round(x * Game.INVENTORY_ITEM_SIZE[0]),
                    round(Game.HEIGHT - y * Game.INVENTORY_ITEM_SIZE[0])
                ),
                sprites=[_ui_assets['inventory_back'][back]]
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
                    (Game.HEIGHT // 2 - (Game.CRAFTING_ITEM_SIZE[0] * CRAFTING_MENUS) // 2) + i * Game.CRAFTING_ITEM_SIZE[0],
                ),
                pos_position='top_left',
                sprites=[_ui_assets['inventory_frame_1']],
                update_func=_crafting_menu_update,
                update_func_args=(i,)
            )
            for i in range(CRAFTING_MENUS)
        ],
        *CRAFTING_ITEMS,
        *INFO_TILES_BACK,
        Element(
            (
                INFO_HORIZONTAL_PADDING,
                (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING * 3
            ),
            pos_position='top_left',
            text='Inputs',
            text_color=Color('black').color,
            text_size=35,
        ),
        Element(
            (
                INFO_HORIZONTAL_PADDING * 2 + _ui_assets['inventory_frame_1'].get_size()[0] * 3,
                (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING * 3
            ),
            pos_position='top_left',
            text='Output',
            text_color=Color('black').color,
            text_size=35,
        ),
        *[
            Element(
                (
                    INFO_HORIZONTAL_PADDING + _ui_assets['inventory_frame_1'].get_size()[0] * i,
                    (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING \
                    + UI.create_rendered_text('Input', 35).get_size()[1] + 20
                ),
                pos_position='top_left',
                sprites=[_ui_assets['inventory_frame_1'], None],
                update_func=_crafting_info_input_update,
                update_func_args=(i,)
            )
            for i in range(3)
        ],
        Element(
            (
                INFO_HORIZONTAL_PADDING * 2 + _ui_assets['inventory_frame_1'].get_size()[0] * 3,
                (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING \
                + UI.create_rendered_text('Input', 35).get_size()[1] + 20
            ),
            pos_position='top_left',
            sprites=[_ui_assets['inventory_frame_1'], None],
            update_func=_crafting_info_output_update
        ),
        Element(
            (
                INFO_HORIZONTAL_PADDING,
                (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING * 2 \
                + UI.create_rendered_text('Input', 35).get_size()[1] + _ui_assets['inventory_frame_1'].get_size()[1] + 10
            ),
            pos_position='top_left',
            text='CRAFT',
            text_size=35,
            text_color=Color('black').color,
            clicked_func=_crafting_button_clicked
        ),
        Element(
            (
                INFO_HORIZONTAL_PADDING,
                (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING * 11
            ),
            pos_position='top_left',
            text='Item Name',
            text_color=Color('black').color,
            text_size=45,
        ),
        Element(
            (
                INFO_HORIZONTAL_PADDING,
                (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING * 13
            ),
            pos_position='top_left',
            text='Description',
            text_color=Color('black').color,
            text_size=35,
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
