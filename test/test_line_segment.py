from unittest import TestCase

from kmlplus.line_segment import ClockwiseCurvedSegment, AnticlockwiseCurvedSegment
from kmlplus.point import Point


class TestClockwiseCurvedSegment(TestCase):
    def setUp(self):
        self.test_obj = ClockwiseCurvedSegment(Point.from_dms('551206.00N', '0045206.234W'),
                                               Point.from_dms('501206.00N', '0045206.234W'))
        self.inverse_test_obj = ClockwiseCurvedSegment(Point.from_dms('501206.00N', '0045206.234W'),
                                                       Point.from_dms('551206.00N', '0045206.234W'))

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
        result = self.test_obj.get_bearing_increment(2)
        self.assertEqual(result, 60)

        result = self.inverse_test_obj.get_bearing_increment(2)
        self.assertEqual(result, 60)


class TestAnticlockwiseCurvedSegment(TestCase):
    def setUp(self):
        self.test_obj = AnticlockwiseCurvedSegment(Point.from_dms('551206.00N', '0045206.234W'),
                                                   Point.from_dms('501206.00N', '0045206.234W'))

        self.inverse_test_obj = AnticlockwiseCurvedSegment(Point.from_dms('501206.00N', '0045206.234W'),
                                                           Point.from_dms('551206.00N', '0045206.234W'))

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
        result = self.test_obj.get_bearing_increment(2)
        self.assertEqual(result, 60)

        result = self.inverse_test_obj.get_bearing_increment(2)
        self.assertEqual(result, 60)
