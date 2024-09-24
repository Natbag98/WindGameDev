import pygame
import os


def _grayscale(surface):
    grayscale_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    surface.lock()
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            grayscale_value = int(0.21 * r + 0.72 * g + 0.07 * b)
            grayscale_surface.set_at((x, y), (grayscale_value, grayscale_value, grayscale_value, a))
    surface.unlock()
    return grayscale_surface


def load_sprite_sheet_single(
    path,
    sheet_name,
    count_x,
    count_y,
    size=1,
    flip_x=False,
    flip_y=False,
    read_axis='x'
):
    path = f'{path}\\{sheet_name}'
    sheet = pygame.image.load(path).convert_alpha()
    sprite_width = sheet.get_size()[0] // count_x
    sprite_height = sheet.get_size()[1] // count_y

    if type(size) in [float, int]:
        size = (sprite_width * size, sprite_height * size)

    sprites = []
    for i in range(count_x):
        for j in range(count_y):
            surface = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA, 32)
            if read_axis == 'x':
                rect = pygame.Rect(i * sprite_width, j * sprite_height, sprite_width, sprite_height)
            else:
                rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
            surface.blit(sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(surface, size))

    return [
        pygame.transform.flip(sprite, flip_x, flip_y)
        for sprite in sprites
        if sprite.get_bounding_rect()
    ]


def load_sprites_from_dir(path, size=1, flip_x=False, flip_y=False, prefix='', return_dict=False, grey=False):
    sprites = []
    files = []
    for file in os.listdir(path):
        if file.startswith(prefix):
            sprite = pygame.image.load(f'{path}\\{file}').convert_alpha()
            if type(size) in [float, int]:
                size = (sprite.get_size()[0] * size, sprite.get_size()[1] * size)
            sprites.append(pygame.transform.scale(sprite, size))
            files.append(file)

    if grey:
        sprites = [_grayscale(sprite) for sprite in sprites]

    if return_dict:
        return {
            files[i].split('.')[0]: pygame.transform.flip(sprite, flip_x, flip_y) for i, sprite in enumerate(sprites)
        }
    return [pygame.transform.flip(sprite, flip_x, flip_y) for sprite in sprites]
