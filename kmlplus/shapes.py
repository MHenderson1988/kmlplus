from typing import Union

from kmlplus.geo import PointFactory, Point
from kmlplus.interface import ICircle, ILocation, I3DObject, IPolygon, ICylinder, I2DObject
from kmlplus.util import convert_to_metres


class Circle(ICircle, I2DObject):
    """
    Plots the coordinates for a 2D circular object.

    Args:
        centre (str): A string representing the central coordinate (focus) of the circle.
        radius (float): The radius of the circle to be draw

    Keyword Args:
        radius_uom (str): Unit of measure for the radius. Accepts and defaults to metres ('M'), statute miles ('MI'),
         kilometres ('KM') and nautical miles ('NM')
        uom (str): Unit of measure for elevation. Accepts and defaults to feet ('FT') and metres ('M')
    """
    __slots__ = ('_centre', '_radius', 'uom', '_z', '_sample', 'point_list')

    def __init__(self, centre: list, radius: float, **kwargs):
        self.uom: str = kwargs.get('uom', 'M')
        self.z: float = kwargs.get('z', None)
        self.sample: int = kwargs.get('sample', 100)
        self.centre: ILocation = self.plot_centre(centre)
        self.radius: float = convert_to_metres(radius, kwargs.get('radius_uom', 'M'))
        self.point_list: list[ILocation] = self.process_points()

    def __eq__(self, another_circle: ICircle) -> bool:
        if self.centre and self.radius == another_circle.centre and another_circle.radius:
            return True
        else:
            return False

    def __len__(self) -> int:
        return len(self.point_list)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.point_list):
            result = self.point_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, index):
        return self.point_list[index]

    def __setitem__(self, index, point) -> None:
        if isinstance(point, Point):
            self.point_list[index] = point
        else:
            raise TypeError('Polygon will only accept objects of type kmlplus.geo.Point')

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value):
        if value:
            self._z = float(value)
        else:
            self._z = None

    @property
    def sample(self) -> int:
        return self._sample

    @sample.setter
    def sample(self, value: int) -> None:
        if isinstance(value, int):
            self._sample = value
        else:
            self._sample = int(value)

    @property
    def centre(self) -> ILocation:
        return self._centre

    @centre.setter
    def centre(self, a_point: ILocation):
        if isinstance(a_point, Point):
            self._centre = a_point
        else:
            raise TypeError('Centre must be passed a kmlplus.geo.Point object.')

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, a_radius: Union[float, int, str]):
        if a_radius > 0 and isinstance(a_radius, float):

            self._radius = a_radius
        elif a_radius > 0:
            try:
                converted_radius = float(a_radius)
                self._radius = converted_radius
            except TypeError:
                print('Radius must be a float or type which can be converted to float eg int or string.')
        else:
            raise ValueError(
                'Radius must be greater than 0 and of type float or other type which can be cast to float.')

    def plot_centre(self, central_location: list[str]) -> ILocation:
        """
        Takes the list passed at construction and creates an ILocation object to represent it

        Args:
            central_location (list): List with a single string representing x, y, z coordinate

        Returns:
            coordinates(ILocation): ILocation object representing the focus of the circle.
        """
        coordinates = PointFactory(central_location, uom=self.uom).process_coordinates()[0]
        return coordinates

    def process_points(self) -> list[ILocation]:
        """
        Plots and creates each ILocation point of the circle.

        Returns:
            point_list (list[ILocation]): List of ILocation objects which form the circle.
        """
        point_list = []

        start_bearing = 0
        bearing_increment = 360 / self.sample

        for n in range(0, self.sample + 1):
            if self.z:
                z = self.z
            else:
                z = self.centre.z
                # Change uom to metres as centre has already been converted. Failure to do so will have further
                # calculations performed
                self.uom = 'M'

            point = Point.from_point_bearing_and_distance(self.centre, start_bearing, self.radius, z=z,
                                                          uom=self.uom)
            point_list.append(point)
            start_bearing -= bearing_increment

        return point_list

    def to_kml(self) -> list[tuple]:
        """
        Processes ILocation objects to give kml formatted string output

        Returns:
            circle (list[tuple]): A list of tuples containing x, y, z coordinate strings.
        """
        point_list = []

        start_bearing = 0
        bearing_increment = 360 / self.sample

        for n in range(0, self.sample + 1):
            point = Point.from_point_bearing_and_distance(self.centre, start_bearing, self.radius, z=self.z,
                                                          uom=self.uom)
            point_list.append(point)
            start_bearing -= bearing_increment

        # kml tuples
        circle = [(p.x, p.y, p.z) for p in point_list]

        return circle


