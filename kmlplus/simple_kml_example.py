import simplekml
from kmlplus import paths, coordinates, floatingpolygon

a_list = [(55.11, -4.11), (55.22, -4.11), (55.22, -4.22), (5.11, -4.22)]
instance_list = [coordinates.Coordinate(x[0], x[1], height=20) for x in a_list]
instance_list_higher = [coordinates.Coordinate(x[0], x[1], height=200) for x in a_list]

def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name="Example polygon")
    lower_surface, upper_surface = paths.LinePath(instance_list), paths.LinePath(instance_list_higher)
    floating_poly = floatingpolygon.FloatingPolygon(lower_surface, upper_surface)
    sides = floating_poly.sides

    pol = fol.newpolygon()
    pol.outerboundaryis = lower_surface
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = upper_surface
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = sides
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    kml.save('Floating polygon example.kml')

if __name__ == "__main__":
    create_kml()