import math
from abc import ABC, abstractmethod

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
        return f'{__class__} y: {self.y} x: {self.x} z: {self.z}'

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

        x1, y1, x2, y2 = map(math.radians, [self.x, self.y, float(another_point.x), float(another_point.y)])

        dlon = x2 - x1
        dlat = y2 - y1
        a = math.sin(dlat / 2) ** 2 + math.cos(y1) * math.cos(y2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = radius_dict[kwargs.pop('uom', 'km')]
        distance = c * r

        return distance

    def get_bearing(self, another_point) -> float:
        # Convert coordinates to radians
        x1, y1, x2, y2 = map(math.radians, [self.x, self.y, float(another_point.x), float(another_point.y)])

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
                curved_segment_points = CurvedSegmentFactory(i).generate_segment()
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
    def __init__(self, coordinate_string):
        self.coordinate_string = coordinate_string

    def process_segment(self):
        string_dict = util.split_segment_string(self.coordinate_string)
        direction = string_dict.setdefault('direction', 'clockwise')

        # Check coordinate type and create point objects

        if string_dict.get('centre') is not None:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}",
                                   f"{string_dict.get('centre')}"]).process_coordinates()
        else:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}"]).process_coordinates()

        if direction == 'anticlockwise':
            # return an anticlockwise segment
            if string_dict.get('centre') is not None:
                return AnticlockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                                  sample=string_dict.get('sample', 100))
            else:
                return AnticlockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100))
        else:
            if string_dict.get('centre') is not None:
                return ClockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                              sample=string_dict.get('sample', 100))
            else:
                return ClockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100))

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


class ClockwiseCurvedSegment(ICurvedSegment):
    def __init__(self, start: str, end: str, **kwargs):
        self.start = start
        self.end = end
        self.z = kwargs.pop('z', 0)
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

        start_bearing = self.centre.get_bearing(self.start)
        distance = self.centre.get_distance(self.start)

        point_list = []

        for n in range(0, self.sample):
            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance, z=self.z)
            point_list.append(arc_point)
            start_bearing += bearing_inc

        return point_list

    def get_bearing_increment(self):
        difference = (self.end_bearing - self.start_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (self.sample + 1)

        return incremental_value


class AnticlockwiseCurvedSegment(ICurvedSegment):
    def __init__(self, start: str, end: str, **kwargs):
        self.start = start
        self.end = end
        self.z = kwargs.pop('z', 0)
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

        start_bearing = self.centre.get_bearing(self.start)
        distance = self.centre.get_distance(self.start)

        point_list = []

        for n in range(0, self.sample):
            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance, z=self.z)
            point_list.append(arc_point)
            start_bearing -= bearing_inc

        return point_list

    def get_bearing_increment(self):
        difference = (self.start_bearing - self.end_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (self.sample + 1)

        return incremental_value


