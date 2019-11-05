import tcod

"""
    Handles menus for the game
"""


# Creates menu and blits to the root console
def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options')

    # Calculate total height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Offscreen console that shows the menu
    window = tcod.console_new(width, height)

    # Print the head with auto-wrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # Print options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit contents of window to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)

    # If header is empty string, don't draw that line
    if header == '':
        tcod.console_blit(window, 0, 1, width, height, 0, x, y, 1.0, 0.5)
    else:
        tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.5)


# Inventory menu that lists each item as an option
def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]

    menu(con, header, options, inventory_width, screen_width, screen_height)


# Main menu (loads at start of game)
def main_menu(con, background_image, screen_width, screen_height):
    tcod.image_blit_2x(background_image, 0, 0, 0, 0, 0)

    tcod.console_set_default_foreground(0, tcod.yellow)
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, tcod.BKGND_NONE, tcod.CENTER,
                          '<Insert better title than BEEF ROGUE>')
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), tcod.BKGND_NONE, tcod.CENTER,
                          'Beef Erikson Studios - v2019.0.2')

    menu(con, '', ['New Game', 'Continue', 'Save and Quit'], 24, screen_width, screen_height)


# Empty message box menu item
def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