class Cylinder(I3DObject, ICylinder):
    """
    Represents a 3D cylindrical object. Top and bottom layers are made up of 2x Circle objects of equal sample size.

    Args:
        lower_coordinates (list[str]): List of string representations of coordinates.
        upper_coordinates (list[str]): List of string representations of coordinates

    Keyword Args:
        radius_uom (str): Unit of measure for the radius. Accepts and defaults to metres ('M'), statute miles ('MI'),
         kilometres ('KM') and nautical miles ('NM')
        uom (str): Unit of measure for elevation. Accepts and defaults to feet ('FT') and metres ('M')
        lower_radius (float): Overrides any radius in the string for the lower circle.
        upper_radius (float): Overrides any radius in the string for the upper circle.
        lower_layer (float): Overrides any elevation in the string for the lower circle.
        upper_layer (float): Overrides any elevation in the string for the upper circle.
        lower_layer_uom (str): Unit of measure for elevation. Defaults to feet ('FT')
        upper_layer_uom (str): Unit of measure for elevation. Defaults to feet ('FT')

    """
    __slots__ = (
        'uom', 'sample', 'radius_uom', '_lower_radius', '_upper_radius', '_upper_layer', '_lower_layer', '_sides')

    def __init__(self, lower_coordinates: list, upper_coordinates: list, **kwargs):
        self.sample = kwargs.get('sample', 100)
        self.radius_uom = kwargs.get('radius_uom', 'M')
        self.lower_radius = lower_coordinates[1]
        self.upper_radius = upper_coordinates[1]
        self.lower_layer = self.create_layer(
            (lower_coordinates[0], self.lower_radius),
            kwargs.get('lower_layer', None),
            kwargs.get('lower_layer_uom', 'M')
        )
        self._upper_layer = self.create_layer(
            (upper_coordinates[0], self.upper_radius),
            kwargs.get('upper_layer', None),
            kwargs.get('upper_layer_uom', 'M')
        )
        self._sides = self.generate_sides()

    @property
    def lower_radius(self) -> float:
        return self._lower_radius

    @lower_radius.setter
    def lower_radius(self, value: float):
        if isinstance(value, (int, float)):
            self._lower_radius = value
        else:
            try:
                value = float(value)
                self.lower_radius = value
            except TypeError:
                print('Radius must be given as float, int or a castable type.')

    @property
    def upper_radius(self) -> float:
        return self._upper_radius

    @upper_radius.setter
    def upper_radius(self, value: float):
        if isinstance(value, (int, float)):
            self._upper_radius = value
        else:
            try:
                value = float(value)
                self.upper_radius = value
            except TypeError:
                print('Radius must be given as float, int or a castable type.')

    @property
    def sides(self) -> list:
        return self._sides

    @sides.setter
    def sides(self, sides: list):
        if isinstance(sides, list):
            self._sides = sides
        else:
            raise TypeError('Sides can only be passed in a list')

    @property
    def lower_layer(self) -> ICircle:
        return self._lower_layer

    @lower_layer.setter
    def lower_layer(self, circle: ICircle):
        if isinstance(circle, ICircle):
            self._lower_layer = circle
        else:
            raise TypeError('Cylinder layers must be type ICircle')

    @property
    def upper_layer(self) -> ICircle:
        return self._upper_layer

    @upper_layer.setter
    def upper_layer(self, circle: ICircle):
        if isinstance(circle, ICircle):
            self._upper_layer = circle
        else:
            raise TypeError('Cylinder layers must be type ICircle')

    def to_kml(self) -> Union[tuple[list, list, list]]:
        """
        Returns kml formatted coordinates in a list for the lower layer, upper layer and sides.
        Returns:
            lower, upper, sides (tuple[list, list, list]): Lists of kml formatted tuples.

        """
        lower = [(p.x, p.y, p.z) for p in self.lower_layer]
        upper = [(p.x, p.y, p.z) for p in self.upper_layer]
        sides = []

        for polygon in self.sides:
            holding_list = []
            for point_list in polygon:
                holding_list.append((point_list.x, point_list.y, point_list.z))
            sides.append(holding_list)

        return lower, upper, sides

    def create_layer(self, coordinate_list: tuple[list[str, float, int]], layer_height, layer_uom) -> ICircle:
        """
        Creates a 2D circle to act as the top or bottom layer of the cylinder
        Args:
            coordinate_list (tuple[list[str, float, int]]): Contains string information for coordinate and radius
            layer_height: The z value of the layer

        Returns:
            circle (ICircle): A circle object
        """
        circle = Circle(coordinate_list[0], coordinate_list[1], z=layer_height,
                        uom=layer_uom, radius_uom=self.radius_uom)
        return circle

    def generate_sides(self) -> list[ICircle]:
        """
        Creates the sides of the cylinder. Requires both layers to contain the same amount of points.

        Returns:
            side_coordinates (list[IPolygon]): A list of polygons joining the upper and lower layers together.

        Raises:
            IndexError: If lower layer and upper layer do not have the same quantity of points.
        """
        if len(self.lower_layer) != len(self.upper_layer):
            raise IndexError(f'Lower and upper polygon must contain the same amount of points.  Point count - lower'
                             f'polygon: {len(self.lower_layer)} upper polygon: {len(self.upper_layer)}')
        else:
            side_coordinates = []
            i = 0
            while i < len(self.lower_layer) - 1:
                polygon_coordinate_list = [self.lower_layer.point_list[i].__str__(), self.lower_layer[i + 1].__str__(),
                                           self.upper_layer[i + 1].__str__(), self.upper_layer[i].__str__(),
                                           self.lower_layer[i].__str__()]

                side_coordinates.append(Polygon(polygon_coordinate_list))

                i += 1

            return side_coordinates


