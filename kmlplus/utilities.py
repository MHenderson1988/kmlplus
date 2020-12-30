from geographiclib.geodesic import Geodesic

"""
This function takes 2 arguments of the coordinate class type and calculates the bearing between the two locations.
This is used in the creation of arcs/circles.
"""


def get_bearing(coordinate_class_1, coordinate_class_2):
    geo_dict = Geodesic.WGS84.Inverse(coordinate_class_1.latitude, coordinate_class_1.longitude,
                                      coordinate_class_2.latitude, coordinate_class_2.longitude)

    bearing = geo_dict['azi1'] % 360
    return round(bearing, 2)
