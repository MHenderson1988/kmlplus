class Point:
    def __init__(self, y, x, **kwargs):
        self.latitude = y
        self.longitude = x
        self.elevation = kwargs.pop('elevation', 0)

    @classmethod
    def from_decimal_degrees(cls, y, x, z):
        return cls(y, x, elevation = z)

    @classmethod
    def from_dms(cls, y, x, z):
        return cls(y, x, elevation = z)

    @classmethod
    def from_utm(cls, y, x, z):
        return cls(y, x, elevation = z)
