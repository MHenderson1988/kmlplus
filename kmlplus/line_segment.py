import math

from kmlplus.point import Point


class LineSegment:
    def __init__(self, point_1: Point, point_2: Point, **kwargs):
        self.point_1 = point_1
        self.point_2 = point_2

    def __str__(self):
        return f'{type} between {self.point_1.__str__()} and {self.point_2.__str__()}.  Distance of' \
               f' {self.get_distance()} KM.'

    def __eq__(self, other):
        if self.__str__() == other.__str__():
            return True
        else:
            return False

    @property
    def point_1(self):
        return self._point_1

    @point_1.setter
    def point_1(self, point_obj: Point):
        if isinstance(point_obj, Point):
            self._point_1 = point_obj
        else:
            raise TypeError('LineSegment objects only accept Point objects as its arguments')

    @property
    def point_2(self):
        return self._point_2

    @point_2.setter
    def point_2(self, point_obj: Point):
        if isinstance(point_obj, Point):
            self._point_2 = point_obj
        else:
            raise TypeError('LineSegment objects only accept Point objects as its arguments')

    def get_distance(self, **kwargs) -> float:
        radius_dict = {'km': 6378.14, 'mi': 3963.19, 'nm': 3443.91795200126}

        x1, y1, x2, y2 = map(math.radians, [self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y])

        dlon = x2 - x1
        dlat = y2 - y1
        a = math.sin(dlat / 2) ** 2 + math.cos(y1) * math.cos(y2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = radius_dict[kwargs.pop('uom', 'km')]
        distance = c * r

        return distance

    def get_bearing(self) -> float:
        # Convert coordinates to radians
        x1, y1, x2, y2 = map(math.radians, [self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y])

        # Calculate the bearing
        bearing = math.atan2(
            math.sin(x2 - x1) * math.cos(y2),
            math.cos(y1) * math.sin(y2) - math.sin(y1) * math.cos(x1) * math.cos(x2 - x1)
        )

        # Convert bearing to degrees
        bearing = math.degrees(bearing)

        # Make sure bearing is positive
        bearing = (bearing + 360) % 360
        return bearing


class CurvedSegment:
    def __init__(self, start: Point, end: Point, **kwargs):
        self.start = start
        self.end = end
        self.number_of_points = kwargs.pop('points', 100)

    def find_midpoint(self, **kwargs):
        x1, x2 = self.start.x, self.end.y
        y1, y2 = self.start.y, self.end.y

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        return Point(y, x, z=kwargs.pop('z', 0))


class ClockwiseCurvedSegement(CurvedSegment):
    def __init__(self, start: Point, end: Point, **kwargs):
        super().__init__(start, end, **kwargs)


class AntiClockwiseCurvedSegement(CurvedSegment):
    def __init__(self, start: Point, end: Point, **kwargs):
        super().__init__(start, end, **kwargs)
