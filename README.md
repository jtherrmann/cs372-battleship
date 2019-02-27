# CS 372 Battleship

## User stories

User stories, from highest to lowest priority:

(Rankings are on the 1, 2, 4, 8 hr. scale.)

### Done

- As a player, I want to choose an initial configuration for my ships.
  - 1 hr.
  - The computer should automatically restrict me to legal configurations, e.g.
    no diagonal placement, no overlapping ships, etc.
- As a player, I want the full range of ship sizes.
  - 1 hr.
  - Destroyer - 2 holes
  - Submarine - 3 holes
  - Cruiser - 3 holes
  - Battleship - 4 holes
  - Carrier - 5 holes
- As a player, I want to choose where to attack on the board.
  - 1 hr.
  - I should automatically see whether it was a hit or a miss and the computer
    should store this information for later reference.
- As a player, I want ships to be sunk when appropriate.
  - 1 hr.
  - Ships should sink when all of their holes have been hit.
- As a player, I want to win or lose when appropriate.
  - 1 hr.
  - A player should lose when all of their ships have been sunk.
- As a player, I want to check the current status of the game.
  - 1 hr.
  - I should be able to see my own ship configuration and the hits that have
    been made on my grid, and the hits and misses that have been made on my
    opponent’s grid (but not their ship configuration).
- As a player, I want a text-based interface in order to test these features.
  - ~~1 hr.~~ 4 hr.
  - As players / project owners, we are most interested in seeing a working
    implementation of the game logic, even if it has no user interface and can
    only be confirmed to work using automated tests. However, we would
    eventually like a simple textual interface with which to test the features
    interactively.
- As a player, I want to play against another player on a single computer.
  - 1 hr.
  - As an extension of the text-based interface idea, we also want to be able
    to take turns at the keyboard in order to play against another human (or
    just play against ourselves).

### TODO

- As a player, I would like to see better error handling.
  - 2 hr.
  - As players / project owners we would like to see improvements to the
    textual interface's current error handling abilities. Rather than simply
    abort when the game identifies an error in the user's input, the interface
    should notify the user with a descriptive message and allow the user to
    re-enter the input.
  - We would also like the game to do its best to detect bugs (including
    uncaught exceptions) and allow the user to send bug reports to the
    developers.
  - As developers, we like these ideas because they will make the game easier
    to test and debug. We believe this user story will be fairly
    straightforward to implement.
- As a player, I want to play against a remote opponent.
  - 8 hr.
  - As players / project owners we would eventually like to be able to play
    against a remote opponent, preferably over an internet connection. This is
    important because it allows us to play against friends at any time and
    because it makes it easier to avoid seeing your opponent's view of the game
    (which will be a limitation of using a single computer).
- As a player, I would eventually like a GUI.
  - 8 hr.
  - As players / project owners we are more interested in seeing a fully
    functioning battleship game with a simple text interface before seeing any
    sort of GUI. As developers we respond that it would be convenient to
    implement a GUI when we implement networked multiplayer, because we could
    convert the game to a web app. As players / project owners, we like this
    idea.
- As a player, I want to play against the computer.
  - Unknown difficulty; probably days or months.
  - Players / project owners and developers agree this can be a low-priority,
    long-term goal. The developers do not know much about AI anyway.
- As a player, I want to play in fully 3-D virtual reality.
  - Unknown difficulty; probably months or years.
  - All involved parties agree this can be a very low-priority goal for the
    very distant future.

## Initial design

First we will write classes and functions to implement the core game logic.
Assuming an object-oriented design, the game components could be separated into
objects such as grids and ships. For example, a ship object could store a data
member representing the ship's number of holes (2, 3, 4, or 5) and another data
member representing the ship's name (Destroyer, Submarine, Cruiser, Battleship,
or Carrier). However, the game may be simple enough that we don't need a fully
object-oriented design.

Players need to be able to check the status of the game, which means they need
to see the state of each grid. But each grid should have a "full" view and a
"partial" view, where the full view presents the locations of hits, misses, and
ships, and can only be seen by the player to which the grid belongs, while the
partial view presents only hits and misses and can be seen by the opponent.
Perhaps each grid object will have a member function for retrieving a full view
and another member function for retrieving a partial view.

At first we will just write unit tests for each function in order to test the
game, but given enough time we will also implement a simple text-based
interface so that two people can play a game on a single computer (or the same
person can play against themselves). If we complete all of the above items, we
will start thinking about how to convert the game into a web app with a GUI and
multiplayer capabilities.