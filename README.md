# YARG (Yet Another Roguelike Game)

![YARG](https://i.imgur.com/LWV2Oa7.png)

## Version 2019.0.4


## Version 2019.0.3 (November 7, 2019)
### Additions
- Stairs/Floors added; can now travel further down the dungeon.
  - Stairs will stay on screen, regardless if in field of view, once discovered.
  - Going down a level will restore half of the player's max health.
  - Current dungeon level can be seen below the player's HP bar.
- "Wait" key added for waiting a turn (numpad 0 or 'z')
- Experience system implemented.
- Leveling up implemented.
  - Each level will take level * 150 + 300 to gain the next level.
- Menu created to handle when a player levels up.
  - Players will have a choice of raising either HP, attack, or defense.
- Character screen created.
  - Displays various characters stats.
  - Accessible via the 'c' key.
### Modifications
- Item drops and enemy spawning significantly changed.
  - Each item/Creature now has a 'weight' which determines the likelihood of it being picked.
  - When deciding what to spawn, the choices and weights are passed to a function and returns a random selection.
  - This is more scalable than my previous system and will take all future additions into consideration.
  - Implementation of the random functions can be seen [here](https://github.com/beef-erikson/PythonBeefRogue/blob/master/src/random_utils.py).
  - The weights of both enemies and items change the further down the dungeon a player goes. See [here](https://github.com/beef-erikson/PythonBeefRogue/blob/master/src/map_objects/game_map.py).
- Stat changes to player and monsters
  - Player initial starting stats have been nerfed but starts with 100 HP.
  - Orc now has twice the starting HP and 1 more power.
  - Troll now has 30 HP (from 16), 1 more defense and double the power.
- Item changes
  - Healing potions now heal for 40 HP.
  - Fireball scroll now deal 25 damage instead of 12 (radius of 3 from targeted area).
  - Lightning scroll now deals 40 damage instead of 20.
### Bug Fixes
- Fullscreen mode now works as intended rather than try to go down stairs.
- Fullscreen will now work from main menu as originally intended

## Version 2019.0.2 (November 5, 2019)
- Menu added, both at start and by hitting escape.
- Several items are now implemented.
   - Healing Potion, restores 4 HP.
   - Scroll of lightning, deals 20 damage to closest enemy.
   - Scroll of fireball, deals 12 damage to target area with a blast radius of 3 tiles.
   - Scroll of Confusion, makes target enemy move randomly (or not move at all) for 10 turns.
- Inventory system complete. Can now use / drop items.
- Saving and loading implemented.
- Autosave on exit implemented.
- Field of view implemented.
- A* pathfinding used for enemy AI paths.
- GUI added with messaging and health display.
- Mouseover on targets displays what it is.

## Version 2019.0.1 (October 28th, 2019)
- Procedural generation of dungeon complete.
- Enemies and Player added.
- Basic combat system implemented.