

class Timers:

    def __init__(self, game):
        self.game = game
        self.timers = {}
        self.timer_max = {}

    def add_timer(self, name, timer_max=0):
        self.timers[name] = 0
        self.timer_max[name] = timer_max

    def check_max(self, name):
        """
        Returns true if the timer is past the max
        """
        if self.timers[name] > self.timer_max[name]:
            return True
        return False

    def set_max(self, name, max):
        self.timer_max[name] = max

    def delete_timer(self, name):
        self.timers.pop(name)
        self.timer_max.pop(name)

    def update(self):
        if not self.game.paused:
            for timer in self.timers:
                self.timers[timer] += self.game.delta_time * 100
