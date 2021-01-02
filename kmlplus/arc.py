"""
It has four parameters - start, end, centre and direction.  It has one optional parameter or points (default 60) which
is how many points will be returned on the arc between the start and end points.

Start, end and centre all accept arguments of the coordinate class.  Start represents the coordinates at which to start
populating the list of coordinates and end is the respective point at which to stop.  Direction allows the user to draw
an arc from the start to the end point in the desired direction (clockwise or anticlockwise).  The centre point is the 
reference point (centre) of the arc.
"""


class Arc:
    def __init__(self, start, end, centre, radius, direction, points=60):
        self._start = start
        self._end = end
        self._centre = centre
        self._radius = radius
        self._direction = direction
        self._amount_of_points = points
        self._heading_increments = self.calculate_increments()

    def list_of_coordinates(self):
        coordinate_list = []

    """
    This function takes three arguments - a starting heading, an end heading and the amount of
    steps to take between the two.  It returns a number which is used to calculate the value to which to 
    increment a heading for x amount of steps.  eg 10 steps between 100 degrees and 200 degrees returns 
    (200-100) / 10 = 
    """
    def calculate_increments(self):
        if self._end > self._start:
            difference = (self._end - self._start) % 360
        else:
            difference = (self._start - self._end) % 360

        incremental_hdg_value = difference / self._amount_of_points
        return incremental_hdg_value

