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
        self._strings_no_height = ["55.213, -4.2342", "821546.12315, 55.122", "22.312,-49281", "55.123, 4.123"]
        self._strings_with_height = ["55.213, -4.2342, 50", "821546.12315, 55.122, -50", "22.312,-49281, 0",
                                     "55.123, 4.123, 100.2"]

    """
    LinePath tests
    """

    def test_linepath(self):
        # Assert LinePath initiates with a list of Coordinate objects
        line_path = paths.LinePath(*self._coordinate_list)
        self.assertIsInstance(line_path, paths.LinePath)

        # Assert LinePath initiates with a single Coordinate object with clockwise direction
        line_path_lower = paths.LinePath(self._c5, arc_points=20)
        actual_length = len(line_path_lower)
        self.assertEqual(actual_length, 20)

        # Asert LinePath initiates with a single Coordinate with default arc-points
        line_path_lower = paths.LinePath(self._c5, arc_points="tRUE")
        self.assertEqual(len(line_path_lower), 50)

        # Assert initiates correctly when reading from a list of stings.  No Coordinate objects present.
        line_path_from_strings = paths.LinePath(*self._strings_no_height)
        for items in line_path_from_strings.coordinate_list:
            self.assertIsInstance(items, coordinates.Coordinate)
        expected_coordinates = [(-4.2342, 55.213, 0.0), (55.122, 82.26281, 0.0), (-5.55583, 22.312, 0.0),
                                (4.123, 55.123, 0.0)]
        self.assertEqual(expected_coordinates, line_path_from_strings.kml_coordinate_list)

        # Assert initiates from list of stings with heights.  No Coordinate objects
        line_path_from_strings = paths.LinePath(*self._strings_with_height)
        for items in line_path_from_strings.coordinate_list:
            self.assertIsInstance(items, coordinates.Coordinate)
        expected_coordinates = [(-4.2342, 55.213, 50.0), (55.122, 82.26281, -50.0), (-5.55583, 22.312, 0.0),
                                (4.123, 55.123, 100.2)]
        self.assertEqual(expected_coordinates, line_path_from_strings.kml_coordinate_list)

        # Assert initiates from a mixture of arguments, coordinate objects AND none coordinate lists of strings.
        # No heights
        lp_from_strings_and_object = paths.LinePath(*self._strings_no_height, self._c4)
        for items in lp_from_strings_and_object.coordinate_list:
            self.assertIsInstance(items, coordinates.Coordinate)
        expected_coordinates = [(-4.2342, 55.213, 0.0), (55.122, 82.26281, 0.0), (-5.55583, 22.312, 0.0),
                                (4.123, 55.123, 0.0), (-5.43667, 55.22, 41.0)]
        self.assertEqual(expected_coordinates, lp_from_strings_and_object.kml_coordinate_list)

        # Assert initiates from a mixture of list of strings and coordinates with heights.
        lp_strings_height_and_object = paths.LinePath(*self._strings_with_height, self._c4)
        for items in lp_strings_height_and_object.coordinate_list:
            self.assertIsInstance(items, coordinates.Coordinate)
        expected_coordinates = [(-4.2342, 55.213, 50.0), (55.122, 82.26281, -50.0), (-5.55583, 22.312, 0.0),
                                (4.123, 55.123, 100.2), (-5.43667, 55.22, 41.0)]
        self.assertEqual(expected_coordinates, lp_strings_height_and_object.kml_coordinate_list)

        # Assert initiates from a mixture of list of strings and coordinates with heights and arc direction.
        lp_strings_height_coordinate_arc = paths.LinePath(*self._strings_with_height, self._c5)
        for items in lp_strings_height_coordinate_arc.coordinate_list:
            self.assertIsInstance(items, coordinates.Coordinate)
        self.assertEqual(lp_strings_height_coordinate_arc.args_list[-1].arc_direction, 'clockwise')
        self.assertEqual(lp_strings_height_coordinate_arc.kml_coordinate_list.__len__(), 54)

        # Assert initial from a mixture of list of string and coordinates with heights, arc direction and with height
        # overridden
        lp_strings_height_coordinate_arc_height_overridden = paths.LinePath(*self._strings_with_height, self._c5,
                                                                            height=400)
        for items in lp_strings_height_coordinate_arc_height_overridden.coordinate_list:
            self.assertEqual(items.height, 400.0)
            self.assertIsInstance(items, coordinates.Coordinate)
        self.assertEqual(lp_strings_height_coordinate_arc_height_overridden.kml_coordinate_list.__len__(), 54)

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
        c1 = coordinates.Coordinate(-43.232, 55.323, 500)
        c2 = coordinates.Coordinate(-43.232, 55.000, 23.2)
        line_path = paths.LinePath(c1, c2, height=500)
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
        c1 = coordinates.Coordinate(-43.232, 55.323, 500)
        c2 = coordinates.Coordinate(-43.232, 55.000, 23.2)
        line_path = paths.LinePath(c1, c2)
        expected = [(55.323, -43.232, 500.0), (55.000, -43.232, 23.2)]
        self.assertEqual(expected, line_path.kml_format())

    def test_create_sides(self):
        # Test for coordinates with 0 height
        coordinate_1, coordinate_2 = coordinates.Coordinate(55.22, -4.11, 0), coordinates.Coordinate(53.12, -3.11, 0)
        # Test for coordinates with varying heights
        c3, c4 = coordinates.Coordinate(55.22, -4.11, 500), coordinates.Coordinate(53.12, -3.11, 900)
        # Test for converting a list into a linepath
        airspace_list = ['11.11, -22.22, 0', '11.12, -22.23, 0']

        lp1 = paths.LinePath(coordinate_1, coordinate_2)
        expected_coordinates = [(-4.11, 55.22, 0.0), (-3.11, 53.12, 0.0)]
        expected_coordinates_upper_layer = [(-4.11, 55.22, 653.2), (-3.11, 53.12, 653.2)]
        expected_sides = [[(-4.11, 55.22, 0.0), (-3.11, 53.12, 0.0), (-3.11, 53.12, 653.2), (-4.11, 55.22, 653.2)],
                          [(-3.11, 53.12, 0.0), (-4.11, 55.22, 0.0), (-4.11, 55.22, 653.2), (-3.11, 53.12, 653.2)]]
        self.assertIsInstance(lp1, paths.LinePath)
        self.assertEqual(expected_coordinates, lp1.kml_coordinate_list)
        for item in lp1.kml_coordinate_list:
            self.assertIsInstance(item, tuple)

        lp2, sides = lp1.create_layer_and_sides(height=653.2)
        self.assertIsInstance(lp2, paths.LinePath)
        self.assertEqual(expected_coordinates_upper_layer, lp2.kml_coordinate_list)
        self.assertEqual(expected_sides, sides)

    def test_sides_deprecated(self):
        lp = paths.LinePath(self._c5)
        expected = "LinePath.sides deprecated since v2.0.  Please use LinePath.create_layer_and_sides()" \
                   " to return a new LinePath layer and sides.  Alternatively call .create_sides() to return" \
                   " a list of sides between this linepath and another."
        self.assertEqual(expected, lp.sides)

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
