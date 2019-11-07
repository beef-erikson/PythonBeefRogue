import tcod
from random import randint

from src.components.ai import BasicMonster
from src.components.fighter import Fighter
from src.components.item import Item
from src.entity import Entity
from src.game_messages import Message
from src.item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from src.map_objects.stairs import Stairs
from src.random_utils import from_dungeon_level, random_choice_from_dict
from src.render_functions import RenderOrder
from src.map_objects.tile import Tile
from src.map_objects.rectangle import Rectangle

"""
    Handles functions related to creating the game map.
    This includes monster and item spawning.
"""


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    # Initializes the dungeon
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    # Populates map
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

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

                    # Used for placement of stairs
                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

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
                self.place_entities(new_room, entities)

                # Append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        # Creates stairs to go down to next level
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', tcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

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
    def place_entities(self, room, entities):
        # Bases number of monsters and item to which level of dungeon the player is on
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        # Monster chances to spawn - trolls will have more weight the further down the floors a player goes
        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }

        # Item chances to drop - item weight changes based on the dungeon level with less healing potions spawning
        item_chances = {
            'healing_potion': 35,
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        # Spawns monsters
        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # TODO - add more monsters as you go further down in levels
            # Checks if location to place monster is empty
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # Used to determine which monster to spawn
                monster_choice = random_choice_from_dict(monster_chances)
                # Orc
                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                # Troll
                else:
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)

        # Spawns items
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # Used to determine what item to spawn
                item_choice = random_choice_from_dict(item_chances)

                # Healing potion - heals 4 damage
                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', tcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)

                # Fireball scroll - deals 12 damage to all enemies in a radius of 3 tiles
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', tcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '#', tcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                # Confuse scroll - confuses enemy for 10 turns
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel', tcod.light_cyan))
                    item = Entity(x, y, '#', tcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                # Lightning scroll - deals 20 damage to nearest enemy
                else:
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '#', tcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    # Checks is tile is able to be walked through
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    # TODO Add in going up a floor
    # Goes down a floor in the dungeon, creating a new floor
    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        # Creates a new map
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        # TODO note when we add stairs back up, we need to make sure that player doesn't gain health again going down
        # Gives player half of their max hp back
        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(Message('You take a moment to rest heading down the stairs, restoring some health',
                                        tcod.violet))

        return entities
