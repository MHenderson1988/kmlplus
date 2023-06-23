from unittest import TestCase

from kmlplus.geo import Point
from kmlplus.shapes import Circle, Polygon, Polyhedron, Cylinder, LineString


class TestCircle(TestCase):
    def setUp(self):
        self.circle_height_args = Circle(['55.1111 -3.2311 10'], 10, sample=100, uom='M')
        self.circle_height_kwargs = Circle(['28.132212 2.332782'], 10, sample=150, z=20, uom='M')
        self.circle_no_height_args = Circle(['55.1111 -3.2311'], 10, sample=100, uom='M')

    def test_create(self):
        self.assertTrue(isinstance(self.circle_height_args.point_list, list))
        self.assertEqual(len(self.circle_height_args.point_list), 101)
        self.assertEqual(self.circle_height_args.point_list[0].z, 10)
        self.assertTrue(isinstance(self.circle_height_args.point_list[2], Point))
        for i in self.circle_height_args.point_list:
            self.assertEqual(10, i.z)

        self.assertTrue(isinstance(self.circle_height_kwargs.point_list, list))
        self.assertEqual(len(self.circle_height_kwargs.point_list), 151)
        self.assertTrue(isinstance(self.circle_height_kwargs.point_list[2], Point))
        self.assertEqual(self.circle_height_kwargs.point_list[0].z, 20)
        for i in self.circle_height_kwargs.point_list:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(i.z, 20)

        # Test uom effects
        c = Circle(['55.1111 -3.2311 10'], 10, sample=100, uom='FT')
        for i in c:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(3.048, i.z)

        c = Circle(['55.1111 -3.2311 10'], 25, z=250, sample=100, uom='M')
        for i in c:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(250, i.z)


class TestCylinder(TestCase):
    def setUp(self):
        self.test_cylinder = Cylinder(
            ['55.1111 -3.2311', 10],
            ['55.1111 -3.2311', 50],
            sample=100,
            radius_uom='NM',
            lower_layer=50,
            upper_layer=100,
            lower_layer_uom='M',
            upper_layer_uom='FT'
        )

    def test_create(self):
        self.assertTrue(isinstance(self.test_cylinder.lower_layer, Circle))
        self.assertTrue(isinstance(self.test_cylinder.upper_layer, Circle))
        self.assertTrue(isinstance(self.test_cylinder.sides, list))
        self.assertEqual(len(self.test_cylinder.sides), 100)
        self.assertTrue(isinstance(self.test_cylinder.sides[0], Polygon))
        self.assertEqual(self.test_cylinder.lower_layer.z, 50)
        self.assertNotEqual(self.test_cylinder.upper_layer.point_list[0].z, 100.0)
        self.assertEqual(self.test_cylinder.upper_layer.point_list[0].z, 30.48)

    def test_lower_radius(self):
        self.assertTrue(isinstance(self.test_cylinder.lower_radius, int))
        self.assertEqual(self.test_cylinder.lower_radius, 10)
        self.assertEqual(self.test_cylinder.radius_uom, 'NM')
        self.assertTrue(isinstance(self.test_cylinder.radius_uom, str))

    def test_upper_radius(self):
        self.assertTrue(isinstance(self.test_cylinder.upper_radius, int))
        self.assertEqual(self.test_cylinder.upper_radius, 50)
        self.assertEqual(self.test_cylinder.radius_uom, 'NM')
        self.assertTrue(isinstance(self.test_cylinder.radius_uom, str))

    def test_sides(self):
        self.assertTrue(isinstance(self.test_cylinder.sides, list))
        self.assertEqual(len(self.test_cylinder.sides), 100)
        self.assertTrue(isinstance(self.test_cylinder.sides[0], Polygon))

    def test_to_kml(self):
        self.assertTrue(isinstance(self.test_cylinder.to_kml(), tuple))
        self.assertEqual(len(self.test_cylinder.to_kml()), 3)
        kml_tup = self.test_cylinder.to_kml()
        for i in kml_tup:
            self.assertTrue(isinstance(i, list))
            for x in kml_tup[0]:
                self.assertTrue(isinstance(x, tuple))
                for y in kml_tup[0][0]:
                    self.assertTrue(isinstance(y, float))

    def test_generate_sides(self):
        self.assertTrue(isinstance(self.test_cylinder.generate_sides(), list))
        self.assertEqual(len(self.test_cylinder.generate_sides()), 100)
        for i in self.test_cylinder.generate_sides():
            self.assertTrue(isinstance(i, Polygon))
            self.assertEqual(len(i), 6)


