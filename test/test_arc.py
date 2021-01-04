from unittest import TestCase
from kmlplus import paths, coordinates


class TestPaths(TestCase):
    def test_linepath(self):
        c1 = coordinates.Coordinate(55.2222, -4.1111)
        l1 = paths.LinePath(c1)
        print(l1)

    def test_arcpath(self):
        c1 = coordinates.Coordinate(55.2222, -4.1111)
        a1 = paths.ArcPath(c1)
        print(a1)