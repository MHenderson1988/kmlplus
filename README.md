# KMLPlus

KMLPlus is library of code for Python which allows the user to easily create standard and 'floating' Polygons, Circles
and Arcs.

## Who is this for

This is for anyone who wishes to easily render polygons, especially 'floating' or curved polygons within Google Earth.

I work in the aviation industry and needed a reliable way to create models of our airspace.  It its useful for creating
models of airways and controlled airspace.  It can be used for anything that takes your fancy!

## Installation

```
pip install kmlplus
```

## Usage

### The Coordinate class
The coordinate class allows the user to create Coordinate objects in either decimal or DMS (Degrees minutes seconds)
format.  Whilst .kml uses decimal coordinates in the longitude, latitude format, KMLPlus takes care of automatically
converting between coordinate types and presenting data in a .kml friendly format.

Creating your first Coordinate object is simple - 

```
from kmlplus import coordinates

# Create a new Coordinate instance
my_coordinate = coordinates.Coordinate(55.23823, -4.37433)
```

We can add a height value to be represented in metres -

```
# Create a new Coordinate instance with a height of 34m
my_coordinate = coordinates.Coordinate(55.23823, -4.37433, height=34)
```

If you're providing a coordinate in DMS format, tell the object so that it can convert it when the time comes - 

```
# Create a Coordinate instance using degrees minutes seconds with a height of 50m
my_coordinate = coordinates.Coordinate(552343, -45432, height=50, coordinate_type='dms'
```

We can specify the creation of a new Coordinate instance by giving a distance, bearing and height from an existing
instance.  We can also obtain a bearing and distance between two coordinate instances.

```
# Create a new coordinate 10km away on a bearing of 250 degrees and 0m height
my_new_coordinate = my_current_coordinate.generate_coordinate(10, 250, 0)

# Get bearing and distance values between two instances.
bearing, distance = my_current_coordinate.get_bearing_and_distance(another_coordinate_instance)
```

### The ArcPath class

The ArcPath class can be used to create arcs and circular polygons.  It takes a central 'origin' point and will create
multiple Coordinate points between the 'start' and 'end' bearings stated by the user.  Creating a circle is as easy as
giving a start heading of 1 and end heading of 359. 

```
from kmlplus import paths
my_circle = paths.ArcPath(my_origin_coordinate, start_bearing=1, end_bearing=359, radius=10, **kwargs)
```

#### The Kwargs
- points -> int - how many points to render between the start and end bearings.  Default = 50 
- height -> int or float - Specifies the height attribute of the Coordinate points to be created.  Defaults to the height 
of the origin Coordinate instance. 
- direction -> str - accepts 'Clockwise' and 'Anticlockwise'.  Default - 'Clockwise'

```
my_circle = paths.ArcPath(my_origin_coordinate, start_bearing=1, end_bearing=359, radius=10, points=100, height=400,
direction='Anticlockwise')
```


### The LinePath class

The LinePath class takes ArcPath and Coordinate instances and produces your polygons.  The most important method of the
class is the create_sides() method.  This method drawns the sides of the polygon between two LinePath instances of equal
length.

```
from kmlplus import paths
my_linepath_lower_surface = paths.LinePath(coordinate_1, coordinate_2, *my_arc_path_instance)
```

create_sides() is the most important function for creating floating 3D polygons.  It takes two LinePath instances of
equal length and creates the polygons required to create the sides between two LinePath instances.  This is what creates
the faux 'floating polygon' effect.

```
my_linepath_lower_surface = paths.LinePath(coordinate_1, coordinate_2, *my_arc_path_instance)
my_linepath_upper_surface = paths.LinePath(coordinate_1_higher_alt, coordinate_2_higher_alt, *my_higher_arc_path
sort=True)
my_linepath_lower_surface.create_sides(my_linepath_upper_surface)
print(my_linepath_lower_surface.sides)
```

#### The Kwargs
- sort -> str - If 'True' the linepath will reorder it's vertices to be rendered anticlockwise around the polygon's centroid.
  Default 'False'
- height -> int or float.  When given, will override the height attributes of all the coordinate instances provided.
Default 'None'

```
my_linepath_lower_surface = paths.LinePath(coordinate_1, coordinate_2, *my_arc_path_instance, sort=True, height=500)
```

### Your first floating polygon

```
import simplekml

from kmlplus import paths, coordinates

# Create a list of tuples in the coordinate format you wish.  DMS coordinates should be provided in DDMMSS format
# without any decimal places.  All coordinates should be presented in the Y, X or latitude, longitude format.

a_list = [(55.11, -4.11), (55.22, -4.11), (55.22, -4.22), (55.11, -4.22)]

# You can iterate through your list of tuples and create instances of the Coordinate object.  The coordinate object
# will accept a 'height' kwarg.

instance_list_lower = [coordinates.Coordinate(x[0], x[1], height=2000) for x in a_list]
instance_list_higher = [coordinates.Coordinate(x[0], x[1], height=6000) for x in a_list]

# Using your list of Coordinate instances, you can create instances of the LinePath object.  The LinePath argument
# will overwrite ALL coordinate instance height information if the LinePath takes a 'height' kwarg.  When the 'sort'
# kwarg is given as True (Default, False), the coordinates will be rearranged in anticlockwise order.  This is to allow
# for correct rendering by the Google Earth engine which needs vertices to be drawn anticlockwise.

lower_surface, upper_surface = paths.LinePath(*instance_list_lower, height=8000, sort=True), \
                               paths.LinePath(*instance_list_higher, height=15000, sort=True)
lower_surface.create_sides(upper_surface)

# You can then use your LinePath instances to render your polygons using SimpleKML.

def create_kml():
    kml = simplekml.Kml()
    fol = kml.newfolder(name="Example polygon")

    pol = fol.newpolygon(name='lower face of polygon')
    pol.outerboundaryis = lower_surface.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    pol = fol.newpolygon()
    pol.outerboundaryis = upper_surface.kml_coordinate_list
    pol.altitudemode = simplekml.AltitudeMode.relativetoground

    i = 0
    for coord_lists in lower_surface.sides:
        pol = fol.newpolygon()
        pol.outerboundaryis = coord_lists
        pol.altitudemode = simplekml.AltitudeMode.relativetoground
        i += 1

    kml.save('..\Floating polygon example.kml')
```



