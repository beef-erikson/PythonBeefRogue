import tcod

from components.ai import BasicMonster
from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from render_functions import clear_all, render_all, RenderOrder
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

    # Monster variables
    max_monsters_per_room = 3

    # Dungeon colors
    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    game_title = 'BeefRogue 2019.0.1'

    # Load player
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component)
    entities = [player]

    # Sets font
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Sets window parameters
    tcod.console_init_root(screen_width, screen_height, game_title, False, tcod.RENDERER_OPENGL2, vsync=True)
    con = tcod.console_new(screen_width, screen_height)

    # Initializes game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player,
                      entities, max_monsters_per_room)

    # Field of view variables
    fov_recompute = True        # We only need to recompute when character moves
    fov_map = initialize_fov(game_map)

    # Variables for keyboard and mouse inputs
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Player goes first
    game_state = GameStates.PLAYERS_TURN

    # Main game loop
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        # Updates field of view if needed
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # Draws player and sets recompute to false until next player move
        render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        tcod.console_flush()

        # Updates spot last at with a blank (avoids multiple @'s)
        clear_all(con, entities)

        # Keyboard input
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        # List to hold for result of battles
        player_turn_results = []

        # Player turn
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        # Quit game on close
        if exit:
            return True

        # Toggles fullscreen
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # Iterates results of battle
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                print(message)

        # Enemies turn
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
