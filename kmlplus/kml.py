import simplekml
from kmlplus.shapes import Kml3D


def create_polygon(coordinate_list, **kwargs):
    lower_poly_name = kwargs.get('lower_name', 'Lower Polygon')
    upper_poly_name = kwargs.get('upper_name', 'Upper Polygon')
    lower_layer = kwargs.get('lower_layer', None)
    upper_layer = kwargs.get('upper_layer', None)

    poly = Kml3D(coordinate_list, coordinate_list, lower_layer=lower_layer, upper_layer=upper_layer)
    lower, upper, sides = poly.to_kml()

    kml = simplekml.Kml()
    lower_pol = kml.newpolygon(name=f'{lower_poly_name}')
    lower_pol.outerboundaryis = lower
    lower_pol.polystyle.color = simplekml.Color.grey
    lower_pol.altitudemode = simplekml.AltitudeMode.relativetoground

    upper_pol = kml.newpolygon(name=f'{upper_poly_name}')
    upper_pol.outerboundaryis = upper
    lower_pol.polystyle.color = simplekml.Color.grey
    upper_pol.altitudemode = simplekml.AltitudeMode.relativetoground

    for coords in sides:
        side_pol = kml.newpolygon(name='A side')
        side_pol.outerboundaryis = coords
        lower_pol.polystyle.color = simplekml.Color.grey
        side_pol.altitudemode = simplekml.AltitudeMode.relativetoground

    kml.save("Point Styling.kml")


if __name__ == '__main__':
    curved_layer_alt_height = ['53.202121 -3.212121 12000',
                               'start=55.2222222 -4.111111 9000, end=55.0 -4.1 20000, direction=clockwise']
    curved_layer = ['start=55.2222222 -4.111111 200, end=55.0 -4.1 8000, direction=anticlockwise',
                    '55.2222222 -4.111111']
    straight_layer = ['22.323232 -4.287282 100', '23.323232 -5.328723 150', '22.112333 -6.23789238923 200',
                      '22.323232 -4.287282 100']

    aberdeen = ['572100N 0023356W', '572100N 0015802W',
                'start=571522N 0015428W, end=570850N 0022913W, centre=571207N 0021152W',
                'start=571520N 0023326W, end=572100N 0023356W, center=571834N 0021602W']
    london_fir = [
        '550000N 0050000E',
        '513000N 0020000E',
        '510700N 0020000E',
        '510000N 0012800E',
        '504000N 0012800E',
        '500000N 0001500W',
        '500000N 0020000W',
        '485000N 0080000W',
        '510000N 0080000W',
        '522000N 0053000W',
        '550000N 0053000W',
        '550000N 0050000E'
    ]

    birmingham_cta_10 = [
        '521803N 0021116W',
        '521544N 0020755W',
        '521634N 0015214W',
        'start=521447N 0015012W, centre=522722N 0014502W, end=521423N 0014442W, direction=anticlockwise',
        '520711N 0014056W',
        '520648N 0020148W',
        '521702N 0021251W',
        '521803N 0021116W'
    ]
