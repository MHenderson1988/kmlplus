from unittest import TestCase
from kmlplus.point import Point


class TestPoint(TestCase):
    def setUp(self):
        pass
    
    def test_from_dms(self):
        test_obj = Point.from_dms('551206.00N', '0045206.234W')
        self.assertEqual(test_obj.y, 55.20166666666667)
        self.assertEqual(test_obj.x, -4.868398333333333)
        self.assertEqual(test_obj.z, 0)

        test_obj = Point.from_dms('501206.00N', '0045206.234W', z=383)
        self.assertEqual(test_obj.y, 50.20166666666667)
        self.assertEqual(test_obj.x, -4.868398333333333)
        self.assertEqual(test_obj.z, 383)

    def test_from_point_bearing_and_distance(self):
        test_obj = Point.from_dms('551206.00N', '0045206.23W')
        test_result = Point.from_point_bearing_and_distance(test_obj, 180.00, 383.00, uom='km')

        self.assertAlmostEqual(51.756802, test_result.y, delta=0.01)
        self.assertAlmostEqual(-4.868396, test_result.x, delta=0.00001)