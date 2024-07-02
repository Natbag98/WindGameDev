import pygame


class PygameTimers:

    def __init__(self, game):
        self.game = game
        self.timers = {}
        self.timer_max = {}
        self.time_at_pause_start = {}
        self.stop_on_pause = {}

    def get_tick_diff(self, ticks, current_time=None):
        if current_time is None:
            current_time = pygame.time.get_ticks()
        return (current_time - ticks) / 1000

    def start_timer(self, name, stop_on_pause=False, timer_max=None):
        self.timers[name] = pygame.time.get_ticks()
        self.timer_max[name] = timer_max
        self.time_at_pause_start[name] = False
        self.stop_on_pause[name] = stop_on_pause

    def get_time(self, name):
        if self.time_at_pause_start[name]:
            return self.get_tick_diff(self.timers[name], self.time_at_pause_start[name])
        else:
            return self.get_tick_diff(self.timers[name])

    def get_max(self, name):
        if self.timer_max[name] is not None:
            if self.get_time(name) >= self.timer_max[name]:
                return True
        return False

    def reset_timer(self, name, timer_max=None):
        self.timers[name] = pygame.time.get_ticks()
        if timer_max:
            self.timer_max[name] = timer_max
        self.time_at_pause_start[name] = False

    def delete_timer(self, name):
        self.timers.pop(name)
        self.timer_max.pop(name)
        self.time_at_pause_start.pop(name)
        self.stop_on_pause.pop(name)

    def pause_timer(self, name):
        if self.time_at_pause_start[name] is False:
            self.time_at_pause_start[name] = pygame.time.get_ticks()

    def unpause_timer(self, name):
        if self.time_at_pause_start[name] is not None:
            self.timers[name] += pygame.time.get_ticks() - self.time_at_pause_start[name]
        self.time_at_pause_start[name] = False

    def update(self):
        if self.game.paused:
            for timer in self.timers:
                if self.stop_on_pause:
                    self.pause_timer(timer)
        else:
            for timer in self.timers:
                if self.stop_on_pause:
                    self.unpause_timer(timer)
