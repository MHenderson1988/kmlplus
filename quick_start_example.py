import simplekml
from kmlplus import paths

# Auto generate a linepath polygon from a list of string representations of coordinates in latitude, longitude, height
# format.  Can be a mix of DMS and decimal.  Make sure the last and first coordinate are the same, otherwise the
# Polygon will not complete
list_of_coordinates = ["55.123, -4.123", "55.600, -41232.12", "55.100, -4.4323", "55.123, -4.123"]

# Pass the list to the LinePath constructor.  You can override the height at this point with the 'height' kwarg.
lower_layer = paths.LinePath(*list_of_coordinates, height=3000)

# Create the upper layer at 800m, and fill in the sides between the two
upper_layer, sides = lower_layer.create_layer_and_sides(height=10000)

# Use simplekml to create the .kml
def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name='Quick start example')

    pol = fol.newpolygon()
    pol.outerboundaryis = lower_layer
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = upper_layer
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    for item in sides:
        pol = fol.newpolygon()
        pol.outerboundaryis = item
        pol.altitudemode = simplekml.AltitudeMode.relativetoground

    kml.save('Quick start example.kml')


if __name__ == "__main__":
    create_kml()
