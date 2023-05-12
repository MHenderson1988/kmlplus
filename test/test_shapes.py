from kmlplus.shapes import Circle, Polygon, ThreeDimensionShape
from kmlplus.geo import Point
from unittest import TestCase


class TestCircle(TestCase):
    def setUp(self):
        self.circle_no_height = Circle('55.1111 -3.2311', 10, sample=100)
        self.circle_height = Circle('28.132212 2.332782', 10, sample=150, z=20)

    def test_create(self):
        self.assertTrue(isinstance(self.circle_no_height.points, list))
        self.assertEqual(len(self.circle_no_height.points), 100)
        self.assertTrue(isinstance(self.circle_no_height.points[2], Point))

        self.assertTrue(isinstance(self.circle_height.points, list))
        self.assertEqual(len(self.circle_height.points), 150)
        self.assertTrue(isinstance(self.circle_height.points[2], Point))


class TestPolygon(TestCase):
    def setUp(self):
        pass

    def test_new_layer(self):
        test_coordinates_no_height = ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923']
        test_coordinates_with_height = ['22.323232 -4.287282 100', '23.323232 -5.328723 150',
                                        '22.112333 -6.23789238923 200']
        test_coordinates_with_height_override = ['22.323232 -4.287282', '23.323232 -5.328723',
                                                 '22.112333 -6.23789238923']
        test_coordinates_with_cw_arc = ['22.23232 -3.232323 0', 'start=21.23211 -4.122121, end=22.054541 -4.1111, z=15,'
                                                                ' direction=clockwise']
        test_coordinates_with_ccw_arc = ['22.23232 -3.232323 0', 'start=21.23211 -4.122121, end=22.054541 -4.1111, '
                                                                 'z=15, direction=anticlockwise']
        test_dms = ['554433N 0010203W', '443322N 0000102W', '443322N 0010102E']

        # Tests for coordinates with no z value provided. Should default to 0.
        result_no_height = Polygon(test_coordinates_no_height)

        self.assertTrue(isinstance(result_no_height, Polygon))
        self.assertEqual(len(result_no_height), 3)
        for i in result_no_height:
            self.assertEqual(i.z, 0)
            self.assertTrue(isinstance(i, Point))

        # Tests for coordinates with a user provided z value.
        result_with_height = Polygon(test_coordinates_with_height)

        self.assertTrue(isinstance(result_with_height, Polygon))
        self.assertEqual(len(result_with_height), 3)
        for i in result_with_height:
            self.assertTrue(isinstance(i, Point))
            self.assertNotEqual(i.z, 0)

        # Test results for coordinates with height overridden.
        result_with_height_override = Polygon(test_coordinates_with_height_override, z=500.11)

        self.assertTrue(isinstance(result_with_height_override, Polygon))
        self.assertEqual(len(result_with_height_override), 3)
        for i in result_with_height_override:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(500.11, i.z)

        # Test with DMS
        result_dms_no_height = Polygon(test_dms)
        self.assertTrue(isinstance(result_dms_no_height, Polygon))
        self.assertEqual(3, len(result_dms_no_height))
        for i in result_dms_no_height:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(0, i.z)

        # Test with DD and curved segment
        result_dd_arc = Polygon(test_coordinates_with_cw_arc)
        self.assertTrue(isinstance(result_dd_arc, Polygon))
        self.assertTrue(len(result_dd_arc) > 100)
        for i in result_dd_arc:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(0, i.z)

        result_dd_arc = Polygon(test_coordinates_with_ccw_arc)
        self.assertTrue(isinstance(result_dd_arc, Polygon))
        self.assertTrue(len(result_dd_arc) > 100)
        for i in result_dd_arc:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(0, i.z)


class TestThreeDimensionShape(TestCase):

    def test_generate_sides(self):
        test_list = ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923']
        poly = ThreeDimensionShape(test_list, test_list)
        self.assertTrue(isinstance(poly, ThreeDimensionShape))
        self.assertTrue(isinstance(poly.sides, list))
        self.assertEqual(3, len(poly.sides))