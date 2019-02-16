import unittest

from battleship import EAST, Ship


class BattleshipTest(unittest.TestCase):

    def test_initial_configuration(self):
        aft_location = (3, 5)
        direction = EAST
        name = 'Submarine'
        ship = Ship(aft_location, direction, name)
        self.assertEqual(ship._aft_location, aft_location)
        self.assertEqual(ship._direction, direction)
        self.assertEqual(ship._name, name)


if __name__ == '__main__':
    unittest.main()
