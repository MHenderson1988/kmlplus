"""
This example file gives a demonstration of how you may use DMS coordinates
as given by the CAA for constructing airspace.  The DDMMSS format is suffixed with
'a' or 'c' at the end of coordinates which begin either a clockwise or anticlockwise
arc.  'read_coordinates' is provided as an example of how one could iterate through
such a list to automatically generate polygons such as airspace.

The example requires the installation of simple kml which can be achieved via -
# pip install simplekml
"""
import simplekml

from kmlplus import paths, coordinates

"""
Make lists of the EGPK CTA areas, as provided on the CAA AIP.  Suffix a denotes the start of an anticlockwise arc
and c denotes the start of a clockwise arc.  Both arcs are based upon the FRZ reference point.
"""
frz_ref_point = coordinates.Coordinate(55.509392, -4.594581)
cta_1 = [
    "554023,-45040", "553734,-44227a", "552811,-44906", "553124,-45830", "554023,-45040"
]

cta_2 = [
    "553044,-44945", "552703,-43902", "552518,-44044", "552811,-44906c", "553044,-44945"
]

cta_3 = [
    "552703,-43902", "552150,-42400c", "552040,-42722", "552518,-44044",
    "552703,-43902"
]

cta_4 = [
    "552838,-41639", "552658,-41154c", "552010,-41916", "552150,-42400a", "552838,-41639"
]

cta_5 = [
    "553124,-45830", "552040,-42722", "551848,-44702", "553124,-45830"
]

cta_6 = [
    "552658,-41154", "552521,-40716c", "551710,-41723", "552040,-42722a", "552150,-42400", "552010,-41916a",
    "552658,-41154"
]

"""
Using the create_polygon function to automate the creation of all coordinates related to cta_1.  Create a new linepath
for the lower layer before creating the upper layer and sides.  These returns can be used to render the full polygon in 
SimpleKml.
"""


def create_polygon(a_list, lower_height, upper_height, arc_origin, **kwargs):
    lp = paths.LinePath(*a_list, height=lower_height, origin=arc_origin)
    lp2, sides = lp.create_layer_and_sides(height=upper_height, origin=arc_origin)
    return lp, lp2, sides


cta_1_lower, cta_1_upper, cta_1_sides = create_polygon(cta_1, 1500, 5500, frz_ref_point)
cta_2_lower, cta_2_upper, cta_2_sides = create_polygon(cta_2, 2000, 5500, frz_ref_point)
cta_3_lower, cta_3_upper, cta_3_sides = create_polygon(cta_3, 3000, 5500, frz_ref_point)
cta_4_lower, cta_4_upper, cta_4_sides = create_polygon(cta_4, 3000, 5500, frz_ref_point)
cta_5_lower, cta_5_upper, cta_5_sides = create_polygon(cta_5, 3500, 5500, frz_ref_point)
cta_6_lower, cta_6_upper, cta_6_sides = create_polygon(cta_6, 4000, 5500, frz_ref_point)


def create_airspace(a_folder, lower_layer, upper_layer, sides):
    pol = a_folder.newpolygon()
    pol.outerboundaryis = lower_layer
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = a_folder.newpolygon()
    pol.outerboundaryis = upper_layer
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    for item in sides:
        pol = a_folder.newpolygon()
        pol.outerboundaryis = item
        pol.altitudemode = simplekml.AltitudeMode.relativetoground


def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name='Example')

    create_airspace(fol, cta_1_lower, cta_1_upper, cta_1_sides)
    create_airspace(fol, cta_2_lower, cta_2_upper, cta_2_sides)
    create_airspace(fol, cta_3_lower, cta_3_upper, cta_3_sides)
    create_airspace(fol, cta_4_lower, cta_4_upper, cta_4_sides)
    create_airspace(fol, cta_5_lower, cta_5_upper, cta_5_sides)
    create_airspace(fol, cta_6_lower, cta_6_upper, cta_6_sides)

    kml.save('Airspace example.kml')


if __name__ == "__main__":
    create_kml()
