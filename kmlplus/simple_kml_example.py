import simplekml

from kmlplus import paths, coordinates

# Create a list of tuples in the coordinate format you wish.  DMS coordinates should be provided in DDMMSS format
# without any decimal places.  All coordinates should be presented in the Y, X or latitude, longitude format.

a_list = [(55.11, -4.11), (55.22, -4.11), (55.22, -4.22), (55.11, -4.22)]

# You can iterate through your list of tuples and create instances of the Coordinate object.  The coordinate object
# will accept a 'height' kwarg.

instance_list_lower = [coordinates.Coordinate(x[0], x[1], height=2000) for x in a_list]
instance_list_higher = [coordinates.Coordinate(x[0], x[1], height=6000) for x in a_list]

# Using your list of Coordinate instances, you can create instances of the LinePath object.  The LinePath argument
# will overwrite ALL coordinate instance height information if the LinePath takes a 'height' kwarg.  When the 'sort'
# kwarg is given as True (Default, False), the coordinates will be rearranged in anticlockwise order.  This is to allow
# for correct rendering by the Google Earth engine which needs vertices to be drawn anticlockwise.

lower_surface, upper_surface = paths.LinePath(*instance_list_lower, height=8000, sort=True), \
                               paths.LinePath(*instance_list_higher, height=15000, sort=True)
lower_surface.create_sides(upper_surface)

# The ArcPath class allows you to create coordinate instances to draw an 'arc' or 'circle'.  This is based upon a
# 'central' point referred to as the origin.  The ArcPath will take a start and end bearing and radius from which to
# plot the arc points.  You can obtain your bearings by using the Coordinate.get_bearing_distance() method.

origin_coordinate = coordinates.Coordinate(55.66, -4.55)

# Warning: Do not use height kwarg when making a second LinePath of the same coordinates.  The height kwarg will
# override both coordinates as they share the same instance.  You will end up with all sides starting and ending
# on the same altitude and therefore appearing not to render.

# Specify all height kwargs for identical LinePaths in their instance creation as seen below alternatively
# create two sets of coordinate instances of different heights as seen above.  This will be corrected in future
# releases.

arc_path_lower = paths.ArcPath(origin_coordinate, start_bearing=1, end_bearing=359, radius=2, height=200)
arc_path_higher = paths.ArcPath(origin_coordinate, start_bearing=1, end_bearing=359, radius=2, height=5000)

# The LinePath instance can take all coordinates obtained from the ArcPath class by using the * prefix to iterate
# through the ArcPath object.

circle_line_path_low = paths.LinePath(*arc_path_lower)
circle_line_path_high = paths.LinePath(*arc_path_higher)

# To use the 'create_sides(LinePath instance here) method, both LinePath MUST be of identical length.  The method
# will create individual polygons between the 'square' vertices ie lower i, lower i+1, higher i+1, higher i.
circle_line_path_low.create_sides(circle_line_path_high)


# You can then use your LinePath instances to render your polygons using SimpleKML.

def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name="Example polygon")

    pol = fol.newpolygon(name='lower face of polygon')
    pol.outerboundaryis = lower_surface.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = upper_surface.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    i = 0
    for coord_lists in lower_surface.sides:
        pol = fol.newpolygon()
        pol.outerboundaryis = coord_lists
        pol.altitudemode = simplekml.AltitudeMode.relativetoground
        i += 1

    pol = fol.newpolygon()
    pol.outerboundaryis = circle_line_path_low.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = circle_line_path_high.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    i = 0
    for x in circle_line_path_low.sides:
        pol = fol.newpolygon()
        pol.outerboundaryis = x
        pol.altitudemode = simplekml.AltitudeMode.relativetoground
        i += 1

    kml.save('..\Floating polygon example.kml')


if __name__ == "__main__":
    create_kml()
