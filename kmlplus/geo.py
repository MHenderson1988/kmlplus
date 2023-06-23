from typing import Union

from pyproj import Geod

from kmlplus.interface import ILocation, ILocationFactory, ICurvedSegmentFactory, ICurvedSegment
from kmlplus.util import dms_to_decimal, detect_coordinate_type, split_segment_string, convert_to_metres


class Point(ILocation):
    """
    A class for representing a coordinate using y, x, z representation.

    Attributes:
        y (str): Latitude
        x (str): Longitude

    Keyword Args:
        z (float): Elevation
        uom (str): Unit of measure for elevation. Defaults to Metres
    """
    __slots__ = ('_y', '_x', '_z', 'uom')

    def __init__(self, y: Union[str, float], x: Union[str, float], **kwargs: Union[str, int, float]):
        self.uom = kwargs.get('uom', 'M')
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
        Args:
            value (float)

        Returns:
            z (float)
        """
        return self._z

    @z.setter
    def z(self, value) -> None:
        if isinstance(value, float):
            self._z = convert_to_metres(value, self.uom)
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
        return cls(y, x, z=kwargs.get('z', 0), uom=kwargs.get('uom', 'M'))

    @classmethod
    def from_dms(cls, y: Union[str, float], x: Union[str, float], **kwargs: Union[float, int, str]) -> ILocation:
        """
        Creates a Point object from coordinates in Degrees Minutes Seconds format.

        Args:
            y (str, float): Latitude value
            x (str, float): Longitude value

        Keyword Args:
            z (str, float): Elevation value
            uom (str): Unit of measurement for elevation.

        Returns:
            An ILocation object
        """
        y = dms_to_decimal(y)
        x = dms_to_decimal(x)
        return cls(y, x, z=kwargs.pop('z', 0.0), uom=kwargs.get('uom', 'M'))

    @classmethod
    def find_midpoint(cls, point_1: ILocation, point_2: ILocation, **kwargs: Union[int, float, str]) -> ILocation:
        """
        Args:
            point_1 (Point):
            point_2 (Point):

        Keyword Args:
            z (str, float): Elevation value


        Returns:
            Returns an ILocation object representing the centre between two Point objects.
        """
        x1, x2 = float(point_1.x), float(point_2.x)
        y1, y2 = float(point_1.y), float(point_2.y)

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        return cls(y, x, z=kwargs.pop('z', 0), uom=kwargs.get('uom', 'M'))

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
        g = Geod(ellps='WGS84')
        geo_tup = g.inv(self.x, self.y, another_point.x, another_point.y)
        # PyProj gives distance in metres
        distance = geo_tup[2]

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

    Args:
        coordinate_list (list): A list of strings containing coordinates in DMS or DD

    Keyword Args:
        z_override: A value with which to override all z values given in the string
    """

    __slots__ = ('_coordinate_list', 'z_override', 'uom')

    def __init__(self, coordinate_list: list, **kwargs):
        self.z_override = kwargs.get('z', None)
        self.coordinate_list = coordinate_list
        self.uom = kwargs.get('uom', 'M')

    @property
    def coordinate_list(self) -> list[str]:
        return self._coordinate_list

    @coordinate_list.setter
    def coordinate_list(self, coordinate_list: list[str]) -> None:
        if isinstance(coordinate_list, list):
            self._coordinate_list = coordinate_list
        else:
            self._coordinate_list = [coordinate_list]

    def process_coordinates(self) -> list[ILocation]:
        """
        Processes coordinate list passed to the factory

        Returns:
            point_list (list[ILocation]): A list of ILocation objects
        """
        point_list = self.populate_point_list()
        return point_list

    def populate_point_list(self) -> list[ILocation]:
        """
        Deduces whether the string represents a single point or a curved segment.

        Returns:
            point_list (list[ILocation])
        """

        def is_curved_segment(coordinate_string: str) -> bool:
            if 'start=' in coordinate_string:
                return True
            else:
                return False

        point_list = []
        for i in self.coordinate_list:
            # Check if a curved segment
            if is_curved_segment(i):
                point_list += self.create_curved_segment(i)
            else:
                point_list.append(self.create_new_point(i))

        return point_list

    def create_curved_segment(self, i: str) -> list[ILocation]:
        curved_segment_points = CurvedSegmentFactory(i, z_override=self.z_override, uom=self.uom). \
            generate_segment()

        return curved_segment_points

    def create_new_point(self, i: str) -> ILocation:
        point_obj = self.process_string(i)
        return point_obj

    def process_string(self, coordinate_string: str) -> ILocation:
        """
        Processes a single coordinate string as a single ILocation, ie - not a curved segment.
        Args:
            coordinate_string (str): A coordinate string in DD or DMS
            coordinate_type (str): DD or DMS

        Returns:
            point (ILocation): An ILocation object
        """
        coordinate_type = detect_coordinate_type(coordinate_string)
        type_dict = {'dd': 'from_decimal_degrees', 'dms': 'from_dms'}
        split = coordinate_string.split(' ')

        if coordinate_type == 'dd' or coordinate_type == 'dms':
            func = getattr(Point, type_dict[coordinate_type])
            if len(split) == 2:
                point = self.process_x_y(split, func)
            elif len(split) == 3:
                point = self.process_x_y_z(split, func)
            else:
                raise IndexError('Coordinate strings should contain latitude and longitude or latitude, longitude'
                                 'and height only.')
        else:
            raise ValueError('Coordinates must be Decimal Degrees (DD.ddddd) or Degrees Minutes Seconds (DDMMSS.dd).')

        return point

    def process_x_y(self, split: list[str], func: callable) -> ILocation:
        """
        Processes coordinate strings which only supply latitude and longitude values.
        Args:
            split (list[str]): A list containing the split coordinate string
            func (callable): The function to call to process the string

        Returns:
            point (ILocation): An ILocation object created from the string.
        """
        if self.z_override is not None:
            point = func(split[0], split[1], z=self.z_override, uom=self.uom)
        else:
            point = func(split[0], split[1], uom=self.uom)
        return point

    def process_x_y_z(self, split: list[str], func: callable) -> ILocation:
        """
        Processes coordinate strings which supply latitude, longitude and elevation values.
        Args:
            split (list[str]): A list containing the split coordinate string
            func (callable): The function to call to process the string

        Returns:
            point (ILocation): An ILocation object created from the string.
        """
        if self.z_override is not None:
            point = func(split[0], split[1], z=self.z_override, uom=self.uom)
        else:
            if split[2]:
                point = func(split[0], split[1], z=split[2], uom=self.uom)
            else:
                point = func(split[0], split[1], z=0.0, uom=self.uom)
        return point


