from typing import Union

import simplekml

from kmlplus.geo import PointFactory
from kmlplus.shapes import Polyhedron, Circle, Cylinder, LineString


class KmlPlus:
    """
    KmlPlus is the main class for creating instance 2D and 3D shapes with KML. The class has methods for creating
    Points, LineString, Circle, Cylinder, Polygon and Polyhedron shapes. Each invocation of a function will save and
    update the outputted .kml file.

    Attributes:
        output_path (str): The location to save the created .kml file.
        save_name (str): The name to be given to the .kml file
        kml (simplekml.Kml()): The simpleKml file created.

    Keyword Args:
        output_path (str): The location to save the created .kml file.
        save_name (str): Name for the new file
    """

    def __init__(self, **kwargs):
        self.output_path = kwargs.get('output', None)
        self.save_name = kwargs.get('file_name', 'KmlPlus.kml')
        self.kml = simplekml.Kml()

    def point(self, coordinate_list: list, **kwargs: str) -> None:
        """

        Args:
            coordinate_list (list): A list containing a single coordinate. Z values are to be given
            in metres (M).

        Keyword Args:
            fol (str): A string to name the folder in which the point is stored.
            z (float): The Z value for the point. Default is 0.
            uom (str): The unit of measurement for the Z value. Default is metres (M).
            point_name (str): String to name the point object
            colour_hex (str): String representing a colour hex
            extrude (int): 1 or 0, Whether to extrude the point
            altitude_mode (str): Accepts simplekml Altitude mode options


        Returns:
            None

        """
        if kwargs.get('altitude_mode') == 'relativetoground':
            altitude_mode = simplekml.AltitudeMode.relativetoground
        else:
            altitude_mode = simplekml.AltitudeMode.absolute

        point = PointFactory(coordinate_list, z=kwargs.get('z', None),
                             uom=kwargs.get('uom', 'M')).process_coordinates()

        fol = self.kml.newfolder(name=kwargs.get('fol', 'KmlPlus Point'))

        pnt = fol.newpoint(name=kwargs.get('point_name', 'KmlPlus Point'))
        pnt.coords = [(point[0].x, point[0].y, point[0].z)]
        pnt.style.color = kwargs.get('colour_hex', '7Fc0c0c0')
        pnt.extrude = kwargs.get('extrude', 0)
        pnt.altitudemode = altitude_mode

        self.kml.save(self.save_name)

    def linestring(self, coordinate_list: list, **kwargs: str) -> None:
        """

        Args:
            coordinate_list (list): A list containing a single coordinate
        Keyword Args:
            uom: The unit of measurement for the Z value. Default is metres (M).
            z (int): The Z value for the point. Default is 0.
            fol (str): A string to name the folder in which the point is stored.
            linestring_name (str): String to name the LineString object
            colour_hex (str): String representing a colour hex
            extrude (int): 1 or 0, Whether to extrude the point
            width(int): Line width
            altitude_mode(str): Accepts simplekml Altitude mode options


        Returns:
            None

        """
        fol = self.kml.newfolder(name=kwargs.get('name', 'KmlPlus LineString'))

        linestring = LineString(coordinate_list)

        if kwargs.get('altitude_mode') == 'relativetoground':
            altitude_mode = simplekml.AltitudeMode.relativetoground
        else:
            altitude_mode = simplekml.AltitudeMode.absolute

        s = fol.newlinestring(name=kwargs.get('linestring_name', 'KmlPlus Linestring'))
        s.coords = [(p.x, p.y, p.z) for p in linestring]
        s.style.color = kwargs.get('colour_hex', '7Fc0c0c0')
        s.extrude = kwargs.get('extrude', 0)
        s.style.linestyle.width = kwargs.get('width', 1)
        s.altitudemode = altitude_mode

        self.kml.save(self.save_name)

    def polyhedron(
            self,
            lower_coordinate_list: list,
            upper_coordinate_list: list,
            **kwargs: Union[float, str]
    ) -> None:
        """

        Args:
            lower_coordinate_list: List of coordinates for the lower polygon
            upper_coordinate_list: List of coordinates for the upper polygon
        Keyword Args:
            fol (str): A string to name the folder in which the point is stored.
            lower_polygon_name (str): Lower polygon object name
            upper_polygon_name (str): Upper polygon object name
            lower_layer (str): Lower layer z value
            upper_layer (str): Upper layer z value
            lower_layer_uom (str): Lower layer unit of measure
            upper_layer_uom (str): Upper layer unit of measure
            colour_hex (str): String representing a colour hex
            fill (str): 1 or 0, whether or not to fill the polygon
            outline (str): 1 or 0, whether to include outline of polygon
            extrude (str): 1 or 0, Whether to extrude the point
            altitude_mode (str): Accepts simplekml Altitude mode options

        Returns:
            None
        """
        poly = Polyhedron(
            lower_coordinate_list,
            upper_coordinate_list,
            lower_layer=kwargs.get('lower_layer', None),
            upper_layer=kwargs.get('upper_layer', None),
            lower_layer_uom=kwargs.get('lower_layer_uom', 'M'),
            upper_layer_uom=kwargs.get('upper_layer_uom', 'M')
        )

        lower, upper, sides = poly.to_kml()

        fol = self.kml.newfolder(name=kwargs.get('fol', 'KmlPlus Polyhedron'))

        if kwargs.get('altitude_mode') == 'relativetoground':
            altitude_mode = simplekml.AltitudeMode.relativetoground
        else:
            altitude_mode = simplekml.AltitudeMode.absolute

        lower_pol = fol.newpolygon(name=kwargs.get('lower_polygon_name', 'Lower Polygon'))
        lower_pol.outerboundaryis = lower
        lower_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        lower_pol.polystyle.fill = kwargs.get('fill', 1)
        lower_pol.style.polystyle.outline = kwargs.get('outline', 1)
        lower_pol.extrude = kwargs.get('extrude', 0)
        lower_pol.altitudemode = altitude_mode

        upper_pol = fol.newpolygon(name=kwargs.get('upper_polygon_name', 'Upper Polygon'))
        upper_pol.outerboundaryis = upper
        upper_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        upper_pol.polystyle.fill = kwargs.get('fill', 1)
        upper_pol.style.polystyle.outline = kwargs.get('outline', 1)
        upper_pol.extrude = kwargs.get('extrude', 0)
        upper_pol.altitudemode = altitude_mode

        for coords in sides:
            side_pol = fol.newpolygon(name='KmlPlus Polygon')
            side_pol.outerboundaryis = coords
            side_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
            side_pol.polystyle.fill = kwargs.get('fill', 1)
            side_pol.style.polystyle.outline = kwargs.get('outline', 1)
            side_pol.altitudemode = altitude_mode

        self.kml.save(self.save_name)

    def circle(self, coordinate_list: list, radius: float, **kwargs: str) -> None:
        """

        Args:
            coordinate_list (list): A list containing a single set of coordinates which is the centre point of the circle
            radius (float): The radius of the circle
        Keyword Args:
            z (float): The Z value for the circle. Default is 0.
            fol (str): Name of the folder in which the KML objects are stored.
            name (str): What to name the Circle object
            uom (str): The unit of measurement of z. Accepted arguments are 'FT', 'NM', 'MI', 'KM' and 'M'.
               Defaults to metres
            radius_uom (str): The unit of measurement of the radius. Accepted arguments are 'FT', 'NM', 'MI', 'KM' and 'M'.
               Defaults to metres
            colour_hex (str): String representing a colour hex
            extrude (int): 1 or 0, Whether to extrude the point
            altitude_mode (str): Accepts simplekml Altitude mode options

        Returns:
            None

        """
        if kwargs.get('altitude_mode') == 'relativetoground':
            altitude_mode = simplekml.AltitudeMode.relativetoground
        else:
            altitude_mode = simplekml.AltitudeMode.absolute

        points = Circle(coordinate_list, radius, radius_uom=kwargs.get('radius_uom', 'M'),
                        uom=('uom', 'M')).process_points()

        fol = self.kml.newfolder(name=kwargs.get('fol', 'KmlPlus Circle'))

        pol = fol.newpolygon(name=kwargs.get('name', 'KmlPlus Circle'))
        pol.outerboundaryis = points
        pol.polystyle.colour = kwargs.get('colour_hex', '7Fc0c0c0')
        pol.extrude = kwargs.get('extrude', 0)
        pol.altitudemode = altitude_mode

        self.kml.save(self.save_name)

    def cylinder(self, coordinate_list: list, radius: float, **kwargs: Union[str, int]):
        """

        Args:
            coordinate_list: A list containing a single set of coordinates representing the centre of the circle
            radius: The radius of the circle
        Keyword Args:
            lower_layer (float): Height/Altitude of the lower layer
            upper_layer (float): Height/Altitude of the upper layer
            lower_layer_uom (str): The unit of measurement of the lower layer z. Defaults to metres
            upper_layer_uom (str): The unit of measurement of the upper layer z. Defaults to metres
            sample (int): How many points to use when creating the circles which make up the cylinder
            lower_circle_name (str): Lower circle object name
            upper_circle_name (str): Upper circle object name
            radius_uom (str): Radius unit of measure.
            fol (str): Name of the folder in which the KML objects are stored.
            uom (str): The unit of measurement of the radius. Accepted arguments are 'FT', 'NM', 'MI', 'KM' and 'M'.
              Defaults to 'NM'
            colour_hex (str): String representing a colour hex
            fill (str): 1 or 0, whether or not to fill the polygon
            outline (str): 1 or 0, whether to include outline of polygon
            altitude_mode (str): Accepts simplekml Altitude mode options

        Returns:
            None
        """
        if kwargs.get('altitude_mode') == 'relativetoground':
            altitude_mode = simplekml.AltitudeMode.relativetoground
        else:
            altitude_mode = simplekml.AltitudeMode.absolute

        cylinder = Cylinder(
            (
                coordinate_list,
                radius,
            ),
            (
                coordinate_list,
                radius,
            ),
            radius_uom=kwargs.get('radius_uom', 'M'),
            lower_layer=kwargs.get('lower_layer', None),
            upper_layer=kwargs.get('upper_layer', None),
            lower_layer_uom=kwargs.get('lower_layer_uom', 'FT'),
            upper_layer_uom=kwargs.get('upper_layer_uom', 'FT'),
            sample=kwargs.get('sample', 100), uom=kwargs.get('uom', 'M'),
        )
        lower, upper, sides = cylinder.to_kml()

        fol = self.kml.newfolder(name=kwargs.get('fol', 'KmlPlus Cylinder'))

        lower_pol = fol.newpolygon(name=kwargs.get('lower_circle_name', 'KmlPlus Circle'))
        lower_pol.outerboundaryis = lower
        lower_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        lower_pol.polystyle.fill = kwargs.get('fill', 1)
        lower_pol.style.polystyle.outline = kwargs.get('outline', 1)
        lower_pol.altitudemode = altitude_mode

        upper_pol = fol.newpolygon(name=kwargs.get('upper_name', 'Upper Circle'))
        upper_pol.outerboundaryis = upper
        upper_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
        upper_pol.polystyle.fill = kwargs.get('fill', 1)
        upper_pol.style.polystyle.outline = kwargs.get('outline', 1)
        upper_pol.altitudemode = altitude_mode

        for coords in sides:
            side_pol = fol.newpolygon(name='A side')
            side_pol.outerboundaryis = coords
            side_pol.polystyle.color = kwargs.get('colour_hex', '7Fc0c0c0')
            side_pol.polystyle.fill = kwargs.get('fill', 1)
            side_pol.style.polystyle.outline = kwargs.get('outline', 1)
            side_pol.altitudemode = altitude_mode

        self.kml.save(self.save_name)
