from unittest import TestCase

from kmlplus import paths, coordinates


class TestPaths(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._origin = coordinates.Coordinate(55.33, -4.33)
        cls._c1 = coordinates.Coordinate("55.3232, -4.11, 0")
        cls._c2 = coordinates.Coordinate(55.22, -4.11, 43)
        cls._c3 = coordinates.Coordinate(55.4345, -4.56356, 12)
        cls._c4 = coordinates.Coordinate(55.22, -48572, 41)

    def setUp(self):
        self._coordinate_list = [self._c1, self._c2, self._c3, self._c4]

    def test_linepath(self):
        line_path = paths.LinePath(*self._coordinate_list)
        self.assertIsInstance(line_path, paths.LinePath)

    def test_centroid(self):
        line_path = paths.LinePath(*self._coordinate_list)
        self.assertIsInstance(line_path.centroid, coordinates.Coordinate)
        self.assertEqual("55.29942, -4.55506, 0", line_path.centroid.__str__())

    def test_height_changes(self):
        line_path = paths.LinePath(*self._coordinate_list, height=500)
        for coordinate in line_path.coordinate_list:
            self.assertEqual(coordinate.height, 500)

    def test_sort(self):
        unsorted_line_path = paths.LinePath(*self._coordinate_list, sort=False)
        sorted_line_path = paths.LinePath(*self._coordinate_list, sort=True)
        a_list = ["55.3232, -4.11", "55.22, -4.11", "55.4345, -4.56356", "55.22, -5.43667"]
        i = 0
        # Assert linepath calling sorted is arranged in anticlockwise order
        self.assertTrue(all(sorted_line_path.coordinate_list[i].bearing_from_centroid >=
                            sorted_line_path.coordinate_list[i+1].bearing_from_centroid
                            for i in range(len(sorted_line_path.coordinate_list)-1)))
        # Assert unsorted line path is ordered in the same order they were passed as arguments
        while i < len(a_list):
            self.assertEqual(a_list[i], unsorted_line_path.coordinate_list[i].to_string_yx())
            i += 1


