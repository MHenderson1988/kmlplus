import simplekml
from kmlplus import paths, coordinates

def read_coordinates(*args, **kwargs):
    list_to_return = []
    origin = kwargs.pop('origin', None)
    for item in args:
        lat_string, long_string = item.split(',')
        if long_string[-1] == 'a':
            long_string = long_string[0:-1]
            coordinate_instance = coordinates.Coordinate(int(lat_string), int(long_string), coordinate_type='dms',
                                                         arc_direction='anticlockwise', start_of_arc=True,
                                                         arc_origin=origin)
        elif long_string[-1] == 'c':
            long_string = long_string[0:-1]
            coordinate_instance = coordinates.Coordinate(int(lat_string), int(long_string), coordinate_type='dms',
                                                         start_of_arc=True, arc_direction='clockwise',
                                                         arc_origin=origin)
        else:
            coordinate_instance = coordinates.Coordinate(int(lat_string), int(long_string), coordinate_type='dms')

        list_to_return.append(coordinate_instance)
    return list_to_return


frz_ref_point = coordinates.Coordinate(55.509392, -4.594581)
cta_1 = [
    "554023,-45040", "553734,-44227a", "552811,-44906", "553124,-45830", "554023,-45040"
]
cta_1_coordinates = read_coordinates(*cta_1, origin=frz_ref_point)
cta_1_lower = paths.LinePath(*cta_1_coordinates, height=1500, sort=False)
cta_1_higher = paths.LinePath(*cta_1_coordinates, height=5500, sort=False)
cta_1_lower.create_sides(cta_1_higher)


def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name="Example polygon")

    pol = fol.newpolygon(name='lower face of polygon')
    pol.outerboundaryis = cta_1_lower
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    kml.save('Floating polygon example.kml')


if __name__ == "__main__":
    create_kml()

"""# You can then use your LinePath instances to render your polygons using SimpleKML.

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
    create_kml()"""
