from unittest import TestCase

from kmlplus.util import dms_to_decimal, get_dms_slice_dict, calculate_dms_to_decimal, get_earth_radius, \
    detect_coordinate_type


class TestUtil(TestCase):
    def test_dms_to_decimal_latitude(self):
        # Using 551206N
        result = dms_to_decimal('551206.00N')
        self.assertEqual(55.20166666666667, result)

        # Test negative
        result = dms_to_decimal('551206.00S')
        self.assertEqual(-55.20166666666667, result)

        # Test longitude
        result = dms_to_decimal('0045206.234W')
        self.assertEqual(-4.868398333333333, result)

        result = dms_to_decimal('0045206.234E')
        self.assertEqual(4.868398333333333, result)

    def test_get_dms_slice_dict(self):
        expected = {'degrees': 55, 'minutes': 12, 'seconds': 06.00, 'hemisphere': 'N'}
        result = get_dms_slice_dict('551206.00N')
        self.assertEqual(result, expected)

        expected = {'degrees': 4, 'minutes': 52, 'seconds': 06.234, 'hemisphere': 'W'}
        result = get_dms_slice_dict('0045206.234W')
        self.assertEqual(result, expected)

    def test_calculate_dms_to_decimal(self):
        result = calculate_dms_to_decimal({'degrees': 55, 'minutes': 12, 'seconds': 6.00, 'hemisphere': 'N'})
        expected = {'degrees': 55, 'minutes': 0.2, 'seconds': 0.00166666666666666666666666666667, 'hemisphere': 'N'}
        self.assertEqual(result, expected)

        result = calculate_dms_to_decimal({'degrees': 4, 'minutes': 52, 'seconds': 6.234, 'hemisphere': 'W'})
        expected = {'degrees': 4, 'minutes': 0.86666666666666666666666666666667,
                    'seconds': 0.00173166666666666666666666666667, 'hemisphere': 'W'}
        self.assertEqual(result, expected)

    def test_get_earth_radius(self):
        # Test for Km
        result = get_earth_radius(uom='km')
        self.assertEqual(result, 6378.14)

        result = get_earth_radius()
        self.assertEqual(result, 6378.14)

        # Test for nautical mile
        result = get_earth_radius(uom='nm')
        self.assertEqual(result, 3443.92)

        # Test for statute miles
        result = get_earth_radius(uom='mi')
        self.assertEqual(result, 3963.19)

        # Test for metres
        result = get_earth_radius(uom='m')
        self.assertEqual(result, 6378140.00)

    def test_detect_coordinate_type(self):
        result = detect_coordinate_type('+55.393922, 4.323232')
        self.assertEqual('dd', result)
        result = detect_coordinate_type('55.393922, 4.323232')
        self.assertEqual('dd', result)
        result = detect_coordinate_type('55.393922, -4.393922')
        self.assertEqual('dd', result)
        result = detect_coordinate_type('55.393922, +04.393922')
        self.assertEqual('dd', result)

        result = detect_coordinate_type('556622.123N, 0045645.21W')
        self.assertEqual('dms', result)
        result = detect_coordinate_type('0045645.21W, 0045645.21W')
        self.assertEqual('dms', result)

        with self.assertRaises(ValueError):
            detect_coordinate_type('+0043212.30W')
        with self.assertRaises(ValueError):
            detect_coordinate_type('+04232.322')
        with self.assertRaises(ValueError):
            detect_coordinate_type('+55.393922N')
