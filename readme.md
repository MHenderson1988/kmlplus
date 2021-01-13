# KMLPlus

KMLPlus is library of code for Python which allows the user to easily create standard and 'floating' Polygons, Circles
and Arcs.

## Who is this for

This is for anyone who wishes to easily render polygons, especially 'floating' or curved polygons within Google Earth.

I work in the aviation industry and needed a reliable way to create models of our airspace.  It its useful for creating
models of airways and controlled airspace.  It can be used for anything that takes your fancy!

## How it works

### The Coordinate class
The coordinate class allows the user to create Coordinate objects in either decimal or DMS (Degrees minutes seconds)
format.  Whilst .kml uses decimal coordinates in the longitude, latitude format, KMLPlus takes care of automatically
converting between coordinate types and presenting data in a .kml friendly format.

Creating your first Coordinate object is simple - 

```
from kmlplus import coordinates
my_coordinate = coordinates.Coordinate(55.23823, -4.37433)
```

We can add a height value to be represented in metres -

```
my_coordinate = coordinates.Coordinate(55.23823, -4.37433, height=34)
```

If you're providing a coordinate in DMS format, tell the object so that it can convert it when the time comes - 

```
my_coordinate = coordinates.Coordinate(552343, -45432, height=50, coordinate_type='dms'
```

### The ArcPath class

The ArcPath class can be used to create arcs and circular polygons.  It takes a central 'origin' point and will create
multiple Coordinate points between the 'start' and 'end' bearings stated by the user.  Creating a circle is as easy as
giving a start heading of 1 and end heading of 359. 

```
from kmlplus import paths
my_circle = paths.ArcPath(my_origin_coordinate, start_bearing=1, end_bearing=359, radius=10, **kwargs)
```

####**Kwargs
- points -> int - how many points to render between the start and end bearings.  Default = 50 \
- height -> int or float - Specifies the height attribute of the Coordinate points to be created.  Defaults to the height 
of the origin Coordinate instance. \
- direction -> str accepts 'Clockwise' and 'Anticlockwise'.  Default - 'Clockwise'

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

#### LinePath.create_sides()

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

####**Kwargs
- sort -> str - If 'True' the linepath will reorder it's vertices to be rendered anticlockwise around the polygon's centroid.
  Default 'False'
- height -> int or float.  When given, will override the height attributes of all the coordinate instances provided.
Default 'None'

```
my_linepath_lower_surface = paths.LinePath(coordinate_1, coordinate_2, *my_arc_path_instance, sort=True, height=500)
```

## Installation

TODO



