import pygame
from main import Game, CollideRect
from map import Map
from pygame import Vector2
import random
import noise
from Enemy.enemies import *


class Chunk:
    CHUNK_DIMENSIONS = (Game.CHUNK_SIZE, Game.CHUNK_SIZE)

    def __init__(self, game, map_, pos, base, colors, new=True, id=str(random.randbytes(20))):
        self.game = game
        self.id = id
        self.map = map_
        self.pos = Vector2(pos)
        self.rect = pygame.Rect(self.pos, self.CHUNK_DIMENSIONS)
        self.base = base

        self.active = False
        self.terrain_surface = pygame.Surface(self.CHUNK_DIMENSIONS)

        if new:
            self.terrain, self.biome_cells = self.generate()
            self.terrain_onto_surface(self.terrain_surface, colors, (0, 0))

            self.shrubs = self.generate_shrubs()
            self.enemies = self.generate_enemies()
            self.floor_items = self.place_floor_items()

            self.delete_overlapping_shrubs()

    def delete_overlapping_shrubs(self):
        for i, shrub_to_check in enumerate(self.shrubs):
            popped = False
            for _, shrub in enumerate(self.shrubs):
                if not shrub_to_check == shrub:
                    if shrub_to_check.get_bounding_rect().colliderect(shrub.get_bounding_rect()) and not popped:
                        self.shrubs.pop(i)
                        popped = True

    def place_floor_items(self):
        floor_items = []
        for biome in Map.BIOMES:
            if self.biome_cells[biome] and biome in Map.FLOOR_ITEM_COUNT_PER_CELL:
                floor_items.extend(
                    [
                        FloorItem(
                            self.game,
                            self,
                            Vector2(random.choice(self.biome_cells[biome])) + self.pos,
                            random.choice(Map.FLOOR_ITEMS[biome])(self.game)
                        )
                        for _ in range(round(Map.FLOOR_ITEM_COUNT_PER_CELL[biome] * len(self.biome_cells[biome])))
                    ]
                )
        return floor_items

    def load_terrain_onto_surface(self, colors):
        self.terrain_onto_surface(self.terrain_surface, colors, (0, 0))

    def generate_enemies(self):
        enemies = []
        for biome in Map.BIOMES:
            if self.biome_cells[biome] and biome in Map.ENEMY_PEACEFUL_COUNT_PER_CELL:
                enemies.extend(
                    [
                        random.choice(Map.BIOME_ENEMIES_PEACEFUL[biome])(
                            self.game,
                            self,
                            Vector2(random.choice(self.biome_cells[biome])),
                            new=True
                        )
                        for _ in range(round(Map.ENEMY_PEACEFUL_COUNT_PER_CELL[biome] * len(self.biome_cells[biome])))
                    ]
                )
        return enemies

    def generate_shrubs(self):
        shrubs = []
        for biome in Map.BIOMES:
            if self.biome_cells[biome] and biome in Map.SHRUB_COUNT_PER_CELL:
                shrubs.extend(
                    [
                        random.choice(Map.BIOME_SHRUBS[biome])(
                            self.game,
                            self,
                            random.choice(self.biome_cells[biome]),
                            new=True
                        )
                        for _ in range(round(Map.SHRUB_COUNT_PER_CELL[biome] * len(self.biome_cells[biome])))
                    ]
                )
        return shrubs

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
                        elif x + self.pos.x > Map.DIMENSIONS[0] /  2:
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

    def basic_damage(self, rect, damage):
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(
                CollideRect(enemy.get_bounding_rect()),
                CollideRect(rect)
            ):
                enemy.damage(damage)

    def place_floor_items_in_rect(self, item, rect, count):
        for i in range(count):
            self.floor_items.append(
                FloorItem(
                    self.game,
                    self,
                    (
                        random.randrange(rect.x, rect.x + rect.size[0]),
                        random.randrange(rect.y, rect.y + rect.size[1])
                    ),
                    item(self.game)
                )
            )

    def update(self):
        self.active = False
        if self.game.camera.rect.colliderect(self.rect):
            self.active = True
        if self.game.player.rect.colliderect(self.rect):
            self.map.active_chunk = self

        if self.enemies:
            [enemy.update() for enemy in self.enemies]

        if self.shrubs:
            [shrub.update() for shrub in self.shrubs]

            if self.active:
                [shrub.active_update() for shrub in self.shrubs]

        if self.floor_items and self.active:
            [floor_item.active_update() for floor_item in self.floor_items]

    def draw(self, surface):
        if self.floor_items:
            [floor_item.draw(surface) for floor_item in self.floor_items]
        if self.enemies:
            [enemy.draw(surface) for enemy in self.enemies]
        if self.shrubs:
            [shrub.draw(surface) for shrub in self.shrubs]
