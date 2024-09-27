import random
import sys
sys.path.append('..')

import pygame
pygame.init()

from color import Color
import profilehooks
import threading

class Game:
    RES = WIDTH, HEIGHT = 1600, 900

    LAYER_COUNT = 4
    FPS = 30
    CHUNK_SIZE = 1000
    CHUNK_COUNT = 3

    FILL_COLOR = Color('black', a=0).color
    BG_COLOR = Color('black', random_=False).color

    PLAYER_INVENTORY_SIZE = 12
    INVENTORY_ITEM_SIZE = (64, 64)
    CAMPFIRE_RANGE = 200
    CAMPFIRE_POWER = 0.75

    CRAFTING_ITEM_SIZE = (64, 64)

    DEEP_ENTRANCES = 2
    DEEP_REQUIREMENT = 1

    CYCLES = {
        'day': [0, 5],
        'sunset': [5, 240],
        'night': [240, 235],
        'sunrise': [235, 0]
    }
    CYCLE_TIMES = {
        'day': 5000,
        'sunset': 2000,
        'night': 3500,
        'sunrise': 1500
    }

    @profilehooks.profile
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.layers = [pygame.Surface(self.RES, pygame.SRCALPHA) for _ in range(self.LAYER_COUNT)]
        self.delta_time = 1
        self.screen = 'main_menu'
        self.paused = False
        self.saving = False

        self.total_chunks = self.CHUNK_COUNT * self.CHUNK_COUNT
        self.chunk_progress = 0

        self.deep_levels = {}

        from window import Window
        self.window = Window(self)

        from input import Input
        from camera import Camera
        from timers import Timers
        from save import Save

        self.input = Input(self)
        self.camera = Camera(self)
        self.timers = Timers(self)
        self.save = Save(self)

        from crafting import CRAFTING_MENU
        for menu in CRAFTING_MENU.values():
            for item in menu:
                item.initialize(self)

        from UI.ui import UI
        from player import Player
        from map import Map

        self.ui = UI(self)
        self.player = Player(self)
        self.map = Map(self)

        self.active_map = self.map
        self.time_timer_name = f'{self}_timer_time'
        self.timers.add_timer(self.time_timer_name)
        self.darkness = 0
        self.cycle = 'sunrise'

        # self.enemy_wave_timer_name = f'{self}_enemy_wave_timer_name'
        # self.enemy_wave_count = 1
        # self.enemy_wave_timer_max = 10000
        # self.timers.add_timer(self.enemy_wave_timer_name, self.enemy_wave_timer_max)

    @staticmethod
    def collide_mask_rect(left, right):
        xoffset = right.rect[0] - left.rect[0]
        yoffset = right.rect[1] - left.rect[1]
        try:
            leftmask = left.mask
        except AttributeError:
            leftmask = pygame.mask.Mask(left.size, True)
        try:
            rightmask = right.mask
        except AttributeError:
            rightmask = pygame.mask.Mask(right.rect.size, True)
        return not bool(leftmask.overlap(rightmask, (xoffset, yoffset)))

    @staticmethod
    def get_centered_position(pos, size):
        return pos[0] - size[0] // 2, pos[1] - size[1] // 2

    @staticmethod
    def div(a, b, default=None):
        if not b:
            if not default:
                return a
            else:
                return default
        return a / b

    @staticmethod
    def draw_transparent_rect(surface, size, pos, color):
        temp_surf = pygame.Surface(size, pygame.SRCALPHA)
        temp_surf.fill(color)
        surface.blit(temp_surf, pos)

    @staticmethod
    def round_base(x, base):
        return base * round(x / base)

    # def manage_enemy_waves(self):
    #     if self.timers.check_max(self.enemy_wave_timer_name):
    #         self

    def setup(self):
        self.screen = 'loading'
        self.chunk_progress = 0
        threading.Thread(target=self.map.generate).start()

    def map_generation_finished(self, set_player_pos=True):
        self.screen = 'game'
        self.map.set_ocean_rect()
        if set_player_pos:
            for row in self.map.chunks:
                for chunk in row:
                    if len(chunk.biome_cells['sand']) > 100:
                        self.player.pos = pygame.Vector2(random.choice(chunk.biome_cells['sand']))
                        return

    def update_day_night_cycle(self):
        if self.timers.check_max(self.time_timer_name):
            next_cycle_index = list(self.CYCLES.keys()).index(self.cycle) + 1
            if next_cycle_index >= len(self.CYCLES):
                next_cycle_index = 0
            self.cycle = list(self.CYCLES.keys())[next_cycle_index]
            self.timers.add_timer(self.time_timer_name, self.CYCLE_TIMES[self.cycle])

        cycle_time = self.timers.timers[self.time_timer_name]
        cycle_progress =  cycle_time / self.CYCLE_TIMES[self.cycle] + 0.000000001
        self.darkness = round(
            (self.CYCLES[self.cycle][1] - self.CYCLES[self.cycle][0]) * cycle_progress + self.CYCLES[self.cycle][0]
        )

        if self.map.campfires:
            shortest_distance = None
            for campfire in self.map.campfires:
                if not shortest_distance:
                    shortest_distance = self.player.pos.distance_to(pygame.Vector2(campfire))
                elif self.player.pos.distance_to(pygame.Vector2(campfire)) < shortest_distance:
                    shortest_distance = self.player.pos.distance_to(pygame.Vector2(campfire))

            if shortest_distance < self.CAMPFIRE_RANGE:
                self.darkness -= (self.CAMPFIRE_RANGE - shortest_distance) * self.CAMPFIRE_POWER

            if self.darkness < 0:
                self.darkness = 0

    def draw_effects(self):
        self.draw_transparent_rect(self.layers[2], self.RES, (0, 0), Color('black', a=self.darkness).color)

    def update(self):
        self.delta_time = self.clock.tick(self.FPS)
        self.delta_time /= 1000

        # = 1 / self.delta_time
        #pygame.display.set_caption(str(frame_rate))

        self.input.update()

        if self.screen == 'game' and not self.paused:
            self.game_update()

        self.camera.update()
        self.ui.update()

    def game_update(self):
        self.update_day_night_cycle()
        self.timers.update()
        self.player.update()
        self.active_map.update()

    def draw(self):
        [layer.fill(self.FILL_COLOR) for layer in self.layers]

        if self.screen in ['paused', 'game']:
            self.game_draw()

        self.ui.draw(self.layers[3])
        self.input.draw(self.layers[3])

    def game_draw(self):
        self.draw_effects()
        self.player.draw(self.layers[1])
        self.active_map.draw(self.layers[0], self.layers[1])

    @profilehooks.profile
    def run(self):
        while self.running:
            self.update()
            self.draw()

            self.window.update()
            self.window.render(self.layers)

        self.quit()

    def quit(self):
        pygame.quit()
        quit()


class CollideRect:

    def __init__(self, rect):
        self.rect = pygame.Rect(rect)


class CollideCircle:

    def __init__(self, rect, radius):
        self.rect = pygame.Rect(rect)
        self.radius = radius


class OceanMask:

    def __init__(self, mask, rect):
        self.mask = mask
        self.rect = rect


if __name__ == '__main__':
    game = Game()
    game.run()
