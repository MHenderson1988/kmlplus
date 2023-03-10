from abc import abstractmethod, ABC
from collections import deque
from kmlplus.geo import PointFactory, Point


class Polygon:
    def __init__(self, point_list):
        self.point_list = point_list

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

    def __getitem__(self, item):
        return self.point_list[item]

    def __setitem__(self, item, point):
        if isinstance(point, Point):
            self.point_list[item] = point
        else:
            raise TypeError('Polygon will only accept objects of type kmlplus.geo.Point')

    @classmethod
    def create_polygon(cls, coordinate_list, **kwargs):
        z_override = kwargs.pop('z', None)
        if z_override is not None:
            return cls(PointFactory(coordinate_list, z=z_override).process_coordinates())
        else:
            return cls(PointFactory(coordinate_list).process_coordinates())


class Polyhedron:
    def __init__(self, lower_polygon, upper_polygon, sides):
        self.lower_polygon = lower_polygon
        self.upper_polygon = upper_polygon
        self.sides = sides


    @classmethod
    def generate_polygon(cls, lower_polygon, upper_polygon):
        pass