class Polygon(IPolygon, I2DObject):
    """
    Creates a polygon made of 2 or more vertices

    Args:
        coordinate_list (list[str]): A list of strings representing coordinates of vertices.

    Keyword Args:
        uom (str): Unit of measure for elevation, FT or M
        z (float): Override all string elevation values with a single blanket value.
    """
    __slots__ = ('uom', '_z', '_point_list', 'centroid')

    def __init__(self, coordinate_list: list, **kwargs: str):
        self.uom = kwargs.get('uom', 'M')
        self.z = kwargs.get('z', None)
        self.point_list = self.process_points(coordinate_list)
        self.centroid = self.calculate_centroid()

    def __len__(self) -> int:
        return len(self.point_list)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.point_list):
            result = self.point_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, index):
        return self.point_list[index]

    def __setitem__(self, index, point):
        if isinstance(point, Point):
            self.point_list[index] = point
        else:
            raise TypeError('Polygon will only accept objects of type kmlplus.geo.Point')

    def __eq__(self, another_2D_object: I2DObject) -> bool:
        return self.__len__() != another_2D_object.__len__()

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value):
        if value:
            self._z = float(value)
        else:
            self._z = None

    @property
    def point_list(self):
        return self._point_list

    @point_list.setter
    def point_list(self, a_point_list: list):
        if len(a_point_list) > 2 and isinstance(a_point_list, list):
            # Close the polygon, if it is not already
            if a_point_list[0] != a_point_list[-1]:
                first_vertice = a_point_list[0]
                a_point_list.append(first_vertice)
            self._point_list = a_point_list
        else:
            raise ValueError('Cannot process_points a polygon from less than 2 points')

    def calculate_centroid(self) -> ILocation:
        """
        Calculates the centre (centroid) of the polygon's area. This is used for sorting the polygons so that they are
        drawn correctly in Google Earth.

        Returns:
            point (ILocation)
        """
        latitude_total, longitude_total = 0, 0
        for coordinate_instance in self.point_list:
            latitude_total += coordinate_instance.y
            longitude_total += coordinate_instance.x
        latitude_average, longitude_average = latitude_total / len(self.point_list), \
                                              longitude_total / len(self.point_list)

        point = Point(latitude_average, longitude_average, uom=self.uom, z=self.z)
        return point

    def calculate_bearing_from_centroid(self, point: ILocation) -> ILocation:
        """
        Calculates the bearing to the point from the centre of the polygon (Centroid)

        Args:
            point (ILocation): The point to find the bearing to

        Returns:
            bearing (float): The bearing in degrees

        """
        bearing = point.get_bearing(self.centroid)
        return bearing

    def process_points(self, point_list: list[str]) -> list[ILocation]:
        """
        Creates ILocation objects from the list of coordinates supplied.
        Args:
            point_list (list[str]): A list of coordinate information in string format

        Returns:
            points (list[ILocation]): A list of ILocation objects representing the vertices of the polygon
        """
        points = PointFactory(
            point_list,
            z=self._z,
            uom=self.uom
        ).process_coordinates()

        return points


