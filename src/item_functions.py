import tcod

from src.game_messages import Message

"""
    Defines how each item is 'used' in the game
"""


# Heals player if not player is less than max hp
def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health.', tcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds are starting to heal!', tcod.green)})

    return results
