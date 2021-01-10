from unittest import TestCase

from kmlplus import coordinates, paths, floatingpolygon


class TestFloatingpolygon(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._c1 = coordinates.Coordinate(55.38327, -4.32723, height=20)
        cls._c2 = coordinates.Coordinate(55.2222, -4.3333, height=20)
        cls._c3 = coordinates.Coordinate(55.3333, -4.4444, height=20)
        cls._c4 = coordinates.Coordinate(55.38327, -4.32723, height=500)
        cls._c5 = coordinates.Coordinate(55.2222, -4.3333, height=500)
        cls._c6 = coordinates.Coordinate(55.3333, -4.4444, height=500)

    def setUp(self):
        self.ap1 = paths.ArcPath(self._c1, start_bearing=90, end_bearing=120, radius=12)
        self.lp1 = paths.LinePath(self._c1, self._c2, self._c3, *self.ap1)
        self.lp2 = paths.LinePath(self._c4, self._c5, self._c6, *self.ap1)

    def test_same_length(self):
        floating_poly = floatingpolygon.FloatingPolygon(self.lp1, self.lp2)
        print(floating_poly)
