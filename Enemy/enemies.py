from Enemy.enemy import Enemy
from load import load_sprite_sheet_single
from main import Game as _Game
from Inventory.items import SquirrelCarcass, HedgehogCarcass
from floor_item import FloorItem

_squirrel_path = 'assets\\enemies\\peaceful\\squirrel'
_squirrel_size = 2

_hedgehog_path = 'assets\\enemies\\aggressive\\hedgehog'
_hedgehog_size = 2

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
            },
        },
        'hit': {
            'up': {
                'left': load_sprite_sheet_single(_squirrel_path, 'hit.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'hit.png', 8, 1, _squirrel_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_squirrel_path, 'hit.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'hit.png', 8, 1, _squirrel_size)
            }
        },
        'death': {
            'up': {
                'left': load_sprite_sheet_single(_squirrel_path, 'death.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'death.png', 8, 1, _squirrel_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_squirrel_path, 'death.png', 8, 1, _squirrel_size, flip_x=True),
                'right': load_sprite_sheet_single(_squirrel_path, 'death.png', 8, 1, _squirrel_size)
            }
        }
    },
    'hedgehog': {
        'idle': {
            'up': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'idle.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'idle.png', 4, 1, _hedgehog_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'idle.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'idle.png', 4, 1, _hedgehog_size)
            }
        },
        'moving': {
            'up': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'moving.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'moving.png', 4, 1, _hedgehog_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'moving.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'moving.png', 4, 1, _hedgehog_size)
            }
        },
        'hit': {
            'up': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'hit.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'hit.png', 4, 1, _hedgehog_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'hit.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'hit.png', 4, 1, _hedgehog_size)
            }
        },
        'death': {
            'up': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'death.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'death.png', 4, 1, _hedgehog_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'death.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'death.png', 4, 1, _hedgehog_size)
            }
        },
        'attacking': {
            'up': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'attack.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'attack.png', 4, 1, _hedgehog_size)
            },
            'down': {
                'left': load_sprite_sheet_single(_hedgehog_path, 'attack.png', 4, 1, _hedgehog_size, flip_x=True),
                'right': load_sprite_sheet_single(_hedgehog_path, 'attack.png', 4, 1, _hedgehog_size)
            }
        },
    }
}


class Squirrel(Enemy):

    def __init__(self, game, chunk, start_pos, *args, **kwargs):
        super().__init__(
            game,
            chunk,
            _SPRITES['squirrel'],
            {'idle': 10, 'moving': 10, 'hit': 10, 'death': 10},
            health=4,
            start_pos=start_pos,
            move_speed=150,
            patrol_radius=_Game.CHUNK_SIZE // 2,
            stop_max=200,
            denied_biomes=('sand', 'ocean', 'deep_ocean', 'mountain', 'swamp')
        )

    def death(self):
        self.chunk.floor_items.append(
            FloorItem(self.game, self.chunk, self.pos, SquirrelCarcass(self.game, self))
        )
        super().death()


class Hedgehog(Enemy):

    def __init__(self, game, chunk, start_pos, *args, **kwargs):
        super().__init__(
            game,
            chunk,
            _SPRITES['hedgehog'],
            {'idle': 10, 'moving': 10, 'hit': 10, 'death': 10,  'attacking': 10},
            health=4,
            start_pos=start_pos,
            move_speed=100,
            patrol_radius=_Game.CHUNK_SIZE // 2,
            stop_max=350,
            denied_biomes=('sand', 'ocean', 'deep_ocean', 'mountain', 'swamp'),
            aggressive=True,
            damage_amount=2,
            attack_cooldown=200
        )

    def death(self):
        self.chunk.floor_items.append(
            FloorItem(self.game, self.chunk, self.pos, HedgehogCarcass(self.game, self))
        )
        super().death()


_ENEMIES = {
    'Squirrel': Squirrel,
    'Hedgehog': Hedgehog
}
