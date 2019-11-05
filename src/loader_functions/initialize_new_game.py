import tcod

from src.components.fighter import Fighter
from src.components.inventory import Inventory
from src.entity import Entity
from src.game_messages import MessageLog
from src.game_states import GameStates
from src.map_objects.game_map import GameMap
from src.render_functions import RenderOrder

"""
    Contains game variables and constants.
    These can be modified to change how the game functions.
"""


# Game Constants
def get_game_constants():
    # Screen variables
    screen_width = 80
    screen_height = 50

    # UI elements
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    # Message bar elements
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Map variables (7 free tiles at bottom for input / messaging)
    map_width = 80
    map_height = 43

    # Room variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Field of view variables
    fov_algorithm = 0           # TODO There are other algorithms as well, check them
    fov_light_walls = True
    fov_radius = 10

    # Monster and item variables
    max_monsters_per_room = 3
    max_items_per_room = 2

    # Dungeon colors
    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    game_title = 'BeefRogue 2019.0.2'

    constants = {
        'game_title': game_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants


# Game Variables
def get_game_variables(constants):
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities,
                      constants['max_monsters_per_room'], constants['max_items_per_room'])

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state

