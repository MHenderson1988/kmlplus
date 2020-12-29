import re
from geographiclib.geodesic import Geodesic
from geopy import distance as gp

# prepend regex pattern with 'r' to show it is a raw string
decimal_pattern = r'^-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,6}'
nats_dms_patten = r'''^s*([+-]?\d{1,3}\*?\s+\d{1,2}'?\s+\d{1,2}"?[NSEW]?|\d{1,3}(:\d{2}){2}\.\d[NSEW]\s*){1,2}$'''


class Coordinate:
    def __init__(self, lat, long, height, coordinate_type):
        self._latitude = lat
        self._longitude = long
        self._height = height
        self._coordinate_type = coordinate_type

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude):
        if re.match(decimal_pattern, a_latitude):
            self._latitude = a_latitude
        else:
            print(ValueError("Latitude must be a valid integer if using DMS coordinates"))

    @latitude.deleter
    def latitude(self):
        del self._latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude):
        if re.match(decimal_pattern, a_longitude):
            self._longitude = a_longitude
        else:
            print(ValueError("Latitude must be a valid integer if using DMS coordinates"))

    @longitude.deleter
    def longitude(self):
        del self._longitude

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, a_height):
        if a_height.isinstance(float) or a_height.isinstance(int):
            self._height = a_height
        else:
            print(ValueError("Height must be a valid floating point number eg -5.3"))

    @height.deleter
    def height(self):
        del self._height

    def to_string(self):
        the_string = "{}, {}".format(self.latitude, self.longitude)
        return the_string
