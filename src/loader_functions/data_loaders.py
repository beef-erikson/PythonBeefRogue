import os
import shelve

"""
    Handles the saving and loading of game
"""

# TODO have it so when game is closed by clicking 'X', it will save the game


# Saves game to savegame.dat
def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open('sav/savegame', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state


# Loads game from savegame.dat if present
def load_game():
    if not os.path.isfile('sav/savegame.dat'):
        raise FileNotFoundError

    with shelve.open('sav/savegame', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state
