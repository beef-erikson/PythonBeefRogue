import tcod


# Draws all entities and game map
def render_all(con, entities, game_map, screen_width, screen_height, colors):
    # Draw game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                tcod.console_set_char_background(con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)

    # Draw entities
    for entity in entities:
        draw_entity(con, entity)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


# Runs clear_entity on all entities
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


# Draws the entity with its properties
def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


# Erase the character (avoids multiples of character)
def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
