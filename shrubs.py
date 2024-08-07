from shrub import Shrub
from load import load_sprites_from_dir
import random
from Inventory.items import OrangeBerries, BlueBerries
from pygame import Vector2

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

    def __init__(self, game, parent, pos, new, id, *args):
        self.target_level = args[0]
        super().__init__(
            game,
            parent,
            pos,
            [_shrub_assets['deep_entrances'][self.target_level.type]],
            id,
            new
        )

    def interact(self):
        self.game.active_map = self.target_level
        self.game.player.pos = Vector2(self.target_level.shrubs[0].pos)


class DeepExit(Shrub):

    def __init__(self, game, parent, pos, new, id, *args):
        self.target_level = args[0]
        self.entrance_pos = args[1]
        super().__init__(
            game,
            parent,
            pos,
            [_shrub_assets['deep_exits'][self.target_level.type]],
            id,
            new
        )

    def interact(self):
        self.game.active_map = self.target_level
        self.game.player.pos = Vector2(self.entrance_pos)


class BushSimple(Shrub):

    def __init__(self, game, chunk, pos, new, id=str(random.randbytes(20))):
        super().__init__(
            game,
            chunk,
            pos,
            [random.choice(_shrub_assets['bush_simple'])],
            id,
            new
        )


class BushFlowers(Shrub):
    FLOWER_COLORS = {
        'orange': OrangeBerries,
        'blue': BlueBerries
    }

    def __init__(self, game, chunk, pos, new, id=str(random.randbytes(20))):
        self.color = random.choice(list(self.FLOWER_COLORS.keys()))
        self.collected = False

        super().__init__(
            game,
            chunk,
            pos,
            [random.choice(_shrub_assets[f'bush_{self.color}_flowers'])],
            id,
            new
        )

    def interact(self):
        if not self.collected:
            self.game.player.inventory.add_item(self.FLOWER_COLORS[self.color](self.game))
            self.collected = True


class TreeSimple(Shrub):

    def __init__(self, game, chunk, pos, new, id=str(random.randbytes(20))):
        super().__init__(
            game,
            chunk,
            pos,
            [random.choice(_shrub_assets['tree_simple'])],
            id,
            new
        )


_SHRUBS = {
    'TreeSimple': TreeSimple,
    'DeepEntrance': DeepEntrance,
    'DeepExit': DeepExit,
    'BushSimple': BushSimple,
    'BushFlowers': BushFlowers
}
