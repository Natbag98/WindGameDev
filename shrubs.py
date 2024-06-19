from shrub import Shrub
from load import load_sprites_from_dir
import random

_shrub_path = 'assets\\environment\\shrubs'
_shrub_assets = {
    'bush_simple': load_sprites_from_dir(f'{_shrub_path}\\bush_simple')
}


class BushSimple(Shrub):

    def __init__(self, game, chunk, pos):
        super().__init__(
            game,
            chunk,
            pos,
            [random.choice(_shrub_assets['bush_simple'])]
        )
