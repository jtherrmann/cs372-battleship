import unittest

from battleship import (
    NORTH, SOUTH, EAST, WEST, SUBMARINE, Ship, ShipOutOfGridError
)


class BattleshipTest(unittest.TestCase):

    def test_initial_configuration(self):
        aft_location = (3, 5)
        direction = EAST
        name = SUBMARINE
        ship = Ship(aft_location, direction, name)
        self.assertEqual(ship._aft_location, aft_location)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_aft_on_grid(self):
        with self.assertRaises(ShipOutOfGridError):
            Ship((-1, 5), WEST, SUBMARINE)

        with self.assertRaises(ShipOutOfGridError):
            Ship((12, 5), WEST, SUBMARINE)

        with self.assertRaises(ShipOutOfGridError):
            Ship((5, -3), WEST, SUBMARINE)

        with self.assertRaises(ShipOutOfGridError):
            Ship((5, 15), WEST, SUBMARINE)

    def test_bow_on_grid(self):
        with self.assertRaises(ShipOutOfGridError):
            Ship((0, 5), WEST, SUBMARINE)

        with self.assertRaises(ShipOutOfGridError):
            Ship((8, 1), EAST, SUBMARINE)

        with self.assertRaises(ShipOutOfGridError):
            Ship((3, 0), NORTH, SUBMARINE)

        with self.assertRaises(ShipOutOfGridError):
            Ship((3, 8), SOUTH, SUBMARINE)


if __name__ == '__main__':
    unittest.main()
