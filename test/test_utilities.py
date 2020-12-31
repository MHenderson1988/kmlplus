from unittest import TestCase

from kmlplus.coordinates import Coordinate
from kmlplus.utilities import get_bearing


class TestUtilities(TestCase):
    def setUp(self):
        self.coordinates_1 = [(55.11, -4.11), (55.22, -4.22), (54.11, 4.11), (54.22, 4.22)]
        self.coordinates_2 = [(52.32, -4.45), (55.75, -4.11), (53.453, -4.8587), (56.2832, -2.4893)]

    def test_get_bearing(self):
        expected_results = [184.15, 6.39, 266.34, 301.04]
        c1 = Coordinate(1, 1, 0, coordinate_type='decimal')
        c2 = Coordinate(1, 1, 0, coordinate_type='decimal')
        i = 0
        while i < len(self.coordinates_1):
            c1.latitude, c1.longitude = self.coordinates_1[i][0], self.coordinates_1[i][1]
            c2.latitude, c2.longitude = self.coordinates_2[i][0], self.coordinates_2[i][1]
            self.assertAlmostEqual(get_bearing(c1,c2), expected_results[i], delta=0.3)
            i += 1