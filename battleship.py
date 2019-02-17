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
