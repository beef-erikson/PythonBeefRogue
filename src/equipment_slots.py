from enum import Enum

"""
    Defines which slots can be used for equipment - see also 'equippable' and 'equipment' in components
    Also edit the player in initialize_new_game if needed as well as game_map to drop in map.
    This is where we'd want to add for more slots (chest, rings etc)
"""


class EquipmentSlots(Enum):
    MAIN_HAND = 1
    OFF_HAND = 2
