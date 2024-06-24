from color import Color
import pygame


class Element:

    def __init__(
        self,
        pos,
        pos_position='center',
        text=None,
        text_size=None,
        font=None,
        sprite=None,
        text_color=Color('white').color,
        clicked_func=None,
        bg_color=Color('black', a=0).color,
        hover_color=Color('black', a=0).color,
        size=None
    ):
        self.game = None
        self.size = None
        self.rect = None
        self.size = size
        self.pos = pos
        self.pos_position = pos_position
        self.text = text
        self.text_size = text_size
        self.font = font
        self.sprite = sprite
        self.text_color = text_color
        self.clicked_func = clicked_func
        self.bg_color = bg_color
        self.default_bg_color = bg_color
        self.hover_color = hover_color

    def initialize(self, game):
        self.game = game

        if self.text:
            self.font = pygame.font.SysFont(self.font, self.text_size)
            self.text = self.font.render(self.text, True, self.text_color)
            self.size = self.text.get_size()
        elif self.sprite:
            self.size = self.sprite.get_size()

        if self.pos_position == 'top_left':
            self.pos = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.size), self.size)

    def update(self):
        if self.game.input.mouse['left'].interact(self.rect):
            self.bg_color = self.hover_color
        else:
            self.bg_color = self.default_bg_color

        if self.game.input.mouse['left'].interact(self.rect, 'clicked') and self.clicked_func:
            self.clicked_func(self.game)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)

        if self.text:
            surface.blit(self.text, self.rect.topleft)
        elif self.sprite:
            surface.blit(self.sprite, self.rect.topleft)
