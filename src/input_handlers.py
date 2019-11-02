import tcod

"""
    Handles keyboard functions and controls - both numpad and vim-like movement layouts
"""


def handle_keys(key):
    key_char = chr(key.c)

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

    # Pick up items key
    if key_char == 'g':
        return {'pickup': True}

    # Toggles fullscreen with alt+enter
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # Exits game
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # No key was pressed
    return {}