from main import Game
from UI.ui_element import Element
from color import Color
from load import load_sprites_from_dir
from crafting import CRAFTING_MENU, CRAFTING_MENUS
from UI.ui import UI
from shrubs import BasicCraftingTable
from Inventory.inventory import Inventory
import pygame

CRAFTING_BACK_SIZE = (Game.INVENTORY_ITEM_SIZE[0] * 1.1, Game.INVENTORY_ITEM_SIZE[1] * 1.1)

INFO_TILES_COUNT = (7, 5)
INFO_HORIZONTAL_PADDING = 15
INFO_VERTICAL_PADDING = 15

CYCLES_TILES_COUNT = (2, 6)

_ui_path = 'assets\\ui'
_ui_assets = {
    'home_button': load_sprites_from_dir(_ui_path, 2, prefix='home_button')[0],
    'inventory_frame_1': load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    'inventory_back': load_sprites_from_dir(f'{_ui_path}\\inventory_back', CRAFTING_BACK_SIZE),
    'cycles': load_sprites_from_dir(f'{_ui_path}\\cycles', return_dict=True),
    'player_status': load_sprites_from_dir(f'{_ui_path}\\player_status', return_dict=True),
    'player_status_grey': load_sprites_from_dir(f'{_ui_path}\\player_status', return_dict=True, grey=True)
}
_ui_assets['inventory_back'].append(
    pygame.transform.flip(
        load_sprites_from_dir(f'{_ui_path}\\inventory_back', CRAFTING_BACK_SIZE, prefix='inventory_back_vertical')[0],
        True,
        False
    )
)

inv_bar_backs = {
    0: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    1: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    2: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    3: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    4: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    5: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    6: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    7: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    8: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    9: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    10: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    11: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    12: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_hand')[0],
    13: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0],
    14: load_sprites_from_dir(_ui_path, Game.INVENTORY_ITEM_SIZE, prefix='inventory_frame_1')[0]
}


def _load_button_clicked(game: Game, element: Element):
    game.save.load()
    game.map_generation_finished()


def _home_button_pressed(game: Game, element: Element):
    game.paused = not game.paused
    if game.paused:
        game.screen = 'paused'
    if not game.paused:
        game.screen = 'game'


def _save_button_pressed(game: Game, element: Element):
    game.save.save()


def _main_menu_button_pressed(game: Game, element: Element):
    game.quit()


def _exit_button_clicked(game: Game, element: Element):
    game.running = False


def _start_button_clicked(game: Game, element: Element):
    game.setup()


def _crafting_button_clicked(game: Game, element: Element):
    if game.ui.active_crafting_recipe:
        game.ui.active_crafting_recipe.craft()


def _inventory_item_hover(game: Game, element: Element, index):
    if index > Game.PLAYER_INVENTORY_SIZE - 1:
        if index == Inventory.HAND_INDEX:
            if game.player.inventory.hand_item:
                game.ui.item_desc_display = game.player.inventory.hand_item.__class__.__name__

    else:
        item = game.player.inventory.items[index]
        if item:
            game.ui.item_desc_display = item.__class__.__name__


def _inventory_button_clicked(game: Game, element: Element, index):
    if index < 12:
        item = game.player.inventory.items[index]
        if item:
            if item.placeable:
                game.player.inventory.remove_item(item.__class__.__name__)
                game.active_map.active_chunk.shrubs.append(
                    item.shrub_to_place(
                        game,
                        game.map.active_chunk,
                        (
                            game.player.rect.x + game.player.rect.size[0],
                            game.player.rect.y + game.player.rect.size[1]
                        ),
                        new=False
                    )
                )
            elif item.hand:
                game.player.inventory.place_in_hand(item.__class__.__name__)
            elif item.__class__.__name__ == 'MeatCooked':
                game.player.inventory.remove_item('MeatCooked')
                game.player.increase_hunger(25)


