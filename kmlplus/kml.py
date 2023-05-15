import simplekml
from kmlplus.shapes import Kml3D

if __name__ == '__main__':
    curved_layer = ['start=55.2222222 -4.111111, end=55.0 -4.1, direction=anticlockwise, sample=200', '55.2222222 -4.111111']
    straight_layer = ['22.323232 -4.287282 100', '23.323232 -5.328723 150', '22.112333 -6.23789238923 200', '22.323232 -4.287282 100']

    poly = Kml3D(curved_layer, curved_layer, lower_layer=10000, upper_layer=20000)
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
