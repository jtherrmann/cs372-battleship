NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

SUBMARINE = 'Submarine'


class IllegalPositionError(Exception):
    pass


class ShipOutOfGridError(IllegalPositionError):
    pass


class Ship:

    _lengths = {SUBMARINE: 3}

    def __init__(self, aft_location, direction, name):
        self._aft_location = aft_location
        self._direction = direction
        self._name = name
        self._length = self._lengths[self._name]
        self._validate_coordinates()

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
