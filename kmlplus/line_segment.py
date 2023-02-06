from kmlplus.point import Point


class ClockwiseCurvedSegment:
    def __init__(self, start: Point, end: Point, **kwargs: Point):
        self.start = start
        self.end = end
        self.centre = kwargs.pop('centre', Point.find_midpoint(start, end))
        self.start_bearing = self.centre.get_bearing(self.start)
        self.end_bearing = self.centre.get_bearing(self.end)

    def plot_arc_points(self, **kwargs: int):
        # How many plots to point on the arc, default 100.
        num_points = kwargs.pop('num_points', 100)

        pass

    def get_heading_increments(self, num_points):
        difference = (self.end_bearing - self.start_bearing) % 360
        incremental_value = difference / num_points
        return difference