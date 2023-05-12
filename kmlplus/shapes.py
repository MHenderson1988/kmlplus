from abc import abstractmethod, ABC
from collections import deque
from kmlplus.geo import PointFactory, Point, CurvedSegmentFactory


class ICircle(ABC):
    @classmethod
    @abstractmethod
    def create(cls, centre, radius):
        pass


class Circle(ICircle):
    def __init__(self, centre, radius):
        self._centre = centre
        self._radius = radius

    def __eq__(self, another_circle):
        if self.centre and self.radius == another_circle.centre and another_circle.radius:
            return True
        else:
            return False

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


class ICylinder(ABC):
    @abstractmethod
    def generate_sides(self):
        pass


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

    @classmethod
    @abstractmethod
    def create_polygon(cls, coordinate_list):
        pass


class Polygon(IPolygon):
    def __init__(self, point_list):
        self._point_list = point_list

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
    def point_list(self):
        return self._point_list
    
    @point_list.setter
    def point_list(self, a_point_list):
        if len(a_point_list) > 2:
            self._point_list = a_point_list
        else:
            raise ValueError('Cannot create a polygon from less than 2 points')
    
    @classmethod
    def create_polygon(cls, coordinate_list, **kwargs):
        z_override = kwargs.pop('z', None)
        if z_override is not None:
            return cls(PointFactory(coordinate_list, z=z_override).process_coordinates())
        else:
            return cls(PointFactory(coordinate_list).process_coordinates())


class IThreeDimensionShape(ABC):
    @abstractmethod
    def generate_sides(self):
        pass


class Polyhedron(IThreeDimensionShape):
    def __init__(self, lower_polygon, upper_polygon):
        self.lower_polygon = lower_polygon
        self.upper_polygon = upper_polygon
        self.sides = self.generate_sides()

    def generate_sides(self):
        if self.lower_polygon != self.upper_polygon:
            raise IndexError(f'Lower and upper polygon must contain the same amount of points.  Point count - lower'
                             f'polygon: {len(self.lower_polygon)} upper polygon: {len(self.upper_polygon)}')
        else:
            side_coordinates = []
            i = 0
            while i < len(self.lower_polygon)-1:
                side_coordinates.append(self.lower_polygon[i])
                side_coordinates.append(self.lower_polygon[i+1])
                side_coordinates.append(self.upper_polygon[i+1])
                side_coordinates.append(self.upper_polygon[i])
                # Return to the original point
                side_coordinates.append(self.lower_polygon[i])

                i += 1

            # When you reach the last point, join it up to the first
            side_coordinates.append(self.lower_polygon[i])
            side_coordinates.append(self.lower_polygon[0])
            side_coordinates.append(self.upper_polygon[0])
            side_coordinates.append(self.upper_polygon[i])
            # Return to the original point
            side_coordinates.append(self.lower_polygon[i])

            return side_coordinates