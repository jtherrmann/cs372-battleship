NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'


class IllegalPositionError(Exception):
    pass


class ShipOutOfGridError(IllegalPositionError):
    pass


class Ship:
    def __init__(self, aft_location, direction, name):
        self._aft_location = aft_location
        self._direction = direction
        self._name = name
