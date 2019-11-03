import math
import tcod

from src.render_functions import RenderOrder

"""
A generic object to represent players, enemies, items, etc.
"""


class Entity:
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    # Move the entity by a given amount
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    # Moves the entity towards a target
    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    # Get distance between a entity and the player
    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    # Moves using the A* algorithm
    # noinspection DuplicatedCode
    def move_astar(self, target, entities, game_map):
        # Create a field of view map that has all dimensions of map
        fov = tcod.map_new(game_map.width, game_map.height)

        # Scans current map each turn and sets walls as un-walkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                        not game_map.tiles[x1][y1].blocked)

        # Scan all objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so start and end points are free)
        # The AI class handles it if self is next to target so it will not use this function anyhow
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as if it was a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set to 0.0 if diagonals are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coords and the target's coords
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also that the path is shorter than 25 tiles
        # This path size matters if you want monster to use alternative longer paths (for example through other rooms)
        # if for example, the player is in a corridor.
        # It makes sense to keep path size relatively low to keep monsters from running around the map if there's an
        # alternate path really far away.
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coords in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coords to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep old move function as a back so that if there are no paths (i.e. another monster blocks a corridor).
            # It will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete path to free memory
            tcod.path_delete(my_path)

    # Finds distance to target
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


# Checks is space to move is a blocking entity
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
