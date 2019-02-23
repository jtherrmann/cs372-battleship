NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

SUBMARINE = 'Submarine'


# TODO: use static methods


class IllegalPositionError(Exception):
    pass


class ShipOffGridError(IllegalPositionError):
    pass


class ShipsOverlapError(IllegalPositionError):
    pass


class Grid:

    def __init__(self):
        self._ships = []

    def attack(self, x, y):
        pass

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


class Ship:

    _lengths = {SUBMARINE: 3}

    def __init__(self, aft_point, direction, name):
        self._aft_point = aft_point
        self._direction = direction
        self._name = name
        self._length = self._lengths[self._name]
        self._validate_location()

    def get_points(self):
        return (self._get_point(i) for i in range(self._length))

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
