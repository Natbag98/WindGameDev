from main import Game


class Inventory:

    def __init__(self, game, player):
        self.game = game
        self.player = player

        self.items = [None for _ in range(Game.PLAYER_INVENTORY_SIZE)]

    def add_item(self, item_to_add):
        for i, item in enumerate(self.items):
            if not item:
                self.items[i] = item_to_add
                break
