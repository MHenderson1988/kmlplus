import re
from geographiclib.geodesic import Geodesic
from geopy import distance as gp

# prepend regex pattern with 'r' to show it is a raw string
coordinate_regex = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'


class Coordinate:
    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, a_latitude):
        if re.match(coordinate_regex, a_latitude):
            self._latitude = a_latitude
        else:
            ValueError("Latitude must be a valid integer if using DMS coordinates")

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude):
        if re.match(coordinate_regex, a_longitude):
            self._longitude = a_longitude
        else:
            ValueError("Latitude must be a valid integer if using DMS coordinates")

    def to_string(self):
        the_string = "{}, {}".format(self.latitude, self.longitude)
        return the_string
