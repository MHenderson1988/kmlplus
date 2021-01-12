import simplekml
from kmlplus import paths, coordinates, floatingpolygon

a_list = [(55.11, -4.11), (55.22, -4.11), (55.22, -4.22), (55.11, -4.22)]
instance_list = [coordinates.Coordinate(x[0], x[1], height=2000) for x in a_list]
instance_list_higher = [coordinates.Coordinate(x[0], x[1], height=6000) for x in a_list]
lower_surface, upper_surface = paths.LinePath(*instance_list, sort=True), paths.LinePath(*instance_list_higher, sort=True)
floating_poly = floatingpolygon.FloatingPolygon(lower_surface, upper_surface)


def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name="Example polygon")
    sides = floating_poly.sides

    pol = fol.newpolygon()
    pol.outerboundaryis = lower_surface.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = upper_surface.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = sides.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    kml.save('Floating polygon example.kml')


if __name__ == "__main__":
    create_kml()