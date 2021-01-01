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
    def decimal_to_dms(coordinate_to_convert):
        degrees = int(coordinate_to_convert)
        minutes = abs((coordinate_to_convert - degrees) * 60)
        seconds = minutes % 1 * 60
        dms_string = str(degrees) + str(int(minutes)) + str(round(seconds))
        return int(dms_string)

    def to_string(self):
        the_string = "{}, {}, {}".format(self._latitude, self._longitude, self._height)
        return the_string

    def convert_to_dms(self):
        if self.coordinate_type == 'dms':
            return TypeError("The coordinates provided are already in the degrees, minutes, seconds format.  You need "
                             "to call the convert_to_decimal function instead")
        else:
            # Convert latitude
            self._latitude = self.decimal_to_dms(self._latitude)
            self._longitude = self.decimal_to_dms(self._longitude)

    """This takes an instance of the Coordinate class as its argument.  It returns the bearing (of type float) from the
    instance which is calling the function to the instance provided in the argument"""

    def get_bearing(self, another_coordinate):
        geo_dict = Geodesic.WGS84.Inverse(self._latitude, self._longitude,
                                          another_coordinate.latitude, another_coordinate.longitude)

        bearing = geo_dict['azi1'] % 360
        return round(bearing, 2)
