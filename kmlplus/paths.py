from kmlplus.coordinates import Coordinate

"""
LinePath is used to create polygons by combining Coordinate objects.  LinePath objects connect coordinate objects via
straight lines when used in conjunction with polygon classes such as the 'floatingpolygon' class.  If a circle or 'arc'
is required, you can first use the ArcPath class and provide it as a * argument to the LinePath class.

If the Coordinate instances provided are not yet in decimal format, the LinePath class will convert it to decimal
automatically.
"""


class LinePath:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.all_coordinates = True
        self.centroid = None
        self.sort = kwargs.pop('sort', False)

        # If user wants coordinates sorted counter clockwise then call the sort vertices method which will change
        # the order of the Coordinate instances in the coordinate_list attribute.  It will sort in descending order
        # of the 'bearing from centroid' attribute.

        self.coordinate_list = args
        if self.sort is True:
            self.sort_vertices()
        self.kml_coordinate_list = self.kml_format()
        self.sides = None

    def __getitem__(self, index):
        return self.kml_coordinate_list[index]

    def __str__(self):
        return "LinePath instance containing {} kml readable Coordinate instances - {}".format(
            len(self.kml_coordinate_list), [str(x) for x in self.kml_coordinate_list])

    def __len__(self):
        return len(self.coordinate_list)

    """
    Find the centroid of the linepath.  This will be used for ordering the coordinates
    to be counter clockwise so as to be best displayed by kml rendering.
    """

    def find_centroid(self):
        latitude_total, longitude_total = 0, 0
        for coordinate_instance in self.coordinate_list:
            latitude_total += coordinate_instance.latitude
            longitude_total += coordinate_instance.longitude
        latitude_average, longitude_average = latitude_total / len(self.coordinate_list), \
                                              longitude_total / len(self.coordinate_list)
        return Coordinate(latitude_average, longitude_average)

    def calculate_bearings_from_centroid(self):
        for coordinate in self.coordinate_list:
            bearing, distance = self.centroid.get_bearing_and_distance(coordinate)
            setattr(coordinate, 'bearing_from_centroid', bearing)

    def sort_vertices(self):
        self.centroid = self.find_centroid()
        self.calculate_bearings_from_centroid()
        self.coordinate_list = sorted(self.coordinate_list, key=lambda x: x.bearing_from_centroid, reverse=True)

    def kml_format(self):
        assert self.coordinate_list.__len__() > 0
        tuple_list = [x.kml_tuple() for x in self.coordinate_list]
        return tuple_list

    def create_sides(self, another_line_path_instance, **kwargs):
        if isinstance(another_line_path_instance, LinePath):
            assert len(self.coordinate_list) == len(another_line_path_instance.coordinate_list),\
                "Sides can only be generated for LinePaths of equal length"
            i = 0
            side_list = []
            # TODO: create separate code for LinePath and ArcPath.  Current code will be for Arc Path
            # This if condition creates the sides up to the last coordinate, else then creates the last side back
            # to the first coordinate
            while i < len(self.coordinate_list):
                if i < len(self.coordinate_list) - 1:
                    side_list.append(
                        [
                            (self.coordinate_list[i].longitude, self.coordinate_list[i].latitude,
                             self.coordinate_list[i].height),
                            (self.coordinate_list[i+1].longitude, self.coordinate_list[i+1].latitude,
                             self.coordinate_list[i+1].height),
                            (another_line_path_instance.coordinate_list[i+1].longitude,
                             another_line_path_instance.coordinate_list[i+1].latitude,
                            another_line_path_instance.coordinate_list[i+1].height),
                            (another_line_path_instance.coordinate_list[i].longitude,
                             another_line_path_instance.coordinate_list[i].latitude,
                            another_line_path_instance.coordinate_list[i].height)
                        ]
                    )
                    i += 1

                # When you get to the final coordinate and need to create side back to the first coordinate, do this
                else:
                    side_list.append(
                        [
                            (self.coordinate_list[i].longitude, self.coordinate_list[i].latitude,
                             self.coordinate_list[i].height),
                            (self.coordinate_list[0].longitude, self.coordinate_list[0].latitude,
                             self.coordinate_list[0].height),
                            (another_line_path_instance.coordinate_list[0].longitude,
                             another_line_path_instance.coordinate_list[0].latitude,
                             another_line_path_instance.coordinate_list[0].height),
                            (another_line_path_instance.coordinate_list[i].longitude,
                             another_line_path_instance.coordinate_list[i].latitude,
                             another_line_path_instance.coordinate_list[i].height)
                        ]
                    )
                    i += 1

            self.sides = side_list

        else:
            raise Exception('create_sides() function only accepts LinePath instances or that of its subclasses')



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
