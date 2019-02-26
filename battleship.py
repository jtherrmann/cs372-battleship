import sys
from collections import namedtuple


NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

CARRIER = 'carrier'
BATTLESHIP = 'battleship'
CRUISER = 'cruiser'
SUBMARINE = 'submarine'
DESTROYER = 'destroyer'
SHIP_NAMES = (CARRIER, BATTLESHIP, CRUISER, SUBMARINE, DESTROYER)


# TODO:
# - use static methods
# - use namedtuples for points


class IllegalPositionError(Exception):
    pass


class ShipOffGridError(IllegalPositionError):
    pass


class ShipsOverlapError(IllegalPositionError):
    pass


Peg = namedtuple('Peg', ('x', 'y', 'is_hit'))


class Grid:

    def __init__(self):
        self._ships = []
        self._pegs = []

    def get_full_view(self):
        return self._get_view(True)

    def get_partial_view(self):
        return self._get_view(False)

    def is_dead(self):
        return all(ship.is_sunk() for ship in self._ships)

    def attack(self, x, y):
        for ship in self._ships:
            if ship.is_hit(x, y):
                self._pegs.append(Peg(x, y, True))
                return True, ship.get_name()
        self._pegs.append(Peg(x, y, False))
        return False

    def add_ship(self, new_ship):
        self._validate_ship(new_ship)
        self._ships.append(new_ship)

    def _validate_ship(self, new_ship):
        for ship in self._ships:
            if self._ships_intersect(ship, new_ship):
                raise ShipsOverlapError

    def _ships_intersect(self, ship1, ship2):
        for point in ship1.get_points():
            if point in ship2.get_points():
                return True
        return False

    def _get_view(self, full_view):
        lines = (self._get_line(row, full_view) for row in range(10))
        return '  1 2 3 4 5 6 7 8 9 10\n' + ''.join(lines)

    def _get_line(self, row, full_view):
        letter = 'ABCDEFGHIJ'[row]
        cells = ' '.join(
            self._get_cell(row, col, full_view) for col in range(10)
        )
        return '{} {} \n'.format(letter, cells)

    def _get_cell(self, row, col, full_view):
        x, y = col, row
        peg = self._get_peg(x, y)
        if peg is not None:
            return 'x' if peg.is_hit else 'o'
        # TODO: we shouldn't have to check full_view for each cell
        return '#' if full_view and self._point_on_ship(x, y) else '.'

    def _get_peg(self, x, y):
        for peg in self._pegs:
            if (x, y) == (peg.x, peg.y):
                return peg
        return None

    def _point_on_ship(self, x, y):
        return any((x, y) in ship.get_points() for ship in self._ships)


class Ship:

    _lengths = {
        CARRIER: 5,
        BATTLESHIP: 4,
        CRUISER: 3,
        SUBMARINE: 3,
        DESTROYER: 2
    }

    def __init__(self, stern_point, direction, name):
        self._stern_point = stern_point
        self._direction = direction
        self._name = name
        self._length = self._lengths[self._name]
        self._hit_points = self._length
        self._validate_location()

    def __eq__(self, other):
        equal = (
            self._stern_point == other._stern_point
            and self._direction == other._direction
            and self._name == other._name
            and self._hit_points == other._hit_points
        )
        if equal:
            assert self._length == other._length
        return equal

    def get_name(self):
        return self._name

    def get_points(self):
        return (self._get_point(i) for i in range(self._length))

    def is_hit(self, x, y):
        hit = (x, y) in self.get_points()
        if hit:
            assert self._hit_points > 0
            self._hit_points -= 1
        return hit

    def is_sunk(self):
        return self._hit_points == 0

    def _validate_location(self):
        self._validate_point(self._stern_point)
        self._validate_point(self._get_bow_point())

    def _validate_point(self, pair):
        for coordinate in pair:
            if not 0 <= coordinate <= 9:
                raise ShipOffGridError()

    def _get_bow_point(self):
        return self._get_point(self._length - 1)

    def _get_point(self, offset):
        if self._direction == NORTH:
            return self._stern_point[0], self._stern_point[1] - offset
        if self._direction == SOUTH:
            return self._stern_point[0], self._stern_point[1] + offset
        if self._direction == EAST:
            return self._stern_point[0] + offset, self._stern_point[1]
        if self._direction == WEST:
            return self._stern_point[0] - offset, self._stern_point[1]


def main():
    # TODO:
    # - error handling
    # - test playing a game all the way through
    display_welcome()
    player1_name, player2_name = 'Player 1', 'Player 2'
    grid1, grid2 = Grid(), Grid()
    configure_ships(grid1, player1_name)
    configure_ships(grid2, player2_name)
    while True:
        if take_turn(grid1, grid2, player1_name):
            break
        if take_turn(grid2, grid1, player2_name):
            break


def display_welcome():
    clear_on_enter('Welcome to Battleship!')


def switch_players():
    clear_on_enter('Please switch players.')


def clear_on_enter(msg):
    clear_screen()
    print('{} Press Enter to continue.'.format(msg))
    input()
    clear_screen()


def clear_screen():
    # TODO: does this method work on any POSIX system? (os.name == 'posix')
    if sys.platform == 'linux':
        print('\033c')
    else:
        print('\nWarning: cannot clear screen on non-Linux platforms.\n\n')


def configure_ships(grid, player_name):
    print(
        "A ship configuration is a comma-separated list of five ships, where\n"
        "each ship is represented by the location of its stern and the\n"
        "cardinal direction in which the ship points. Ships are given in the\n"
        "following order:\n\n{}, {}, {}, {}, {}\n\n"
        "The following is a valid ship configuration:\n\n"
        "A3 E, B1 S, C10 W, I2 N, J8 N\n".format(*SHIP_NAMES)
    )
    all_ships = parse_all_ships(
        input('Ship configuration for {}:\n> '.format(player_name))
    )
    for ship in all_ships:
        grid.add_ship(ship)
    clear_screen()


def parse_all_ships(inpt):
    points_and_directions = inpt.split(',')
    assert len(points_and_directions) == len(SHIP_NAMES)
    return tuple(
        parse_ship(point_and_direction, ship_name)
        for point_and_direction, ship_name in
        zip(points_and_directions, SHIP_NAMES)
    )


def parse_ship(point_and_direction, ship_name):
    values = point_and_direction.split()
    assert len(values) == 2
    point = parse_point(values[0])
    direction = values[1].upper()
    assert direction in (NORTH, SOUTH, EAST, WEST)
    return Ship(point, direction, ship_name)


def take_turn(attacking_grid, defending_grid, attacking_player_name):
    print('Your move, {}.\n'.format(attacking_player_name))
    print(defending_grid.get_partial_view())
    print(attacking_grid.get_full_view())
    x, y = parse_point(input('Attack: '))
    defending_grid.attack(x, y)
    # TODO: print whether hit or miss
    # TODO: print which ship was hit
    defender_dead = defending_grid.is_dead()
    if defender_dead:
        print('{} has won!'.format(attacking_player_name))
    else:
        switch_players()
    return defender_dead


def parse_point(inpt):
    row_letter = inpt[0].upper()
    y = ord(row_letter) - 65
    assert 0 <= y <= 9

    col_number = inpt[1:]
    x = int(col_number) - 1
    assert 0 <= x <= 9

    return x, y


if __name__ == '__main__':
    main()
