# YARG (Yet Another Roguelike Game)

## Version 2019.0.3 (Still in development - missing enemy difficulty increase)
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