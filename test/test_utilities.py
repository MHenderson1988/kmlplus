from unittest import TestCase

from kmlplus.coordinates import Coordinate
from kmlplus.utilities import get_bearing


class TestUtilities(TestCase):
    def test_get_bearing(self):
        list_of_coordinates = [(55.11, -4.11), (55.22, -4.22), (54.11, 4.11), (54.22, 4.22)]
        reversed_list_of_coordinates = [coordinates[::-1] for coordinates in list_of_coordinates]
        expected_results = []
        c1 = Coordinate(1, 1, 0, coordinate_type='decimal')
        c2 = Coordinate(1, 1, 0, coordinate_type='decimal')
        i = 0
        while i < len(list_of_coordinates):
            c1.latitude, c1.longitude = list_of_coordinates[i][0], list_of_coordinates[i][1]
            c2.latitude, c1.longitude = reversed_list_of_coordinates[i][0], reversed_list_of_coordinates[i][1]
            print(get_bearing(c1, c2))
            i += 1