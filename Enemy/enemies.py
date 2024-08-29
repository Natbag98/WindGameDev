from Enemy.enemy import Enemy
from load import load_sprite_sheet_single, load_sprites_from_dir
from main import Game as _Game
from Inventory.items import SquirrelCarcass, HedgehogCarcass
from floor_item import FloorItem

_squirrel_path = 'assets\\enemies\\peaceful\\squirrel'
_squirrel_size = 2

_hedgehog_path = 'assets\\enemies\\aggressive\\hedgehog'
_hedgehog_size = 2

_aggressive_path = 'assets\\enemies\\aggressive'
_peaceful_path = 'assets\\enemies\\peaceful'

_skeleton_size = 1.5

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
    },
    'slime': {
        'idle': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\idle', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\idle')
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\idle', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\idle')
            }
        },
        'moving': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\move', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\move')
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\move', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\move')
            }
        },
        'hit': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\hit', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\hit')
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\hit', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\hit')
            }
        },
        'death': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\death', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\death')
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\death', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\death')
            }
        },
        'attacking': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\attack', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\attack')
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\slime\\attack', flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\slime\\attack')
            }
        },
    },
    'skeleton': {
        'idle': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\idle', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\idle', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\idle', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\idle', size=_skeleton_size)
            }
        },
        'moving': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\move', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\move', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\move', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\move', size=_skeleton_size)
            }
        },
        'hit': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\hit', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\hit', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\hit', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\hit', size=_skeleton_size)
            }
        },
        'death': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\death', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\death', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\death', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\death', size=_skeleton_size)
            }
        },
        'attacking': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\attack', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\attack', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\attack', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\skeleton\\attack', size=_skeleton_size)
            }
        },
    },
    'strong_skeleton': {
        'idle': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\idle', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\idle', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\idle', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\idle', size=_skeleton_size)
            }
        },
        'moving': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\move', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\move', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\move', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\move', size=_skeleton_size)
            }
        },
        'hit': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\hit', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\hit', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\hit', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\hit', size=_skeleton_size)
            }
        },
        'death': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\death', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\death', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\death', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\death', size=_skeleton_size)
            }
        },
        'attacking': {
            'up': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\attack', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\attack', size=_skeleton_size)
            },
            'down': {
                'left': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\attack', size=_skeleton_size, flip_x=True),
                'right': load_sprites_from_dir(f'{_aggressive_path}\\strong_skeleton\\attack', size=_skeleton_size)
            }
        },
    },
}


class Squirrel(Enemy):

    def __init__(self, game, chunk, start_pos, *args, **kwargs):
        super().__init__(
            game,
            chunk,
            _SPRITES['squirrel'],
            {'idle': 10, 'moving': 10, 'hit': 10, 'death': 10},
            health=3,
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
            health=3,
            start_pos=start_pos,
            move_speed=100,
            patrol_radius=_Game.CHUNK_SIZE // 2,
            stop_max=350,
            denied_biomes=('sand', 'ocean', 'deep_ocean', 'mountain', 'swamp'),
            aggressive=True,
            damage_amount=2,
            attack_cooldown=200,
            attack_frame=3
        )

    def death(self):
        self.chunk.floor_items.append(
            FloorItem(self.game, self.chunk, self.pos, HedgehogCarcass(self.game, self))
        )
        super().death()


class Slime(Enemy):

    def __init__(self, game, chunk, start_pos, *args, **kwargs):
        super().__init__(
            game,
            chunk,
            _SPRITES['slime'],
            {'idle': 10, 'moving': 10, 'hit': 10, 'death': 10,  'attacking': 10},
            health=8,
            start_pos=start_pos,
            move_speed=20,
            patrol_radius=_Game.CHUNK_SIZE // 2,
            stop_max=2000,
            denied_biomes=('sand', 'ocean', 'deep_ocean', 'mountain', 'plains'),
            aggressive=True,
            damage_amount=4,
            attack_cooldown=200,
            aggressive_range=150,
            attack_frame=6
        )


class Skeleton(Enemy):

    def __init__(self, game, chunk, start_pos, *args, **kwargs):
        super().__init__(
            game,
            chunk,
            _SPRITES['skeleton'],
            {'idle': 8, 'moving': 8, 'hit': 8, 'death': 8,  'attacking': 10},
            health=3,
            start_pos=start_pos,
            move_speed=50,
            patrol_radius=_Game.CHUNK_SIZE // 2,
            stop_max=400,
            denied_biomes=('sand', 'ocean', 'deep_ocean', 'forest', 'plains'),
            aggressive=True,
            damage_amount=6,
            attack_cooldown=100,
            aggressive_range=150,
            attack_frame=4
        )


class StrongSkeleton(Enemy):

    def __init__(self, game, chunk, start_pos, *args, **kwargs):
        super().__init__(
            game,
            chunk,
            _SPRITES['strong_skeleton'],
            {'idle': 8, 'moving': 8, 'hit': 8, 'death': 8,  'attacking': 10},
            health=10,
            start_pos=start_pos,
            move_speed=50,
            patrol_radius=_Game.CHUNK_SIZE // 2,
            stop_max=200,
            denied_biomes=('sand', 'ocean', 'deep_ocean', 'forest', 'plains'),
            aggressive=True,
            damage_amount=5,
            attack_cooldown=150,
            aggressive_range=200,
            attack_frame=3
        )


_ENEMIES = {
    'Squirrel': Squirrel,
    'Hedgehog': Hedgehog
}
