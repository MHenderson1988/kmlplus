import copy

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
        self.sort = kwargs.pop('sort', False)
        self.height = kwargs.pop('height', None)
        self.arc_points = kwargs.pop('arc_points', 50)
        self.origin = kwargs.pop('origin', None)

        # Validate arc_point input is int else try to cast or throw exception
        self.arc_points = self.validate_int(self.arc_points)

        self.args_list = self.generate_coordinate_object(*args)

        # If user has entered a height, check it is a valid float or int
        if self.height is not None:
            self.height = self.validate_float(self.height)
            # If user passes a height value, change altitude values for all coordinate instances passed as arguments
            for coord in self.args_list:
                coord.height = self.height

        self.coordinate_list = self.check_args()
        self.all_coordinates = True
        self.centroid = self.find_centroid()
        self.sides = self.sides_depreciated()

        # If no origin is provided for arcs, make it the centroid
        if self.origin is None:
            self.origin = self.centroid

        """If user wants coordinates sorted counter clockwise then call the sort vertices method which will change
        the order of the Coordinate instances in the coordinate_list attribute.  It will sort in descending order
        of the 'bearing from centroid' attribute."""

        if self.sort is True:
            self.sort_vertices()
        self.kml_coordinate_list = self.kml_format()

    def __getitem__(self, index):
        return self.kml_coordinate_list[index]

    def __str__(self):
        return "LinePath instance containing {} kml readable Coordinate instances - {}".format(
            len(self.kml_coordinate_list), [str(x) for x in self.kml_coordinate_list])

    def __len__(self):
        return len(self.coordinate_list)

    @staticmethod
    def validate_int(a_value):
        if not isinstance(a_value, int):
            try:
                a_value = int(a_value)
                return a_value
            except ValueError as error:
                print(error)
                print('Defaulting value to int 50')
                return 50
        else:
            return a_value

    @staticmethod
    def validate_float(a_value):
        if not isinstance(a_value, float):
            try:
                a_value = float(a_value)
                return a_value
            except ValueError as error:
                print(error)
                print('Defaulting value to None')
                return None
        else:
            return a_value

    @staticmethod
    def sides_depreciated():
        deprecated_warning = "LinePath.sides deprecated since v2.0.  Please use LinePath.create_layer_and_sides()" \
                             " to return a new LinePath layer and sides.  Alternatively call .create_sides() to return" \
                             " a list of sides between this linepath and another."
        return deprecated_warning

    def generate_coordinate_object(self, *args):
        list_to_return = []
        for arg in args:
            if not isinstance(arg, Coordinate):
                try:
                    if self.height is not None:
                        new_coordinate = Coordinate(arg, height=self.height, arc_origin=self.origin)
                    else:
                        new_coordinate = Coordinate(arg, arc_origin=self.origin)
                    list_to_return.append(new_coordinate)
                except TypeError as error:
                    print(error)
            elif isinstance(arg, Coordinate):
                list_to_return.append(arg)
        return list_to_return

    """
    Check each coordinate.  If it has a kwarg identifying it as the start of an arc path, create said path and return
    it with the other coordinates.
    """

    def check_args(self):
        a_list_to_return = []
        i = 0
        while i < len(self.args_list):
            # If not the start of an arc, ie not suffixed with 'a' or 'c'
            if self.args_list[i].arc_direction is None:
                a_list_to_return.append(self.args_list[i])

            # Else if an arc
            elif self.args_list[i].arc_direction == 'clockwise' or self.args_list[i].arc_direction == 'anticlockwise':

                # If the coordinate has an arc directional value but no origin designated, make the origin the centroid
                # of the polygon.
                if self.args_list[i].arc_origin is None:
                    self.args_list[i].arc_origin = self.find_centroid()

                # Set the start bearing and distance
                a_start_bearing, a_start_distance = self.args_list[i].get_bearing_and_distance(
                    self.args_list[i].arc_origin)

                # Evaluates True if not the last coordinate in the arguments passed
                if i < len(self.args_list) - 1:
                    end_bearing, end_distance = self.args_list[i + 1].get_bearing_and_distance(
                        self.args_list[i].arc_origin)

                # Evaluates True if this is the last coordinate in the list
                else:
                    end_bearing, end_distance = self.args_list[0].get_bearing_and_distance(self.args_list[i].arc_origin)

                new_arc = ArcPath(self.args_list[i].arc_origin, start_bearing=a_start_bearing, end_bearing=end_bearing,
                                  radius=a_start_distance, direction=self.args_list[i].arc_direction,
                                  points=self.arc_points, height=self.height)

                # Unpack the ArcPath's coordinates into the LinePath's coordinate list
                for coordinate in new_arc:
                    a_list_to_return.append(coordinate)
            i += 1
        return a_list_to_return

    """
    Find the centroid of the linepath.  This will be used for ordering the coordinates
    to be counter clockwise so as to be best displayed by kml rendering.
    """

    def find_centroid(self):
        latitude_total, longitude_total = 0, 0
        for coordinate_instance in self.args_list:
            latitude_total += coordinate_instance.latitude
            longitude_total += coordinate_instance.longitude
        latitude_average, longitude_average = latitude_total / len(self.args_list), \
                                              longitude_total / len(self.args_list)
        if self.height is not None:
            height = self.height
        else:
            height = 0.0
        return Coordinate(latitude_average, longitude_average, height)

    """
    This method takes each vertices and calculates it's bearing from the centroid.  This is then used to sort the 
    vertices into anticlockwise ordering.
    """

    def calculate_bearings_from_centroid(self):
        for coordinate in self.coordinate_list:
            bearing, distance = coordinate.get_bearing_and_distance(self.centroid)
            setattr(coordinate, 'bearing_from_centroid', bearing)

    """
    This method sorts the vertices into anticlockwise ordering
    """

    def sort_vertices(self):
        self.centroid = self.find_centroid()
        self.calculate_bearings_from_centroid()
        self.coordinate_list = sorted(self.coordinate_list, key=lambda x: x.bearing_from_centroid, reverse=True)

    """
    kml_format takes self as it's only argument and returns a list of tuples or coordinate information in x,y format.
    ie - a .kml readable format
    """

    def kml_format(self):
        assert self.coordinate_list.__len__() > 0
        tuple_list = [x.kml_tuple() for x in self.coordinate_list]
        return tuple_list

    """
    Create_sides takes args and kwargs as it's arguments.  Args must be valid LinePath instances containing coordinate
    instances.  Both LinePath instance must be of equal length.  It does not return anything however it updates the 
    self.sides attribute to a list of kml readable tuples which are used to draw the 'sides' of the polygons.
    """

    def create_sides(self, *args):
        for args in args:
            if isinstance(args, LinePath):
                assert len(self.coordinate_list) == len(args.coordinate_list), \
                    "Sides can only be generated for LinePaths of equal length"
                i = 0
                side_list = []
                # This if condition creates the sides up to the last coordinate, else then creates the last side back
                # to the first coordinate
                while i < len(self.coordinate_list):
                    if i < len(self.coordinate_list) - 1:
                        side_list.append(
                            [
                                (self.coordinate_list[i].longitude, self.coordinate_list[i].latitude,
                                 self.coordinate_list[i].height),
                                (self.coordinate_list[i + 1].longitude, self.coordinate_list[i + 1].latitude,
                                 self.coordinate_list[i + 1].height),
                                (args.coordinate_list[i + 1].longitude,
                                 args.coordinate_list[i + 1].latitude,
                                 args.coordinate_list[i + 1].height),
                                (args.coordinate_list[i].longitude,
                                 args.coordinate_list[i].latitude,
                                 args.coordinate_list[i].height)
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
                                (args.coordinate_list[0].longitude,
                                 args.coordinate_list[0].latitude,
                                 args.coordinate_list[0].height),
                                (args.coordinate_list[i].longitude,
                                 args.coordinate_list[i].latitude,
                                 args.coordinate_list[i].height)
                            ]
                        )
                        i += 1

                return side_list

            else:
                raise Exception('create_sides() function only accepts LinePath instances or that of its subclasses')

    def create_layer_and_sides(self, **kwargs):
        self.__dict__.update(kwargs)
        height = kwargs.pop('height', 100.0)
        copy_of_args = copy.deepcopy(self.args_list)
        new_line_path = LinePath(*copy_of_args, height=height)

        return new_line_path, self.create_sides(new_line_path)


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
        self.direction = kwargs.pop('direction', 'clockwise')
        self.points = kwargs.pop('points', 50)
        self.coordinates = self.populate_path_list()

        # If user passes a height value, change altitude values for all coordinate instances passed as arguments
        if self.height is not None:
            for coordinate in self.coordinates:
                coordinate.height = self.height

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

    def calculate_heading_increments(self, start_bearing, end_bearing):
        if self.direction == 'clockwise':
            difference = end_bearing - start_bearing
            if difference < 0:
                difference = difference + 360
        else:
            difference = start_bearing - end_bearing
            if difference < 0:
                difference = difference + 360
        incremental_heading_value = difference / self.points
        return incremental_heading_value

    def populate_path_list(self):
        coordinates_list = []
        increments = self.calculate_heading_increments(self.start_bearing, self.end_bearing)
        bearing = self.start_bearing
        while coordinates_list.__len__() < self.points:
            coordinates_list.append(self.origin.generate_coordinates(self.radius, bearing, self.height))
            if self.direction == 'clockwise':
                bearing = (bearing + increments) % 360
            else:
                bearing = (bearing - increments) % 360
        return coordinates_list
