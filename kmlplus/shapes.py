from abc import abstractmethod, ABC

from kmlplus.geo import PointFactory, Point


class ICircle(ABC):
    @abstractmethod
    def create(self):
        pass


class Circle(ICircle):
    def __init__(self, centre, radius, **kwargs):
        self._centre = PointFactory(centre).process_coordinates()[0]
        self._radius = radius
        self.uom = kwargs.get('uom', 'nm')
        self._z = kwargs.get('z', 0)
        self._sample = kwargs.get('sample', 100)
        self.point_list = self.create()

    def __eq__(self, another_circle):
        if self.centre and self.radius == another_circle.centre and another_circle.radius:
            return True
        else:
            return False

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
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if isinstance(float, value):
            self._z = value
        else:
            self._z = float(value)

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value):
        if isinstance(int, value):
            self._sample = value
        else:
            self._sample = int(value)

    @property
    def centre(self):
        return self._centre

    @centre.setter
    def centre(self, a_point):
        if isinstance(a_point, Point):
            self._centre = a_point
        else:
            raise TypeError('Centre must be passed a kmlplus.geo.Point object.')

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, a_radius):
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

    def create(self):
        point_list = []

        start_bearing = 0
        bearing_increment = 360 / self.sample

        for n in range(0, self.sample + 1):
            point = Point.from_point_bearing_and_distance(self.centre, start_bearing, self.radius, z=self.z,
                                                          uom=self.uom)
            point_list.append(point)
            start_bearing -= bearing_increment

        return point_list

    def to_kml(self):
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


class Cylinder:
    def __init__(self, lower_tuple, upper_tuple, **kwargs):
        self.lower_circle = Circle(lower_tuple[0], lower_tuple[1], z=kwargs.get('lower_layer', None),
                                   sample=kwargs.get('sample', 100), uom=kwargs.get('uom', 'nm'))
        self.upper_circle = Circle(upper_tuple[0], upper_tuple[1], z=kwargs.get('upper_layer', None),
                                   sample=kwargs.get('sample', 100), uom=kwargs.get('uom', 'nm'))
        self._sample = kwargs.get('sample', 100)
        self.uom = kwargs.get('uom', 'Ft')
        self.sides = self.generate_sides()

    @property
    def lower_circle(self):
        return self._lower_polygon

    @lower_circle.setter
    def lower_circle(self, list_of_points):
        self._lower_polygon = list_of_points

    @property
    def upper_circle(self):
        return self._upper_polygon

    @upper_circle.setter
    def upper_circle(self, list_of_points):
        self._upper_polygon = list_of_points

    @property
    def centre(self):
        return self._centre

    @centre.setter
    def centre(self, a_point):
        if isinstance(a_point, Point):
            self._centre = a_point
        else:
            raise TypeError('Centre must be passed a kmlplus.geo.Point object.')

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, a_radius):
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

    def to_kml(self):
        lower = [(p.x, p.y, p.z) for p in self.lower_circle]
        upper = [(p.x, p.y, p.z) for p in self.upper_circle]
        sides = []

        for polygon in self.sides:
            holding_list = []
            for point_list in polygon:
                holding_list.append((point_list.x, point_list.y, point_list.z))
            sides.append(holding_list)

        return lower, upper, sides

    def create_layer(self, coordinate_list, layer_height, **kwargs):
        is_side = kwargs.get('sides', False)
        if is_side:
            circle = [Polygon(x) for x in coordinate_list]
        else:
            if layer_height:
                circle = Circle(self.centre, self.radius, z=layer_height, uom=self.uom)
            else:
                circle = Circle(self.centre, self.radius)
        return circle

    def generate_sides(self):
        if len(self.lower_circle) != len(self.upper_circle.point_list):
            raise IndexError(f'Lower and upper polygon must contain the same amount of points.  Point count - lower'
                             f'polygon: {len(self.lower_circle)} upper polygon: {len(self.upper_circle)}')
        else:
            side_coordinates = []
            i = 0
            while i < len(self.lower_circle) - 1:
                polygon_coordinate_list = [self.lower_circle[i].__str__(), self.lower_circle[i + 1].__str__(),
                                           self.upper_circle[i + 1].__str__(), self.upper_circle[i].__str__(),
                                           self.lower_circle[i].__str__()]

                side_coordinates.append(Polygon(polygon_coordinate_list))

                i += 1

            return side_coordinates


