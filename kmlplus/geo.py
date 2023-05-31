from typing import Union
from pyproj import Geod
from kmlplus.util import dms_to_decimal, detect_coordinate_type, split_segment_string
from kmlplus.interface import ILocation, ILocationFactory, ICurvedSegmentFactory, ICurvedSegment


class Point(ILocation):
    """
    A class for representing a coordinate using y, x, z representation.

    Attributes:
        y (str): Latitude
        x (str): Longitude

    Keyword Args:
        uom (str): Unit of measure to be applied to elevation values.
        z (float): Elevation
    """

    def __init__(self, y: Union[str, float], x: Union[str, float], **kwargs: Union[str, int, float]):
        self.uom = kwargs.get('uom', 'FT')
        self.y: Union[str, float] = y
        self.x: Union[str, float] = x
        self.z: Union[str, float] = kwargs.get('z', 0.0)

    def __str__(self) -> str:
        return f'{self.y} {self.x} {self.z}'

    def __repr__(self) -> str:
        return f'{__class__} x: {self.x} y: {self.y} z: {self.z}'

    def __eq__(self, other) -> bool:
        return self.__str__ == other.__str__

    @property
    def y(self) -> Union[str, float]:
        return self._y

    @y.setter
    def y(self, value) -> None:
        if isinstance(value, float):
            self._y = value
        else:
            self._y = float(value)

    @property
    def x(self) -> Union[str, float]:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        if isinstance(value, float):
            self._x = value
        else:
            self._x = float(value)

    @property
    def z(self) -> Union[str, float]:
        """
        If z value is not a float, casts and then converts to M (KML default uom)

        Args:
            value (float)

        Returns:
            z (float)
        """
        return self._z

    @z.setter
    def z(self, value) -> None:
        if isinstance(value, float):
            conversion_dict = {'FT': 0.3048, 'M': 1}
            self._z = value * conversion_dict[self.uom]
        else:
            if value is None:
                self._z = 0.0
            else:
                self.z = float(value)

    @classmethod
    def from_decimal_degrees(cls, y: Union[str, float], x: Union[str, float], **kwargs: Union[int, float]) -> ILocation:
        """
        Args:
            y (str): Latitude value
            x (str): Longitude value

        Keyword Args:
            z (int | float):

        Returns:
            An ILocation object
        """
        return cls(y, x, z=kwargs.get('z', 0), uom=kwargs.get('uom', 'FT'))

    @classmethod
    def from_dms(cls, y: Union[str, float], x: Union[str, float], **kwargs: Union[float, int, str]) -> ILocation:
        """
        Creates a Point object from coordinates in Degrees Minutes Seconds format.

        Args:
            y (str, float): Latitude value
            x (str, float): Longitude value

        Keyword Args:
            z (str, float): Elevation value
            uom (str): Unit of measurement for elevation

        Returns:
            An ILocation object
        """
        y = dms_to_decimal(y)
        x = dms_to_decimal(x)
        return cls(y, x, z=kwargs.pop('z', 0), uom=kwargs.get('uom', 'FT'))

    @classmethod
    def find_midpoint(cls, point_1: ILocation, point_2: ILocation, **kwargs: Union[int, float, str]) -> ILocation:
        """
        Args:
            point_1 (Point):
            point_2 (Point):

        Keyword Args:
            z (str, float): Elevation value


        Returns:
            Returns an ILocation object representing the midpoint between two Point objects.
        """
        x1, x2 = float(point_1.x), float(point_2.x)
        y1, y2 = float(point_1.y), float(point_2.y)

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        return cls(y, x, z=kwargs.pop('z', 0), uom=kwargs.get('uom', 'FT'))

    @classmethod
    def from_point_bearing_and_distance(cls, point: ILocation, bearing: float, distance: float, **kwargs) -> ILocation:
        """
        Calculates a new Point based upon the bearing and distance from an existing one.

        Args:
            point (Point): A Point object
            bearing (float): A bearing
            distance (float): A distance (Defaults to M)

        Keyword Args:
            distance_uom (str): Unit of measurement for distance. Options - 'M', 'KM, 'MI', 'NM'.

        Returns:
            A Point object at the declared bearing and distance from another Point object.
        """
        radius_dict = {'KM': 1000, 'MI': 1609.34, 'NM': 1852, 'M': 1}
        distance_uom = kwargs.get('distance_uom', 'M')
        conversion_value = radius_dict.get(distance_uom)
        # PyProj gives distance in metres
        distance = distance * conversion_value

        g = Geod(ellps='WGS84')
        p = g.fwd(point.x, point.y, az=bearing, dist=distance)

        return cls(p[1], p[0], z=kwargs.get('z', 0), uom=kwargs.get('uom', 'M'))

    def get_distance(self, another_point: ILocation, **kwargs: str) -> float:
        """
        Calculates the distance between two points.
        Args:
            another_point (Point): A Point object.

        Keyword Args:
            distance_uom (str): Unit of measurement for distance. Options - 'M', 'KM, 'MI', 'NM'.

        Returns:
            distance (float): The distance between two points.

        """
        radius_dict = {'KM': 1000, 'MI': 1609.34, 'NM': 1852, 'M': 1}
        conversion_value = radius_dict.get(kwargs.get('distance_uom'), 1)
        g = Geod(ellps='WGS84')
        geo_tup = g.inv(self.x, self.y, another_point.x, another_point.y)

        # PyProj gives distance in metres
        distance = geo_tup[2] * conversion_value

        return distance

    def get_bearing(self, another_point: ILocation) -> float:
        """
        Calculates the bearing between one kmlplus.geo.Point object and another.

        Args:
            another_point (kmlplus.geo.Point): kmlplus.geo.Point object.

        Returns:
            bearing (float): The bearing between two points
        """
        g = Geod(ellps='WGS84')
        geo_tup = g.inv(self.x, self.y, another_point.x, another_point.y)
        bearing = geo_tup[0]
        return bearing

    def get_inverse_bearing(self, another_point: ILocation) -> float:
        """
        Calculates the inverse bearing between one kmlplus.geo.Point object and another.

        Args:
            another_point (kmlplus.geo.Point): kmlplus.geo.Point object.

        Returns:
            bearing (float): The inverse bearing between two points
        """
        g = Geod(ellps='WGS84')
        geo_tup = g.inv(self.x, self.y, another_point.x, another_point.y)
        bearing = geo_tup[1]
        return bearing

    def kml_friendly(self) -> tuple:
        kml_tuple = (self.x, self.y, self.z)
        return kml_tuple


