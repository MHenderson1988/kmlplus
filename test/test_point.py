from unittest import TestCase

import util
from kmlplus.point import Point, PointFactory
from kmlplus.point import detect_coordinate_type


class TestPoint(TestCase):
    def setUp(self):
        self.test_point_1 = Point.from_dms('551206.00N', '0045206.234W')
        self.test_point_2 = Point.from_dms('501206.00N', '0045206.234W')
        self.test_midpoint = Point.find_midpoint(self.test_point_1, self.test_point_2)

    def test_from_dms(self):
        test_obj = Point.from_dms('551206.00N', '0045206.234W')
        self.assertEqual(test_obj.y, 55.20166666666667)
        self.assertEqual(test_obj.x, -4.868398333333333)
        self.assertEqual(test_obj.z, 0)

        test_obj = Point.from_dms('501206.00N', '0045206.234W', z=383)
        self.assertEqual(test_obj.y, 50.20166666666667)
        self.assertEqual(test_obj.x, -4.868398333333333)
        self.assertEqual(test_obj.z, 383)

    def test_find_midpoint(self):
        mp = Point.find_midpoint(self.test_point_1, self.test_point_2)
        self.assertAlmostEqual(52.701666666667, mp.y, delta=0.0000001)
        self.assertAlmostEqual(-4.8683983333333, mp.x, delta=0.0000001)

    def test_from_point_bearing_and_distance(self):
        test_obj = Point.from_dms('551206.00N', '0045206.23W')
        test_result = Point.from_point_bearing_and_distance(test_obj, 180.00, 383.00, uom='km')

        self.assertAlmostEqual(51.756802, test_result.y, delta=0.01)
        self.assertAlmostEqual(-4.868396, test_result.x, delta=0.00001)

    def test_get_distance(self):
        # test km
        test_obj = Point.from_dms('551206.00N', '0045206.234W')
        distance = test_obj.get_distance(Point.from_dms('501206.00N', '0045206.234W'))
        self.assertEqual(556.5977157657558, distance)

        # test miles
        test_obj = Point.from_dms('551206.00N', '0045206.234W')
        distance = test_obj.get_distance(Point.from_dms('501206.00N', '0045206.234W'), uom='mi')
        self.assertEqual(345.8535719105704, distance)

    def test_get_bearing(self):
        result = self.test_point_1.get_bearing(self.test_point_2)
        self.assertEqual(180, result)

        result = self.test_point_2.get_bearing(self.test_point_1)
        self.assertEqual(0, result)

        result = self.test_midpoint.get_bearing(self.test_point_1)
        self.assertEqual(0, result)

        result = self.test_midpoint.get_bearing(self.test_point_2)
        self.assertEqual(180, result)

    def test_get_inverse_bearing(self):
        inverse_bearing = self.test_point_1.get_inverse_bearing(self.test_point_2)
        self.assertEqual(0, inverse_bearing)

        inverse_bearing = self.test_point_2.get_inverse_bearing(self.test_point_1)
        self.assertEqual(180, inverse_bearing)

        inverse_bearing = self.test_midpoint.get_inverse_bearing(self.test_point_2)
        self.assertEqual(0, inverse_bearing)

        inverse_bearing = self.test_midpoint.get_inverse_bearing(self.test_point_1)
        self.assertEqual(180, inverse_bearing)


class TestPointFactory(TestCase):
    def setUp(self):
        pass

    def test_process_coordinates(self):
        test_dd = PointFactory.process_coordinates(['22.323232, -4.287282',
                                                    '23.323232, -5.328723',
                                                    '22.112333, -6.23789238923'])
        self.assertTrue(isinstance(test_dd[0], Point))

        # Test that dms coordinates are correctly returned as decimal degrees.
        test_dms = PointFactory.process_coordinates(['532452N, 0045263W', '542352N, 0053421W', '563321N, 0054844W'])
        type_result = util.detect_coordinate_type(f'{test_dms[0].y}, {test_dms[0].x}')
        self.assertEqual(type_result, 'dd')
