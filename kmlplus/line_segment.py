from abc import abstractmethod, ABC

from kmlplus.point import Point


class ICurvedSegment(ABC):
    @abstractmethod
    def get_points(self, **kwargs: int) -> list:
        pass

    @abstractmethod
    def get_bearing_increment(self, num_points: int):
        pass


class ClockwiseCurvedSegment(ICurvedSegment):
    def __init__(self, start: Point, end: Point, **kwargs: Point):
        self.start = start
        self.end = end
        self.centre = kwargs.pop('centre', Point.find_midpoint(start, end))
        self.start_bearing = self.centre.get_bearing(self.start)
        self.end_bearing = self.centre.get_bearing(self.end)

    def get_points(self, **kwargs: int):
        # How many plots to point on the arc, default 100.
        num_points = kwargs.pop('num_points', 100)
        bearing_inc = self.get_bearing_increment(num_points)

        start_bearing = self.centre.get_bearing(self.start)
        distance = self.centre.get_distance(self.start)

        point_list = []

        for n in range(0, 100):
            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance)
            point_list.append(arc_point)
            start_bearing += bearing_inc

        return point_list

    def get_bearing_increment(self, num_points):
        difference = (self.end_bearing - self.start_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (num_points + 1)

        return incremental_value


class AnticlockwiseCurvedSegment(ICurvedSegment):
    def __init__(self, start: Point, end: Point, **kwargs: Point):
        self.start = start
        self.end = end
        self.centre = kwargs.pop('centre', Point.find_midpoint(start, end))
        self.start_bearing = self.centre.get_bearing(self.start)
        self.end_bearing = self.centre.get_bearing(self.end)

    def get_points(self, **kwargs: int):
        # How many plots to point on the arc, default 100.
        num_points = kwargs.pop('num_points', 100)
        bearing_inc = self.get_bearing_increment(num_points)

        start_bearing = self.centre.get_bearing(self.start)
        distance = self.centre.get_distance(self.start)

        point_list = []

        for n in range(0, 100):
            arc_point = Point.from_point_bearing_and_distance(self.centre, start_bearing, distance)
            point_list.append(arc_point)
            start_bearing -= bearing_inc

        return point_list

    def get_bearing_increment(self, num_points):
        difference = (self.start_bearing - self.end_bearing) % 360
        # number points + 1 so it plots points between start and end points
        incremental_value = difference / (num_points + 1)

        return incremental_value
