from unittest import TestCase
from kmlplus.coordinates import Coordinate


class TestCoordinates(TestCase):
    def test_coordinate(self):
        c1 = Coordinate(55.21434, -4.38487)
        print(c1.__dict__)