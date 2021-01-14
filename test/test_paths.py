from unittest import TestCase

from kmlplus import paths, coordinates


class TestPaths(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._origin = coordinates.Coordinate(55.33, -4.33)
        cls._c1 = coordinates.Coordinate(55.11, -4.11)
        cls._c2 = coordinates.Coordinate(55.22, -4.11)
        cls._c3 = coordinates.Coordinate(55.11, -4.22)
        cls._c4 = coordinates.Coordinate(55.22, -4.22, start_of_arc=True, arc_direction='Clockwise',
                                         arc_origin=cls._origin)
        cls._lp = paths.LinePath(cls._c1, cls._c2, cls._c3, cls._c4, height=6000, sort=True)
        cls._lp2 = paths.LinePath(cls._c1, cls._c2, cls._c3, cls._c4, height=12000, sort=True)
        cls._a1 = paths.ArcPath(cls._c1, start_bearing=100, end_bearing=180, radius=10)

    def test_linepath(self):
        self.assertIsInstance(self._lp, paths.LinePath)
        self._lp.create_sides(self._lp2)
        print(self._lp.sides)

    def test_arcpath(self):
        self.assertIsInstance(self._a1, paths.ArcPath)
        lp = paths.LinePath(self._c1, *self._a1)
