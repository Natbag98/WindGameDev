import random


class Color:
    COLORS = {
        'deep_ocean': [(29, 162, 216)],
        'ocean': [(127, 205, 255)],
        'sand': [
            (246, 215, 176),
            (242, 210, 169),
            (236, 204, 162),
            (231, 196, 150),
            (225, 191, 146)
        ],
        'swamp': [
            (85, 92, 69),
            (130, 140, 81),
            (166, 185, 111)
        ],
        'mountain': [(170, 170, 170)],
        'plains': [
            (19, 109, 21),
            (17, 124, 19),
            (19, 133, 16),
            (38, 139, 7),
            (65, 152, 10)
        ],
        'forest': [
            (74, 103, 65),
            (63, 90, 54),
            (55, 79, 47),
            (48, 69, 41),
            (34, 49, 29)
        ],

        'grey': (128, 128, 128),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }

    def __init__(self, color, r=None, g=None, b=None, a=255, random_=False):
        if random_:
            self.color = random.choice(self.COLORS[color])
        else:
            self.color = self.COLORS[color]

        if r:
            self.color[0] = r
        if g:
            self.color[1] = g
        if b:
            self.color[2] = b

        self.color = (self.color[0], self.color[1], self.color[2], a)
