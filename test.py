import unittest

from battleship import (
    NORTH, SOUTH, EAST, WEST, SUBMARINE, Grid, Ship, ShipOffGridError,
    ShipsOverlapError
)


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

    def test_attack(self):
        grid = Grid()
        grid.add_ship(Ship((0, 0), EAST, SUBMARINE))

        self.assertEqual(grid.attack(0, 0), True)
        self.assertEqual(grid.attack(1, 0), True)
        self.assertEqual(grid.attack(2, 0), True)
        self.assertEqual(grid.attack(3, 0), False)
        self.assertEqual(grid.attack(0, 1), False)


class ShipTestCase(unittest.TestCase):

    def test_create_ship(self):
        aft_point = (3, 5)
        direction = EAST
        name = SUBMARINE
        ship = Ship(aft_point, direction, name)
        self.assertEqual(ship._aft_point, aft_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_aft_on_grid(self):
        with self.assertRaises(ShipOffGridError):
            Ship((-1, 5), WEST, SUBMARINE)

        with self.assertRaises(ShipOffGridError):
            Ship((12, 5), WEST, SUBMARINE)

        with self.assertRaises(ShipOffGridError):
            Ship((5, -3), WEST, SUBMARINE)

        with self.assertRaises(ShipOffGridError):
            Ship((5, 15), WEST, SUBMARINE)

    def test_bow_on_grid(self):
        with self.assertRaises(ShipOffGridError):
            Ship((0, 5), WEST, SUBMARINE)

        with self.assertRaises(ShipOffGridError):
            Ship((8, 1), EAST, SUBMARINE)

        with self.assertRaises(ShipOffGridError):
            Ship((3, 0), NORTH, SUBMARINE)

        with self.assertRaises(ShipOffGridError):
            Ship((3, 8), SOUTH, SUBMARINE)

    def test_get_bow_point(self):
        self.assertEqual(
            Ship((0, 5), NORTH, SUBMARINE)._get_bow_point(), (0, 2)
        )
        self.assertEqual(
            Ship((0, 5), SOUTH, SUBMARINE)._get_bow_point(), (0, 8)
        )
        self.assertEqual(
            Ship((5, 0), EAST, SUBMARINE)._get_bow_point(), (8, 0)
        )
        self.assertEqual(
            Ship((5, 0), WEST, SUBMARINE)._get_bow_point(), (2, 0)
        )

    def test_get_points(self):
        self.assertEqual(
            tuple(Ship((0, 0), EAST, SUBMARINE).get_points()),
            ((0, 0), (1, 0), (2, 0))
        )
        self.assertEqual(
            tuple(Ship((0, 0), SOUTH, SUBMARINE).get_points()),
            ((0, 0), (0, 1), (0, 2))
        )
        self.assertEqual(
            tuple(Ship((9, 0), WEST, SUBMARINE).get_points()),
            ((9, 0), (8, 0), (7, 0))
        )
        self.assertEqual(
            tuple(Ship((0, 9), NORTH, SUBMARINE).get_points()),
            ((0, 9), (0, 8), (0, 7))
        )


if __name__ == '__main__':
    unittest.main()