class CurvedSegmentFactory(ICurvedSegmentFactory):
    """
    A factory for creating clockwise and anticlockwise curved segments.

    Args:
        coordinate_string (str): A string representing the curved segment

    Keyword Args:
        z_override (float|None): Overrides all z values passed within the string.
    """

    __slots__ = ('coordinate_string', 'z_override', 'uom')

    def __init__(self, coordinate_string: str, **kwargs: str):
        self.coordinate_string = coordinate_string
        self.z_override = kwargs.get('z_override', None)
        self.uom = kwargs.get('uom', 'M')

    def process_segment(self) -> ICurvedSegment:
        """
        Populates all ILocation values within the segment string.

        Returns:
            segment (ICurvedSegment)
        """
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

    def construct_point_list(self, string_dict: dict) -> list[ILocation]:
        """
        Creates each individual ILocation object in the segment.
        Args:
            string_dict (dict): A dict containing start, end and other optional data for the curved segment.

        Returns:
            point_list (list[ILocation])
        """
        if string_dict.get('centre') is not None:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}",
                                       f"{string_dict.get('centre')}"], z=self.z_override,
                                      uom=self.uom).process_coordinates()
        else:
            point_list = PointFactory([f"{string_dict['start']}", f"{string_dict['end']}"],
                                      z=self.z_override, uom=self.uom).process_coordinates()
        return point_list

    def create_clockwise_segment(self, point_list: list, string_dict: dict) -> ICurvedSegment:
        if string_dict.get('centre') is not None:
            segment = ClockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                             sample=string_dict.get('sample', 100), z=self.z_override,
                                             uom=self.uom)
        else:
            segment = ClockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100),
                                             z=self.z_override, uom=self.uom)
        return segment

    def create_anticlockwise_segment(self, point_list: list, string_dict: dict) -> ICurvedSegment:
        if string_dict.get('centre') is not None:
            segment = AnticlockwiseCurvedSegment(point_list[0], point_list[1], centre=point_list[2],
                                                 sample=string_dict.get('sample', 100), z=self.z_override,
                                                 uom=self.uom)
        else:
            segment = AnticlockwiseCurvedSegment(point_list[0], point_list[1], sample=string_dict.get('sample', 100),
                                                 z=self.z_override, uom=self.uom)
        return segment

    def generate_segment(self) -> list[ILocation]:
        segment = self.process_segment()
        segment_points = segment.get_points()

        return segment_points


