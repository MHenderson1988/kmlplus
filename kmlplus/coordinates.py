from geographiclib.geodesic import Geodesic
from geopy import distance as gp


class Coordinate:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self._latitude = None
        self._longitude = None
        self._height = 0
        self.coordinate_type = None
        self.lat_long_height_arguments(args)
        self.name = kwargs.pop('name', None)
        self.arc_direction = kwargs.pop('arc_direction', None)
        self.arc_origin = kwargs.pop('arc_origin', None)

        # Convert coordinates to decimal degrees if given as DMS
        if self.detect_coordinate_type(self.latitude) == 'dms':
            self.latitude = self.convert_to_decimal(self.latitude)
        if self.detect_coordinate_type(self.longitude) == 'dms':
            self.longitude = self.convert_to_decimal(self.longitude)
        self.coordinate_type = 'decimal'

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude):
        self._latitude = self.validate_attribute_input(a_latitude)
        if self.detect_coordinate_type(self.latitude) == 'dms':
            self._latitude = round(self.convert_to_decimal(self.latitude), 4)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude):
        self._longitude = self.validate_attribute_input(a_longitude)
        if self.detect_coordinate_type(self.longitude) == 'dms':
            self._longitude = round(self.convert_to_decimal(self.longitude), 4)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, a_height):
        self._height = self.validate_attribute_input(a_height)

    def validate_attribute_input(self, a_value):
        if isinstance(a_value, int) or isinstance(a_value, float):
            return a_value
        elif isinstance(a_value, str):
            try:
                stripped_string = self.strip_whitespace(a_value)
                return float(stripped_string)
            except TypeError:
                print("Couldn't convert to string")

    @staticmethod
    def is_negative(aNumber):
        if aNumber < 0:
            return True
        else:
            return False

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
        if string_of_coordinate.find('.') == -1:
            return 'dms'
        else:
            position_of_decimal = string_of_coordinate.find('.')
            if position_of_decimal >= 5:
                return 'dms'
            else:
                return 'decimal'

    @staticmethod
    def strip_whitespace(a_string):
        return a_string.strip()

    """Takes no arguments.  This function checks that the coordinate is firstly of the correct type (dms).  If not it
    returns a TypeError.  If successful, the function calls the decimal coordinate to dms coordinate conversion
    function and updates the instance accordingly"""

    def convert_to_dms(self):
        if self.coordinate_type == 'dms':
            raise TypeError("The coordinates provided are already in the degrees, minutes, seconds format.  You need "
                            "to call the convert_to_decimal function instead")
        else:
            try:
                self._latitude = self.decimal_to_dms(self._latitude)
                self._longitude = self.decimal_to_dms(self._longitude)

            except TypeError:
                print("Something went wrong while converting from decimal to dms")

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
        degrees, split_minutes, split_seconds = self.split_dms_for_calc(coordinate_to_convert)
        degrees = float(degrees)
        minutes = float(split_minutes) / 60
        seconds = float(split_seconds) / 3600

        if degrees >= 0:
            decimal_degrees = round(float(degrees + (minutes + seconds)), 5)
        else:
            decimal_degrees = round(float(degrees - (minutes + seconds)), 5)
        return decimal_degrees

    def split_dms_for_calc(self, coordinate_to_convert):
        is_negative = self.is_negative(coordinate_to_convert)
        coordinate_string = str(coordinate_to_convert)
        # Split string to isolate DDMMSS without decimal places
        split_string = coordinate_string.split('.')
        before_decimal = split_string[0]
        length = len(before_decimal)

        if is_negative:
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
        the_string = "{}, {}, {}".format(self._latitude, self._longitude, self._height)
        return the_string

    def lat_long_height_arguments(self, args):
        if len(args) == 3:
            self._latitude = args[0]
            self._longitude = args[1]
            self._height = args[2]
        elif len(args) == 2:
            self._latitude = args[0]
            self._longitude = args[1]
            self._height = 0
        elif len(args) == 1:
            try:
                split_string = args[0].split(',')
                if len(split_string) == 3:
                    self._latitude = float(split_string[0])
                    self._longitude = float(split_string[1])
                    self._height = float(split_string[2])
                elif len(split_string) == 2:
                    self._latitude = float(split_string[0])
                    self._longitude = float(split_string[1])
            except TypeError:
                Exception("Something went wrong initialising the latitude, longitude and height values.")

    def check_for_direction(self, a_longitude_string):
        if a_longitude_string[-1].isalpha():
            self.set_direction_from_letter(a_longitude_string[-1])
            return float(a_longitude_string[0:-1])
        else:
            return float(a_longitude_string)

    def set_direction_from_letter(self, aCharacter):
        if aCharacter == 'a':
            self.arc_direction = 'anticlockwise'
        elif aCharacter == 'c':
            self.arc_direction = 'clockwise'
        else:
            Exception("Longitude strings should be suffixed with either 'a' or 'c'")

    def to_string_yx(self):
        the_string = "{}, {}".format(self._latitude, self._longitude)
        return the_string

    #  Gives an xyz tuple which is readable by kml
    def kml_tuple(self):
        return self._longitude, self._latitude, self._height

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

    """This takes an instance of the Coordinate class as its argument.  It returns the bearing (of type float) from the
    instance which is calling the function to the instance provided in the argument"""

    def get_bearing_and_distance(self, another_coordinate):
        geo_dict = Geodesic.WGS84.Inverse(another_coordinate.latitude, another_coordinate.longitude, self._latitude,
                                          self._longitude, )

        bearing, distance = geo_dict['azi1'] % 360, geo_dict['s12'] / 1000  # converts metres to kilometres for distance
        return round(bearing, 2), distance
