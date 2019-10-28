import tcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from render_functions import clear_all, render_all
from src.map_objects.game_map import GameMap


def main():
    # Screen variables
    screen_width = 80
    screen_height = 50

    # Map variables (5 free pixels at bottom for input)
    map_width = 80
    map_height = 45

    # Room variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Field of view variables
    fov_algorithm = 0           # TODO There are other algorithms as well, check them
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    game_title = 'BeefRogue 2019.0.1'

    # Load entities
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.yellow)
    entities = [npc, player]

    # Sets font
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Sets window parameters
    tcod.console_init_root(screen_width, screen_height, game_title, False, tcod.RENDERER_OPENGL2, vsync=True)
    con = tcod.console_new(screen_width, screen_height)

    # Initializes game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # Field of view variables
    fov_recompute = True        # We only need to recompute when character moves
    fov_map = initialize_fov(game_map)

    # Variables for keyboard and mouse inputs
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Main game loop
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        # Updates field of view if needed
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # Draws player and sets recompute to false until next player move
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        tcod.console_flush()

        # Updates spot last at with a blank (avoids multiple @'s)
        clear_all(con, entities)

        # Keyboard input
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
