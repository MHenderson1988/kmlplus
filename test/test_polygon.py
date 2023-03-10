from unittest import TestCase
from kmlplus.polygon import Polygon
from kmlplus.geo import Point


class TestPolygon(TestCase):
    def setUp(self):
        pass

    def test_new_layer(self):
        test_coordinates_no_height = ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923']
        test_coordinates_with_height = ['22.323232 -4.287282 100', '23.323232 -5.328723 150', '22.112333 -6.23789238923 200']
        test_coordinates_with_height_override = ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923']

        test_dms = ['554433N 0010203W', '443322N 0000102W', '443322N 0010102E']
        
        # Tests for coordinates with no z value provided. Should default to 0.
        result_no_height = Polygon.create_polygon(test_coordinates_no_height)

        self.assertTrue(isinstance(result_no_height, Polygon))
        self.assertEqual(len(result_no_height), 3)
        for i in result_no_height:
            self.assertEqual(i.z, 0)
            self.assertTrue(isinstance(i, Point))
        
        # Tests for coordinates with a user provided z value.
        result_with_height = Polygon.create_polygon(test_coordinates_with_height)
        
        self.assertTrue(isinstance(result_with_height, Polygon))
        self.assertEqual(len(result_with_height), 3)
        for i in result_with_height:
            self.assertTrue(isinstance(i, Point))
            self.assertNotEqual(i.z, 0)

        # Test results for coordinates with height overridden.
        result_with_height_override = Polygon.create_polygon(test_coordinates_with_height_override, z=500.11)

        self.assertTrue(isinstance(result_with_height_override, Polygon))
        self.assertEqual(len(result_with_height_override), 3)
        for i in result_with_height_override:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(500.11, i.z)

        # Test with DMS
        result_dms_no_height = Polygon.create_polygon(test_dms)
        self.assertTrue(isinstance(result_dms_no_height, Polygon))
        self.assertEqual(3, len(result_dms_no_height))
        for i in result_dms_no_height:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(0, i.z)

