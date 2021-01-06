from unittest import TestCase

from kmlplus import paths, coordinates


class TestPaths(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._c1 = coordinates.Coordinate(55.38327, -4.32723)
        cls._c2 = coordinates.Coordinate(0, 0)
        cls._c3 = coordinates.Coordinate(554323, -47543, height=20)

    def test_singlelinepath(self):
        lp1 = paths.LinePath(self._c1, self._c2, self._c3)
        print(lp1.kml_format())

    def test_arcpath(self):
        a1 = paths.ArcPath(self._c1, start_bearing=100, end_bearing=180, radius=10)
        print(a1.coordinates_kml_format())
