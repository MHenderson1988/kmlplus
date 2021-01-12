import simplekml
from kmlplus import paths, coordinates

a_list = [(55.11, -4.11), (55.22, -4.11), (55.22, -4.22), (55.11, -4.22)]
instance_list = [coordinates.Coordinate(x[0], x[1], height=2000) for x in a_list]
instance_list_higher = [coordinates.Coordinate(x[0], x[1], height=6000) for x in a_list]
lower_surface, upper_surface = paths.LinePath(*instance_list, height=8000, sort=True),\
                               paths.LinePath(*instance_list_higher, height=15000, sort=True)
lower_surface.create_sides(upper_surface)

origin_coordinate = coordinates.Coordinate(55.66, -4.55)

# Warning: Do not use height kwarg when making a second LinePath of the same coordinates.  The height kwarg will
# override both coordinates as they share the same instance.  You will end up with all sides starting and ending
# on the same altitude and therefore appearing not to render.

# Specify all height kwargs for identical LinePaths in their instance creation as seen below alternatively
# create two sets of coordinate instances of different heights as seen above.  This will be corrected in future
# releases.

arc_path_lower = paths.ArcPath(origin_coordinate, start_bearing=1, end_bearing=359, radius=2, height=200)
arc_path_higher = paths.ArcPath(origin_coordinate, start_bearing=1, end_bearing=359, radius=2, height=5000)
circle_line_path_low = paths.LinePath(*arc_path_lower)
circle_line_path_high = paths.LinePath(*arc_path_higher)
circle_line_path_low.create_sides(circle_line_path_high)


def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name="Example polygon")

    pol = fol.newpolygon()
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