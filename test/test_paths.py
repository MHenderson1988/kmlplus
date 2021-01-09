from unittest import TestCase

from kmlplus import paths, coordinates


class TestPaths(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._c1 = coordinates.Coordinate(55.38327, -4.32723)
        cls._c2 = coordinates.Coordinate(52.323, 0.3233)
        cls._c3 = coordinates.Coordinate(554323, -47543, height=20)
        cls._lp = paths.LinePath(cls._c1, cls._c2, cls._c3)
        cls._a1 = paths.ArcPath(cls._c1, start_bearing=100, end_bearing=180, radius=10)

    def test_linepath(self):
        self.assertIsInstance(self._lp, paths.LinePath)
        print(self._lp)

    def test_arcpath(self):
        self.assertIsInstance(self._a1, paths.ArcPath)
        lp = paths.LinePath(self._c1, *self._a1)
        print(lp)
