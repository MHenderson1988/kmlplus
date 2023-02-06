from unittest import TestCase

from kmlplus.line_segment import ClockwiseCurvedSegment
from kmlplus.point import Point


class TestClockwiseCurvedSegment(TestCase):
    def setUp(self):
        self.test_obj = ClockwiseCurvedSegment(Point.from_dms('551206.00N', '0045206.234W'),
                                               Point.from_dms('501206.00N', '0045206.234W'))

    def test_get_heading_increments(self):
        self.test_obj.get_heading_increments(2)
        pass
