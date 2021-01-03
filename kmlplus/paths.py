from kmlplus import coordinates

"""
The paths class is used to return lists of tuples in the y,x,z format.  y, x, z is the format which is used by .kml as
opposed to the more regular x, y, z format.  Ie - kml requires longitude, latitude, height not latitude, longitude,
height as may appear more logical.

The paths class has two parameters - points and height which default to 50 points and 0 metres respectively.
"""


class Paths:
    def __init__(self, points=50, height=0):
        self._amount_of_points = points
        self._height = height
        self._points_list = self.generate_coordinates()

    """
    Generates a list of coordinate instances representing the points between the start and end heading as projected
    from the central point and radius.  Returns a list of coordinate class instances.
    """

    def generate_coordinates(self):
        coordinate_list = []

        return coordinate_list


class LinePath(Paths):
    def __init__(self, _amount_of_points, _height):
        super(Paths, self).__init__()


"""
The ArcPath class is used to return a tuple list of coordinates in .kml readable format ie - y, x, z.  It accepts the 
following parameters - 

origin - an x, y coordinate string which indicates the central location from which the arc will be drawn.
start_hdg - a heading/bearing relative to the origin from which the arc will commence
end_hdg - a heading/bearing relative to the origin at which the arc will end
radius - the distance from the origin the arc points will be plotted.  Accepts an int or float representing metres.

returns - a list of y, x, z tuples.
"""


class ArcPath(Paths):
    def __init__(self, origin, start_hdg, end_hdg, radius, _amount_of_points, _height):
        super(Paths, self).__init__()
        self._origin = origin
        self._start_hdg = start_hdg
        self._end_hdg = end_hdg
        self._radius = radius
        self._heading_increments = self.calculate_increments()

    """
        TODO - comment
    """

    def generate_coordinates(self):
        coordinate_list = []
        while coordinate_list.__len__() < self._amount_of_points:
            coordinate_list.append(coordinates.generate_coordinates(self._origin, self._radius, self._origin))
            if self._heading_increments == "Clockwise":
                self._start_hdg = (self._start_hdg + self._heading_increments) % 360
            elif self._heading_increments == "Anticlockwise":
                self._start_hdg = (self._start_hdg - self._heading_increments) % 360
        return coordinate_list

    """
       TODO - comment
    """

    def calculate_increments(self):
        if self._end_hdg > self._start:
            difference = (self._end_hdg - self._start) % 360
        else:
            difference = (self._start - self._end_hdg) % 360

        incremental_hdg_value = difference / self._amount_of_points
        return incremental_hdg_value
