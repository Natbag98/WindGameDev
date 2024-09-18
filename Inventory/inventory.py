from main import Game


class Inventory:
    HAND_INDEX = 12

    def __init__(self, game, player):
        self.game = game
        self.player = player

        self.hand_item = None

        self.items = [None for _ in range(Game.PLAYER_INVENTORY_SIZE)]

        from Inventory.items import Campfire
        self.items[0] = Campfire(game)

    def place_in_hand(self, item_name):
        item = self.get_item(item_name)
        if item:
            self.remove_item(item_name)

            if self.hand_item:
                self.add_item(self.hand_item)

            self.hand_item = item

    # noinspection PyUnresolvedReferences
    def get_item(self, item_name):
        for item in self.items:
            if item.__class__.__name__ == item_name:
                return item
        return False

    def add_item(self, item_to_add):
        for i, item in enumerate(self.items):
            if not item:
                self.items[i] = item_to_add
                break

    # noinspection PyUnresolvedReferences
    def remove_item(self, remove_item_name, quantity=1):
        """
        Returns true if the item was removed successfully
        Returns False if the item was not found
        """

        if self.has_item(remove_item_name, quantity):
            for _ in range(quantity):
                for i, item in enumerate(self.items):
                    if item.__class__.__name__ == remove_item_name:
                        self.items[i] = None
                        break
            return True
        return False

    # noinspection PyUnresolvedReferences
    def has_item(self, check_item_name, quantity=1):
        count = 0
        for item in self.items:
            if item.__class__.__name__ == check_item_name:
                count += 1
        return count >= quantity
