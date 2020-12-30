from unittest import TestCase

from kmlplus.coordinates import Coordinate
from kmlplus.utilities import get_bearing


class TestUtilities(TestCase):
    def test_get_bearing(self):
        c1 = Coordinate(55.11, -4.11, 0, coordinate_type='decimal')
        c2 = Coordinate(55.22, -4.22, 0, coordinate_type='decimal')
        print(get_bearing(c1, c2))
