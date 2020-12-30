from geographiclib.geodesic import Geodesic
from geopy import distance as gp

"""
The arc class provides functionality to return a list of kml friendly coordinates (y, x, z as opposed to the traditional
x, y, z).  It has four parameters - start, end, centre and direction.

Start, end and centre all accept arguments of the coordinate class.  Start represents the coordinates at which to start
populating the list of coordinates and end is the respective point at which to stop.  Direction allows the user to draw
an arc from the start to the end point in the desired direction (clockwise or anticlockwise).  The centre point is the 
reference point (centre) of the arc.
"""


class Arc:
    def __init__(self, start, end, centre, direction):
        self._start = start
        self._end = end
        self._centre = centre
        self._direction = direction

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, coordinate_object):
        self._start = coordinate_object

    @start.deleter
    def start(self):
        del self._start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, coordinate_object):
        self._end = coordinate_object

    @end.deleter
    def end(self):
        del self._end

    @property
    def centre(self):
        return self._centre

    @centre.setter
    def centre(self, coordinate_object):
        self._centre = coordinate_object

    @centre.deleter
    def centre(self):
        del self._centre

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, clockwise_or_anticlockwise):
        self._direction = clockwise_or_anticlockwise

    @direction.deleter
    def direction(self):
        del self._direction
