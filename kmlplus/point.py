from kmlplus.util import dms_to_decimal


class Point:
    def __init__(self, y, x, **kwargs):
        self.latitude = y
        self.longitude = x
        self.elevation = kwargs.pop('elevation', 0)

    @classmethod
    def from_decimal_degrees(cls, y, x, z):
        return cls(y, x, elevation=z)

    @classmethod
    def from_dms(cls, y, x, z):
        y = dms_to_decimal(y)
        x = dms_to_decimal(x)
        return cls(y, x, elevation=z)

    @classmethod
    def from_utm(cls, y, x, z):
        return cls(y, x, elevation=z)

    def __str__(self):
        return f'{__class__} y: {self.latitude} x: {self.longitude} z: {self.elevation}'

    def __eq__(self, other):
        return self.__str__ == other.__str__
