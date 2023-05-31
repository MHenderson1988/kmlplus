from typing import Union

from kmlplus.geo import PointFactory, Point
from kmlplus.interface import ICircle, ILocation, I3DObject, IPolygon, ICylinder, I2DObject


class Circle(ICircle, I2DObject):
    def __init__(self, centre: str, radius, **kwargs):
        self.radius_uom = kwargs.get('radius_uom', 'M')
        self.uom = kwargs.get('uom', 'FT')
        self.z = kwargs.get('z', 0)
        self.sample = kwargs.get('sample', 100)
        self.centre = self.plot_centre(
            centre
        )
        self._radius = radius
        self.point_list = self.process_points()

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
        if isinstance(value, float):
            self._z = value
        else:
            self._z = float(value)

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

    def plot_centre(self, central_location: list) -> ILocation:
        coordinates = PointFactory(central_location, uom=self.uom).process_coordinates()[0]
        return coordinates

    def process_points(self) -> list:
        point_list = []

        start_bearing = 0
        bearing_increment = 360 / self.sample

        for n in range(0, self.sample + 1):
            if self.z:
                z = self.z
            else:
                z = self.centre.z

            point = Point.from_point_bearing_and_distance(self.centre, start_bearing, self.radius, z=z,
                                                          uom=self.uom, radius_uom=self.radius_uom)
            point_list.append(point)
            start_bearing -= bearing_increment

        return point_list

    def to_kml(self) -> list[tuple]:
        point_list = []

        start_bearing = 0
        bearing_increment = 360 / self.sample

        for n in range(0, self.sample + 1):
            point = Point.from_point_bearing_and_distance(self.centre, start_bearing, self.radius, z=self.z)
            point_list.append(point)
            start_bearing -= bearing_increment

        # kml tuples
        circle = [(p.x, p.y, p.z) for p in point_list]

        return circle


class Cylinder(I3DObject, ICylinder):
    def __init__(self, lower_coordinates: list, upper_coordinates: list, **kwargs):
        self.uom = kwargs.get('uom', 'FT')
        self.sample = kwargs.get('sample', 100)
        self.radius_uom = kwargs.get('radius_uom', 'M')
        self.lower_radius = lower_coordinates[1]
        self.upper_radius = upper_coordinates[1]
        self.lower_layer = self.create_layer(
            (lower_coordinates[0], self.lower_radius),
            kwargs.get('lower_layer', None),
            sample=kwargs.get('sample', 100),
            uom=kwargs.get('uom', 'nm')
        )
        self._upper_layer = self.create_layer(
            (upper_coordinates[0], self.upper_radius),
            kwargs.get('upper_layer', None),
            sample=kwargs.get('sample', 100),
            uom=kwargs.get('uom', 'nm')
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
        lower = [(p.x, p.y, p.z) for p in self.lower_layer]
        upper = [(p.x, p.y, p.z) for p in self.upper_layer]
        sides = []

        for polygon in self.sides:
            holding_list = []
            for point_list in polygon:
                holding_list.append((point_list.x, point_list.y, point_list.z))
            sides.append(holding_list)

        return lower, upper, sides

    def create_layer(self, coordinate_list, layer_height, **kwargs) -> ICircle:
        if layer_height:
            circle = Circle(coordinate_list[0], coordinate_list[1], z=layer_height, uom=self.uom)
        else:
            circle = Circle(coordinate_list[0], coordinate_list[1])
        return circle

    def generate_sides(self) -> list:
        if len(self.lower_layer) != len(self.upper_layer):
            raise IndexError(f'Lower and upper polygon must contain the same amount of points.  Point count - lower'
                             f'polygon: {len(self.lower_layer)} upper polygon: {len(self.upper_layer)}')
        else:
            side_coordinates = []
            i = 0
            while i < len(self.lower_layer) - 1:
                polygon_coordinate_list = [self.lower_layer[i].__str__(), self.lower_layer[i + 1].__str__(),
                                           self.upper_layer[i + 1].__str__(), self.upper_layer[i].__str__(),
                                           self.lower_layer[i].__str__()]

                side_coordinates.append(Polygon(polygon_coordinate_list))

                i += 1

            return side_coordinates


class Polygon(IPolygon, I2DObject):
    def __init__(self, point_list: list, **kwargs: str):
        self.uom = kwargs.get('uom', 'FT')
        self.z = kwargs.get('z', None)
        self.point_list = self.process_points(point_list, uom=self.uom)
        self.centroid = self.calculate_centroid()
        self.sorted_point_list = self.point_list

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
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if not value:
            self._z = 0.0
        elif isinstance(value, float):
            self._z = value
        else:
            self.z = float(value)

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

    @property
    def sorted_point_list(self):
        return self._sorted_point_list

    @sorted_point_list.setter
    def sorted_point_list(self, unsorted_point_list):
        self._sorted_point_list = unsorted_point_list.sort(reverse=True,
                                                           key=lambda x: self.calculate_bearing_from_centroid(x))

    def calculate_centroid(self) -> ILocation:
        latitude_total, longitude_total = 0, 0
        for coordinate_instance in self.point_list:
            latitude_total += coordinate_instance.y
            longitude_total += coordinate_instance.x
        latitude_average, longitude_average = latitude_total / len(self.point_list), \
                                              longitude_total / len(self.point_list)

        return Point(latitude_average, longitude_average)

    def calculate_bearing_from_centroid(self, point: ILocation) -> ILocation:
        bearing = point.get_bearing(self.centroid)
        return point

    def process_points(self, point_list: list[ILocation], **kwargs: str) -> list[ILocation]:
        points = PointFactory(
            point_list,
            z=self._z,
            uom=kwargs.get('uom', 'FT')
        ).process_coordinates()

        return points


class Polyhedron(I3DObject):
    def __init__(self, lower_coordinates: list[str], upper_coordinates: list[str], **kwargs: str):
        self.uom = kwargs.get('uom', 'FT')
        self.lower_layer = self.create_layer(lower_coordinates, kwargs.get('lower_layer', None))
        self.upper_layer = self.create_layer(upper_coordinates, kwargs.get('upper_layer', None))
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
        self._upper_layer = a_polygon.sort(reverse=True, key=lambda x: a_polygon.calculate_bearing_from_centroid(x))

    @property
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, sides: list):
        if isinstance(sides, list):
            self._sides = sides
        else:
            raise TypeError('Sides can only be passed in a list')

    def to_kml(self):
        lower = [(p.x, p.y, p.z) for p in self.lower_layer]
        upper = [(p.x, p.y, p.z) for p in self.upper_layer]
        sides = []

        for polygon in self.sides:
            holding_list = []
            for point_list in polygon:
                holding_list.append((point_list.x, point_list.y, point_list.z))
            sides.append(holding_list)

        return lower, upper, sides

    def create_layer(self, coordinate_list, layer_height, **kwargs):
        if layer_height:
            poly = Polygon(coordinate_list, z=layer_height, uom=self.uom)
        else:
            poly = Polygon(coordinate_list)
        return poly

    def generate_sides(self):
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

                side_coordinates.append(Polygon(polygon_coordinate_list))

                i += 1

            return side_coordinates


class LineString(I2DObject):
    def __init__(self, coordinate_list, **kwargs):
        self.uom = kwargs.get('uom', 'FT')
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

    def create(self, coordinate_list):
        point_list = PointFactory(coordinate_list, uom=self.uom).process_coordinates()
        return point_list
