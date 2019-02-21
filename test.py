import unittest

from battleship import (
    NORTH, SOUTH, EAST, WEST, SUBMARINE, Grid, Ship, ShipOutOfGridError,
    ShipsOverlapError
)

# TODO: fix names


class GridTestCase(unittest.TestCase):

    def test_create_grid(self):
        grid = Grid()
        self.assertEqual(grid._ships, [])

    def test_add_ships(self):
        grid = Grid()
        ships = [
            Ship((0, 0), EAST, SUBMARINE),
            Ship((5, 5), WEST, SUBMARINE),
            Ship((9, 9), WEST, SUBMARINE)
        ]
        grid.add_ship(ships[0])
        self.assertEqual(grid._ships, [ships[0]])
        grid.add_ship(ships[1])
        self.assertEqual(grid._ships, [ships[0], ships[1]])
        grid.add_ship(ships[2])
        self.assertEqual(grid._ships, [ships[0], ships[1], ships[2]])

    def test_no_ships_overlap(self):
        grid = Grid()
        grid.add_ship(Ship((2, 5), EAST, SUBMARINE))

        with self.assertRaises(ShipsOverlapError):
            grid.add_ship(Ship((0, 5), EAST, SUBMARINE))

        with self.assertRaises(ShipsOverlapError):
            grid.add_ship(Ship((4, 5), WEST, SUBMARINE))

        with self.assertRaises(ShipsOverlapError):
            grid.add_ship(Ship((2, 7), NORTH, SUBMARINE))

        with self.assertRaises(ShipsOverlapError):
            grid.add_ship(Ship((2, 3), SOUTH, SUBMARINE))


class ShipTestCase(unittest.TestCase):

    def test_create_ship(self):
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

    def test_get_bow_location(self):
        self.assertEqual(
            Ship((0, 5), NORTH, SUBMARINE)._get_bow_location(), (0, 2)
        )
        self.assertEqual(
            Ship((0, 5), SOUTH, SUBMARINE)._get_bow_location(), (0, 8)
        )
        self.assertEqual(
            Ship((5, 0), EAST, SUBMARINE)._get_bow_location(), (8, 0)
        )
        self.assertEqual(
            Ship((5, 0), WEST, SUBMARINE)._get_bow_location(), (2, 0)
        )


if __name__ == '__main__':
    unittest.main()
