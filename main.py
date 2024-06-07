import pygame
import moderngl


class App:

    def __init__(self):
        self.text = 'Hello World'

    def run(self):
        print(self.text)


if __name__ == '__main__':
    app = App()
    app.run()
