from geographiclib.geodesic import Geodesic
from geopy import distance as gp


class Coordinate:
    def __init__(self, lat: int or float, long: int or float, height=0.0):
        self._latitude = lat
        self._longitude = long
        self._height = height
        self.coordinate_type = self.detect_coordinate_type(self._latitude)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude: int or float):
        self._latitude = a_latitude
        self.coordinate_type = self.detect_coordinate_type(self._latitude)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude: int or float):
        self._longitude = a_longitude
        self.coordinate_type = self.detect_coordinate_type(self._latitude)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, a_height: int or float):
        if a_height.isinstance(float) or a_height.isinstance(int):
            self._height = a_height
        else:
            print(ValueError("Height must be a valid floating point number eg -5.3"))

    """This converts a given float from a decimal coordinate to a degrees minutes seconds coordinate.  It returns 
    an int"""

    @staticmethod
    def decimal_to_dms(coordinate_to_convert: float or int) -> int:
        degrees = int(coordinate_to_convert)
        minutes = abs((coordinate_to_convert - degrees) * 60)
        seconds = minutes % 1 * 60
        dms_string = str(degrees) + str(int(minutes)) + str(round(seconds))
        return int(dms_string)

    """Takes one argument of type int and returns a float representing a decimal coordinate"""

    @staticmethod
    def dms_to_decimal(coordinate_to_convert: int) -> float:
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
    def detect_coordinate_type(a_coordinate: float or int) -> str:
        string_of_coordinate = str(a_coordinate)
        if string_of_coordinate.find('.') == -1:
            return 'dms'
        else:
            return 'decimal'

    """Takes argument of self and returns a string representation of the coordinates and height"""

    def to_string_xyz(self) -> str:
        the_string = "{}, {}, {}".format(self._latitude, self._longitude, self._height)
        return the_string

    def to_string_xy(self) -> str:
        the_string = "{}, {}".format(self._latitude, self._longitude)
        return the_string

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

    def get_bearing(self, another_coordinate) -> float:
        geo_dict = Geodesic.WGS84.Inverse(self._latitude, self._longitude,
                                          another_coordinate.latitude, another_coordinate.longitude)

        bearing = geo_dict['azi1'] % 360
        return round(bearing, 2)


"""
Takes 3 parameters and 1 key word argument for height.  Accepts a string of decimal lat/long, a bearing from 0 - 359 degrees
and a distance in kilometres.  Optional keyword argument of height in metres.  Returns an instance of the Coordinate class
which is the desired bearing and distance from the lat/long string provided.
"""


def generate_coordinates(lat_long_string, distance_km, a_bearing, **kwargs):
    point = gp.Point.from_string(lat_long_string)
    decimal_lat_lon_string = gp.distance(kilometers=distance_km).destination(point=point,
                                                                             bearing=a_bearing).format_decimal()
    decimal_lat_lon_string = decimal_lat_lon_string.split(',')
    new_coordinate_instance = Coordinate(decimal_lat_lon_string[0], decimal_lat_lon_string[1], **kwargs)
    return new_coordinate_instance
