"""
The ArcPath class is used to return a tuple list of coordinates in .kml readable format ie - y, x, z.  It accepts the 
following parameters - 

origin - an x, y coordinate string which indicates the central location from which the arc will be drawn.
start_hdg - a heading/bearing relative to the origin from which the arc will commence
end_hdg - a heading/bearing relative to the origin at which the arc will end
radius - the distance from the origin the arc points will be plotted.  Accepts an int or float representing metres.

returns - a list of y, x, z tuples.
"""


class ArcPath:
    def __init__(self, origin, start_bearing, end_bearing, radius, **kwargs):
        self.__dict__.update(kwargs)
        self.origin = origin
        self.start_bearing = start_bearing
        self.end_bearing = end_bearing
        self.radius = radius
        # if no height provided, defaults to the height of the origin coordinate
        self.height = kwargs.pop('height', self.origin.height)
        self.direction = kwargs.pop('direction', 'Clockwise')
        self.points = kwargs.pop('points', 50)
        self.kml_coordinates = self.coordinates_to_kml_format()

    def calculate_heading_increments(self):
        if self.end_bearing > self.start_bearing:
            difference = (self.end_bearing - self.start_bearing) % 360
        else:
            difference = (self.start_bearing - self.end_bearing) % 360

        incremental_heading_value = difference / self.points
        return incremental_heading_value

    def populate_path_list(self):
        coordinates_list = []
        increments = self.calculate_heading_increments()

        while coordinates_list.__len__() < self.points:
            coordinates_list.append(self.origin.generate_coordinates(self.radius, self.start_bearing, self.height))
            if self.direction == 'Clockwise':
                self.start_bearing = (self.start_bearing - increments) % 360
            else:
                self.start_bearing = (self.start_bearing + increments) % 360
        return coordinates_list

    def coordinates_to_kml_format(self):
        coordinate_list = self.populate_path_list()
        kml_format_list = []
        for coordinate_instance in coordinate_list:
            kml_format_list.append(coordinate_instance.kml_tuple())
        return kml_format_list
