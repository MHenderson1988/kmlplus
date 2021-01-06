from unittest import TestCase

from kmlplus import arcpath, coordinates


class TestPaths(TestCase):
    def test_arcpath(self):
        c1 = coordinates.Coordinate(55.2222, -4.1111, height=55)
        a1 = arcpath.ArcPath(c1, start_bearing=100, end_bearing=180, radius=10)
        print(a1.coordinates_to_kml_format())