class TestPolygon(TestCase):
    def setUp(self):
        pass

    def test_new_layer(self):
        test_coordinates_no_height = ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923']
        test_coordinates_with_height = ['22.323232 -4.287282 100', '23.323232 -5.328723 150',
                                        '22.112333 -6.23789238923 200']
        test_coordinates_with_height_override = ['22.323232 -4.287282', '23.323232 -5.328723',
                                                 '22.112333 -6.23789238923']
        test_coordinates_with_cw_arc = ['22.23232 -3.232323 0', 'start=21.23211 -4.122121, end=22.054541 -4.1111, z=15,'
                                                                ' direction=clockwise']
        test_coordinates_with_ccw_arc = ['22.23232 -3.232323 0', 'start=21.23211 -4.122121, end=22.054541 -4.1111, '
                                                                 'z=15, direction=anticlockwise']
        test_dms = ['554433N 0010203W', '443322N 0000102W', '443322N 0010102E']

        # Tests for coordinates with no z value provided. Should default to 0.
        result_no_height = Polygon(test_coordinates_no_height)

        self.assertTrue(isinstance(result_no_height, Polygon))
        self.assertEqual(len(result_no_height), 4)
        for i in result_no_height:
            self.assertNotEqual(i.z, 1.0)
            self.assertEqual(i.z, 0)
            self.assertFalse(i.z)
            self.assertTrue(isinstance(i, Point))

        # Tests for coordinates with a user provided z value.
        result_with_height = Polygon(test_coordinates_with_height)

        self.assertTrue(isinstance(result_with_height, Polygon))
        self.assertEqual(len(result_with_height), 4)
        for i in result_with_height:
            self.assertTrue(isinstance(i, Point))
            self.assertNotEqual(i.z, 0.0)

        # Test results for coordinates with height overridden.
        result_with_height_override = Polygon(test_coordinates_with_height_override, z=500.11)

        self.assertTrue(isinstance(result_with_height_override, Polygon))
        self.assertEqual(len(result_with_height_override), 4)
        for i in result_with_height_override:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(500.11, i.z)

        # Test with DMS
        result_dms_no_height = Polygon(test_dms)
        self.assertTrue(isinstance(result_dms_no_height, Polygon))
        self.assertEqual(4, len(result_dms_no_height))
        for i in result_dms_no_height:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(0, i.z)

        # Test with DD and curved segment
        result_dd_arc = Polygon(test_coordinates_with_cw_arc)
        self.assertTrue(isinstance(result_dd_arc, Polygon))
        self.assertTrue(len(result_dd_arc) > 100)
        for i in result_dd_arc:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(0, i.z)

        result_dd_arc = Polygon(test_coordinates_with_ccw_arc)
        self.assertTrue(isinstance(result_dd_arc, Polygon))
        self.assertTrue(len(result_dd_arc) > 100)
        for i in result_dd_arc:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(0, i.z)


class TestPolyhedron(TestCase):
    def setUp(self) -> None:
        self.poly = Polyhedron(
            ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923'],
            ['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923'],
            lower_layer_uom='FT',
            upper_layer_uom='M',
            upper_layer=100,
            lower_layer=10,
        )

    def test_create(self):
        self.assertTrue(isinstance(self.poly, Polyhedron))
        self.assertEqual(len(self.poly.lower_layer), 4)
        self.assertEqual(len(self.poly.upper_layer), 4)
        self.assertTrue(isinstance(self.poly.lower_layer, Polygon))
        self.assertTrue(isinstance(self.poly.upper_layer, Polygon))

        self.assertTrue(self.poly.lower_layer.z, 3.048)
        self.assertTrue(self.poly.upper_layer.z, 100)

    def test_generate_sides(self):
        self.assertTrue(isinstance(self.poly.generate_sides(), list))
        self.assertEqual(len(self.poly.generate_sides()), 3)
        for i in self.poly.generate_sides():
            self.assertTrue(isinstance(i, Polygon))
            self.assertEqual(len(i), 6)

    def test_to_kml(self):
        self.assertTrue(isinstance(self.poly.to_kml(), tuple))
        for i in self.poly.to_kml():
            self.assertTrue(isinstance(i, list))


class TestLineString(TestCase):
    def setUp(self):
        self.LineString = LineString(['22.323232 -4.287282', '23.323232 -5.328723', '22.112333 -6.23789238923'])
        self.LineString_m = LineString(['22.323232 -4.287282 20', '23.323232 -5.328723 20'], uom='m')
        self.LineString_km = LineString(['22.323232 -4.287282 50', '23.323232 -5.328723 50'], uom='km')
        self.LineString_ft = LineString(['22.323232 -4.287282 20', '23.323232 -5.328723 20'], uom='ft')
        self.LineString_mi = LineString(['22.323232 -4.287282 5', '23.323232 -5.328723 5'], uom='mi')
        self.LineString_nm = LineString(['22.323232 -4.287282 1', '23.323232 -5.328723 1'], uom='nm')

    def test_create(self):
        self.assertTrue(isinstance(self.LineString, LineString))
        self.assertEqual(len(self.LineString), 3)
        for i in self.LineString:
            self.assertTrue(isinstance(i, Point))

        for i in self.LineString_m:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(i.uom, 'm')
            self.assertEqual(i.z, 20)

        for i in self.LineString_km:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(i.uom, 'km')
            self.assertNotEqual(i.z, 50)
            self.assertEqual(i.z, 50000)

        for i in self.LineString_ft:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(i.uom, 'ft')
            self.assertEqual(i.z, 6.096)
            self.assertNotEqual(i.z, 50)

        for i in self.LineString_mi:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(i.uom, 'mi')
            self.assertEqual(i.z, 8046.72)
            self.assertNotEqual(i.z, 5)

        for i in self.LineString_nm:
            self.assertTrue(isinstance(i, Point))
            self.assertEqual(i.uom, 'nm')
            self.assertEqual(i.z, 1852)
            self.assertNotEqual(i.z, 1)


class TestThreeDimensionShape(TestCase):

    def test_generate_sides(self):
        test_list = ['22.323232 -4.287282 20', '23.323232 -5.328723', '22.112333 -6.23789238923',
                     '22.323232 -4.287282 20']
        poly = Polyhedron(test_list, test_list, upper_layer=100)
        self.assertTrue(isinstance(poly, Polyhedron))
        self.assertTrue(isinstance(poly.sides, list))
        self.assertEqual(4, len(poly.sides))

    def test_to_kml(self):
        test_list = ['22.323232 -4.287282 20', '23.323232 -5.328723', '22.112333 -6.23789238923']
        poly = Polyhedron(test_list, test_list, upper_layer=100)
        lower, upper, sides = poly.to_kml()

        self.assertTrue(isinstance(lower, list))
