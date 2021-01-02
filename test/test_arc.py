from unittest import TestCase

from kmlplus import arc, coordinates


class TestArc(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create classes
        cls._c1 = coordinates.Coordinate(55.38327, -4.32723)
        cls._c2 = coordinates.Coordinate(55.74623, -4.37365)
        cls._c3 = coordinates.Coordinate(55.54645, -4.34564)
        cls._arc1 = arc.Arc(100, 180, cls._c3, "Clockwise")

    def test_calculate_increments(self):
        print(self._arc1.calculate_increments())
