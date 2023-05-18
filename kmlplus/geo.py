from abc import ABC, abstractmethod

from pyproj import Geod

import util
from kmlplus.util import dms_to_decimal, detect_coordinate_type


class Point:
    def __init__(self, y, x, **kwargs):
        self.y = y
        self.x = x
        self.z = kwargs.pop('z', 0.0)

    def __str__(self):
        return f'{self.y} {self.x} {self.z}'

    def __repr__(self):
        return f'{__class__} x: {self.x} y: {self.y} z: {self.z}'

    def __eq__(self, other):
        return self.__str__ == other.__str__

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if isinstance(value, float):
            self._y = value
        else:
            self._y = float(value)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if isinstance(value, float):
            self._x = value
        else:
            self._x = float(value)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if isinstance(value, float):
            self._z = value
        else:
            if value is None:
                self._z = 0.0
            else:
                self._z = float(value)

    @classmethod
    def from_decimal_degrees(cls, y, x, **kwargs):
        return cls(y, x, z=kwargs.pop('z', 0))

    @classmethod
    def from_dms(cls, y, x, **kwargs):
        y = dms_to_decimal(y)
        x = dms_to_decimal(x)
        return cls(y, x, z=kwargs.pop('z', 0))

    @classmethod
    def find_midpoint(cls, point_1, point_2, **kwargs):
        x1, x2 = float(point_1.x), float(point_2.x)
        y1, y2 = float(point_1.y), float(point_2.y)

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        return cls(y, x, z=kwargs.pop('z', 0))

    @classmethod
    def from_point_bearing_and_distance(cls, point, bearing: float, distance: float, **kwargs):
        radius_dict = {'km': 1000, 'mi': 1609.34, 'nm': 1852, 'm': 1}
        # PyProj gives distance in metres
        distance = distance * radius_dict[kwargs.pop('uom', 'm')]

        g = Geod(ellps='WGS84')
        p = g.fwd(point.x, point.y, az=bearing, dist=distance)

        return cls(p[1], p[0], z=kwargs.pop('z', 0))

    def get_distance(self, another_point, **kwargs: str):
        radius_dict = {'km': 0.001, 'mi': 0.000621371, 'nm': 0.000539957, 'm': 1}
        g = Geod(ellps='WGS84')
        geo_tup = g.inv(self.x, self.y, another_point.x, another_point.y)

        # PyProj gives distance in metres
        distance = geo_tup[2] * radius_dict[kwargs.pop('uom', 'm')]

        return distance

    def get_bearing(self, another_point) -> float:
        g = Geod(ellps='WGS84')
        geo_tup = g.inv(self.x, self.y, another_point.x, another_point.y)
        bearing = geo_tup[0]
        return bearing

    def get_inverse_bearing(self, another_point) -> float:
        g = Geod(ellps='WGS84')
        geo_tup = g.inv(self.x, self.y, another_point.x, another_point.y)
        bearing = geo_tup[1]
        return bearing

    def kml_friendly(self):
        kml_tuple = (self.x, self.y, self.z)
        return kml_tuple


class PointFactory:
    def __init__(self, coordinate_list: list, **kwargs):
        self.coordinate_list = coordinate_list
        self.z_override = kwargs.pop('z', None)

    def process_coordinates(self):
        point_list = self.populate_point_list()
        return point_list

    def populate_point_list(self):

        def is_curved_segment(coordinate_string):
            if 'start=' in coordinate_string:
                return True
            else:
                return False

        point_list = []
        for i in self.coordinate_list:
            # Check if a curved segment
            if is_curved_segment(i):
                curved_segment_points = CurvedSegmentFactory(i, z_override=self.z_override).generate_segment()
                point_list += curved_segment_points
            else:
                coordinate_type = detect_coordinate_type(i)
                if coordinate_type == 'dd' or coordinate_type == 'dms':
                    point_obj = self.process_string(i, coordinate_type)
                    point_list.append(point_obj)
                else:
                    raise TypeError('Coordinates must be DMS, decimal degrees or UTM')

        return point_list

    def process_string(self, coordinate_string, coordinate_type):
        type_dict = {'dd': 'from_decimal_degrees', 'dms': 'from_dms'}

        split = coordinate_string.split(' ')
        if len(split) == 2:
            func = getattr(Point, type_dict[coordinate_type])
            if self.z_override is not None:
                return func(split[0], split[1], z=self.z_override)
            else:
                return func(split[0], split[1])

        elif len(split) == 3:
            func = getattr(Point, type_dict[coordinate_type])
            if self.z_override is not None:
                return func(split[0], split[1], z=self.z_override)
            else:
                return func(split[0], split[1], z=split[2])
        else:
            raise IndexError('Coordinate strings should contain latitude and longitude or latitude, longitude'
                             'and height only.')


