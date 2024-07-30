import noise
import random


class Level:
    LEVEL_SIZE = 1000
    MAX_DEPTH = 5
    SCALE = 4000
    WALL_HEIGHT = 0.5

    def __init__(self, game, depth, type):
        self.game = game
        self.depth = depth
        self.type = type

        self.terrain, self.floor_cells = self.generate()

    def generate(self):
        from map import Map
        terrain = []
        floor_cells = []

        for y in range(0, self.LEVEL_SIZE, Map.CELL_SIZE):
            row = []
            for x in range(0, self.LEVEL_SIZE, Map.CELL_SIZE):
                value = noise.snoise2(
                    x / self.SCALE,
                    y / self.SCALE,
                    octaves=6,
                    persistence=0.5,
                    lacunarity=2,
                    repeatx=self.LEVEL_SIZE,
                    repeaty=self.LEVEL_SIZE,
                    base=random.randrange(self.LEVEL_SIZE)
                )
                value = (value - Map.MIN_VAL) / (Map.MAX_VAL - Map.MIN_VAL)

                if x < self.LEVEL_SIZE / 2:
                    value *= x / (self.LEVEL_SIZE / 2)
                elif x > self.LEVEL_SIZE / 2:
                    value *= (self.LEVEL_SIZE - x) / (self.LEVEL_SIZE / 2)

                if y < self.LEVEL_SIZE / 2:
                    value *= y / (self.LEVEL_SIZE / 2)
                elif y > self.LEVEL_SIZE / 2:
                    value *= (self.LEVEL_SIZE - y) / (self.LEVEL_SIZE / 2)

                if value < self.WALL_HEIGHT:
                    row.append('wall')
                else:
                    row.append('floor')
                    floor_cells.append((x, y))

            terrain.append(row)

        return terrain, floor_cells