class PointFactory(ILocationFactory):
    """
    A class which interprets how to handle the coordinate strings provided. It deduces between DMS/DD and straight
    or curved lines.
    """

    def __init__(self, coordinate_list: list, **kwargs):
        self.uom = kwargs.get('uom', 'FT')
        self.z_override = kwargs.get('z', None)
        self.coordinate_list = coordinate_list

    @property
    def coordinate_list(self) -> list:
        return self._coordinate_list

    @coordinate_list.setter
    def coordinate_list(self, coordinate_list: list) -> None:
        if isinstance(coordinate_list, list):
            self._coordinate_list = coordinate_list
        else:
            self._coordinate_list = [coordinate_list]

    def process_coordinates(self) -> list:
        point_list = self.populate_point_list()
        return point_list

    def populate_point_list(self) -> list:

        def is_curved_segment(coordinate_string: str) -> bool:
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

    def process_string(self, coordinate_string: str, coordinate_type: str) -> ILocation:
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
                return func(split[0], split[1], z=split[2], uom=self.uom)
        else:
            raise IndexError('Coordinate strings should contain latitude and longitude or latitude, longitude'
                             'and height only.')


class CurvedSegmentFactory(ICurvedSegmentFactory):
    """
    A factory for creating clockwise and anticlockwise curved segments.
    """

    def __init__(self, coordinate_string: str, **kwargs: str):
        self.coordinate_string = coordinate_string
        self.z_override = kwargs.get('z_override', None)

    def process_segment(self) -> ICurvedSegment:
        string_dict = split_segment_string(self.coordinate_string)
        direction = string_dict.setdefault('direction', 'clockwise')

        # Check coordinate type and process_points point objects

        point_list = self.construct_point_list(string_dict)

        if direction == 'anticlockwise':
            # return an anticlockwise segment
            segment = self.create_anticlockwise_segment(point_list, string_dict)
        else:
            segment = self.create_clockwise_segment(point_list, string_dict)

        return segment

    def construct_point_list(self, string_dict):
        if string_dict.get('midpoint') is not None:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}",
                                       f"{string_dict.get('midpoint')}"], z=self.z_override).process_coordinates()
        else:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}"],
                                      z=self.z_override).process_coordinates()
        return point_list

    def create_clockwise_segment(self, point_list, string_dict):
        if string_dict.get('midpoint') is not None:
            segment = ClockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                             sample=string_dict.get('sample', 100),
                                             z=self.z_override)
        else:
            segment = ClockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100),
                                             z=self.z_override)
        return segment

    def create_anticlockwise_segment(self, point_list, string_dict):
        if string_dict.get('midpoint') is not None:
            segment = AnticlockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                                 sample=string_dict.get('sample', 100), z=self.z_override)
        else:
            segment = AnticlockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100),
                                                 z=self.z_override)
        return segment

    def generate_segment(self) -> list:
        segment = self.process_segment()
        segment_points = segment.get_points()

        return segment_points


