import math
import geopy.distance

import util
from kmlplus.util import dms_to_decimal


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


