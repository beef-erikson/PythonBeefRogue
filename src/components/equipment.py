from src.equipment_slots import EquipmentSlots

"""
    Equipment details
    Properties of each stat are set here as well as toggle equip command
    Edit equipment, equippable, inventory components as well as equipment_slots and engine in src.
    Also edit the player in initialize_new_game if needed.
"""


class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    @property
    def max_hp_bonus(self):
        bonus = 0

        # Main hand HP bonus
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        # Off hand HP bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        # Main hand power bonus
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        # Off hand power bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        # Main hand defense bonus
        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        # Off hand defense bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    # Toggles equipment wielding/wearing
    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        # Main Hand
        if slot == EquipmentSlots.MAIN_HAND:
            # Dequipps item from main hand
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})

            # Equips main hand, switching out old item if present
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': self.main_hand})

        # Off Hand
        elif slot == EquipmentSlots.OFF_HAND:
            # Dequipps item from off hand
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})

            # Equips off hand, switching out old item if present
            else:
                if self.off_hand == equippable_entity:
                    results.append({'dequipped': equippable_entity})

                self.off_hand = equippable_entity
                results.append({'dequipped': equippable_entity})

        return results
