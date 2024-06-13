from main import Game
from color import Color
import random


class Map:
    BIOME_HEIGHTS = [
        {
            0.1: 'deep_ocean',
            0.2: 'ocean',
            0.25: 'sand',
            0.45: '',
            0.58: 'swamp',
            1: 'mountain'
        },
        {
            0.5: 'grass',
            1: 'forest'
        }
    ]

    ISLAND_EDGE = 350
    CELL_SIZE = 1
    SCALE = 500
    DIMENSIONS = (Game.CHUNK_SIZE * Game.CHUNK_COUNT, Game.CHUNK_SIZE * Game.CHUNK_COUNT)
    MIN_VAL = -0.8
    MAX_VAL = 0.8

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

    def draw(self, surface):
        for row in self.chunks:
            for chunk in row:
                if self.game.camera.rect.colliderect(chunk.rect):
                    surface.blit(chunk.terrain_surface, chunk.pos - self.game.camera.offset)