class ClockwiseCurvedSegment(ICurvedSegment):
    """
    A class for creating curved segments in a clockwise direction.
    """

    def __init__(self, start: ILocation, end: ILocation, **kwargs):
        self.z = kwargs.get('z', None)
        self.start = start
        self.end = end
        self.midpoint = kwargs.get('midpoint', self.find_midpoint())
        self.sample = kwargs.get('sample', 100)
        self.start_bearing = self.find_start_bearing()
        self.end_bearing = self.find_end_bearing()

    @property
    def start(self) -> ILocation:
        return self._start

    @start.setter
    def start(self, value: ILocation):
        if isinstance(value, ILocation):
            self._start = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def end(self) -> ILocation:
        return self._end

    @end.setter
    def end(self, value: ILocation):
        if isinstance(value, ILocation):
            self._end = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def midpoint(self) -> ILocation:
        return self._midpoint

    @midpoint.setter
    def midpoint(self, value: ILocation):
        if isinstance(value, ILocation):
            self._midpoint = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def sample(self) -> int:
        return self._sample

    @sample.setter
    def sample(self, value: int):
        if isinstance(value, int):
            self._sample = value
        else:
            try:
                self.sample = int(value)
            except TypeError:
                print('Sample can only be an int or castable string')

    def find_midpoint(self):
        p = Point.find_midpoint(self.start, self.end)
        return p

    def find_start_bearing(self):
        bearing = self.midpoint.get_bearing(self.start)
        return bearing

    def find_end_bearing(self):
        bearing = self.midpoint.get_bearing(self.end)
        return bearing

    def get_points(self):
        # How many plots to point on the arc, default 100.
        bearing_inc = self.get_bearing_increment()
        if self.z is None:
            height_inc = self.get_height_increment()
        else:
            height_inc = 0

        start_bearing = self.start_bearing
        distance = self.midpoint.get_distance(self.start)

        point_list = []

        for n in range(0, self.sample + 1):
            if self.z is None:
                self.z = self.start.z

            arc_point = Point.from_point_bearing_and_distance(self.midpoint, start_bearing, distance, z=self.z)
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
        self.midpoint = kwargs.pop('midpoint', self.find_midpoint())
        self.sample = kwargs.pop('sample', 100)
        self.start_bearing = self.find_start_bearing()
        self.end_bearing = self.find_end_bearing()

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
    def midpoint(self):
        return self._midpoint

    @midpoint.setter
    def midpoint(self, value):
        if isinstance(value, Point):
            self._midpoint = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value: int):
        if isinstance(value, int):
            self._sample = value
        else:
            try:
                self.sample = int(value)
            except TypeError:
                print('Sample can only be an int or castable string')

    def find_midpoint(self):
        p = Point.find_midpoint(self.start, self.end)
        return p

    def find_start_bearing(self):
        bearing = self.midpoint.get_bearing(self.start)
        return bearing

    def find_end_bearing(self):
        bearing = self.midpoint.get_bearing(self.end)
        return bearing

    def get_points(self):
        # How many plots to point on the arc, default 100.
        bearing_inc = self.get_bearing_increment()
        if self.z is None:
            height_inc = self.get_height_increment()
        else:
            height_inc = 0

        start_bearing = self.midpoint.get_bearing(self.start)
        distance = self.midpoint.get_distance(self.start)

        point_list = []

        for n in range(0, self.sample + 1):
            if self.z is None:
                self.z = self.start.z

            arc_point = Point.from_point_bearing_and_distance(self.midpoint, start_bearing, distance, z=self.z)
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
