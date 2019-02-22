NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

SUBMARINE = 'Submarine'


# TODO: use static methods


class IllegalPositionError(Exception):
    pass


class ShipOutOfGridError(IllegalPositionError):
    pass


class ShipsOverlapError(IllegalPositionError):
    pass


class Grid:

    def __init__(self):
        self._ships = []

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

    def __init__(self, aft_location, direction, name):
        self._aft_location = aft_location
        self._direction = direction
        self._name = name
        self._length = self._lengths[self._name]
        self._validate_coordinates()

    def get_points(self):
        if self._direction == NORTH:
            return (
                (self._aft_location[0], self._aft_location[1] - i)
                for i in range(self._length)
            )
        if self._direction == SOUTH:
            return (
                (self._aft_location[0], self._aft_location[1] + i)
                for i in range(self._length)
            )
        if self._direction == EAST:
            return (
                (self._aft_location[0] + i, self._aft_location[1])
                for i in range(self._length)
            )
        if self._direction == WEST:
            return (
                (self._aft_location[0] - i, self._aft_location[1])
                for i in range(self._length)
            )

    def _validate_coordinates(self):
        self._validate_coordinate_pair(self._aft_location)
        self._validate_coordinate_pair(self._get_bow_location())

    def _validate_coordinate_pair(self, pair):
        for coordinate in pair:
            if not 0 <= coordinate <= 9:
                raise ShipOutOfGridError()

    def _get_bow_location(self):
        if self._direction == NORTH:
            return self._aft_location[0], self._aft_location[1] - self._length
        if self._direction == SOUTH:
            return self._aft_location[0], self._aft_location[1] + self._length
        if self._direction == EAST:
            return self._aft_location[0] + self._length, self._aft_location[1]
        if self._direction == WEST:
            return self._aft_location[0] - self._length, self._aft_location[1]
