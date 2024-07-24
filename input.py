import pygame


class Input:
    MOUSE_BUTTONS = {
        'left': 0,
        'middle': 1,
        'right': 2
    }

    def __init__(self, game):
        self.game = game

        self.keys = {
            pygame.__dict__[attr]: Key(pygame.__dict__[attr])
            for attr in dir(pygame)
            if attr.startswith('K_')
        }

        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = (
            self.mouse_pos[0] * self.game.window.res_scale,
            self.mouse_pos[1] * self.game.window.res_scale
        )
        self.mouse = {
            key: MouseButton(self.MOUSE_BUTTONS[key], self)
            for key in self.MOUSE_BUTTONS
        }

    def update(self):
        keys = pygame.key.get_pressed()
        [key.update(keys) for key in self.keys.values()]

        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = (
            self.mouse_pos[0] / self.game.window.res_scale[0],
            self.mouse_pos[1] / self.game.window.res_scale[1]
        )
        [mouse_button.update() for mouse_button in self.mouse.values()]

    def draw(self, surface):
        #pygame.draw.circle(surface, 'red', self.mouse_pos, 10)
        pass


class MouseButton:

    def __init__(self, button, input):
        self.button = button
        self.input = input
        self.clicked = False
        self.held = False
        self.released = False

    def interact(self, rect, click_type=None):
        if not click_type:
            return rect.collidepoint(self.input.mouse_pos)
        return rect.collidepoint(self.input.mouse_pos) and self.__dict__[click_type]

    def update(self):
        if pygame.mouse.get_pressed()[self.button]:
            if self.clicked:
                self.clicked = False

            if not self.held:
                self.clicked = True
            self.held = True
        else:
            if self.held:
                self.released = True
                self.held = False


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
