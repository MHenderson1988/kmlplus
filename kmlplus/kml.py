import simplekml
from kmlplus.shapes import Kml3D
import test_data.airspace

class KmlPlus:
    def __init__(self, save_name, **kwargs):
        self.output_path = kwargs.get('output', None)
        self.save_name = save_name        
        self.kml = simplekml.Kml()
    
    def polyhedron(self, coordinate_list, **kwargs):
        name = kwargs.get('name', None)
        colour_hex = kwargs.get('colour_hex', '7Fc0c0c0')
        lower_poly_name = kwargs.get('lower_name', 'Lower Polygon')
        upper_poly_name = kwargs.get('upper_name', 'Upper Polygon')
        lower_layer = kwargs.get('lower_layer', None)
        upper_layer = kwargs.get('upper_layer', None)
        
        poly = Kml3D(coordinate_list, coordinate_list, lower_layer=lower_layer, upper_layer=upper_layer)
        lower, upper, sides = poly.to_kml()
        
        if name:
            
            fol = self.kml.newfolder(name=name)
            
            lower_pol = fol.newpolygon(name=lower_poly_name)
            lower_pol.outerboundaryis = lower
            lower_pol.polystyle.color = colour_hex
            lower_pol.altitudemode = simplekml.AltitudeMode.relativetoground
        
            upper_pol = fol.newpolygon(name=upper_poly_name)
            upper_pol.outerboundaryis = upper
            upper_pol.polystyle.color = colour_hex
            upper_pol.altitudemode = simplekml.AltitudeMode.relativetoground
        
            for coords in sides:
                side_pol = fol.newpolygon(name='A side')
                side_pol.outerboundaryis = coords
                side_pol.polystyle.color = colour_hex
                side_pol.altitudemode = simplekml.AltitudeMode.relativetoground
                
        else:
            lower_pol = self.kml.newpolygon(name=lower_poly_name)
            lower_pol.outerboundaryis = lower
            lower_pol.polystyle.color = colour_hex
            lower_pol.altitudemode = simplekml.AltitudeMode.relativetoground
        
            upper_pol = self.kml.newpolygon(name=upper_poly_name)
            upper_pol.outerboundaryis = upper
            uipper_pol.polystyle.color = colour_hex
            upper_pol.altitudemode = simplekml.AltitudeMode.relativetoground
        
            for coords in sides:
                side_pol = self.kml.newpolygon(name='A side')
                side_pol.outerboundaryis = coords
                side_pol.polystyle.color = colour_hex
                side_pol.altitudemode = simplekml.AltitudeMode.relativetoground
    
        self.kml.save(self.save_name)


if __name__ == '__main__':
    kml_file = KmlPlus('Point Styling.kml')
    kml_file.polyhedron(test_data.airspace.london_fir, lower_layer=19500, upper_layer=24500, name='London FIR')
    kml_file.polyhedron(test_data.airspace.birmingham_cta_10, lower_layer=6500, upper_layer=10500, name='Birmingham CTA 10')
    kml_file.polyhedron(test_data.airspace.birmingham_cta_9, lower_layer=6500, upper_layer=8500, name='Birmingham CTA 9')
    kml_file.polyhedron(test_data.airspace.prestwick_cta_1, lower_layer=1500, upper_layer=5500, name='Prestwick CTA 1')