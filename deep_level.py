import noise
import random
import pygame
from shrubs import DeepExit, DeepEntrance
from color import Color


class Level:
    LEVEL_SIZE = 2000
    MAX_DEPTH = 4
    SCALE = 800
    WALL_HEIGHT = 0.06
    MAX_EXITS = 2
    CELL_SIZE = 4

    COLORS = {
        'basic': {
            'wall': Color('black').color,
            'floor': Color('grey').color
        }
    }

    def __init__(self, game, depth, type, parent, entrance_pos):
        self.game = game
        self.depth = depth
        self.type = type
        self.parent = parent
        self.entrance_pos = entrance_pos

        self.shrubs = []

        self.game.total_chunks += 1
        self.terrain, self.floor_cells = self.generate()

        self.entrance_positions = []
        if not self.depth == self.MAX_DEPTH:
            for i in range(0, random.randrange(0, self.MAX_EXITS + 1)):
                self.entrance_positions.append(random.choice(self.floor_cells))

        self.place_exit()
        self.place_entrance()
        self.surface = pygame.Surface((self.LEVEL_SIZE, self.LEVEL_SIZE))
        self.terrain_onto_surface(self.surface)
        self.game.chunk_progress += 1

    def place_entrance(self):
        for pos in self.entrance_positions:
            self.shrubs.append(
                DeepEntrance(
                    self.game,
                    self,
                    pos,
                    Level(self.game, self.depth + 1, 'basic', self, pos)
                )
            )

    def place_exit(self):
        self.shrubs.append(
            DeepExit(
                self.game,
                self,
                random.choice(self.floor_cells),
                self.parent,
                self.entrance_pos
            )
        )

    def generate(self):
        from map import Map
        terrain = []
        floor_cells = []
        
        base = random.randrange(0, self.LEVEL_SIZE, self.CELL_SIZE)

        for y in range(0, self.LEVEL_SIZE, self.CELL_SIZE):
            row = []
            for x in range(0, self.LEVEL_SIZE, self.CELL_SIZE):
                value = noise.snoise2(
                    x / self.SCALE,
                    y / self.SCALE,
                    octaves=6,
                    persistence=0.5,
                    lacunarity=2,
                    repeatx=self.LEVEL_SIZE,
                    repeaty=self.LEVEL_SIZE,
                    base=base
                )
                value = (value - Map.MIN_VAL) / (Map.MAX_VAL - Map.MIN_VAL)

                if x < self.LEVEL_SIZE / 2:
                    value *= (x) / (self.LEVEL_SIZE / 2)
                elif x > self.LEVEL_SIZE / 2:
                    value *= (self.LEVEL_SIZE - (x)) / (self.LEVEL_SIZE / 2)

                if y < self.LEVEL_SIZE / 2:
                    value *= (y) / (self.LEVEL_SIZE / 2)
                elif y > self.LEVEL_SIZE / 2:
                    value *= (self.LEVEL_SIZE - (y)) / (self.LEVEL_SIZE / 2)

                if value < self.WALL_HEIGHT:
                    row.append('wall')
                else:
                    row.append('floor')
                    floor_cells.append((x, y))

            terrain.append(row)

        return terrain, floor_cells

    def terrain_onto_surface(self, surface):
        chunk_surface = pygame.Surface((self.LEVEL_SIZE, self.LEVEL_SIZE))
        for i, row in enumerate(self.terrain):
            for j, cell in enumerate(row):
                pygame.draw.rect(
                    chunk_surface,
                    self.COLORS[self.type][cell],
                    (j * self.CELL_SIZE, i * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                )
        surface.blit(chunk_surface, (0, 0))

    def update(self):
        [shrub.update() for shrub in self.shrubs]
        [shrub.active_update() for shrub in self.shrubs]

    def draw(self, ground_surface, shrub_surface):
        ground_surface.blit(self.surface, -self.game.camera.offset)
        [shrub.draw(shrub_surface) for shrub in self.shrubs]
