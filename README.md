# KML+

KML+ (KMLPlus) is library of code for Python which allows the user to easily create standard and 'floating' Polygons,
Circles and Arcs.

## Who is this for

This is for anyone who wishes to easily render polygons, especially 'floating' or curved polygons within Google Earth.

I work in the aviation industry and needed a reliable way to create models of our airspace. It its useful for creating
models of airways and controlled airspace. It can be used for anything that takes your fancy!

![Prestwick airspace example](img/egpk_airspace_sideon.png)

![Floating polygon example](img/floating_polygon_1.jpg)

## Installation

### pip

```
pip install kmlplus
```

## Usage

### Recommendations

KML+ easily integrates with the fantastic [Simplekml](https://pypi.org/project/simplekml/) library and I highly
recommend using it in conjunction with KML+ for the best experience.

Take a look at the example .py file provided to see how KML+ integrates with SimpleKML to create airspace
representations from CAA AIP supplied data.

### Classes

KML+ comprises three classes -

- Coordinate class
- LinePath class
- ArcPath class

The user should be able to create simple floating polygons without touching the ArcPath class however it is documented
here in case you should wish to use it in other ways.

***

#### Coordinate

```Coordinate(**args, name=None, arc_direction=None, arc_origin=None*)```

The Coordinate class accepts up to three arguments - latitude, longitude and height. This can be given as either one
string or three separate arguments. Latitude and longitude must be either decimal coordinates or degrees minutes
seconds (DMS). The coordinate object will auto-detect the coordinate type and will automatically convert DMS coordinates
to kml readable decimal coordinates.

Coordinate instances can also be designated as the start point of a clockwise or anti-clockwise arc/circle. This is
achieved by appending either 'a' or 'c' to end of the latitude or longitude value.

Examples -

```
from kmlplus import coordinates

# A standard coordinate object with a default height of 0
c1 = coordinates.Coordinate(55.123, -4.1234)

# The same coordinate initialised with a height of 50m
c1 = coordinates.Coordinate(55.123, -4.1234, 50)

# Now with a string
c1 = coordinates.Coordinate("55.123, -4.1234")

# Specifying that this coordinate is the start of a clockwise 'arc'
c1 = coordinates.Coordinate(55.123, '-4.1234c')

# You can combine coordinate types
c1 = coordinates.Coordinate(55.123, '-41232.327847834c')
```

A note on arcs -

* Values must be passed as a String eg - "55.22132c" is valid, 55.22132c will throw an error

* If kwarg arc_origin is not passed, it will default to the centroid of the LineString created later on.

***

#### LinePath

The LinePath class takes Coordinate objects or lists of Coordinate objects as its arguments. If a Coordinate object
defines itself as the start of a clockwise or anticlockwise arc, the LinePath class will call an ArcPath instance. This
will automatically create the required arc as part of the LinePath objects coordinates.

```LinePath(*args, sort=False, height=None, points=50*)```

*args must all be instances of Type Coordinate.

*sort=True* will sort the Coordinate objects into anticlockwise order around the polygon's centroid therefore allowing
correct rendering by Google Earth. This is experimental and is highly unlikely to work with concave polygons.

*height=float or int* will override all height values in the Coordinate arguments.

*points=int* will define how many coordinates should be created for any detected arcs/circles.

```
from kmlplus import paths
my_line_path = paths.Linepath(coordinate_1, coordinate_2, *arcpath_1)
```

Sides of polygons are generated using the LinePath.create_sides(*another_linepath*). See the example code supplied.

ArcPath objects must be passed as iterable arguments by using the * operator.

***

#### ArcPath

```ArcPath(*origin, start_bearing, end_bearing, radius, height=self.origin.height, direction='Clockwise', points=50*)```

ArcPath objects are used to create a series of Coordinate objects to simulate a circle or arc which starts and ends on a
specified bearing from a specified origin at a given radius. They can be 'Clockwise' or 'Anticlockwise' and return as
many or as few 'points' as desired.

#### Acknowledgements

- [Simplekml](https://pypi.org/project/simplekml/) - for creating an awesome library which has helped me create many
  things and also inspiring me to write this library.`


