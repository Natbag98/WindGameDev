

class Color:
    COLORS = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }

    def __init__(self, color, r=None, g=None, b=None, a=255):
        self.color = self.COLORS[color]

        if r:
            self.color[0] = r
        if g:
            self.color[1] = g
        if b:
            self.color[2] = b

        self.color = (self.color[0], self.color[1], self.color[2], a)
