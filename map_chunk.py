import pygame
import noise
from main import Game
from map import Map
from pygame import Vector2


class Chunk:
    CHUNK_DIMENSIONS = (Game.CHUNK_SIZE, Game.CHUNK_SIZE)

    def __init__(self, game, map_, pos, edges, base, colors):
        self.game = game
        self.map = map_
        self.pos = Vector2(pos)
        self.rect = pygame.Rect(self.pos, self.CHUNK_DIMENSIONS)
        self.edges = edges
        self.base = base

        self.terrain = self.generate()
        self.terrain_surface = pygame.Surface(self.CHUNK_DIMENSIONS)

        self.game.chunk_progress += 1
        print(f'{self.game.chunk_progress} / {self.game.total_chunks}')

        self.terrain_onto_surface(self.terrain_surface, colors, (0, 0))

    def generate(self):
        terrain = []

        for y in range(0, Game.CHUNK_SIZE, Map.CELL_SIZE):
            row = []
            for x in range(0, Game.CHUNK_SIZE, Map.CELL_SIZE):
                for i, layer in enumerate(Map.BIOME_HEIGHTS):
                    value = noise.snoise2(
                        (self.pos[0] + x) / Map.SCALE,
                        (self.pos[1] + y) / Map.SCALE,
                        octaves=6,
                        persistence=0.5,
                        lacunarity=2,
                        repeatx=Map.DIMENSIONS[0],
                        repeaty=Map.DIMENSIONS[1],
                        base=self.base[i]
                    )
                    value = (value - Map.MIN_VAL) / (Map.MAX_VAL - Map.MIN_VAL)

                    if i == 0:
                        if (x + self.pos.x) < Map.DIMENSIONS[0] / 2:
                            value *= (x + self.pos.x) / (Map.DIMENSIONS[0] / 2)
                        elif x + self.pos.x > Map.DIMENSIONS[0] / 2:
                            value *= ((x + self.pos.x) - Map.DIMENSIONS[0]) / (Map.DIMENSIONS[0] / 2)

                    in_layer = False

                    for biome in Map.BIOME_HEIGHTS[i]:
                        if not Map.BIOME_HEIGHTS[i][biome]:
                            if not i == len(Map.BIOME_HEIGHTS[i]) - 1:
                                if value > biome:
                                    continue
                            break
                        elif value < biome:
                            row.append(Map.BIOME_HEIGHTS[i][biome])
                            in_layer = True
                            break

                    if in_layer:
                        break

            terrain.append(row)

        return terrain

    def terrain_onto_surface(self, surface, colors, pos=None):
        if not pos:
            pos = self.pos

        chunk_surface = pygame.Surface(self.CHUNK_DIMENSIONS)
        for i, row in enumerate(self.terrain):
            for j, biome in enumerate(row):
                pygame.draw.rect(
                    chunk_surface,
                    colors[biome],
                    (j * Map.CELL_SIZE, i * Map.CELL_SIZE, Map.CELL_SIZE, Map.CELL_SIZE)
                )
        surface.blit(chunk_surface, pos)
