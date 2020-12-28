from geographiclib.geodesic import Geodesic

"""
This function takes 2 arguments of the coordinate class type and calculates the bearing between the two locations.
This is used in the creation of arcs/circles.  It returns a float representing a bearing from coordinate 1
to coordinate 2.  This bearing is based upon true north, not magnetic north.
"""


def get_bearing(coordinate_class_1, coordinate_class_2):
    geo_dict = Geodesic.WGS84.Inverse(coordinate_class_1.latitude, coordinate_class_1.longitude,
                                      coordinate_class_2.latitude, coordinate_class_2.longitude)

    bearing = geo_dict['azi1'] % 360
    return round(bearing, 2)