class IPolygon(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    @abstractmethod
    def __setitem__(self, index, point):
        pass

    @abstractmethod
    def __ne__(self, another_polygon):
        pass


class Polygon(IPolygon):
    def __init__(self, point_list, **kwargs):
        self.uom = kwargs.get('uom', 'Ft')
        self._z = kwargs.get('z', None)
        self._point_list = PointFactory(point_list, z=self._z).process_coordinates()

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

    def __ne__(self, another_polygon):
        return self.__len__() != another_polygon.__len__()

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if isinstance(value, float):
            self._z = value
        else:
            self._z = float(value)

    @property
    def point_list(self):
        return self._point_list

    @point_list.setter
    def point_list(self, a_point_list):
        if len(a_point_list) > 2:
            # Close the polygon, if it is not already
            if a_point_list[0] != a_point_list[-1]:
                first_vertice = a_point_list[0]
                a_point_list.append(first_vertice)
            self._point_list = a_point_list

        else:
            raise ValueError('Cannot create a polygon from less than 2 points')

    def calculate_centroid(self):
        latitude_total, longitude_total = 0, 0
        for coordinate_instance in self.point_list:
            latitude_total += coordinate_instance.y
            longitude_total += coordinate_instance.x
        latitude_average, longitude_average = latitude_total / len(self.point_list), \
                                              longitude_total / len(self.point_list)

        return Point(latitude_average, longitude_average)

    def calculate_bearing_from_centroid(self, point):
        return point.get_bearing(self.calculate_centroid())


class Polyhedron:
    def __init__(self, lower_coordinates, upper_coordinates, **kwargs):
        self.uom = kwargs.get('uom', 'Ft')
        self._lower_polygon = self.create_layer(lower_coordinates, kwargs.get('lower_layer', None))
        self._upper_polygon = self.create_layer(upper_coordinates, kwargs.get('upper_layer', None))
        self.sides = self.generate_sides()

    @property
    def lower_polygon(self):
        return self._lower_polygon

    @lower_polygon.setter
    def lower_polygon(self, a_polygon):
        self._lower_polygon = a_polygon.sort(reverse=True, key=lambda x: a_polygon.calculate_bearing_from_centroid(x))

    @property
    def upper_polygon(self):
        return self._upper_polygon

    @upper_polygon.setter
    def upper_polygon(self, a_polygon):
        self._upper_polygon = a_polygon.sort(reverse=True, key=lambda x: a_polygon.calculate_bearing_from_centroid(x))

    def to_kml(self):
        lower = [(p.x, p.y, p.z) for p in self.lower_polygon]
        upper = [(p.x, p.y, p.z) for p in self.upper_polygon]
        sides = []

        for polygon in self.sides:
            holding_list = []
            for point_list in polygon:
                holding_list.append((point_list.x, point_list.y, point_list.z))
            sides.append(holding_list)

        return lower, upper, sides

    def create_layer(self, coordinate_list, layer_height, **kwargs):
        is_side = kwargs.get('sides', False)
        if is_side:
            poly = [Polygon(x) for x in coordinate_list]
        else:
            if layer_height:
                poly = Polygon(coordinate_list, z=layer_height, uom=self.uom)
            else:
                poly = Polygon(coordinate_list)
        return poly

    def generate_sides(self):
        if self.lower_polygon != self.upper_polygon:
            raise IndexError(f'Lower and upper polygon must contain the same amount of points.  Point count - lower'
                             f'polygon: {len(self.lower_polygon)} upper polygon: {len(self.upper_polygon)}')
        else:
            side_coordinates = []
            i = 0
            while i < len(self.lower_polygon) - 1:
                polygon_coordinate_list = [self.lower_polygon[i].__str__(), self.lower_polygon[i + 1].__str__(),
                                           self.upper_polygon[i + 1].__str__(), self.upper_polygon[i].__str__(),
                                           self.lower_polygon[i].__str__()]

                side_coordinates.append(Polygon(polygon_coordinate_list))

                i += 1

            # When you reach the last point, join it up to the first
            # polygon_coordinate_list = [self.lower_circle[i].__str__(), self.lower_circle[0].__str__(), self.upper_circle[0].__str__(), self.upper_circle[i].__str__(), self.lower_circle[i].__str__()]

            # side_coordinates.append(Polygon(polygon_coordinate_list))

            return side_coordinates

class LineString:
    def __init__(self, coordinate_list):
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

    def __ne__(self, another_polygon):
        return self.__len__() != another_polygon.__len__()

    def create(self, coordinate_list):
        point_list = PointFactory(coordinate_list).process_coordinates()
        return point_list