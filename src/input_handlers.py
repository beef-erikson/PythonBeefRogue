import tcod

from src.game_states import GameStates

"""
    Handles keyboard functions and controls - both numpad and vim-like movement layouts
    Keys are handled via GameState
"""


# Returns functions of keys based on GameState
def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)

    # No key press
    return {}


# TODO Make inventory items mouse clickable
# Inventory keys (while in inventory)
def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # No key press
    return {}


# TODO Make level up menu mouse clickable
# Level up menu keys (when player levels)
def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    # No keys hit
    return {}


# Character screen keys, escape exits menu
def handle_character_screen(key):
    if key.vk == tcod.KEY_ESCAPE or chr(key.c) == 'c':
        return {'exit': True}

    # No key hit
    return {}


# TODO Make these mouse clickable
# Main menu keys
def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # No key press
    return {}


# Handles targeting keys
def handle_targeting_keys(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


# Handles game-play keys
def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # TODO - make moving mouse-based as well (i.e. clicking on tile moves you there)
    # Movement keys                                                                             # vim key layout
    if key.vk == tcod.KEY_UP or key_char == 'k' or key.vk == tcod.KEY_KP8:                      # yku
        return {'move': (0, -1)}                                                                # h l
    elif key.vk == tcod.KEY_DOWN or key_char == 'j'or key.vk == tcod.KEY_KP2:                   # bjn
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == 'h'or key.vk == tcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == 'l'or key.vk == tcod.KEY_KP6:
        return {'move': (1, 0)}
    elif key_char == 'y' or key.vk == tcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key_char == 'u' or key.vk == tcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key_char == 'b' or key.vk == tcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key_char == 'n' or key.vk == tcod.KEY_KP3:
        return {'move': (1, 1)}
    elif key_char == 'z' or key.vk == tcod.KEY_KP0:
        return {'wait': True}

    # Pick up items key
    if key_char == 'g':
        return {'pickup': True}

    # Display inventory
    elif key_char == 'i':
        return {'show_inventory': True}

    # Drops item from inventory
    elif key_char == 'd':
        return {'drop_inventory': True}

    # TODO Make player go back upstairs
    # Goes down stairs
    elif key.vk == tcod.KEY_ENTER or key.shift and key_char == '.':   # > key doesn't work, hack to make it work.
        return {'take_stairs_down': True}

    # Access character screen
    elif key_char == 'c':
        return {'show_character_screen': True}

    # Toggles fullscreen with alt+enter
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # Exits game
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # No key was pressed
    return {}


# Handles keys if player is dead
def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # No key was pressed
    return {}


# Handles mouse targeting
def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
