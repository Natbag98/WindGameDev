from Enemy.enemy import Enemy
from load import load_sprite_sheet_single
from main import Game as _Game

_squirrel_path = 'assets\\enemies\\peaceful\\squirrel'
_squirrel_size = 2
_SPRITES = {
    'squirrel': {
        'idle': {
            'up': {
                'left': load_sprite_sheet_single(_squirrel_path, 'idle_1.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'idle_1.png', 8, 1, _squirrel_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_squirrel_path, 'idle_1.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'idle_1.png', 8, 1, _squirrel_size)
            }
        },
        'moving': {
            'up': {
                'left': load_sprite_sheet_single(_squirrel_path, 'moving.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'moving.png', 8, 1, _squirrel_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_squirrel_path, 'moving.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'moving.png', 8, 1, _squirrel_size)
            }
        }
    }
}


class Squirrel(Enemy):

    def __init__(self, game, chunk, start_pos, *args, **kwargs):
        super().__init__(
            game,
            chunk,
            _SPRITES['squirrel'],
            {'idle': 10, 'moving': 10},
            start_pos=start_pos,
            move_speed=150,
            patrol_radius=_Game.CHUNK_SIZE // 2,
            stop_max=200,
            denied_biomes=('sand', 'ocean', 'deep_ocean', 'mountain', 'swamp')
        )
