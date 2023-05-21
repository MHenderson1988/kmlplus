import simplekml

import test_data.airspace
from kmlplus.shapes import Polyhedron, Circle, Cylinder, LineString
from kmlplus.geo import PointFactory


class KmlPlus:
    def __init__(self, save_name, **kwargs):
        self.output_path = kwargs.get('output', None)
        self.save_name = save_name
        self.kml = simplekml.Kml()

    def point(self, coordinate, **kwargs):
        point = PointFactory(coordinate).process_coordinates()

        fol = self.kml.newfolder(name=kwargs.get('name', 'KmlPlus Point'))

        pnt = fol.newpoint(name=kwargs.get('point_name', 'KmlPlus Point'))
        pnt.coords = [(point[0].x, point[0].y, point[0].z)]
        pnt.style.color = kwargs.get('colour_hex', '7Fc0c0c0')
        pnt.extrude = kwargs.get('extrude', 0)
        pnt.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        self.kml.save(self.save_name)

    def linestring(self, coordinate_list, **kwargs):
        fol = self.kml.newfolder(name=kwargs.get('name', 'KmlPlus LineString'))

        linestring = LineString(coordinate_list)

        s = fol.newlinestring(name=kwargs.get('linestring_name', 'KmlPlus Linestring'))
        s.coords = [(p.x, p.y, p.z) for p in linestring]
        s.style.color = kwargs.get('colour_hex', '7Fc0c0c0')
        s.extrude = kwargs.get('extrude', 0)
        s.style.linestyle.width = kwargs.get('width', 1)
        s.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        self.kml.save(self.save_name)

    def polyhedron(self, coordinate_list, **kwargs):
        poly = Polyhedron(coordinate_list, coordinate_list, lower_layer=kwargs.get('lower_layer', None),
                          upper_layer=kwargs.get('upper_layer', None))
        lower, upper, sides = poly.to_kml()

        fol = self.kml.newfolder(name=kwargs.get('fol', 'KmlPlus Polyhedron'))

        lower_pol = fol.newpolygon(name=kwargs.get('lower_name', 'Lower Polygon'))
        lower_pol.outerboundaryis = lower
        lower_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        lower_pol.polystyle.fill = kwargs.get('fill', 1)
        lower_pol.style.polystyle.outline = kwargs.get('outline', 1)
        lower_pol.extrude = kwargs.get('extrude', 0)
        lower_pol.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        upper_pol = fol.newpolygon(name=kwargs.get('upper_name', 'Upper Polygon'))
        upper_pol.outerboundaryis = upper
        upper_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        upper_pol.polystyle.fill = kwargs.get('fill', 1)
        upper_pol.style.polystyle.outline = kwargs.get('outline', 1)
        upper_pol.extrude = kwargs.get('extrude', 0)
        upper_pol.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        for coords in sides:
            side_pol = fol.newpolygon(name='KmlPlus Polygon')
            side_pol.outerboundaryis = coords
            side_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
            side_pol.polystyle.fill = kwargs.get('fill', 1)
            side_pol.style.polystyle.outline = kwargs.get('outline', 1)
            side_pol.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        self.kml.save(self.save_name)

    def circle(self, coordinate, radius, **kwargs):
        points = Circle(coordinate, radius).create()

        fol = self.kml.newfolder(name=kwargs.get('fol', 'KmlPlus Cricle'))

        pol = fol.newpolygon(name=kwargs.get('name'))
        pol.outerboundaryis = points
        pol.polystyle.colour = kwargs.get('colour_hex', '7Fc0c0c0')
        pol.extrude = kwargs.get('extrude', 0)
        pol.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        self.kml.save(self.save_name)

    def cylinder(self, coordinate, radius, **kwargs):

        cylinder = Cylinder((coordinate, radius), (coordinate, radius),
                            lower_layer=kwargs.get('lower_layer', None), upper_layer=kwargs.get('upper_layer', None),
                            sample=kwargs.get('sample', 100), uom=kwargs.get('uom', 'nm'))
        lower, upper, sides = cylinder.to_kml()

        fol = self.kml.newfolder(name=kwargs.get('name', 'KmlPlus Cylinder'))

        lower_pol = fol.newpolygon(name=kwargs.get('lower_circle_name', 'KmlPlus Circle'))
        lower_pol.outerboundaryis = lower
        lower_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        lower_pol.polystyle.fill = kwargs.get('fill', 1)
        lower_pol.style.polystyle.outline = kwargs.get('outline', 1)
        lower_pol.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        upper_pol = fol.newpolygon(name=kwargs.get('upper_name', 'Upper Circle'))
        upper_pol.outerboundaryis = upper
        upper_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        upper_pol.polystyle.fill = kwargs.get('fill', 1)
        upper_pol.style.polystyle.outline = kwargs.get('outline', 1)
        upper_pol.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        for coords in sides:
            side_pol = fol.newpolygon(name='A side')
            side_pol.outerboundaryis = coords
            side_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
            side_pol.polystyle.fill = kwargs.get('fill', 1)
            side_pol.style.polystyle.outline = kwargs.get('outline', 1)
            side_pol.altitudemode = kwargs.get('altitude_mode', simplekml.AltitudeMode.relativetoground)

        self.kml.save(self.save_name)


if __name__ == '__main__':
    kml_file = KmlPlus('Point Styling.kml')

    """kml_file.polyhedron(test_data.airspace.london_fir, lower_layer=19500, upper_layer=24500, name='London FIR')"""

    kml_file.linestring(test_data.airspace.birmingham_cta_9)
    kml_file.cylinder(test_data.airspace.beccles_parachute, 1, upper_layer=5000)
    kml_file.point(test_data.airspace.beccles_parachute)

    kml_file.polyhedron(test_data.airspace.birmingham_cta_10, lower_layer=6500, upper_layer=10500,
                        name='Birmingham CTA 10')
    kml_file.polyhedron(test_data.airspace.birmingham_cta_9, lower_layer=6500, upper_layer=8500,
                        name='Birmingham CTA 9')

    kml_file.polyhedron(test_data.airspace.prestwick_cta_1, lower_layer=1500, upper_layer=5500, name='Prestwick CTA 1')
    kml_file.polyhedron(test_data.airspace.prestwick_cta_2, lower_layer=2000, upper_layer=5500, name='Prestwick CTA 2')
    kml_file.polyhedron(test_data.airspace.prestwick_cta_3, lower_layer=3000, upper_layer=5500, name='Prestwick CTA 3')
    kml_file.polyhedron(test_data.airspace.prestwick_cta_4, lower_layer=3000, upper_layer=5500, name='Prestwick CTA 4')
    kml_file.polyhedron(test_data.airspace.prestwick_cta_5, lower_layer=3500, upper_layer=5500, name='Prestwick CTA 5')
    kml_file.polyhedron(test_data.airspace.prestwick_cta_6, lower_layer=4000, upper_layer=5500, name='Prestwick CTA 6')
    kml_file.polyhedron(test_data.airspace.prestwick_ctr, upper_layer=5500, name='Prestwick CTR')
