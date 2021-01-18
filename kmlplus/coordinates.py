from geographiclib.geodesic import Geodesic
from geopy import distance as gp


class Coordinate:
    def __init__(self, lat, long, **kwargs):
        self.__dict__.update(kwargs)
        self._latitude = lat
        self._longitude = long
        self.height = kwargs.pop('height', 0)
        self.name = kwargs.pop('name', None)
        self.coordinate_type = kwargs.pop('coordinate_type', 'decimal')
        self.arc_direction = kwargs.pop('arc_direction', None)
        self.arc_origin = kwargs.pop('arc_origin', None)
        if self.coordinate_type == 'dms':
            self.coordinate_type = self.convert_to_decimal()

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude):
        if type(a_latitude) is float or int:
            self._latitude = round(a_latitude, 6)
        else:
            try:
                float(a_latitude)
            except TypeError:
                print("Could not convert latitude value of type {} to string, define latitude and longitude as int or \
                float".format(type(a_latitude)))

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude):
        if type(a_longitude) is float or int:
            self._longitude = round(a_longitude, 6)
            self.coordinate_type = self.detect_coordinate_type(self._latitude)
        else:
            try:
                float(a_longitude)
            except TypeError:
                print("Could not convert longitude of type {} to string.  Latitude and longitude should be specified as\
                type int or float".format(type(a_longitude)))

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, a_height):
        if type(a_height) is float or int:
            self._height = a_height
        else:
            try:
                float(a_height)
            except ValueError:
                print(ValueError("Height must be a valid floating point number eg -5.3"))

    """This converts a given float from a decimal coordinate to a degrees minutes seconds coordinate.  It returns 
    an int"""

    @staticmethod
    def decimal_to_dms(coordinate_to_convert):
        degrees = int(coordinate_to_convert)
        minutes = abs((coordinate_to_convert - degrees) * 60)
        seconds = minutes % 1 * 60
        dms_string = str(degrees) + str(int(minutes)) + str(round(seconds))
        return int(dms_string)

    """Takes one argument of type int and returns a float representing a decimal coordinate"""

    @staticmethod
    def dms_to_decimal(coordinate_to_convert):
        degrees = int(str(coordinate_to_convert)[0:-4])
        minutes = float(str(coordinate_to_convert)[-4:-2]) / 60
        seconds = float(str(coordinate_to_convert)[-2:]) / 3600

        if degrees >= 0:
            decimal_degrees = round(float(degrees + (minutes + seconds)), 5)
        else:
            decimal_degrees = round(float(degrees - (minutes + seconds)), 5)
        return decimal_degrees

    """Takes an argument of type float or int.  Returns a string indicating whether the given coordinate is of type
    dms or decimal"""

    @staticmethod
    def detect_coordinate_type(a_coordinate):
        string_of_coordinate = str(a_coordinate)
        if string_of_coordinate.find('.') == -1:
            return 'dms'
        else:
            return 'decimal'

    """Takes argument of self and returns a string representation of the coordinates and height"""

    def __str__(self):
        the_string = "{}, {}, {}".format(self._latitude, self._longitude, self._height)
        return the_string

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
                self.coordinate_type = 'dms'

            except TypeError:
                print("Something went wrong while converting from decimal to dms")

    """Takes no arguments.  This function checks that the coordinate is firstly of the correct type (decimal).  If not it
        returns a TypeError.  If successful, the function calls the decimal coordinate to dms coordinate conversion
        function and updates the instance accordingly"""

    def convert_to_decimal(self):
        if self.coordinate_type == 'decimal':
            raise TypeError("The coordinates are already decimal format.  Either call the convert to dms function OR"
                            "check you have the correct coordinates set")
        else:
            try:
                self._latitude = self.dms_to_decimal(self._latitude)
                self._longitude = self.dms_to_decimal(self._longitude)
                self.coordinate_type = 'decimal'

            except TypeError:
                print("Something went wrong while converting from dms to decimal")

    """This takes an instance of the Coordinate class as its argument.  It returns the bearing (of type float) from the
    instance which is calling the function to the instance provided in the argument"""

    def get_bearing_and_distance(self, another_coordinate):
        geo_dict = Geodesic.WGS84.Inverse(another_coordinate.latitude, another_coordinate.longitude, self._latitude,
                                          self._longitude, )

        bearing, distance = geo_dict['azi1'] % 360, geo_dict['s12'] / 1000  # converts metres to kilometres for distance
        return round(bearing, 2), distance
