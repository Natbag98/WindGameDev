from main import Game
from UI.ui_element import Element
from color import Color


def _exit_button_clicked(game: Game):
    game.running = False

def _start_button_clicked(game: Game):
    game.setup()
    game.screen = 'game'


SCREENS = {
    'game': [
        Element(
            (Game.WIDTH - 30, 30),
            bg_color=Color('white').color,
            hover_color=Color('white').color,
            clicked_func=_exit_button_clicked,
            size=(20, 20)
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
            bg_color=Color('white').color,
            size=(150, 40),
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
