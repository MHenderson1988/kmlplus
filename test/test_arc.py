from unittest import TestCase

from kmlplus import paths, coordinates

class TestPaths(TestCase):
    def test_singlelinepath(self):
        c1 = coordinates.Coordinate(55.2222, -4.1111, height=55)
        c2 = coordinates.Coordinate(55.3333, -4.1111, height=60)
        c3 = coordinates.Coordinate(55.4444, -4.1111, height=65)
        lp1 = paths.LinePath(c1, c2, c3)
        print(lp1.kml_format())

    def test_arcpath(self):
        c1 = coordinates.Coordinate(55.2222, -4.1111, height=55)
        a1 = paths.ArcPath(c1, start_bearing=100, end_bearing=180, radius=10)
        print(a1.coordinates_kml_format())
