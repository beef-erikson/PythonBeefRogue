import tcod
from input_handlers import handle_keys


def main():
    screen_width = 80
    screen_height = 50
    game_title = 'BeefRogue 2019.0.1'

    # Starting player position
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # Sets font
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Sets window parameters
    tcod.console_init_root(screen_width, screen_height, game_title, False, tcod.RENDERER_OPENGL2, vsync=True)

    # TODO fix depreciation - check tcod.console.Console(...)
    con = tcod.console_new(screen_width, screen_height)

    # Variables for keyboard and mouse inputs
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Main game loop
    # TODO fix depreciation - use the event system.
    #  See: https://buildmedia.readthedocs.org/media/pdf/python-tcod/latest/python-tcod.pdf page 33
    while not tcod.console_is_window_closed():
        # TODO fix depreciation - tcod.event.get to check events
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        # Draws player
        # TODO fix depreciation - set con.default_fg attribute instead
        tcod.console_set_default_foreground(con, tcod.white)
        tcod.console_put_char(con, player_x, player_y, '@', tcod.BKGND_NONE)
        # TODO fix depreciation - apparently it's now Console.blit?
        tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        tcod.console_flush()

        # Updates spot last at with a blank (avoids multiple @'s)
        tcod.console_put_char(con, player_x, player_y, ' ', tcod.BKGND_NONE)

        # Keyboard input
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
