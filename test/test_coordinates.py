from unittest import TestCase

from kmlplus import coordinates


class TestCoordinates(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create classes
        cls._c1 = coordinates.Coordinate(55.38327, -4.32723)
        cls._c2 = coordinates.Coordinate(10, 10)
        cls._c3 = coordinates.Coordinate(554323, -47543, height=20, coordinate_type='dms')

    def setUp(self):
        # Populate data sets for use with the tests
        self.decimal_coordinates_1 = [(55.11, -4.11), (55.22, -4.22), (54.11, 4.11), (54.22, 4.22)]
        self.decimal_coordinates_2 = [(52.32, -4.45), (55.75, -4.11), (53.453, -4.8587), (56.2832, -2.4893)]
        self.dms_coordinates_1 = [(546512, -25545), (556545, -45210), (505425, 42215), (540012, 40214)]

    def test_coordinate(self):
        for coordinate_pair in self.decimal_coordinates_1:
            # Change the coordinates of the instance
            self._c1.latitude = coordinate_pair[0]
            self._c1.longitude = coordinate_pair[1]
            # Check the coordinates have changed, as expected
            self.assertEqual(self._c1.latitude, coordinate_pair[0])
            self.assertEqual(self._c1.longitude, coordinate_pair[1])
            # Check the to_string test works
            self.assertEqual(self._c1.__str__(), "{}, {}, {}".format(coordinate_pair[0], coordinate_pair[1], 0))

    def test_get_bearing_and_distance(self):
        # Populate the expected results from online calculators
        expected_results = [184.15, 6.39, 266.34, 301.04]
        i = 0
        while i < len(self.decimal_coordinates_1):
            self._c1.latitude, self._c1.longitude = self.decimal_coordinates_1[i][0], self.decimal_coordinates_1[i][1]
            self._c2.latitude, self._c2.longitude = self.decimal_coordinates_2[i][0], self.decimal_coordinates_2[i][1]
            bearing, distance = self._c1.get_bearing_and_distance(self._c2)
            """self.assertAlmostEqual(self._c1.get_bearing_and_distance(self._c2), expected_results[i], delta=0.3)"""
            i += 1

    def test_decimal_to_dms(self):
        # Populate the expected results from online calculators
        expected = [(55636, -4636), (551312, -41312), (54636, 4636), (541312, 41312)]
        i = 0
        while i < len(self.dms_coordinates_1):
            # Change the coordinates to the next pair in the data set
            self._c1.latitude, self._c1.longitude = self.decimal_coordinates_1[i][0], self.decimal_coordinates_1[i][1]
            # Attempt to convert the coordinates from decimal to degrees minutes seconds
            self._c1.convert_to_dms()
            # Check that the coordinates have been converted as expected
            self.assertEqual(self._c1.latitude, expected[i][0])
            self.assertEqual(self._c1.longitude, expected[i][1])
            i += 1

    def test_dms_to_decimal(self):
        i = 0
        expected = [(55.08667, -2.92916), (56.095833, -4.86944), (50.90694, 4.37083),
                    (54.00333, 4.03722)]
        while i < len(self.dms_coordinates_1):
            # Change the coordinates to the next pair in the data set
            self._c3.latitude, self._c3.longitude = self.dms_coordinates_1[i][0], self.dms_coordinates_1[i][1]
            # Attempt to convert the coordinates from degrees minutes seconds to decimal
            self._c3.convert_to_decimal()
            # Check that the coordinates have been converted as expected
            self.assertAlmostEqual(self._c3.latitude, expected[i][0], delta=0.1)
            self.assertAlmostEqual(self._c3.longitude, expected[i][1], delta=0.1)
            # Check that passing a coordinate type of decimal to the conversion method raises a type error
            with self.assertRaises(TypeError):
                self._c3.convert_to_decimal()
            i += 1

    def test_generate_coordinates(self):
        self._c1.latitude, self._c1.longitude = 55.123, -4.321
        new_instance = self._c1.generate_coordinates(10, 350, 20)
        lat_lon_tuple = (float(new_instance.latitude), float(new_instance.longitude))
        expected_tuple = (55.211575, -4.348375)
        i = 0
        while i < len(lat_lon_tuple):
            self.assertAlmostEqual(lat_lon_tuple[i], expected_tuple[i], delta=0.001)
            i += 1
