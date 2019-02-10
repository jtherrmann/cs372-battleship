# CS 372 Battleship

## Initial requirements

User stories, from highest to lowest priority:

- As a player, I want the ability to choose an initial configuration for my
  ships.
  - The computer should automatically restrict me to legal configurations, e.g.
    no diagonal placement, no overlapping ships, etc.
- As a player, I want the full range of ship sizes.
  - Destroyer - 2 holes
  - Submarine - 3 holes
  - Cruiser - 3 holes
  - Battleship - 4 holes
  - Carrier - 5 holes
- As a player, I want the ability to choose where to attack on the board.
  - I should automatically see whether it was a hit or a miss and the computer
    should store this information for later reference.
- As a player, I want to be able to check the current status of the game.
  - I should be able to see my own ship configuration and the hits and misses
    that have been made on my grid, but I should only be able to see the hits
    and misses that have been made on my opponent’s grid (but not their ship
    configuration).
- As a player, I want ships to be sunk when appropriate.
  - Ships should sink when all of their holes have been hit.
- As a player, I want to win or lose when appropriate.
  - A player should lose when all of their ships have been sunk.
- As a player, I want the ability to play against another human player.
  - As players / project owners we would eventually like to be able to play
    against a remote opponent, preferably over an internet connection. As
    developers, we respond that it would be easier to allow two players to play
    against each other on the same computer, at least initially. As players /
    project owners we respond that this would be an acceptable first version.
- As a player, I would eventually like a GUI.
  - As players / project owners we are more interested in seeing a fully
    functioning battleship game with a simple text interface before seeing any
    sort of GUI. As developers we respond that it would be convenient to
    implement a GUI when we implement networked multiplayer, because we could
    convert the game to a web app. As players / project owners, we like this
    idea.
- As a player, I want the ability to play against the computer.
  - Players / project owners and developers agree this can be a low-priority,
    long-term goal. The developers do not know much about AI anyway.
- As a player, I want to play in fully 3-D virtual reality.
  - All involved parties agree this can be a very low-priority goal for the
    very distant future.