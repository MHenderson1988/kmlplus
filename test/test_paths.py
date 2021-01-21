from unittest import TestCase

from kmlplus import paths, coordinates


class TestPaths(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._origin = coordinates.Coordinate(55.33, -4.33)
        cls._c1 = coordinates.Coordinate("55.3232, -4.11, 0.0")
        cls._c2 = coordinates.Coordinate(55.22, -4.11, 43.0)
        cls._c3 = coordinates.Coordinate(55.4345, -4.56356, 12.0)
        cls._c4 = coordinates.Coordinate(55.22, -48572, 41.0)

        cls._c5 = coordinates.Coordinate("34.232, -50.232323c")

    def setUp(self):
        self._coordinate_list = [self._c1, self._c2, self._c3, self._c4]

    """
    LinePath tests
    """

    def test_linepath(self):
        line_path = paths.LinePath(*self._coordinate_list)
        self.assertIsInstance(line_path, paths.LinePath)

        line_path_lower = paths.LinePath(self._c5, arc_points=20)
        actual_length = len(line_path_lower)
        self.assertEqual(actual_length, 20)

        line_path_lower = paths.LinePath(self._c5, arc_points="tRUE")
        self.assertEqual(len(line_path_lower), 50)

    def test_validate_int(self):
        # Assert that string can be cast to int
        lp = paths.LinePath(self._c5, arc_points="100")
        self.assertEqual(len(lp), 100)

        # Assert float can be cast to int
        lp = paths.LinePath(self._c5, arc_points=6.432983)
        self.assertEqual(len(lp), 6)

        # Assert default value works when not a valid int
        lp = paths.LinePath(self._c5, arc_points="True")
        self.assertEqual(len(lp), 50)

    def test_validate_float(self):
        # Assert string can be cast
        lp = paths.LinePath(self._c5, height="5555")
        self.assertEqual(lp.height, 5555.0)

        # Assert int can be cast
        lp = paths.LinePath(self._c5, height=-5555)
        self.assertEqual(lp.height, -5555.0)

        # Assert String of characters returns None by default
        lp = paths.LinePath(self._c5, height="KLkljfdaklj;dafs")
        self.assertEqual(None, lp.height)

    def test_centroid(self):
        line_path = paths.LinePath(*self._coordinate_list)
        self.assertIsInstance(line_path.centroid, coordinates.Coordinate)
        self.assertEqual("55.29942, -4.55506, 0.0", line_path.centroid.__str__())

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
                            sorted_line_path.coordinate_list[i + 1].bearing_from_centroid
                            for i in range(len(sorted_line_path.coordinate_list) - 1)))
        # Assert unsorted line path is ordered in the same order they were passed as arguments
        while i < len(a_list):
            self.assertEqual(a_list[i], unsorted_line_path.args_list[i].to_string_yx())
            i += 1

    def test_kml_format(self):
        line_path = paths.LinePath(self._c1, self._c2)
        expected = [(-4.11, 55.3232, 0.0), (-4.11, 55.22, 0.0)]
        self.assertEqual(expected, line_path.kml_format())

    def test_create_sides(self):
        coordinate_1 = coordinates.Coordinate(55.22, -4.11, 0)
        coordinate_2 = coordinates.Coordinate(53.12, -3.11, 0)

        line_path_lower = paths.LinePath(coordinate_1, coordinate_2)
        line_path_higher, sides = line_path_lower.create_layer_and_sides(height=50)

        expected = [[(-4.11, 55.22, 0.0), (-3.11, 53.12, 0.0), (-3.11, 53.12, 50.0), (-4.11, 55.22, 50.0)],
                    [(-3.11, 53.12, 0.0), (-4.11, 55.22, 0.0), (-4.11, 55.22, 50.0), (-3.11, 53.12, 50.0)]]

        self.assertEqual(expected, sides)

        """
        ArcPath Tests
        """

    def test_arc_path(self):
        ap = paths.ArcPath(self._origin, 100, 200, 10)
        self.assertIsInstance(ap.origin, coordinates.Coordinate)
        self.assertEqual(ap.start_bearing, 100)
        self.assertEqual(ap.end_bearing, 200)
        self.assertEqual(ap.radius, 10)
        for coord in ap.coordinates:
            self.assertIsInstance(coord, coordinates.Coordinate)

    def test_calculate_heading_increments(self):
        ap = paths.ArcPath(self._origin, 150, 250, 10)
        ap2 = paths.ArcPath(self._origin, 250, 180, 10)
        self.assertEqual(ap.calculate_heading_increments(100, 200), 100 / 50)
        self.assertEqual(ap2.calculate_heading_increments(270, 180), 270 / 50)

    def test_populate_path_list(self):
        ap = paths.ArcPath(self._origin, 150, 250, 10, points=200)
        self.assertIsInstance(ap.coordinates, list)
        for coord in ap.coordinates:
            self.assertIsInstance(coord, coordinates.Coordinate)

    def test_create_layer_and_sides(self):
        line_path = paths.LinePath(*self._coordinate_list)
        line_path_2, sides = line_path.create_layer_and_sides(height=400)
        self.assertIsInstance(line_path_2, paths.LinePath)
        self.assertIsInstance(sides, list)