class ClockwiseCurvedSegment(ICurvedSegment):
    """
    A class for creating curved segments in a clockwise direction.
    """
    __slots__ = ('z', '_start', '_end', '_centre', '_sample', 'start_bearing', 'end_bearing', 'uom')

    def __init__(self, start: ILocation, end: ILocation, **kwargs):
        self.z = kwargs.get('z', None)
        self.start = start
        self.end = end
        self.uom = kwargs.get('uom', 'M')
        self.centre = kwargs.get('centre', self.find_midpoint())
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
    def centre(self) -> ILocation:
        """
        The centre between the start and end ILocations

        Returns:
            centre (ILocation)
        """
        return self._midpoint

    @centre.setter
    def centre(self, value: ILocation):
        if isinstance(value, ILocation):
            self._midpoint = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def sample(self) -> int:
        """
        How many points to sample between the start and end points.
        Returns:
            sample (int)
        """
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

    def find_midpoint(self) -> ILocation:
        """
        Finds the centre between the start and end of the segment.
        Returns:
            centre (ILocation): The centre.
        """
        midpoint = Point.find_midpoint(self.start, self.end)
        return midpoint

    def find_start_bearing(self) -> float:
        """
        Finds the start bearing of the segment

        Returns:
            bearing (float): A bearing in degrees.
        """
        bearing = self.centre.get_bearing(self.start)
        return bearing

    def find_end_bearing(self) -> float:
        """
        As above, except the end bearing

        Returns:
            bearing (float): A bearing in degrees.
        """
        bearing = self.centre.get_bearing(self.end)
        return bearing

    def get_points(self) -> list:
        """
        Creates the individual points of the segment
        Returns:
            point_list (list[ILocation])

        """
        bearing_inc = self.get_bearing_increment()
        height_inc = self.get_height_increment()
        start_bearing = self.start_bearing
        distance = self.centre.get_distance(self.start)
        point_list = []

        for n in range(0, self.sample + 1):
            if self.z is None:
                self.z = self.start.z

            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance, z=self.z,
                                                              uom=self.uom)
            point_list.append(arc_point)
            start_bearing += bearing_inc
            self.z += height_inc

        point_list.append(self.end)

        return point_list

    def get_bearing_increment(self) -> float:
        """
        Calculates how much to increment the bearing value by, depending on the sample size.
        Returns:
            incremental_value (float)

        """
        difference = (self.end_bearing - self.start_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (self.sample + 1)
        return incremental_value

    def get_height_increment(self) -> float:
        """
        If start and end height are different, calculates how much to increment for each point to give a smooth
        transition.

        Returns:
            difference (float)
        """
        if self.start.z > self.end.z:
            difference = -abs(self.start.z - self.end.z) / self.sample
        else:
            difference = abs(self.start.z - self.end.z) / self.sample
        return difference


class AnticlockwiseCurvedSegment(ICurvedSegment):
    """
    Creates an AnticlockwiseCurvedSegment. For documentation, see ClockwiseCurvedSegment.
    """
    __slots__ = ('z', '_start', '_end', '_centre', '_sample', 'start_bearing', 'end_bearing', 'uom')

    def __init__(self, start: ILocation, end: ILocation, **kwargs):
        self.start = start
        self.end = end
        self.z = kwargs.pop('z', None)
        self.uom = kwargs.get('uom', 'M')
        self.centre = kwargs.pop('centre', self.find_midpoint())
        self.sample = kwargs.pop('sample', 100)
        self.start_bearing = self.find_start_bearing()
        self.end_bearing = self.find_end_bearing()

    @property
    def start(self) -> ILocation:
        return self._start

    @start.setter
    def start(self, value: ILocation):
        if isinstance(value, Point):
            self._start = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def end(self) -> ILocation:
        return self._end

    @end.setter
    def end(self, value: ILocation):
        if isinstance(value, Point):
            self._end = value
        else:
            raise TypeError('CurvedSegment will only accept either Point or str for its start.')

    @property
    def centre(self) -> ILocation:
        return self._midpoint

    @centre.setter
    def centre(self, value: ILocation):
        if isinstance(value, Point):
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

    def find_midpoint(self) -> ILocation:
        midpoint = Point.find_midpoint(self.start, self.end)
        return midpoint

    def find_start_bearing(self) -> float:
        bearing = self.centre.get_bearing(self.start)
        return bearing

    def find_end_bearing(self) -> float:
        bearing = self.centre.get_bearing(self.end)
        return bearing

    def get_points(self) -> list:
        # How many plots to point on the arc, default 100.
        bearing_inc = self.get_bearing_increment()
        height_inc = self.get_height_increment()
        start_bearing = self.centre.get_bearing(self.start)
        distance = self.centre.get_distance(self.start)

        point_list = []

        for n in range(0, self.sample + 1):
            if self.z is None:
                self.z = self.start.z

            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance, z=self.z,
                                                              uom=self.uom)
            point_list.append(arc_point)
            start_bearing -= bearing_inc
            self.z += height_inc

        point_list.append(self.end)

        return point_list

    def get_bearing_increment(self) -> float:
        difference = (self.start_bearing - self.end_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (self.sample + 1)
        return incremental_value

    def get_height_increment(self) -> float:
        if self.start.z > self.end.z:
            difference = -abs(self.start.z - self.end.z) / self.sample
        else:
            difference = abs(self.start.z - self.end.z) / self.sample
        return difference
