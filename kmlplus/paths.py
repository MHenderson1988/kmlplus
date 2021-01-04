from kmlplus import coordinates

"""
The paths class is used to return lists of tuples in the y,x,z format.  y, x, z is the format which is used by .kml as
opposed to the more regular x, y, z format.  Ie - kml requires longitude, latitude, height not latitude, longitude,
height as may appear more logical.

The paths class has two parameters - points and height which default to 50 points and 0 metres respectively.
"""


class LinePath:
    def __init__(self, origin, **kwargs):
        self.__dict__.update(kwargs)
        self.origin = origin
        self.points = kwargs.pop('points', 50)
        self.height = kwargs.pop('height', 0)
        self.path_list = self.generate_coordinates()

    """
    Generates a list of coordinate instances representing the points between the start and end heading as projected
    from the central point and radius.  Returns a list of coordinate class instances.
    """

    def generate_coordinates(self):
        coordinate_list = []

        return coordinate_list


"""
The ArcPath class is used to return a tuple list of coordinates in .kml readable format ie - y, x, z.  It accepts the 
following parameters - 

origin - an x, y coordinate string which indicates the central location from which the arc will be drawn.
start_hdg - a heading/bearing relative to the origin from which the arc will commence
end_hdg - a heading/bearing relative to the origin at which the arc will end
radius - the distance from the origin the arc points will be plotted.  Accepts an int or float representing metres.

returns - a list of y, x, z tuples.
"""


class ArcPath(LinePath):
    def __init__(self, origin, **kwargs):
        super().__init__(origin, **kwargs)
        self.start_bearing = kwargs.pop('start_bearing', 0)
        self.end_bearing = kwargs.pop('end_bearing', 359)
        self.radius = kwargs.pop('radius', 10)