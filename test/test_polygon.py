from unittest import TestCase
from kmlplus.polygon import Polygon
from kmlplus.geo import Point


class TestPolygon(TestCase):
    def setUp(self):
        pass

    def test_new_layer(self):
        test_coordinates = ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923']
        result = Polygon(test_coordinates).new_layer()

        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 3)
        for i in result:
            self.assertTrue(isinstance(i, Point))