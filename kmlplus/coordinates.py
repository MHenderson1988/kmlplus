from geographiclib.geodesic import Geodesic


class Coordinate:
    def __init__(self, lat, long, height, coordinate_type):
        self._latitude = lat
        self._longitude = long
        self._height = height
        self.coordinate_type = coordinate_type

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude):
        self._latitude = a_latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude):
        self._longitude = a_longitude

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, a_height):
        if a_height.isinstance(float) or a_height.isinstance(int):
            self._height = a_height
        else:
            print(ValueError("Height must be a valid floating point number eg -5.3"))

    @staticmethod
    def find_decimal_point(a_float):
        string_to_index = str(a_float)
        an_index = string_to_index.index('.')
        return an_index

    def to_string(self):
        the_string = "{}, {}, {}".format(self._latitude, self._longitude, self._height)
        return the_string

    def convert_to_dms(self):
        if self.coordinate_type == 'dms':
            return TypeError("The coordinates provided are already in the degrees, minutes, seconds format.  You need "
                             "to call the convert_to_decimal function instead")
        else:
            # Convert latitude
            latitude_string = str(self._latitude)
            degrees = latitude_string[0:self.find_decimal_point(latitude_string)]
            minutes = float(latitude_string[self.find_decimal_point(latitude_string):-1]) * 60
            seconds = round(float(str(minutes)[self.find_decimal_point(minutes):-1]) * 60, 2)
            degrees, minutes, seconds = str(degrees), str(minutes), str(seconds)
            pass

    """This takes an instance of the Coordinate class as its argument.  It returns the bearing (of type float) from the
    instance which is calling the function to the instance provided in the argument"""

    def get_bearing(self, another_coordinate):
        geo_dict = Geodesic.WGS84.Inverse(self._latitude, self._longitude,
                                          another_coordinate.latitude, another_coordinate.longitude)

        bearing = geo_dict['azi1'] % 360
        return round(bearing, 2)
