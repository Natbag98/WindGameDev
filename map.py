import profilehooks
from main import Game
from color import Color
import random
from shrubs import (
    TreeSimple,
    BushSimple
)


class Map:
    BIOME_HEIGHTS = [
        {
            0.01: 'deep_ocean',
            0.02: 'ocean',
            0.06: 'sand',
            0.28: '',
            0.44: 'swamp',
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
        'sand': [],
        'swamp': [],
        'mountain': [],
        'plains': [BushSimple, BushSimple, BushSimple, TreeSimple],
        'forest': [TreeSimple, BushSimple, TreeSimple]
    }

    ISLAND_EDGE = 350
    CELL_SIZE = 3
    SCALE = 4000
    DIMENSIONS = (Game.CHUNK_SIZE * Game.CHUNK_COUNT, Game.CHUNK_SIZE * Game.CHUNK_COUNT)
    MIN_VAL = -0.8
    MAX_VAL = 0.8

    SHRUB_COUNT_PER_CELL = {
        'plains': 0.00025,
        'forest': 0.00015
    }

    def __init__(self, game):
        self.game = game
        self.chunks = self.generate()

    def generate(self):
        from map_chunk import Chunk
        chunks = []

        base = [random.randrange(min(Chunk.CHUNK_DIMENSIONS)) for _ in range(len(Map.BIOME_HEIGHTS))]

        colors = {
            biome: Color(biome, random_=True).color
            for dict in Map.BIOME_HEIGHTS
            for biome in dict.values()
            if biome
        }

        for i, y in enumerate(range(Game.CHUNK_COUNT)):
            row = []
            for j, x in enumerate(range(Game.CHUNK_COUNT)):
                edges = []
                if i == 0:
                    edges.append('top')
                elif i == Game.CHUNK_COUNT - 1:
                    edges.append('bottom')

                if j == 0:
                    edges.append('left')
                elif j == Game.CHUNK_COUNT - 1:
                    edges.append('right')

                row.append(
                    Chunk(
                        self.game,
                        self,
                        (Game.CHUNK_SIZE * x, Game.CHUNK_SIZE * y),
                        edges,
                        base,
                        colors
                    )
                )

            chunks.append(row)

        return chunks

    def update(self):
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
