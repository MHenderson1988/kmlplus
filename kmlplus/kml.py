import simplekml
from kmlplus.shapes import Kml3D

if __name__ == '__main__':
    curved_layer_alt_height = ['53.202121 -3.212121 12000','start=55.2222222 -4.111111 9000, end=55.0 -4.1 20000, direction=clockwise']
    curved_layer = ['start=55.2222222 -4.111111 200, end=55.0 -4.1 8000, direction=anticlockwise', '55.2222222 -4.111111']
    straight_layer = ['22.323232 -4.287282 100', '23.323232 -5.328723 150', '22.112333 -6.23789238923 200', '22.323232 -4.287282 100']

    aberdeen = ['572100N 0023356W', '572100N 0015802W', 'start=571522N 0015428W, end=570850N 0022913W, centre=571207N 0021152W', 'start=571520N 0023326W, end=572100N 0023356W, center=571834N 0021602W']

    poly = Kml3D(aberdeen, aberdeen, upper_layer=11500)
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
