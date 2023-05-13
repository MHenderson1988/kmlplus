import simplekml
from kmlplus.shapes import Kml3D

if __name__ == '__main__':
    layer = ['start=55.23211 -4.122121, end=55.054541 -4.1111, direction=anticlockwise', '55.23211 -4.122121']

    poly = Kml3D(layer, layer, upper_layer=5000)
    lower, upper, sides = poly.to_kml()

    kml = simplekml.Kml()
    lower_pol = kml.newpolygon(name='A Polygon')
    lower_pol.outerboundaryis = lower
    lower_pol.polystyle.color = simplekml.Color.grey
    lower_pol.altitudemode = simplekml.AltitudeMode.relativetoground

    upper_pol = kml.newpolygon(name='A Polygon')
    upper_pol.outerboundaryis = upper
    lower_pol.polystyle.color = simplekml.Color.grey
    upper_pol.altitudemode = simplekml.AltitudeMode.relativetoground

    for coords in sides:
        side_pol = kml.newpolygon(name='A side')
        side_pol.outerboundaryis = coords
        lower_pol.polystyle.color = simplekml.Color.grey
        side_pol.altitudemode = simplekml.AltitudeMode.relativetoground

    kml.save("Point Styling.kml")
