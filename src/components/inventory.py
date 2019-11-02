import tcod

from src.game_messages import Message

"""
    Handles player inventory
    Capacity - number of items player can carry
    Items - items in the inventory
"""


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    # Adds item to the player's inventory if not full
    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', tcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0} and place it in your inventory'.format(item.name),
                                   tcod.blue)
            })

            self.items.append(item)

        return results
