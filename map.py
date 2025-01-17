from color import Color
from deep_level import Level
from Enemy.enemies import *
from concurrent.futures import ThreadPoolExecutor
from shrubs import *
from Inventory.items import StonesSmall


class Map:
    BIOME_HEIGHTS = [
        {
            0.01: 'deep_ocean',
            0.02: 'ocean',
            0.06: 'sand',
            0.26: '',
            0.38: 'swamp',
            1: 'mountain'
        },
        {
            0.5: 'plains',
            1: 'forest'
        }
    ]

    BIOMES = [
        'deep_ocean',
        'ocean',
        'sand',
        'swamp',
        'mountain',
        'plains',
        'forest'
    ]

    BIOME_SHRUBS = {
        'deep_ocean': [],
        'ocean': [],
        'sand': [SandGeneral,  SandGeneral, Ship],
        'swamp': [SwampGeneral],
        'mountain': [MountainGeneral, RockBasic, RockBasic, RockBlue, RockOrange],
        'plains': [BushSimple, BushSimple, BushSimple, TreeSimple, BushFlowers],
        'forest': [TreeSimple, BushSimple, TreeSimple, ForestGeneral, ForestGeneral, ForestGeneral]
    }

    BIOME_ENEMIES_PEACEFUL = {
        'deep_ocean': [],
        'ocean': [],
        'sand': [],
        'swamp': [],
        'mountain': [],
        'plains': [Squirrel, Hedgehog],
        'forest': [Squirrel, Hedgehog]
    }

    ENEMY_PEACEFUL_COUNT_PER_CELL = {
        'plains': 0.000015,
        'forest': 0.000025
    }

    FLOOR_ITEMS = {
        'plains': [StonesSmall],
        'forest': [StonesSmall]
    }
    FLOOR_ITEM_COUNT_PER_CELL = {
        'plains': 0.000025,
        'forest': 0.00004
    }

    ISLAND_EDGE = 350
    CELL_SIZE = 3
    SCALE = 4000
    DIMENSIONS = (Game.CHUNK_SIZE * Game.CHUNK_COUNT, Game.CHUNK_SIZE * Game.CHUNK_COUNT)
    MIN_VAL = -0.8
    MAX_VAL = 0.8

    SHRUB_COUNT_PER_CELL = {
        'sand': 0.00005,
        'plains': 0.00015,
        'forest': 0.0001,
        'swamp': 0.0001,
        'mountain': 0.00005
    }

    def __init__(self, game, id=str(random.randbytes(20))):
        self.game = game
        self.id = id
        self.chunks = None
        self.type = 'basic'
        self.shrubs_colliding_with_player = []
        self.campfires = []

    # noinspection PyUnresolvedReferences
    def generate(self):
        from map_chunk import Chunk
        chunks = [
            [None for _ in range(Game.CHUNK_COUNT)]
            for _ in range(Game.CHUNK_COUNT)
        ]

        base = [random.randrange(min(Chunk.CHUNK_DIMENSIONS)) for _ in range(len(Map.BIOME_HEIGHTS))]

        self.game.colors = {
            biome: Color(biome, random_=True).color
            for height in Map.BIOME_HEIGHTS
            for biome in height.values()
            if biome
        }

        with ThreadPoolExecutor() as executor:
            chunk_results = []
            for i, y in enumerate(range(Game.CHUNK_COUNT)):
                for j, x in enumerate(range(Game.CHUNK_COUNT)):
                    chunk_results.append(executor.submit(self.create_chunk, y, x, base, self.game.colors))

            for result in chunk_results:
                chunk, y, x = result.result()
                chunks[y][x] = chunk
                self.game.chunk_progress += 1

        self.chunks = chunks
        #self.place_deep_entrances()
        self.game.map_generation_finished()
        self.active_chunk = self.chunks[0][0]

    def place_deep_entrances(self):
        print('starting_deep')
        for i in range(Game.DEEP_ENTRANCES):
            while True:
                chunk = random.choice(
                    random.choice(self.chunks)
                )

                if len(chunk.biome_cells['mountain']) > Game.DEEP_REQUIREMENT:
                    pos = random.choice(chunk.biome_cells['mountain'])
                    chunk.shrubs.append(
                        DeepEntrance(
                            self.game,
                            chunk,
                            pos,
                            True,
                            str(random.randbytes(20)),
                            Level(self.game, 0, 'basic', self, pos)
                        )
                    )
                    break
        print('finished_deep')

    def create_chunk(self, x, y, base, colors):
        from map_chunk import Chunk
        return Chunk(
            self.game,
            self,
            (Game.CHUNK_SIZE * x, Game.CHUNK_SIZE * y),
            base,
            colors
        ), y, x

    def basic_damage(self, rect, damage):
        for row in self.chunks:
            for chunk in row:
                if chunk.active:
                    chunk.basic_damage(rect, damage)

    def update(self):
        self.shrubs_colliding_with_player = []
        [
            [chunk.update() for chunk in row]
            for row in self.chunks
        ]

    def draw(self, ground_surface, shrub_surface):
        for row in self.chunks:
            for chunk in row:
                if chunk.active:
                    ground_surface.blit(chunk.terrain_surface, chunk.pos - self.game.camera.offset)
                    chunk.draw(shrub_surface)
