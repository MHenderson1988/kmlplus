from unittest import TestCase

import util
from kmlplus.geo import Point, PointFactory, ClockwiseCurvedSegment, AnticlockwiseCurvedSegment, CurvedSegmentFactory


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
        self.pf = PointFactory(['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923'])

    def test_process_coordinates(self):
        test_dd = self.pf.process_coordinates()
        for i in range(len(test_dd)):
            self.assertTrue(isinstance(test_dd[i], Point))

        # Test that dms coordinates are correctly returned as decimal degrees.
        test_dms = self.pf.process_coordinates()
        type_result = util.detect_coordinate_type(f'{test_dms[0].y} {test_dms[0].x}')
        self.assertEqual(type_result, 'dd')

    def test_populate_point_list(self):
        test_point_list = self.pf.populate_point_list()
        self.assertTrue(isinstance(test_point_list, list))

    def test_process_string(self):
        no_height = '22.323232 -4.287282'
        with_height = '22.323232 -4.287282, 8'

        dms_test = '521244N 0056555W'

        no_height_obj = self.pf.process_string(no_height, 'dd')
        with_height_obj = self.pf.process_string(with_height, 'dd')
        dms_obj = self.pf.process_string(dms_test, 'dms')

        self.assertTrue(isinstance(no_height_obj, Point))
        self.assertTrue(isinstance(with_height_obj, Point))
        self.assertTrue(isinstance(dms_obj, Point))

        self.assertEqual(no_height_obj.z, 0.0)
        self.assertEqual(with_height_obj.z, 8.0)
        self.assertEqual(dms_obj.y, 52.21222222222222)


class TestCurvedSegmentFactory(TestCase):
    def test_process_segment(self):
        c_cs = CurvedSegmentFactory.process_segment(
            'start=522423N 0042354W, end=522428N 0042254W, direction=clockwise,' \
            ' centre=502211N 0043212W, sample=50')
        ac_cs = CurvedSegmentFactory.process_segment(
            'start=522423N 0042354W, end=522428N 0042254W, direction=anticlockwise,' \
            ' centre=502211N 0043212W, sample=50')
        self.assertTrue(isinstance(c_cs, ClockwiseCurvedSegment))
        self.assertTrue(isinstance(ac_cs, AnticlockwiseCurvedSegment))

    def test_generate_segment(self):
        c_cs = CurvedSegmentFactory.generate_segment(
            'start=522423N 0042354W, end=522428N 0042254W, direction=clockwise,' \
            ' centre=502211N 0043212W, sample=50')
        ac_cs = CurvedSegmentFactory.generate_segment(
            'start=522423N 0042354W, end=522428N 0042254W, direction=anticlockwise,' \
            ' centre=502211N 0043212W, sample=50')
        self.assertTrue(len(c_cs) == 50)
        self.assertTrue(len(ac_cs) == 50)
        for i in c_cs:
            self.assertTrue(isinstance(i, Point))
        for i in ac_cs:
            self.assertTrue(isinstance(i, Point))


class TestClockwiseCurvedSegment(TestCase):
    def setUp(self):
        self.test_obj = ClockwiseCurvedSegment(Point.from_dms('551206.00N', '0045206.234W'),
                                               Point.from_dms('501206.00N', '0045206.234W'),
                                               sample=100)
        self.inverse_test_obj = ClockwiseCurvedSegment(Point.from_dms('501206.00N', '0045206.234W'),
                                                       Point.from_dms('551206.00N', '0045206.234W'),
                                                       sample=2)

    def test_get_points(self):
        result = self.test_obj.get_points()
        self.assertEqual(len(result), 100)

        # Check start and end points are accurately computed
        # Delta 7 implies tolerance of 1.11cm
        self.assertAlmostEqual(result[0].y, 55.20166666666667, delta=7)
        self.assertAlmostEqual(result[0].x, -4.868398333333333, delta=7)

        self.assertAlmostEqual(result[99].y, 50.20166666666667, delta=7)
        self.assertAlmostEqual(result[99].x, -4.868398333333333, delta=7)

        # As this is moving clockwise, the longitude should increase due to the arc as its moving easterly.
        self.assertTrue(result[0].x < result[49].x)

    def test_get_heading_increments(self):
        result = self.test_obj.get_bearing_increment()
        self.assertEqual(result, 1.7821782178217822)

        result = self.inverse_test_obj.get_bearing_increment()
        self.assertEqual(result, 60)


class TestAnticlockwiseCurvedSegment(TestCase):
    def setUp(self):
        self.test_obj = AnticlockwiseCurvedSegment(Point.from_dms('551206.00N', '0045206.234W'),
                                                   Point.from_dms('501206.00N', '0045206.234W'), sample=100)

        self.inverse_test_obj = AnticlockwiseCurvedSegment(Point.from_dms('501206.00N', '0045206.234W'),
                                                           Point.from_dms('551206.00N', '0045206.234W', sample=100))

    def test_get_points(self):
        result = self.test_obj.get_points()
        self.assertEqual(len(result), 100)

        # Check start and end points are accurately computed
        # Delta 7 implies tolerance of 1.11cm
        self.assertAlmostEqual(result[0].y, 55.20166666666667, delta=7)
        self.assertAlmostEqual(result[0].x, -4.868398333333333, delta=7)

        self.assertAlmostEqual(result[99].y, 50.20166666666667, delta=7)
        self.assertAlmostEqual(result[99].x, -4.868398333333333, delta=7)

        # As this is moving anti-clockwise, the longitude should decrease due to the arc as its moving westerly.
        self.assertTrue(result[0].x > result[49].x)

    def test_get_heading_increments(self):
        result = self.test_obj.get_bearing_increment()
        self.assertEqual(1.7821782178217822, result)

        result = self.inverse_test_obj.get_bearing_increment()
        self.assertEqual(1.7821782178217822, result)
