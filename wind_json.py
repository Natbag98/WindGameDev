import json
from map import Map
from map_chunk import Chunk
import pygame
from shrub import Shrub
from shrubs import BushFlowers, DeepExit, DeepEntrance
from Enemy.enemy import Enemy
from deep_level import Level
from player import Player
from floor_item import FloorItem
from Inventory.inventory import Inventory
from Inventory.item import Item


class WindEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Map):
            chunks = []
            for row in obj.chunks:
                for chunk in row:
                    chunks.append(chunk)
            return {
                'id': obj.id,
                'chunks': chunks
            }

        if isinstance(obj, Chunk):
            return {
                'id': obj.id,
                'pos': obj.pos,
                'terrain': obj.terrain,
                'biome_cells': obj.biome_cells,
                'shrubs': obj.shrubs,
                'enemies': obj.enemies,
                'floor_items': obj.floor_items
            }

        if isinstance(obj, FloorItem):
            return {
                'chunk_id': obj.chunk.id,
                'pos': obj.pos,
                'item': obj.item
            }

        if isinstance(obj, pygame.Vector2):
            return {
                'x': obj.x,
                'y': obj.y
            }

        if isinstance(obj, Shrub):
            to_return = {
                'type': obj.__class__.__name__,
                'id': obj.id,
                'pos': obj.pos,
                'parent_type': obj.parent_type,
                'parent_id': obj.parent.id,
                'active_sprite': obj.active_sprite
            }

            if isinstance(obj, BushFlowers):
                to_return.update(
                    {
                        'color': obj.color,
                        'collected': obj.collected
                    }
                )

            if isinstance(obj, DeepEntrance):
                to_return.update(
                    {
                        'target_level_id': obj.target_level.id
                    }
                )

            if isinstance(obj, DeepExit):
                to_return.update(
                    {
                        'target_level_id': obj.target_level.id,
                        'entrance_pos': obj.entrance_pos
                    }
                )

            return to_return

        if isinstance(obj, Enemy):
            return {
                'type': obj.__class__.__name__,
                'chunk_id': obj.chunk.id,
                'health': obj.health,
                'pos': obj.pos,
                'start_pos_base': obj.start_pos_base
            }

        if isinstance(obj, Level):
            return {
                'id': obj.id,
                'depth': obj.depth,
                'type': obj.type,
                'parent_id': obj.parent.id,
                'entrance_pos': obj.entrance_pos,
                'shrubs': obj.shrubs,
                'terrain': obj.terrain,
                'floor_cells': obj.floor_cells,
                'entrance_positions': obj.entrance_positions
            }

        if isinstance(obj, Player):
            return {
                'health': obj.health,
                'inventory': obj.inventory,
                'pos': obj.pos
            }

        if isinstance(obj, Inventory):
            return {
                'items': obj.items
            }

        if isinstance(obj, Item):
            return {
                'type': obj.__class__.__name__
            }

        return super().default(obj)
