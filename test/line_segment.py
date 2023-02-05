from unittest import TestCase
from kmlplus.line_segment import LineSegment, CurvedSegment
from kmlplus.point import Point


class TestLineSegment(TestCase):
    def setUp(self):
        test_point_1 = Point.from_dms('551206.00N', '0045206.234W')
        test_point_2 = Point.from_dms('501206.00N', '0045206.234W')

        self.test_segment = LineSegment(test_point_1, test_point_2)

    def test_get_distance(self):
        # test km
        distance = self.test_segment.get_distance()
        self.assertEqual(556.5977157657558, distance)

        # test miles
        distance = self.test_segment.get_distance(uom='mi')
        self.assertEqual(345.8535719105704, distance)

    def test_get_bearing(self):
        result = self.test_segment.get_bearing()

        self.assertEqual(180, result)


class TestCurvedSegment(TestCase):
    def setUp(self):
        pass

    def test_constructor(self):
        test_point_1 = Point.from_dms('551206.00N', '0045206.234W')
        test_point_2 = Point.from_dms('501206.00N', '0045206.234W')
        cs = CurvedSegment()
        print(cs.centre)
