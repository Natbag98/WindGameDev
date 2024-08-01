from shrub import Shrub
from load import load_sprites_from_dir
import random
from Inventory.items import OrangeBerries, BlueBerries

_shrub_path = 'assets\\environment\\shrubs'
_shrub_assets = {
    'bush_simple': load_sprites_from_dir(f'{_shrub_path}\\bush_simple'),
    'bush_orange_flowers': load_sprites_from_dir(f'{_shrub_path}\\bush_orange_flowers'),
    'bush_blue_flowers': load_sprites_from_dir(f'{_shrub_path}\\bush_blue_flowers'),
    'tree_simple': load_sprites_from_dir(f'{_shrub_path}\\tree_simple'),
    'deep_entrances': load_sprites_from_dir(f'{_shrub_path}\\deep_entrances', return_dict=True),
    'deep_exits': load_sprites_from_dir(f'{_shrub_path}\\deep_exits', return_dict=True)
}


class DeepEntrance(Shrub):

    def __init__(self, game, parent, pos, target_level):
        self.target_level = target_level
        super().__init__(
            game,
            parent,
            pos,
            [_shrub_assets['deep_entrances'][target_level.type]]
        )

    def interact(self):
        self.game.active_map = self.target_level


class DeepExit(Shrub):

    def __init__(self, game, parent, pos, target_level):
        self.target_level = target_level
        super().__init__(
            game,
            parent,
            pos,
            [_shrub_assets['deep_exits'][target_level.type]]
        )

    def interact(self):
        self.game.active_map = self.target_level


class BushSimple(Shrub):

    def __init__(self, game, chunk, pos):
        super().__init__(
            game,
            chunk,
            pos,
            [random.choice(_shrub_assets['bush_simple'])]
        )


class BushFlowers(Shrub):
    FLOWER_COLORS = {
        'orange': OrangeBerries,
        'blue': BlueBerries
    }

    def __init__(self, game, chunk, pos):
        self.color = random.choice(list(self.FLOWER_COLORS.keys()))
        self.collected = False

        super().__init__(
            game,
            chunk,
            pos,
            [random.choice(_shrub_assets[f'bush_{self.color}_flowers'])]
        )

    def interact(self):
        if not self.collected:
            self.game.player.inventory.add_item(self.FLOWER_COLORS[self.color](self.game))
            self.collected = True


class TreeSimple(Shrub):

    def __init__(self, game, chunk, pos):
        super().__init__(
            game,
            chunk,
            pos,
            [random.choice(_shrub_assets['tree_simple'])]
        )
