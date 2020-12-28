from unittest import TestCase

from kmlplus.coordinates import Coordinate
from kmlplus.utilities import get_bearing


class TestUtilities(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c1 = Coordinate(1, 1, 0, coordinate_type='decimal')
        cls.c2 = Coordinate(1, 1, 0, coordinate_type='decimal')

    def setUp(self):
        self.list_of_coordinates_1 = [(55.11, -4.11), (55.22, -4.22), (54.11, -4.11), (54.22, -4.22)]
        self.list_of_coordinates_2 = [(55.55, -4.22), (55.89, -4.11), (54.22, -4.22), (55.11, -4.11)]
        self.error_threshold = 1
        self.expected_bearing_results = [351, 5, 329, 4]

    def test_get_bearing(self):
        i = 0
        while i < len(self.list_of_coordinates_1):
            self.c1.latitude, self.c1.longitude = self.list_of_coordinates_1[i][0], self.list_of_coordinates_1[i][1]
            self.c2.latitude, self.c2.longitude = self.list_of_coordinates_2[i][0], self.list_of_coordinates_2[i][1]
            bearing = get_bearing(self.c1, self.c2)
            self.assertTrue((bearing - self.error_threshold) <= self.expected_bearing_results[i]
                            <= (bearing + self.error_threshold))
            i += 1
