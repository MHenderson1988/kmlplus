from kmlplus.coordinates import Coordinate

"""
LinePath is a basic class which returns a path of straight lines between the arguments passed.  It returns a tuple of
kml readable coordinates which can be used to generate the path in google earth.
"""


class LinePath:
    def __init__(self, *args):
        self.coordinate_list = args

    def kml_format(self):
        tuple_list = [(x.longitude, x.latitude, x.height) for x in self.coordinate_list]
        return tuple_list




"""
The ArcPath class is used to return a tuple list of coordinates in .kml readable format ie - y, x, z.  It accepts the 
following parameters - 

origin - an x, y coordinate string which indicates the central location from which the arc will be drawn.
start_hdg - a heading/bearing relative to the origin from which the arc will commence
end_hdg - a heading/bearing relative to the origin at which the arc will end
radius - the distance from the origin the arc points will be plotted.  Accepts an int or float representing metres.

returns - a list of x, y, z tuples.
"""


class ArcPath:
    def __init__(self, origin, start_bearing, end_bearing, radius, **kwargs):
        self.__dict__.update(kwargs)
        self.origin = origin
        self.start_bearing = start_bearing
        self.end_bearing = end_bearing
        self.radius = radius
        # if no height provided, defaults to the height of the origin coordinate
        self.height = kwargs.pop('height', self.origin.height)
        self.direction = kwargs.pop('direction', 'Clockwise')
        self.points = kwargs.pop('points', 50)
        self.kml_coordinates = self.coordinates_kml_format()

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, a_origin):
        if isinstance(a_origin, Coordinate):
            self._origin = a_origin
        else:
            TypeError("Error: origin MUST be an instance of the Coordinate class")

    def calculate_heading_increments(self):
        if self.end_bearing > self.start_bearing:
            difference = (self.end_bearing - self.start_bearing) % 360
        else:
            difference = (self.start_bearing - self.end_bearing) % 360

        incremental_heading_value = difference / self.points
        return incremental_heading_value

    def populate_path_list(self):
        coordinates_list = []
        increments = self.calculate_heading_increments()

        while coordinates_list.__len__() < self.points:
            coordinates_list.append(self.origin.generate_coordinates(self.radius, self.start_bearing, self.height))
            if self.direction == 'Clockwise':
                self.start_bearing = (self.start_bearing - increments) % 360
            else:
                self.start_bearing = (self.start_bearing + increments) % 360
        return coordinates_list

    def coordinates_kml_format(self):
        coordinate_list = self.populate_path_list()
        kml_format_list = []
        for coordinate_instance in coordinate_list:
            kml_format_list.append(coordinate_instance.kml_tuple())
        return kml_format_list
