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
        self._latitude = a_latitude

    @latitude.deleter
    def latitude(self):
        del self._latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, a_longitude):
        self._longitude = a_longitude

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
        the_string = "{}, {}, {}".format(self._latitude, self._longitude, self._height)
        return the_string