def _inventory_item_update(game: Game, element: Element, index):
    if index > Game.PLAYER_INVENTORY_SIZE - 1:
        if index == Inventory.HAND_INDEX:
            if game.player.inventory.hand_item:
                element.sprites[1] = game.player.inventory.hand_item.sprite
                if game.player.inventory.hand_item.inventory_sprite:
                    element.sprites[1] = game.player.inventory.hand_item.inventory_sprite
            else:
                element.sprites[1] = None

    else:
        item = game.player.inventory.items[index]
        if item:
            element.sprites[1] = item.sprite
            if item.inventory_sprite:
                element.sprites[1] = item.inventory_sprite
        else:
            element.sprites[1] = None


def _loading_text_update(game: Game, element: Element):
    element.text = f'Loading: {game.chunk_progress} \\ {game.total_chunks}'
    element.render_text()


_CRAFTING_INDEXES = {
    0: True,
    1: 'basic_crafting',
    2: 'advanced_crafting',
    3: 'food_crafting'
}


def _crafting_menu_update(game: Game, element: Element, index):
    if type(_CRAFTING_INDEXES[index]) is str:
        if not game.player.__getattribute__(_CRAFTING_INDEXES[index]):
            if game.ui.crafting_menu_open == index:
                game.ui.crafting_menu_open = None
            element.hidden = True
            return

    element.hidden = False

    if game.input.mouse['left'].interact(element.rect, 'clicked'):
        if game.ui.crafting_menu_open == index:
            game.ui.crafting_menu_open = None
            return
        game.ui.crafting_menu_open = index


def _crafting_menu_bg_update(game: Game, element: Element, index):
    element.hidden = True
    if game.ui.crafting_menu_open == index:
        element.hidden = False


def _crafting_item_update(game: Game, element: Element, index, crafting_recipe):
    _crafting_menu_bg_update(game, element, index)
    if game.input.mouse['left'].interact(element.rect, 'clicked') and not element.hidden:
        if game.ui.active_crafting_recipe == crafting_recipe:
            game.ui.active_crafting_recipe = None
        else:
            game.ui.active_crafting_recipe = crafting_recipe


def _crafting_info_input_update(game: Game, element: Element, index):
    element.sprites[1] = None
    if game.ui.active_crafting_recipe:
        if len(game.ui.active_crafting_recipe.input_items) >= index + 1:
            element.sprites[1] = game.ui.active_crafting_recipe.input_items[index].sprite


def _crafting_info_output_update(game: Game, element: Element):
    element.sprites[1] = None
    if game.ui.active_crafting_recipe:
        element.sprites[1] = game.ui.active_crafting_recipe.output_item.sprite


def _crafting_info_output_hover(game: Game, element: Element):
    if game.ui.active_crafting_recipe:
        game.ui.item_desc_display = game.ui.active_crafting_recipe.output_item.__class__.__name__


def _item_name_update(game: Game, element: Element):
    if game.ui.item_desc_display:
        element.render_text(game.ui.item_desc_name[game.ui.item_desc_display])
    else:
        element.render_text()


def _item_desc_update(game: Game, element: Element):
    if game.ui.item_desc_display:
        element.render_text(game.ui.item_desc[game.ui.item_desc_display])
    else:
        element.render_text()


def _cycles_disp_update(game: Game, element: Element):
    element.sprites = [_ui_assets['cycles'][game.cycle]]


def _heart_colored_display_update(game: Game, element: Element):
    sprite = _ui_assets['player_status']['heart']
    img = pygame.Surface(element.sprites[0].get_size(), pygame.SRCALPHA)
    img.blit(
        sprite,
        (
            0,
            0
        ),
        (
            0,
            0,
            sprite.get_size()[0],
            sprite.get_size()[1] * (game.player.health / game.player.max_health)
        )
    )
    element.sprites = [img]


def _stomach_colored_display_update(game: Game, element: Element):
    sprite = _ui_assets['player_status']['stomach']
    img = pygame.Surface(element.sprites[0].get_size(), pygame.SRCALPHA)
    img.blit(
        sprite,
        (
            0,
            0
        ),
        (
            0,
            0,
            sprite.get_size()[0],
            sprite.get_size()[1] * (game.player.hunger / game.player.max_hunger)
        )
    )
    element.sprites = [img]


