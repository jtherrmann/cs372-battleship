from collections import namedtuple


NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

CARRIER = 'Carrier'
BATTLESHIP = 'Battleship'
CRUISER = 'Cruiser'
SUBMARINE = 'Submarine'
DESTROYER = 'Destroyer'


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
        peg = Peg(
            x, y, any(ship.is_hit(x, y) for ship in self._ships)
        )
        self._pegs.append(peg)
        # TODO: return value never used?
        return peg.is_hit

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

    def __init__(self, aft_point, direction, name):
        self._aft_point = aft_point
        self._direction = direction
        self._name = name
        self._length = self._lengths[self._name]
        self._hit_points = self._length
        self._validate_location()

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
        self._validate_point(self._aft_point)
        self._validate_point(self._get_bow_point())

    def _validate_point(self, pair):
        for coordinate in pair:
            if not 0 <= coordinate <= 9:
                raise ShipOffGridError()

    def _get_bow_point(self):
        return self._get_point(self._length)

    def _get_point(self, offset):
        if self._direction == NORTH:
            return self._aft_point[0], self._aft_point[1] - offset
        if self._direction == SOUTH:
            return self._aft_point[0], self._aft_point[1] + offset
        if self._direction == EAST:
            return self._aft_point[0] + offset, self._aft_point[1]
        if self._direction == WEST:
            return self._aft_point[0] - offset, self._aft_point[1]


def main():
    # TODO: clear screen and prompt players to switch spots where appropriate
    grid1, grid2 = Grid(), Grid()
    configure_ships(grid1)
    configure_ships(grid2)
    while True:
        if take_turn(grid1, grid2):
            break
        if take_turn(grid2, grid1):
            break


def configure_ships(grid):
    all_ships = parse_all_ships(input('TODO'))
    for ship in all_ships:
        grid.add_ship(ship)


def take_turn(attacking_grid, defending_grid):
    print(defending_grid.get_partial_view())
    print(attacking_grid.get_full_view())
    attack_point = parse_point(input('TODO'))
    defending_grid.attack(attack_point)
    return defending_grid.is_dead()


if __name__ == '__main__':
    main()
