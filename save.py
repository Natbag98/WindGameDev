import os
import json

import pygame
from pygame import Vector2

from wind_json import WindEncoder
from map import Map
from main import Game
from map_chunk import Chunk
from shrubs import _SHRUBS
from deep_level import Level
from Enemy.enemies import _ENEMIES


class Save:

    def __init__(self, game):
        self.game = game
        self.app_data_path = os.path.expandvars('%LOCALAPPDATA%\\Wind')
        self.id_objects = {}

        if not os.path.exists(self.app_data_path):
            os.mkdir(self.app_data_path)

    def save(self, slot=0):
        with open(f'{self.app_data_path}\\{slot}.sav', 'w') as file:
            file.write(json.dumps(self.game.map, cls=WindEncoder, indent=2))
        with open(f'{self.app_data_path}\\_{slot}.sav', 'w') as file:
            file.write(
                json.dumps(
                    {
                        'colors': self.game.colors,
                        'deep_levels': self.game.deep_levels
                    },
                    cls=WindEncoder,
                    indent=2
                )
            )

    def set_id(self, obj, id):
        obj.id = id
        self.id_objects[id] = obj

    def load_pos(self, pos):
        if type(pos) is dict:
            return (pos['x'], pos['y'])
        else:
            return tuple(pos)

    def load_shrub(self, shrub):
        if not shrub['type'].startswith('Deep'):
            new_shrub = _SHRUBS[shrub['type']](
                self.game,
                self.id_objects[shrub['parent_id']],
                Vector2(self.load_pos(shrub['pos']))
            )
        else:
            if 'entrance_pos' in shrub.keys():
                new_shrub = _SHRUBS[shrub['type']](
                    self.game,
                    self.id_objects[shrub['parent_id']],
                    Vector2(self.load_pos(shrub['pos'])),
                    self.id_objects[shrub['target_level_id']],
                    Vector2(self.load_pos(shrub['entrance_pos']))
                )
            else:
                new_shrub = _SHRUBS[shrub['type']](
                    self.game,
                    self.id_objects[shrub['parent_id']],
                    Vector2(self.load_pos(shrub['pos'])),
                    self.id_objects[shrub['target_level_id']]
                )

        new_shrub.active_sprite = shrub['active_sprite']

        if shrub['type'] == 'BushFlowers':
            new_shrub.color = shrub['color']
            new_shrub.collected = shrub['collected']

        return new_shrub

    def load_enemy(self, enemy):
        new_enemy = _ENEMIES[enemy['type']](
            self.game,
            self.id_objects[enemy['chunk_id']],
            self.load_pos(enemy['start_pos_base'])
        )
        new_enemy.pos = Vector2(self.load_pos(enemy['pos']))
        new_enemy.health = enemy['health']
        return new_enemy

    def load(self, slot=0):
        with open(f'{self.app_data_path}\\{slot}.sav', 'r') as file:
            data = json.loads(file.read())
        with open(f'{self.app_data_path}\\_{slot}.sav', 'r') as file:
            game_data = json.loads(file.read())

        self.game.map = Map(self.game)
        self.set_id(self.game.map, data['id'])

        self.game.map.chunks = [
            [
                None for _ in range(Game.CHUNK_COUNT)
            ]
            for _ in range(Game.CHUNK_COUNT)
        ]
        for chunk in data['chunks']:
            if type(chunk) is list:
                chunk = chunk[0]
            x = int(chunk['pos']['x'] // Game.CHUNK_SIZE)
            y = int(chunk['pos']['y'] // Game.CHUNK_SIZE)
            self.game.map.chunks[y][x] = Chunk(
                self.game,
                self.game.map,
                self.load_pos(chunk['pos']),
                None,
                None,
                new=False
            )

            levels = []
            for id in game_data['deep_levels']:
                level = game_data['deep_levels'][id]
                new_level = Level(
                    self.game,
                    level['depth'],
                    level['type'],
                    level['parent_id'],
                    level['entrance_pos'],
                    new=False
                )
                self.set_id(new_level, id)

                self.id_objects[id].terrain = level['terrain']
                self.id_objects[id].floor_cells = level['floor_cells']
                self.id_objects[id].entrance_positions = [self.load_pos(pos) for pos in level['entrance_positions']]
                levels.append((self.id_objects[id], level))

            for level in levels:
                level[0].parent = self.id_objects[level[0].parent]
                level[0].shrubs = [self.load_shrub(shrub) for shrub in level[1]['shrubs']]

            self.set_id(self.game.map.chunks[y][x], chunk['id'])
            self.game.map.chunks[y][x].terrain = chunk['terrain']
            self.game.map.chunks[y][x].biome_cells = chunk['biome_cells']
            self.game.map.chunks[y][x].shrubs = [self.load_shrub(shrub) for shrub in chunk['shrubs']]
            self.game.map.chunks[y][x].enemies = [self.load_enemy(enemy) for enemy in chunk['enemies']]
            self.game.map.chunks[y][x].floor_items = chunk['floor_items']
            self.game.map.chunks[y][x].load_terrain_onto_surface(game_data['colors'])

        self.game.active_map = self.game.map
