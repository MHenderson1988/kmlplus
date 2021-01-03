from kmlplus import coordinates

"""
The paths class is used to return lists of tuples in the y,x,z format.  y, x, z is the format which is used by .kml as
opposed to the more regular x, y, z format.  Ie - kml requires longitude, latitude, height not latitude, longitude,
height as may appear more logical.

The paths class has two parameters - points and height which default to 50 points and 0 metres respectively.
"""


class LinePath:
    def __init__(self, origin, points=50, height=0):
        self._origin = origin
        self._amount_of_points = points
        self._height = height
        self._points_list = self.generate_coordinates()

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, coordinate_instance):
        assert isinstance(coordinate_instance, coordinates.Coordinate), "Error: LinePath origin must be an instance " \
                                                                        "of type Coordinate "
        self._origin = coordinate_instance

    @property
    def amount_of_points(self):
        return self._amount_of_points

    @amount_of_points.setter
    def amount_of_points(self, a_int: int):
        assert type(a_int) is int, "Amount of points attribute only accepts whole numbers (int)"
        self._amount_of_points = a_int

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, a_value: float or int):
        assert type(a_value) is float or type(a_value) is int, "Height value only accepts type float or int"
        self._height = a_value

    """
    Generates a list of coordinate instances representing the points between the start and end heading as projected
    from the central point and radius.  Returns a list of coordinate class instances.
    """

    def generate_coordinates(self, a_destination_string, final_height):
        assert type(a_destination_string) is str, "Error: Coordinates for must be a string eg - '''55.2123, " \
                                                  "-4.43783''' or an instance of the Coordinate class "
        coordinate_list = []

        return coordinate_list


"""
The ArcPath class is used to return a tuple list of coordinates in .kml readable format ie - y, x, z.  It accepts the 
following parameters - 

origin - an x, y coordinate string which indicates the central location from which the arc will be drawn.
start_hdg - a heading/bearing relative to the origin from which the arc will commence
end_hdg - a heading/bearing relative to the origin at which the arc will end
radius - the distance from the origin the arc points will be plotted.  Accepts an int or float representing metres.

returns - a list of y, x, z tuples.
"""


class ArcPath(LinePath):
    def __init__(self, origin, start_hdg, end_hdg, radius, direction, points=50, height=0):
        self._origin = origin
        self._start_hdg = start_hdg
        self._end_hdg = end_hdg
        self._radius = radius
        self._direction = direction
        self._points = points
        self._height = height
        self._heading_increments = self.calculate_increments()

    """
        TODO - comment
    """

    def generate_coordinates(self):
        coordinate_list = [self._origin]
        heading = self._start_hdg
        while coordinate_list.__len__() < self._points:
            coordinate_list.append(self._origin.generate_coordinates(self._radius, heading))
            if self._direction == "Clockwise":
                heading = (heading + self._heading_increments) % 360
            elif self._direction == "Anticlockwise":
                heading = (heading - self._heading_increments) % 360
        return coordinate_list

    """
       TODO - comment
    """

    def calculate_increments(self):
        if self._end_hdg > self._start_hdg:
            difference = (self._end_hdg - self._start_hdg) % 360
        else:
            difference = (self._start_hdg - self._end_hdg) % 360

        incremental_hdg_value = difference / self._points
        return incremental_hdg_value
