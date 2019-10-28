import tcod


def handle_keys(key):
    # Movement keys
    if key.vk == tcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT:
        return {'move': (1, 0)}

    # Toggles fullscreen with alt+enter
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # Exits game
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # No key was pressed
    return {}