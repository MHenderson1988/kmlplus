from unittest import TestCase

from kmlplus import arc, coordinates


class TestArc(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create classes
        cls._c1 = coordinates.Coordinate(55.38327, -4.32723, 0)
        cls._c2 = coordinates.Coordinate(0, 0, 0)
        cls._arc1 = arc.Arc(55)

    def test_calculate_increments(self):
        print()
