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

        for coordinate in self._aft_location:
            if not 0 <= coordinate <= 9:
                raise ShipOutOfGridError()

        for coordinate in self.get_bow_location():
            if not 0 <= coordinate <= 9:
                raise ShipOutOfGridError()

    def get_bow_location(self):
        if self._direction == NORTH:
            return self._aft_location[0], self._aft_location[1] - self._length
        if self._direction == SOUTH:
            return self._aft_location[0], self._aft_location[1] + self._length
        if self._direction == EAST:
            return self._aft_location[0] + self._length, self._aft_location[1]
        if self._direction == WEST:
            return self._aft_location[0] - self._length, self._aft_location[1]
