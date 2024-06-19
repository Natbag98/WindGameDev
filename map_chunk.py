import pygame
import noise
from main import Game
from map import Map
from pygame import Vector2
from shrubs import BushSimple
import random


class Chunk:
    CHUNK_DIMENSIONS = (Game.CHUNK_SIZE, Game.CHUNK_SIZE)

    def __init__(self, game, map_, pos, edges, base, colors):
        self.game = game
        self.map = map_
        self.pos = Vector2(pos)
        self.rect = pygame.Rect(self.pos, self.CHUNK_DIMENSIONS)
        self.edges = edges
        self.base = base

        self.active = False

        self.terrain, self.biome_cells = self.generate()
        self.terrain_surface = pygame.Surface(self.CHUNK_DIMENSIONS)

        self.game.chunk_progress += 1
        print(f'{self.game.chunk_progress} / {self.game.total_chunks}')

        self.terrain_onto_surface(self.terrain_surface, colors, (0, 0))

        self.shrubs = self.generate_shrubs()

    def generate_shrubs(self):
        shrubs = []
        for biome in Map.BIOMES:
            shrubs.append(*self.place_shrubs(biome))
        return shrubs

    def place_shrubs(self, biome):
        if self.biome_cells[biome] and biome in Map.SHRUB_COUNT_PER_CELL:
            count = round(Map.SHRUB_COUNT_PER_CELL[biome] * len(self.biome_cells[biome]))

            return [
                BushSimple(
                    self.game,
                    self,
                    random.choice(self.biome_cells[biome])
                )
                for _ in range(count)
            ]

    def generate(self):
        terrain = []
        biome_cells = {biome: [] for biome in Map.BIOMES}

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
                        if x + self.pos.x < Map.DIMENSIONS[0] / 2:
                            value *= (x + self.pos.x) / (Map.DIMENSIONS[0] / 2)
                        elif x + self.pos.x > Map.DIMENSIONS[0] / 2:
                            value *= (Map.DIMENSIONS[0] - (x + self.pos.x)) / (Map.DIMENSIONS[0] / 2)

                        if y + self.pos.y < Map.DIMENSIONS[1] / 2:
                            value *= (y + self.pos.y) / (Map.DIMENSIONS[1] / 2)
                        elif y + self.pos.y > Map.DIMENSIONS[1] / 2:
                            value *= (Map.DIMENSIONS[0] - (y + self.pos.y)) / (Map.DIMENSIONS[1] / 2)

                    in_layer = False

                    for biome in Map.BIOME_HEIGHTS[i]:
                        if not Map.BIOME_HEIGHTS[i][biome]:
                            if not i == len(Map.BIOME_HEIGHTS[i]) - 1:
                                if value > biome:
                                    continue
                            break
                        elif value < biome:
                            row.append(Map.BIOME_HEIGHTS[i][biome])
                            biome_cells[Map.BIOME_HEIGHTS[i][biome]].append((x, y))
                            in_layer = True
                            break

                    if in_layer:
                        break

            terrain.append(row)


        return terrain, biome_cells

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

    def update(self):
        if self.game.camera.rect.colliderect(self.rect):
            self.active = True

        if self.shrubs:
            [shrub.update() for shrub in self.shrubs]

    def draw(self, surface):
        if self.shrubs:
            [shrub.draw(surface) for shrub in self.shrubs]
