"""
The arc class provides functionality to return a list of kml friendly coordinates (y, x, z as opposed to the traditional
x, y, z).  It has four parameters - start, end, centre and direction.

Start, end and centre all accept arguments of the coordinate class.  Start represents the coordinates at which to start
populating the list of coordinates and end is the respective point at which to stop.  Direction allows the user to draw
an arc from the start to the end point in the desired direction (clockwise or anticlockwise).  The centre point is the 
reference point (centre) of the arc.
"""


class Arc:
    def __init__(self, start, end, centre, direction):
        self.start = start
        self.end = end
        self.centre = centre
        self.direction = direction
