import tcod
from random import randint

from src.components.ai import BasicMonster
from src.components.fighter import Fighter
from src.components.item import Item
from src.entity import Entity
from src.render_functions import RenderOrder
from src.map_objects.tile import Tile
from src.map_objects.rectangle import Rectangle

"""
    Handles functions related to creating the game map.
    This includes monster and item spawning.
"""


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    # Initializes the dungeon
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    # Populates map
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player,
                 entities, max_monsters_per_room, max_items_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # Random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # Random position while staying in boundaries of map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Creates room and checks for intersections
            new_room = Rectangle(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # Valid room with no intersections, create room
                self.create_room(new_room)

                # Center coords of new room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # First room, place player here
                    player.x = new_x
                    player.y = new_y
                else:
                    # All other rooms will connect to previous room with a tunnel

                    # Center coords of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Flip coin
                    if randint(0, 1) == 1:
                        # First move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # First move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # Place monsters and items
                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

                # Append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    # Creates a room
    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    # Creates horizontal tunnel
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    # Creates a vertical tunnel
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    # Places a random number of monsters and items in rooms
    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        # Spawns monsters
        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Checks if location to place monster is empty
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)

        # Spawns items
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_component = Item()
                item = Entity(x, y, '!', tcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                              item=item_component)

                entities.append(item)

    # Checks is tile is able to be walked through
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
