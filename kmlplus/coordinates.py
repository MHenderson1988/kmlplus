from geographiclib.geodesic import Geodesic
from geopy import distance as gp


class Coordinate:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        # Initialise the arc direction attribute here so it is not overwritten by the lat_long arguments
        self.arc_direction = kwargs.pop('arc_direction', None)
        self.name = kwargs.pop('name', None)
        self.height = kwargs.pop('height', 0.0)
        self.arc_origin = kwargs.pop('arc_origin', None)
        self.latitude, self.longitude, self.height = self.lat_long_height_arguments(args)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude):
        self._latitude = self.validate_attribute_input(a_latitude)
        if self.detect_coordinate_type(self.latitude) == 'dms':
            self._latitude = round(self.convert_to_decimal(self.latitude), 5)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude):
        self._longitude = self.validate_attribute_input(a_longitude)
        if self.detect_coordinate_type(self.longitude) == 'dms':
            self._longitude = round(self.convert_to_decimal(self.longitude), 5)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, a_height):
        self._height = self.validate_attribute_input(a_height)

    def validate_attribute_input(self, a_value):
        if isinstance(a_value, float):
            return round(a_value, 5)
        elif isinstance(a_value, int):
            return float(a_value)
        elif isinstance(a_value, str):
            try:
                stripped_string = self.strip_whitespace(a_value)
                return float(self.check_for_direction(a_value))
            except TypeError:
                print("Couldn't convert to string")

    """Takes one argument of type int or float and returns True if the number is a negative (less than zero)
    number.  Returns False if it is positive"""

    @staticmethod
    def is_negative(aNumber):
        try:
            if aNumber < 0:
                return True
            else:
                return False
        except TypeError:
            print("is_negative can only evaluate numbers.  Please provide valid input.")

    """This converts a given float from a decimal coordinate to a degrees minutes seconds coordinate.  It returns 
    an int"""

    @staticmethod
    def decimal_to_dms(coordinate_to_convert):
        degrees = int(coordinate_to_convert)
        minutes = abs((coordinate_to_convert - degrees) * 60)
        seconds = minutes % 1 * 60
        dms_string = str(degrees) + str(int(minutes)) + str(round(seconds, 2))
        return float(dms_string)

    """Takes an argument of type float or int.  Logically a coordinate of dms will not have a decimal place until at
    least six positions in eg - 552312.374, -45643.2 or 824512, -1795212.548 whereas decimal coordinates will have a
    decimal occur earlier.  Returns a string indicating whether the given coordinate is of type dms or decimal"""

    @staticmethod
    def detect_coordinate_type(a_coordinate):
        string_of_coordinate = str(a_coordinate)
        try:
            if string_of_coordinate.find('.') == -1:
                return 'dms'
            else:
                position_of_decimal = string_of_coordinate.find('.')
                if position_of_decimal >= 5:
                    return 'dms'
                else:
                    return 'decimal'
        except TypeError:
            print("A coordinate must be type decimal or dms")

    """Takes one argument of type string and returns a string object stripped of whitespace"""

    @staticmethod
    def strip_whitespace(a_string):
        return a_string.strip()

    """Takes no arguments.  This function checks that the coordinate is firstly of the correct type (decimal).  If not it
        returns a TypeError.  If successful, the function calls the decimal coordinate to dms coordinate conversion
        function and updates the instance accordingly"""

    def convert_to_decimal(self, a_value):
        if self.detect_coordinate_type(a_value) == 'decimal':
            raise TypeError("Coordinate is already a decimal value")
        else:
            try:
                return self.dms_to_decimal(a_value)
            except TypeError:
                print("Something went wrong while converting from dms to decimal")

    """Takes one argument of type int and returns a float representing a decimal coordinate"""

    def dms_to_decimal(self, coordinate_to_convert):
        # Ensure value is a string, if not cast to a string for further evaluation
        if not isinstance(coordinate_to_convert, str):
            try:
                str(coordinate_to_convert)
            except TypeError:
                print("Value could not be converted to a string.  dms_to_decimal requires either float,"
                      "int or str to execute")

        degrees, split_minutes, split_seconds = self.split_dms_for_calc(coordinate_to_convert)
        degrees = float(degrees)
        minutes = float(split_minutes) / 60
        seconds = float(split_seconds) / 3600

        if degrees >= 0:
            decimal_degrees = round(float(degrees + (minutes + seconds)), 5)
        else:
            decimal_degrees = round(float(degrees - (minutes + seconds)), 5)
        return decimal_degrees

    """Takes one argument of type int or float and returns three strings representing degrees, minutes and seconds
    of the DMS coordinate provided"""

    def split_dms_for_calc(self, coordinate_to_convert):

        # Check argument is string and if not try to cast.
        if not isinstance(coordinate_to_convert, str):
            try:
                str(coordinate_to_convert)
            except TypeError:
                print("Cannot cast value to string for split_dms_for_calc method")

        coordinate_string = str(coordinate_to_convert)
        # Split string to isolate DDMMSS without decimal places
        split_string = coordinate_string.split('.')
        before_decimal = split_string[0]
        length = len(before_decimal)

        degrees = None
        minutes = None
        seconds = None

        if self.is_negative(coordinate_to_convert):
            if length == 8:
                degrees = before_decimal[0:4]
                minutes = before_decimal[4:6]
                seconds = coordinate_string[6:]
            elif length == 7:
                degrees = before_decimal[0:3]
                minutes = before_decimal[3:5]
                seconds = coordinate_string[5:]
            elif length == 6:
                degrees = before_decimal[0:2]
                minutes = before_decimal[2:4]
                seconds = coordinate_string[4:]
        else:
            if length == 7:
                degrees = before_decimal[0:3]
                minutes = before_decimal[3:5]
                seconds = coordinate_string[5:]
            elif length == 6:
                degrees = before_decimal[0:2]
                minutes = before_decimal[2:4]
                seconds = coordinate_string[4:]
            elif length == 5:
                degrees = before_decimal[0:1]
                minutes = before_decimal[1:3]
                seconds = coordinate_string[3:]

        return degrees, minutes, seconds

    """Takes argument of self and returns a string representation of the coordinates and height"""

    def __str__(self):
        the_string = "{}, {}, {}".format(self.latitude, self.longitude, self.height)
        return the_string

    """Takes multiple arguments and returns nothing.  Initialises the latitude, longitude and height attributes
    of the object when initialised."""

    def lat_long_height_arguments(self, args):
        latitude = 0
        longitude = 0
        height = 0

        try:
            if len(args) == 3:
                latitude = args[0]
                longitude = self.check_for_direction(str(args[1]))
                height = args[2]

            elif len(args) == 2:
                latitude = args[0]
                longitude = self.check_for_direction(str(args[1]))
                height = self.height

            elif len(args) == 1:
                try:
                    split_string = args[0].split(',')

                    if len(split_string) == 3:
                        latitude = split_string[0]
                        longitude = split_string[1]
                        height = split_string[2]

                    elif len(split_string) == 2:
                        latitude = split_string[0]
                        longitude = split_string[1]
                        height = self.height

                except AttributeError:
                    Exception("Something went wrong initialising the latitude, longitude and height values.")

            return latitude, longitude, height

        except TypeError:
            Exception("args must be either a single string or 2-3 int or float arguments.")

    """
    Takes one argument of type string.  Checks to see if string is suffixed with a letter denoting arc direction.
    If so calls the set_direction_from_letter function and returns the coordinate without it's suffix.
    """

    def check_for_direction(self, a_longitude_string):
        if not isinstance(a_longitude_string, str):
            try:
                a_longitude_string = str(a_longitude_string)
            except TypeError:
                Exception("Cannot cast to string for check_for_direction")
        if a_longitude_string[-1].isalpha():
            self.arc_direction = self.set_direction_from_letter(a_longitude_string[-1])
            return float(a_longitude_string[0:-1])
        else:
            return float(a_longitude_string)

    """
    Takes one argument of type char and sets the object's arc_direction attribute accordingly.  If the char is not valid
    throws an Exception.
    """

    @staticmethod
    def set_direction_from_letter(aCharacter):
        try:
            if aCharacter == 'a':
                return 'anticlockwise'
            elif aCharacter == 'c':
                return 'clockwise'
        except TypeError:
            Exception("Longitude strings should be suffixed with either 'a' or 'c'")

    """
    Takes no arguments and returns a string of 'Latitude, Longitude'
    """

    def to_string_yx(self):
        the_string = "{}, {}".format(self.latitude, self.longitude)
        return the_string

    """
    Takes zero arguments and returns a .kml readable tuple in the xyz format.
    """

    #  Gives an xyz tuple which is readable by kml
    def kml_tuple(self):
        return self.longitude, self.latitude, self.height

    """Takes 2 parameters and 1 key word argument for height.  Accepts a string of decimal lat/long, a bearing from 0 
    - 359 degrees and a distance in kilometres.  Optional keyword argument of height in metres.  Returns an instance 
    of the Coordinate class which is the desired bearing and distance from the lat/long string provided. """

    def generate_coordinates(self, distance_km, a_bearing, a_height):
        point = gp.Point.from_string(self.to_string_yx())
        decimal_lat_lon_string = gp.distance(kilometers=distance_km).destination(point=point,
                                                                                 bearing=a_bearing).format_decimal()
        decimal_lat_lon_string = decimal_lat_lon_string.split(',')
        lat_float, long_float = round(float(decimal_lat_lon_string[0]), 6), round(float(decimal_lat_lon_string[1]), 6)

        new_coordinate_instance = Coordinate(lat_float, long_float, height=a_height)
        return new_coordinate_instance

    """This takes an instance of the Coordinate class as its argument.  It returns the bearing and distance FROM the argument to the
    instance calling the function.  IE - if you're using instance A to call this function against instance B, it will return
    the heading from B to A"""

    def get_bearing_and_distance(self, another_coordinate):
        geo_dict = Geodesic.WGS84.Inverse(another_coordinate.latitude, another_coordinate.longitude, self.latitude,
                                          self.longitude, )

        bearing, distance = geo_dict['azi1'] % 360, round(geo_dict['s12'] / 1000,
                                                          3)  # converts metres to kilometres for distance
        return round(bearing, 2), distance
