import unittest

from battleship import (
    NORTH,
    SOUTH,
    EAST,
    WEST,
    CARRIER,
    BATTLESHIP,
    CRUISER,
    SUBMARINE,
    DESTROYER,
    Peg,
    Grid,
    Ship,
    ShipOffGridError,
    ShipsOverlapError,
    parse_all_ships,
    parse_point
)


class ParseTestCase(unittest.TestCase):
    # TODO: test that parse functions raise exceptions for bad syntax

    def test_parse_all_ships(self):
        all_ships = parse_all_ships(
            'A3 E, B1 S, C10 W, I2 N, J8 N'
        )
        expected = (
            Ship((2, 0), EAST, CARRIER),
            Ship((0, 1), SOUTH, BATTLESHIP),
            Ship((9, 2), WEST, CRUISER),
            Ship((1, 8), NORTH, SUBMARINE),
            Ship((7, 9), NORTH, DESTROYER)
        )
        self.assertEqual(all_ships, expected)

    def test_parse_all_ships_cases_spaces(self):
        all_ships = parse_all_ships(
            '    A3    e,b1 S    ,   c10 w, I2     N    ,J8    n    '
        )
        expected = (
            Ship((2, 0), EAST, CARRIER),
            Ship((0, 1), SOUTH, BATTLESHIP),
            Ship((9, 2), WEST, CRUISER),
            Ship((1, 8), NORTH, SUBMARINE),
            Ship((7, 9), NORTH, DESTROYER)
        )
        self.assertEqual(all_ships, expected)

    def test_parse_point(self):
        self.assertEqual(parse_point('A1'), (0, 0))
        self.assertEqual(parse_point('a1'), (0, 0))
        self.assertEqual(parse_point('A3'), (2, 0))
        self.assertEqual(parse_point('a3'), (2, 0))
        self.assertEqual(parse_point('C1'), (0, 2))
        self.assertEqual(parse_point('c1'), (0, 2))
        self.assertEqual(parse_point('D5'), (4, 3))
        self.assertEqual(parse_point('d5'), (4, 3))
        self.assertEqual(parse_point('J10'), (9, 9))
        self.assertEqual(parse_point('j10'), (9, 9))


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
        grid.add_ship(Ship((9, 9), WEST, BATTLESHIP))

        self.assertEqual(grid.attack(0, 0), (SUBMARINE, False))
        self.assertEqual(grid.attack(1, 0), (SUBMARINE, False))
        self.assertEqual(grid.attack(2, 0), (SUBMARINE, True))
        self.assertEqual(grid.attack(3, 0), None)
        self.assertEqual(grid.attack(0, 1), None)
        self.assertEqual(grid.attack(9, 9), (BATTLESHIP, False))
        self.assertEqual(grid.attack(8, 9), (BATTLESHIP, False))
        self.assertEqual(grid.attack(7, 9), (BATTLESHIP, False))
        self.assertEqual(grid.attack(6, 9), (BATTLESHIP, True))
        self.assertEqual(grid.attack(5, 9), None)
        self.assertEqual(grid.attack(5, 5), None)
        self.assertEqual(grid.attack(7, 5), None)

        self.assertEqual(
            grid._pegs,
            [Peg(0, 0, True),
             Peg(1, 0, True),
             Peg(2, 0, True),
             Peg(3, 0, False),
             Peg(0, 1, False),
             Peg(9, 9, True),
             Peg(8, 9, True),
             Peg(7, 9, True),
             Peg(6, 9, True),
             Peg(5, 9, False),
             Peg(5, 5, False),
             Peg(7, 5, False)]
        )

    def test_is_dead(self):
        grid = Grid()
        grid.add_ship(Ship((0, 0), EAST, SUBMARINE))
        self.assertFalse(grid.is_dead())
        grid.attack(0, 0)
        grid.attack(1, 0)
        grid.attack(2, 0)
        self.assertTrue(grid.is_dead())

    def test_get_full_view(self):
        grid = Grid()
        grid.add_ship(Ship((0, 0), EAST, SUBMARINE))
        grid.add_ship(Ship((8, 1), SOUTH, CARRIER))
        grid.attack(0, 0)
        grid.attack(5, 5)
        grid.attack(7, 2)
        grid.attack(8, 3)
        self.assertEqual(
            grid.get_full_view(),
            '  1 2 3 4 5 6 7 8 9 10\n'
            'A x # # . . . . . . . \n'
            'B . . . . . . . . # . \n'
            'C . . . . . . . o # . \n'
            'D . . . . . . . . x . \n'
            'E . . . . . . . . # . \n'
            'F . . . . . o . . # . \n'
            'G . . . . . . . . . . \n'
            'H . . . . . . . . . . \n'
            'I . . . . . . . . . . \n'
            'J . . . . . . . . . . \n'
        )

    def test_get_partial_view(self):
        grid = Grid()
        grid.add_ship(Ship((0, 0), EAST, SUBMARINE))
        grid.add_ship(Ship((8, 1), SOUTH, CARRIER))
        grid.attack(0, 0)
        grid.attack(5, 5)
        grid.attack(7, 2)
        grid.attack(8, 3)
        self.assertEqual(
            grid.get_partial_view(),
            '  1 2 3 4 5 6 7 8 9 10\n'
            'A x . . . . . . . . . \n'
            'B . . . . . . . . . . \n'
            'C . . . . . . . o . . \n'
            'D . . . . . . . . x . \n'
            'E . . . . . . . . . . \n'
            'F . . . . . o . . . . \n'
            'G . . . . . . . . . . \n'
            'H . . . . . . . . . . \n'
            'I . . . . . . . . . . \n'
            'J . . . . . . . . . . \n'
        )


class ShipTestCase(unittest.TestCase):

    def test_create_carrier(self):
        stern_point = (4, 9)
        direction = EAST
        name = CARRIER
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_create_battleship(self):
        stern_point = (2, 9)
        direction = NORTH
        name = BATTLESHIP
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_create_cruiser(self):
        stern_point = (4, 2)
        direction = WEST
        name = CRUISER
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_create_submarine(self):
        stern_point = (3, 5)
        direction = EAST
        name = SUBMARINE
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_create_destroyer(self):
        stern_point = (7, 4)
        direction = NORTH
        name = DESTROYER
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_create_ship_with_stern_at_edge(self):
        stern_point = (0, 2)
        direction = EAST
        name = CRUISER
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_create_vertical_ship_with_bow_at_edge(self):
        stern_point = (0, 2)
        direction = NORTH
        name = CRUISER
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_create_horizontal_ship_with_bow_at_edge(self):
        stern_point = (4, 0)
        direction = WEST
        name = CARRIER
        ship = Ship(stern_point, direction, name)
        self.assertEqual(ship._stern_point, stern_point)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)

    def test_stern_on_grid(self):
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
            Ship((0, 5), NORTH, SUBMARINE)._get_bow_point(), (0, 3)
        )
        self.assertEqual(
            Ship((0, 5), SOUTH, SUBMARINE)._get_bow_point(), (0, 7)
        )
        self.assertEqual(
            Ship((5, 0), EAST, SUBMARINE)._get_bow_point(), (7, 0)
        )
        self.assertEqual(
            Ship((5, 0), WEST, SUBMARINE)._get_bow_point(), (3, 0)
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
