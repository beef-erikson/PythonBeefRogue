from enum import Enum

"""
    Defines which slots can be used for equipment - see also 'equippable' and 'equipment' in components
    This is where we'd want to add for more slots (chest, rings etc)
"""


class EquipmentSlots(Enum):
    MAIN_HAND = 1
    OFF_HAND = 2
