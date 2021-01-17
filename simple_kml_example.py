"""
This example file gives a demonstration of how you may use DMS coordinates
as given by the CAA for constructing airspace.  The DDMMSS format is suffixed with
'a' or 'c' at the end of coordinates which begin either a clockwise or anticlockwise
arc.  'read_coordinates' is provided as an example of how one could iterate through
such a list to automatically generate polygons such as airspace.

The example requires the installation of simple kml which can be achieved via -
# pip install simplekml
"""

import copy
import simplekml

from kmlplus import paths, coordinates


def read_coordinates(*args, **kwargs):
    list_to_return = []
    # Provide a reference point, as supplied by CAA in AIP, for arcs
    origin = kwargs.pop('origin', None)
    lower_height = kwargs.pop('lower_height', 1500)
    upper_height = kwargs.pop('upper_height', 5500)
    # Retrieve each DMS coordinate in the list supplied
    for item in args:
        # Split the string into lat and long
        lat_string, long_string = item.split(',')
        # If the coordinate is the start of an arc do the following
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
        # If not the start of an arc, just create a normal new coordinate
        else:
            coordinate_instance = coordinates.Coordinate(int(lat_string), int(long_string), coordinate_type='dms')

        list_to_return.append(coordinate_instance)

    lower, upper = create_upper_lower(list_to_return, lower_height, upper_height)
    return lower, upper


"""If using the same coordinates but different heights for your upper and lower
levels.  Do one of two things - 

Two SEPARATE lists with new objects created for each ie use the read_coordinates twice
OR import copy as is seen below and create a deep copy of the first list. 

If you do not then the 'height' kwarg will malfunction and will keep overwriting
existing objects in both layers resulting in a failed polygon"""


def create_upper_lower(a_list, lower_height, upper_height):
    a_list_copy = copy.deepcopy(a_list)
    lower = paths.LinePath(*a_list, height=lower_height)
    upper = paths.LinePath(*a_list_copy, height=upper_height)
    return lower, upper


frz_ref_point = coordinates.Coordinate(55.509392, -4.594581)
cta_1 = [
    "554023,-45040", "553734,-44227a", "552811,-44906", "553124,-45830", "554023,-45040"
]

cta_2 = [
    "553044,-44945", "552703,-43902", "552518,-44044", "552811,-44906c", "553044,-44945"
]

cta_1_lower, cta_1_higher = read_coordinates(*cta_1, origin=frz_ref_point, lower_height=1500, upper_height=5500)
cta_2_lower, cta_2_higher = read_coordinates(*cta_2, origin=frz_ref_point, lower_height=2000, upper_height=5500)
cta_1_lower.create_sides(cta_1_higher)
cta_2_lower.create_sides(cta_2_higher)


def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name="CTA1")

    pol = fol.newpolygon(name='lower face of polygon')
    pol.outerboundaryis = cta_1_lower
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon(name='Upper face of polygon')
    pol.outerboundaryis = cta_1_higher
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    for item in cta_1_lower.sides:
        pol = fol.newpolygon()
        pol.outerboundaryis = item
        pol.altitudemode = simplekml.AltitudeMode.relativetoground

    fol = kml.newfolder(name="CTA2")

    pol = fol.newpolygon(name='lower face of polygon')
    pol.outerboundaryis = cta_2_lower
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon(name='Upper face of polygon')
    pol.outerboundaryis = cta_2_higher
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    for item in cta_2_lower.sides:
        pol = fol.newpolygon()
        pol.outerboundaryis = item
        pol.altitudemode = simplekml.AltitudeMode.relativetoground

    kml.save('Floating polygon example.kml')


if __name__ == "__main__":
    create_kml()