def _brain_colored_display_update(game: Game, element: Element):
    sprite = _ui_assets['player_status']['brain']
    img = pygame.Surface(element.sprites[0].get_size(), pygame.SRCALPHA)
    img.blit(
        sprite,
        (
            0,
            0
        ),
        (
            0,
            0,
            sprite.get_size()[0],
            sprite.get_size()[1] * (game.player.sanity / game.player.max_sanity)
        )
    )
    element.sprites = [img]


INV_CENTRE = Game.WIDTH // 2 + 50
CRAFT_CENTRE = Game.HEIGHT // 2 - 300

INV_BAR_BG = []
for i in range(Game.PLAYER_INVENTORY_SIZE + 3):
    back = 1
    if i == 0:
        back = 2
    elif i == Game.PLAYER_INVENTORY_SIZE + 2:
        back = 4
    INV_BAR_BG.append(
        Element(
            (
                (INV_CENTRE - (Game.INVENTORY_ITEM_SIZE[0] * Game.PLAYER_INVENTORY_SIZE + 3) // 2) + i * Game.INVENTORY_ITEM_SIZE[0],
                (Game.HEIGHT - Game.INVENTORY_ITEM_SIZE[1])
            ),
            pos_position='top_left',
            sprites=[_ui_assets['inventory_back'][back]]
        )
    )

CRAFTING_MENU_BG = []
for i in range(CRAFTING_MENUS):
    back = 5
    if i == 0:
        back = 4
    elif i == CRAFTING_MENUS - 1:
        back = 3
    CRAFTING_MENU_BG.append(
        Element(
            (
                0,
                (CRAFT_CENTRE - (CRAFTING_BACK_SIZE[1] * CRAFTING_MENUS) // 2) + i * CRAFTING_BACK_SIZE[1],
            ),
            pos_position='top_left',
            sprites=[_ui_assets['inventory_back'][back]]
        )
    )

CRAFTING_ITEM_MENUS_BG = []
for i in range(CRAFTING_MENUS):
    for j in range(len(list(CRAFTING_MENU.values())[i])):
        back = 5
        if j == 0:
            back = 4
        elif j == len(list(CRAFTING_MENU.values())[i]) - 1:
            back = 3
        CRAFTING_ITEM_MENUS_BG.append(
            Element(
                (
                    CRAFTING_BACK_SIZE[0],
                    (CRAFT_CENTRE - (CRAFTING_BACK_SIZE[1] * CRAFTING_MENUS) // 2) + j * CRAFTING_BACK_SIZE[1],
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
                    (CRAFT_CENTRE - (Game.CRAFTING_ITEM_SIZE[0] * CRAFTING_MENUS) // 2) + j * Game.CRAFTING_ITEM_SIZE[0],
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


CYCLES_TILES_BACK = []
for x in range(CYCLES_TILES_COUNT[0]):
    for y in range(CYCLES_TILES_COUNT[1]):
        back = 0
        if y == CYCLES_TILES_COUNT[1] - 1 and x == CYCLES_TILES_COUNT[0] - 1:
            back = 2
        elif y == CYCLES_TILES_COUNT[1] - 1:
            back = 1
        elif x == CYCLES_TILES_COUNT[0] - 1:
            back = 6
        CYCLES_TILES_BACK.append(
            Element(
                (
                    round(Game.WIDTH - x * Game.INVENTORY_ITEM_SIZE[0]),
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
        *INV_BAR_BG,
        *[
            Element(
                (
                    3 + (INV_CENTRE - (Game.INVENTORY_ITEM_SIZE[0] * Game.PLAYER_INVENTORY_SIZE + 3) // 2) + i * Game.INVENTORY_ITEM_SIZE[0],
                    5 + (Game.HEIGHT - Game.INVENTORY_ITEM_SIZE[1])
                ),
                pos_position='top_left',
                sprites=[inv_bar_backs[i], None],
                clicked_func=_inventory_button_clicked,
                clicked_func_args=(i,),
                update_func=_inventory_item_update,
                update_func_args=(i,),
                hovered_func=_inventory_item_hover,
                hovered_func_args=(i,)
            )
            for i in range(Game.PLAYER_INVENTORY_SIZE + 3)
        ],
        *CRAFTING_MENU_BG,
        *CRAFTING_ITEM_MENUS_BG,
        *[
            Element(
                (
                    0,
                    (CRAFT_CENTRE - (Game.CRAFTING_ITEM_SIZE[0] * CRAFTING_MENUS) // 2) + i * Game.CRAFTING_ITEM_SIZE[0],
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
            update_func=_crafting_info_output_update,
            hovered_func=_crafting_info_output_hover
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
            text=' ',
            text_color=Color('black').color,
            text_size=45,
            update_func=_item_name_update
        ),
        Element(
            (
                INFO_HORIZONTAL_PADDING,
                (Game.HEIGHT - (INFO_TILES_COUNT[1] * Game.INVENTORY_ITEM_SIZE[1])) + INFO_VERTICAL_PADDING * 13
            ),
            pos_position='top_left',
            text=' ',
            text_color=Color('black').color,
            text_size=35,
            update_func=_item_desc_update
        ),
        *CYCLES_TILES_BACK,
        Element(
            Game.RES,
            pos_position='center_2',
            sprites=[_ui_assets['cycles']['day']],
            update_func=_cycles_disp_update
        ),
        Element(
            (
                Game.WIDTH,
                Game.HEIGHT - 80
            ),
            pos_position='center_2',
            sprites=[_ui_assets['player_status_grey']['heart']]
        ),
        Element(
            (
                Game.WIDTH,
                Game.HEIGHT - 80
            ),
            pos_position='center_2',
            sprites=[_ui_assets['player_status']['heart']],
            update_func=_heart_colored_display_update
        ),
        Element(
            (
                Game.WIDTH,
                Game.HEIGHT - 80 * 2
            ),
            pos_position='center_2',
            sprites=[_ui_assets['player_status_grey']['stomach']]
        ),
        Element(
            (
                Game.WIDTH,
                Game.HEIGHT - 80 * 2
            ),
            pos_position='center_2',
            sprites=[_ui_assets['player_status']['stomach']],
            update_func=_stomach_colored_display_update
        ),
        Element(
            (
                Game.WIDTH,
                Game.HEIGHT - 80 * 3
            ),
            pos_position='center_2',
            sprites=[_ui_assets['player_status_grey']['brain']]
        ),
        Element(
            (
                Game.WIDTH,
                Game.HEIGHT - 80 * 3
            ),
            pos_position='center_2',
            sprites=[_ui_assets['player_status']['brain']],
            update_func=_brain_colored_display_update
        )
    ],
    'paused': [
        Element(
            (0, 0),
            pos_position='top_left',
            size=Game.RES,
            bg_color=Color('black', a=180).color,
            hover_color=Color('black', a=180).color
        ),
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 - 50
            ),
            text='Resume',
            text_size=50,
            clicked_func=_home_button_pressed
        ),
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2
            ),
            text='Save',
            text_size=50,
            clicked_func=_save_button_pressed
        ),
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 + 50
            ),
            text='Exit',
            text_size=50,
            clicked_func=_main_menu_button_pressed
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
            (Game.WIDTH // 2, Game.HEIGHT // 2),
            text='Load Game',
            text_size=80,
            clicked_func=_load_button_clicked
        ),
        Element(
            (Game.WIDTH // 2, Game.HEIGHT // 2 - 75),
            text='Start New',
            text_size=80,
            clicked_func=_start_button_clicked
        ),
        Element(
            (Game.WIDTH // 2, Game.HEIGHT // 2 + 75),
            text='Exit',
            text_size=80,
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
    ],
    'death_1': [
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 - 50
            ),
            text='You were killed',
            text_size=100
        ),
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 + 50
            ),
            text='Quit',
            text_size=50,
            clicked_func=_exit_button_clicked
        ),
    ],
    'death_2': [
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 - 50
            ),
            text='You starved to death',
            text_size=100
        ),
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 + 50
            ),
            text='Quit',
            text_size=50,
            clicked_func=_exit_button_clicked
        ),
    ],
    'death_3': [
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 - 50
            ),
            text='You went insane',
            text_size=100
        ),
        Element(
            (
                Game.WIDTH // 2,
                Game.HEIGHT // 2 + 50
            ),
            text='Quit',
            text_size=50,
            clicked_func=_exit_button_clicked
        ),
    ]
}
