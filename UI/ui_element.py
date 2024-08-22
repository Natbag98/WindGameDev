from color import Color
import pygame
from main import Game


class Element:

    def __init__(
        self,
        pos,
        pos_position='center',
        text=None,
        text_size=None,
        font=None,
        sprites=None,
        text_color=Color('white').color,
        clicked_func=None,
        clicked_func_args=(),
        bg_color=Color('black', a=0).color,
        hover_color=Color('black', a=0).color,
        size=None,
        update_func=None,
        update_func_args=(),
        hidden=False,
        hovered_func=None,
        hovered_func_args=()
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
        self.text_color = text_color
        self.clicked_func = clicked_func
        self.clicked_func_args = clicked_func_args
        self.bg_color = bg_color
        self.default_bg_color = bg_color
        self.hover_color = hover_color
        self.hovering = False
        self.bounding_rect = None
        self.update_func=update_func
        self.sprites = sprites
        self.update_func_args = update_func_args
        self.hidden = hidden
        self.hovered_func=hovered_func
        self.hovered_func_args=hovered_func_args

    def initialize(self, game):
        self.game = game

        if self.text:
            self.render_text()
        elif self.sprites:
            self.size = self.sprites[0].get_size()
            self.bounding_rect = self.sprites[0].get_bounding_rect()

        if self.pos_position == 'top_left':
            self.pos = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)
        elif self.pos_position == 'bottom_center':
            self.pos = (self.pos[0], self.pos[1] - self.size[1] // 2)
        elif self.pos_position == 'left_center':
            self.pos = (self.pos[0] + self.size[0] // 2, self.pos[1])

        self.rect = pygame.Rect(self.game.get_centered_position(self.pos, self.size), self.size)

    def render_text(self, pre_rendered=None):
        if pre_rendered:
            self.text = pre_rendered
            self.size = self.text.get_size
        else:
            sys_font = pygame.font.SysFont(self.font, self.text_size)
            if type(self.text) not in [str, bytes]:
                self.text = ' '
            self.text = sys_font.render(self.text, True, self.text_color)
            self.size = self.text.get_size()

    def update(self):
        if self.game.input.mouse['left'].interact(self.rect):
            self.bg_color = self.hover_color
            self.hovering = True
        else:
            self.bg_color = self.default_bg_color
            self.hovering = False

        if self.game.input.mouse['left'].interact(self.rect) and self.hovered_func:
            self.hovered_func(self.game, self, *self.hovered_func_args)

        if self.game.input.mouse['left'].interact(self.rect, 'clicked') and self.clicked_func and not self.hidden:
            self.clicked_func(self.game, self, *self.clicked_func_args)

        if self.update_func:
            self.update_func(self.game, self, *self.update_func_args)

    def draw(self, surface):
        if not self.hidden:
            if not self.sprites:
                Game.draw_transparent_rect(surface, self.rect.size, self.rect.topleft, self.bg_color)
            else:
                [surface.blit(sprite, self.rect.topleft) for sprite in self.sprites if sprite]
                if self.hovering:
                    Game.draw_transparent_rect(
                        surface,
                        self.bounding_rect.size,
                        (
                            self.bounding_rect.topleft[0] + self.rect.topleft[0],
                            self.bounding_rect.topleft[1] + self.rect.topleft[1]
                        ),
                        self.bg_color
                    )

            if self.text:
                surface.blit(self.text, self.rect.topleft)
