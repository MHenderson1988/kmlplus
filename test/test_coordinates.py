from unittest import TestCase

from kmlplus.coordinates import Coordinate


class TestCoordinates(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._c1 = Coordinate(55.38327, -4.32723, 0, coordinate_type="decimal")
        cls._c2 = Coordinate(0, 0, 0, coordinate_type="decimal")

    def setUp(self):
        self.decimal_coordinates_1 = [(55.11, -4.11), (55.22, -4.22), (54.11, 4.11), (54.22, 4.22)]
        self.decimal_coordinates_2 = [(52.32, -4.45), (55.75, -4.11), (53.453, -4.8587), (56.2832, -2.4893)]
        self.dms_coordinates_1 = [(55636, -4636), (551312, -41312), (54636, 4636), (541312, 41312)]

    def test_coordinate(self):
        for coordinate_pair in self.decimal_coordinates_1:
            self._c1.latitude = coordinate_pair[0]
            self._c1.longitude = coordinate_pair[1]
            self.assertEqual(self._c1.latitude, coordinate_pair[0])
            self.assertEqual(self._c1.longitude, coordinate_pair[1])
            self.assertEqual(self._c1.to_string(), "{}, {}, {}".format(coordinate_pair[0], coordinate_pair[1], 0))

    def test_get_bearing(self):
        expected_results = [184.15, 6.39, 266.34, 301.04]
        i = 0
        while i < len(self.decimal_coordinates_1):
            self._c1.latitude, self._c1.longitude = self.decimal_coordinates_1[i][0], self.decimal_coordinates_1[i][1]
            self._c2.latitude, self._c2.longitude = self.decimal_coordinates_2[i][0], self.decimal_coordinates_2[i][1]
            self.assertAlmostEqual(self._c1.get_bearing(self._c2), expected_results[i], delta=0.3)
            i += 1

    def test_decimal_to_dms(self):
        i = 0
        while i < len(self.dms_coordinates_1):
            self._c1.latitude = self.decimal_coordinates_1[i][0]
            self._c1.longitude = self.decimal_coordinates_1[i][1]
            self._c1.convert_to_dms()
            self.assertEqual(self._c1.latitude, self.dms_coordinates_1[i][0])
            self.assertEqual(self._c1.longitude, self.dms_coordinates_1[i][1])
            i += 1