import pygame


class Input:

    def __init__(self):
        self.keys = {
            pygame.__dict__[attr]: Key(pygame.__dict__[attr])
            for attr in dir(pygame)
            if attr.startswith('K_')
        }

    def update(self):
        keys = pygame.key.get_pressed()
        [key.update(keys) for key in self.keys.values()]


class Key:

    def __init__(self, key):
        self.key = key
        self.pressed = False
        self.held = False
        self.released = False

    def update(self, keys):
        if keys[self.key]:
            if self.pressed:
                self.pressed = False

            if not self.held:
                self.pressed = True
            self.held = True
        else:
            if self.held:
                self.released = True
                self.held = False
