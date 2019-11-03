import tcod

from src.components.ai import ConfusedMonster
from src.game_messages import Message

"""
    Defines how each item is 'used' in the game
    1. Healing Potion (4 hp)
    2. Lightning Scroll (20 damage to nearest enemy)
    3. Fireball Scroll (12 damage to a targeted spot in a radius of 3 tiles)
    4. Confusion Scroll (confuses targeted enemy for 10 turns
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


# Scroll of lightning - hits closest enemy
def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message(
            'A lightning bolt strikes the {0} with a thunderous boom! {1} takes {2} damage.'.format(
                target.name, target.name, damage), tcod.dark_yellow)})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message(
            'No enemy is close enough to strike.', tcod.red)})

    return results


# Scroll of Fireball - hits a target enemy with a blast radius
def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target something outside your field of view',
                                                              tcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles.'.
                                                         format(radius), tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage),
                            tcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results


# TODO - Make number of turns of confusion a property of the scroll in the map placement, rather than here.
# Scroll of Confusion - targeted monster moves randomly (or not at all) for 10 turns
def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target something outside your field of view.',
                                                              tcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} glaze over, as it starts to '
                                                                 'stumble around'.format(entity.name),
                                                                 tcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.',
                                                              tcod.yellow)})
    return results
