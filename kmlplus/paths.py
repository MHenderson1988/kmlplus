from kmlplus.coordinates import Coordinate

"""
LinePath is used to create polygons by combining Coordinate objects.  LinePath objects connect coordinate objects via
straight lines when used in conjunction with polygon classes such as the 'floatingpolygon' class.  If a circle or 'arc'
is required, you can first use the ArcPath class and provide it as a * argument to the LinePath class.

If the Coordinate instances provided are not yet in decimal format, the LinePath class will convert it to decimal
automatically.
"""


class LinePath:
    def __init__(self, *args):
        self.all_coordinates = True

        # Check all args are instances of the Coordinate class in decimal form
        for arg in args:
            try:
                if isinstance(arg, Coordinate):
                    # Convert to decimal format if dms
                    if arg.coordinate_type != 'decimal':
                        arg.convert_to_decimal()
                    else:
                        continue
                else:
                    self.all_coordinates = False
                    break
            except TypeError:
                self.all_coordinates = False

        if self.all_coordinates:
            self.coordinate_list = args
            self.kml_coordinate_list = self.kml_format()

    def kml_format(self):
        assert self.coordinate_list.__len__() > 0
        tuple_list = [x.kml_tuple() for x in self.coordinate_list]
        return tuple_list

    def __getitem__(self, index):
        return self.kml_coordinate_list[index]

    def __str__(self):
        return "LinePath instance containing {} kml readable Coordinate instances - {}".format(
            len(self.kml_coordinate_list), [str(x) for x in self.kml_coordinate_list])

    def __len__(self):
        return len(self.coordinate_list)


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
        self.coordinates = self.populate_path_list()

    def __getitem__(self, item):
        return self.coordinates[item]

    def __str__(self):
        return "ArcPath instance containing {} Coordinate instances - {}".format(
            len(self.coordinates), [str(x) for x in self.coordinates])

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


"""    def coordinates_kml_format(self):
        coordinate_list = self.populate_path_list()
        kml_format_list = []
        for coordinate_instance in coordinate_list:
            kml_format_list.append(coordinate_instance.kml_tuple())
        return kml_format_list"""

"""
SlopedArcPath class is a subclass of ArcPath.  It it used to create an ArcPath which ends at 
a different height from which it originally started.
"""


class SlopedArcPath(ArcPath):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
