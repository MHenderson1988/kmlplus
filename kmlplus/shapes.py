from abc import abstractmethod, ABC
from kmlplus.geo import PointFactory, Point, CurvedSegmentFactory


class ICircle(ABC):
    @abstractmethod
    def create(self):
        pass


class Circle(ICircle):
    def __init__(self, centre, radius, **kwargs):
        self._centre = centre
        self._radius = radius
        self._z = kwargs.get('z', 0)
        self._sample = kwargs.get('sample', 100)
        self.points = self.create()

    def __eq__(self, another_circle):
        if self.centre and self.radius == another_circle.centre and another_circle.radius:
            return True
        else:
            return False

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
            raise ValueError('Radius must be greater than 0 and of type float or other type which can be cast to float.')

    def create(self):
        start_point = Point.from_point_bearing_and_distance(Point(self.centre.split(' ')[1], self.centre.split(' ')[0]), 0, self.radius)
        circle = CurvedSegmentFactory(f'start={start_point.y} {start_point.x}, end={start_point.y} {start_point.x}, '
                                      f'centre={self.centre}, sample={self.sample}').generate_segment()
        return circle


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
            self._point_list = a_point_list
        else:
            raise ValueError('Cannot create a polygon from less than 2 points')


class ThreeDimensionShape:
    def __init__(self, lower_coordinates, upper_coordinates, **kwargs):
        self.lower_polygon = self.create_layer(lower_coordinates, kwargs.get('lower_layer', None))
        self.upper_polygon = self.create_layer(upper_coordinates, kwargs.get('lower_layer', None))
        self.sides = self.generate_sides()

    def create_layer(self, coordinate_list, layer_height):
        if layer_height:
            poly = Polygon(coordinate_list, z=layer_height)
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
                side_coordinates.append(
                [
                    self.lower_polygon[i],
                    self.lower_polygon[i + 1],
                    self.upper_polygon[i + 1],
                    self.upper_polygon[i],

                # Return to the original point

                    self.lower_polygon[i]
                ]
            )

                i += 1

            # When you reach the last point, join it up to the first
            side_coordinates.append(
                [
                    self.lower_polygon[i],
                    self.lower_polygon[0],
                    self.upper_polygon[0],
                    self.upper_polygon[i],
                    # Return to the original point
                    self.lower_polygon[i]
                 ]
            )

            return side_coordinates