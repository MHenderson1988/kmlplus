from unittest import TestCase

from kmlplus import coordinates


class TestCoordinates(TestCase):

    def test_latitude_and_longitude(self):
        c1 = coordinates.Coordinate("55.11213, -4.24453")
        c2 = coordinates.Coordinate("55.33, -4.33, 483")
        c3 = coordinates.Coordinate(33.232, -4.232)
        c4 = coordinates.Coordinate(223212, -32312, 40)

        # Make sure initial values have initialised correctly
        self.assertEqual(c1._latitude, 55.11213)
        self.assertEqual(c1._longitude, -4.24453)
        # Switch them up
        c1.latitude = 34.32433
        c1.longitude = -4.3823
        # Check the new values have updated correctly
        self.assertEqual(c1.latitude, 34.32433)
        self.assertEqual(c1.longitude, -4.3823)

        # Check c2 initialises correctly
        self.assertEqual(c2.latitude, 55.33)
        self.assertEqual(c2.longitude, -4.33)
        self.assertEqual(c2.height, 483)

        # Test updating c2 values
        c2.latitude = "55.1111"
        c2.longitude = "-1200203"
        c2.height = "53.23"
        self.assertEqual(c2.latitude, 55.1111)
        self.assertEqual(c2.longitude, -120.03417)
        self.assertEqual(c2.height, 53.23)

        # Check c3 initialises correctly
        self.assertEqual(c3.latitude, 33.232)
        self.assertEqual(c3.longitude, -4.232)
        self.assertEqual(c3.height, 0)

        # Check c4 initialises correctly
        self.assertEqual(c4.latitude, 22.53667)
        self.assertEqual(c4.longitude, -3.38667)
        self.assertEqual(c4.height, 40)

    def test_validate_attribute_input(self):
        c1 = coordinates.Coordinate("55.232, -43.3821")
        self.assertRaises(TypeError, c1.validate_attribute_input(True))

    def test_is_negative(self):
        c1 = coordinates.Coordinate(873212, -600312, 5)
        self.assertTrue(c1.is_negative(c1.longitude))
        self.assertFalse(c1.is_negative(c1.latitude))

    def test_decimal_to_dms(self):
        c1 = coordinates.Coordinate("55.11213, -4.24453")
        self.assertIsInstance(c1.decimal_to_dms(c1.latitude), float)
        self.assertEqual(55643.67, c1.decimal_to_dms(c1.latitude))
        self.assertIsInstance(c1.decimal_to_dms(c1.longitude), float)
        self.assertEqual(-41440.31, c1.decimal_to_dms(c1.longitude))

    def test_detect_coordinate_type(self):
        c1 = coordinates.Coordinate(881232.12, 1795410.00, 4568.45)
        # Check that conversion happens on init
        self.assertEqual(c1.detect_coordinate_type(c1.latitude), 'decimal')
        self.assertEqual(c1.detect_coordinate_type(c1.longitude), 'decimal')
        self.assertRaises(TypeError, c1.detect_coordinate_type(True))

    def test_strip_whitespace(self):
        c1 = coordinates.Coordinate(341222.212343, -55312.32894389, 0)
        string_to_strip = c1.strip_whitespace("    Hello")
        self.assertEqual("Hello", string_to_strip)

    def test_convert_to_dms(self):
        c1 = coordinates.Coordinate(341222.212343, -55312.32894389, 0)
        self.assertRaises(TypeError, c1.convert_to_dms())

    def test_convert_to_decimal(self):

