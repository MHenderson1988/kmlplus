import math

import util
from kmlplus.util import dms_to_decimal, detect_coordinate_type


class Point:
    def __init__(self, y, x, **kwargs):
        self.y = y
        self.x = x
        self.z = kwargs.pop('z', 0)

    def __str__(self):
        return f'{__class__} y: {self.y} x: {self.x} z: {self.z}'

    def __eq__(self, other):
        return self.__str__ == other.__str__

    @classmethod
    def from_decimal_degrees(cls, y, x, **kwargs):
        return cls(y, x, z=kwargs.pop('z', 0))

    @classmethod
    def from_dms(cls, y, x, **kwargs):
        y = dms_to_decimal(y)
        x = dms_to_decimal(x)
        return cls(y, x, z=kwargs.pop('z', 0))

    @classmethod
    def from_utm(cls, y, x, **kwargs):
        return cls(y, x, z=kwargs.pop('z', 0))

    @classmethod
    def find_midpoint(cls, point_1, point_2, **kwargs):
        x1, x2 = point_1.x, point_2.x
        y1, y2 = point_1.y, point_2.y

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        return cls(y, x, z=kwargs.pop('z', 0))

    @classmethod
    def from_point_bearing_and_distance(cls, point, bearing: float, distance: float, **kwargs):
        d = distance
        R = util.get_earth_radius(uom=kwargs.pop('uom', 'km'))
        lat1, lon1, brng = map(math.radians, [point.y, point.x, bearing])

        lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                         math.cos(lat1) * math.sin(d / R) * math.cos(brng))

        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                                 math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)

        return cls(lat2, lon2, z=kwargs.pop('z', 0))

    def get_distance(self, another_point, **kwargs: str):
        radius_dict = {'km': 6378.14, 'mi': 3963.19, 'nm': 3443.91795200126}

        x1, y1, x2, y2 = map(math.radians, [self.x, self.y, another_point.x, another_point.y])

        dlon = x2 - x1
        dlat = y2 - y1
        a = math.sin(dlat / 2) ** 2 + math.cos(y1) * math.cos(y2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = radius_dict[kwargs.pop('uom', 'km')]
        distance = c * r

        return distance

    def get_bearing(self, another_point) -> float:
        # Convert coordinates to radians
        x1, y1, x2, y2 = map(math.radians, [self.x, self.y, another_point.x, another_point.y])

        # Calculate the bearing
        bearing = math.atan2(
            math.sin(x2 - x1) * math.cos(y2),
            math.cos(y1) * math.sin(y2) - math.sin(y1) * math.cos(y1) * math.cos(x2 - x1)
        )

        # Convert bearing to degrees
        bearing = math.degrees(bearing)

        # Make sure bearing is positive
        bearing = (bearing + 360) % 360
        return bearing

    def get_inverse_bearing(self, another_point) -> float:
        bearing = self.get_bearing(another_point)
        return (bearing + 180) % 360


class PointFactory:

    @classmethod
    def process_coordinates(cls, coordinate_list):

        def process_string(coordinate_string, coordinate_type):
            type_dict = {'dd': 'from_decimal_degrees', 'dms': 'from_dms'}

            split = coordinate_string.split(', ')
            if len(split) == 2:
                func = getattr(Point, type_dict[coordinate_type])
                return func(split[0], split[1])
            elif len(split) == 3:
                func = getattr(Point, type_dict[coordinate_type])
                return func(split[0], split[1], z=split[2])
            else:
                raise IndexError('Coordinate strings should contain latitude and longitude or latitude, longitude'
                                 'and height only.')

        def populate_point_list(coordinate_list):
            point_list = []
            for i in coordinate_list:
                coordinate_type = detect_coordinate_type(i)
                if coordinate_type == 'dd' or coordinate_type == 'dms':
                    point_obj = process_string(i, coordinate_type)
                    point_list.append(point_obj)
                else:
                    raise TypeError('Coordinates must be DMS, decimal degrees or UTM')

            if len(point_list) > 2:
                return point_list
            else:
                raise ValueError('Cannot create a polygon from less than 2 points')

        return populate_point_list(coordinate_list)