class CurvedSegmentFactory:
    def __init__(self, coordinate_string, **kwargs):
        self.coordinate_string = coordinate_string
        self.z_override = kwargs.get('z_override', None)

    def process_segment(self):
        string_dict = util.split_segment_string(self.coordinate_string)
        direction = string_dict.setdefault('direction', 'clockwise')

        # Check coordinate type and create point objects

        if string_dict.get('centre') is not None:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}",
                                       f"{string_dict.get('centre')}"], z=self.z_override).process_coordinates()
        else:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}"],
                                      z=self.z_override).process_coordinates()

        if direction == 'anticlockwise':
            # return an anticlockwise segment
            if string_dict.get('centre') is not None:
                return AnticlockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                                  sample=string_dict.get('sample', 100), z=self.z_override)
            else:
                return AnticlockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100),
                                                  z=self.z_override)
        else:
            if string_dict.get('centre') is not None:
                return ClockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                              sample=string_dict.get('sample', 100),
                                              z=self.z_override)
            else:
                return ClockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100),
                                              z=self.z_override)

    def generate_segment(self):
        segment = self.process_segment()
        segment_points = segment.get_points()

        return segment_points


class ICurvedSegment(ABC):
    @abstractmethod
    def get_points(self) -> list:
        pass

    @abstractmethod
    def get_bearing_increment(self):
        pass

    @abstractmethod
    def get_height_increment(self):
        pass


class ClockwiseCurvedSegment(ICurvedSegment):
    def __init__(self, start: str, end: str, **kwargs):
        self.start = start
        self.end = end
        self.z = kwargs.pop('z', None)
        self.centre = kwargs.pop('centre', Point.find_midpoint(self.start, self.end))
        self.sample = kwargs.pop('sample', 100)
        self.start_bearing = self.centre.get_bearing(self.start)
        self.end_bearing = self.centre.get_bearing(self.end)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, Point):
            self._start = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if isinstance(value, Point):
            self._end = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its centre.')

    @property
    def centre(self):
        return self._centre

    @centre.setter
    def centre(self, value):
        if isinstance(value, Point):
            self._centre = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its centre.')

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value):
        if isinstance(value, int):
            self._sample = value
        elif isinstance(value, str):
            self._sample = int(value)
        else:
            raise TypeError('Sample can only be an int or castable string')

    def get_points(self):
        # How many plots to point on the arc, default 100.
        bearing_inc = self.get_bearing_increment()
        if self.z is None:
            height_inc = self.get_height_increment()
        else:
            height_inc = 0

        start_bearing = self.start_bearing
        distance = self.centre.get_distance(self.start)

        point_list = []

        for n in range(0, self.sample + 1):
            if self.z is None:
                self.z = self.start.z

            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance, z=self.z)
            point_list.append(arc_point)
            start_bearing += bearing_inc
            self.z += height_inc

        point_list.append(self.end)

        return point_list

    def get_bearing_increment(self):
        difference = (self.end_bearing - self.start_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (self.sample + 1)

        return incremental_value

    def get_height_increment(self):
        if self.start.z > self.end.z:
            difference = -abs(self.start.z - self.end.z) / self.sample
            return difference
        else:
            difference = abs(self.start.z - self.end.z) / self.sample
            return difference


class AnticlockwiseCurvedSegment(ICurvedSegment):
    def __init__(self, start: str, end: str, **kwargs):
        self.start = start
        self.end = end
        self.z = kwargs.pop('z', None)
        self.centre = kwargs.pop('centre', Point.find_midpoint(self.start, self.end))
        self.sample = kwargs.pop('sample', 100)
        self.start_bearing = self.centre.get_bearing(self.start)
        self.end_bearing = self.centre.get_bearing(self.end)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, Point):
            self._start = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if isinstance(value, Point):
            self._end = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def centre(self):
        return self._centre

    @centre.setter
    def centre(self, value):
        if isinstance(value, Point):
            self._centre = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value):
        if isinstance(value, str):
            self._sample = int(value)
        elif isinstance(value, int):
            self._sample = value
        else:
            raise TypeError('Sample can only be an int or castable string')

    def get_points(self):
        # How many plots to point on the arc, default 100.
        bearing_inc = self.get_bearing_increment()
        if self.z is None:
            height_inc = self.get_height_increment()
        else:
            height_inc = 0

        start_bearing = self.centre.get_bearing(self.start)
        distance = self.centre.get_distance(self.start)

        point_list = []

        for n in range(0, self.sample + 1):
            if self.z is None:
                self.z = self.start.z

            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance, z=self.z)
            point_list.append(arc_point)
            start_bearing -= bearing_inc
            self.z += height_inc

        point_list.append(self.end)

        return point_list

    def get_bearing_increment(self):
        difference = (self.start_bearing - self.end_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (self.sample + 1)

        return incremental_value

    def get_height_increment(self):
        if self.start.z > self.end.z:
            difference = -abs(self.start.z - self.end.z) / self.sample
            return difference
        else:
            difference = abs(self.start.z - self.end.z) / self.sample
            return difference