class Polyhedron(I3DObject):
    """
    A Polyhedron (3D object) comprised of a lower layer, upper layer and sides.

    Args:
        lower_coordinates (list[str]): A list of str representation of coordinates.
        upper_coordinates (list[str]): A list of str representation of coordinates.

    Keyword Args:
        uom = Unit of measure for elevation, FT or M
        lower_layer (float): The elevation of the lower layer
        lower_layer_uom (str): Unit of measure for elevation
        upper_layer (float): The elevation of the upper layer
        upper_layer_uom (str): Unit of measure for elevation

    """

    __slots__ = ('uom', '_lower_layer', '_upper_layer', '_sides')

    def __init__(self, lower_coordinates: list[str], upper_coordinates: list[str], **kwargs: str):
        self.lower_layer = self.create_layer(
            lower_coordinates,
            kwargs.get('lower_layer', 0.0),
            kwargs.get('lower_layer_uom', 'M')
        )
        self.upper_layer = self.create_layer(
            upper_coordinates,
            kwargs.get('upper_layer', 0.0),
            kwargs.get('upper_layer_uom', 'M'),
        )
        self.sides = self.generate_sides()

    @property
    def lower_layer(self) -> I2DObject:
        return self._lower_layer

    @lower_layer.setter
    def lower_layer(self, a_polygon: I2DObject):
        if isinstance(a_polygon, I2DObject):
            self._lower_layer = a_polygon
        else:
            raise TypeError('Lower layer must be a type of I2DObject')

    @property
    def upper_layer(self):
        return self._upper_layer

    @upper_layer.setter
    def upper_layer(self, a_polygon):
        self._upper_layer = a_polygon

    @property
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, sides: list):
        if isinstance(sides, list):
            self._sides = sides
        else:
            raise TypeError('Sides can only be passed in a list')

    def create_layer(self, coordinate_list: list[str], layer_height: str, layer_uom) -> IPolygon:
        """
        Creates a layer for the polygon
        Args:
            coordinate_list (list): List containing a string of coordinate information
            layer_height (str): The elevation value of the layer

        Returns:

        """
        if layer_height:
            poly = Polygon(coordinate_list, z=layer_height, uom=layer_uom)
        else:
            poly = Polygon(coordinate_list)
        return poly

    def to_kml(self) -> tuple:
        """
        Processes the upper, lower layers and sides. Converts their data to a KML friendly format.

        Returns:
            lower, upper, sides (tuple):
        """
        lower = [(p.x, p.y, p.z) for p in self.lower_layer]
        upper = [(p.x, p.y, p.z) for p in self.upper_layer]
        sides = []

        for polygon in self.sides:
            holding_list = []
            for point_list in polygon:
                holding_list.append((point_list.x, point_list.y, point_list.z))
            sides.append(holding_list)

        return lower, upper, sides

    def generate_sides(self) -> list[IPolygon]:
        """
        Creates the side polygons to connect the upper and lower layers. Requires upper and lower layers to have
        matching amount of vertices

        Returns:
            side_coordinates (list[IPolygon]): List of polygons which make up the sides of the polyhedron.
        """
        if len(self.lower_layer) != len(self.upper_layer):
            raise IndexError(f'Lower and upper polygon must contain the same amount of points.  Point count - lower '
                             f'polygon: {len(self.lower_layer)} upper polygon: {len(self.upper_layer)}')
        else:
            side_coordinates = []
            i = 0
            while i < len(self.lower_layer) - 1:
                polygon_coordinate_list = [self.lower_layer[i].__str__(), self.lower_layer[i + 1].__str__(),
                                           self.upper_layer[i + 1].__str__(), self.upper_layer[i].__str__(),
                                           self.lower_layer[i].__str__()]

                side_polygon = Polygon(polygon_coordinate_list)

                side_coordinates.append(side_polygon)

                i += 1

            return side_coordinates


class LineString(I2DObject):
    """
    Represents a kml LineString.

    Args:
        coordinate_list (list[str]): A list containing two or more strings representing coordinates

    Keyword Args:
        uom (str): Unit of measure for elevation, FT or M.
    """

    __slots__ = ('uom', '_z', 'point_list')

    def __init__(self, coordinate_list, **kwargs):
        self.uom = kwargs.get('uom', 'M')
        self.z = kwargs.get('z', None)
        self.point_list = self.create(coordinate_list)

    def __len__(self):
        return len(self.point_list)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.point_list):
            result = self.point_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, index):
        return self.point_list[index]

    def __setitem__(self, index, point):
        if isinstance(point, Point):
            self.point_list[index] = point
        else:
            raise TypeError('Polygon will only accept objects of type kmlplus.geo.Point')

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value):
        if value:
            self._z = float(value)
        else:
            self._z = None

    def create(self, coordinate_list: list[str]) -> list[ILocation]:
        point_list = PointFactory(coordinate_list, z=self.z, uom=self.uom).process_coordinates()
        return point_list
