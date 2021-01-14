# KML+

KML+ (KMLPlus) is library of code for Python which allows the user to easily create standard and 'floating' Polygons, Circles
and Arcs.

## Who is this for

This is for anyone who wishes to easily render polygons, especially 'floating' or curved polygons within Google Earth.

I work in the aviation industry and needed a reliable way to create models of our airspace.  It its useful for creating
models of airways and controlled airspace.  It can be used for anything that takes your fancy!

![Floating polygon example](img/floating_polygon_1.jpg)

![Prestwick airspace example](img/egpk_airspace_sideon.png)

## Installation
###pip
```
pip install kmlplus
```

## Usage

###Recommendations

KML+ easily integrates with the fantastic [Simplekml](https://pypi.org/project/simplekml/) library and I highly
recommend using it in conjunction with KML+ for the best experience.  

### Classes

KML+ is comprised of three classes -

- Coordinate class
- LinePath class
- ArcPath class


#### Coordinate

Coordinate(*lat, long, height=0, name=None, coordinate_type='decimal', start_of_arc=None, arc_direction=None,
arc_origin=None*)

```
from kmlplus import coordinates
my_new_coordinate = coordinates.Coordinate(55.22, -4.12432)
```

You can also use Degrees Minutes Seconds (DMS) however you must state this on creation.

```
my_dms_coordinate = coordinates.Coordinate(552233, -43212, coordinate_type='dms')
```

Coordinates Objects can automatically create an ArcPath when passed to the LinePath class using the *start_of_arc=None, arc_direction=None,
arc_origin=None* kwargs.  When doing so, the ArcPath bearing and radius will be calculated between the Coordinate and the Origin.
The ArcPath will end at the next argument or will return the first if it is the last argument passed.

```
coordinate_arc_start = (55.22, -4.11, start_of_arc=True, arc_direction='Clockwise', arc_origin=an_origin_coordinate
lp = paths.LinePath(c1, c2, coordinate_arc_start, c4)
```

In the above example the coordinate_arc_start instance will prompt the creation of an arc in a clockwise direction to the next argument - c4.
If it was the last argument passed, the arc would end at c1, thereby 'closing' the polygon.

#### LinePath

LinePath(*args, sort=False, height=None*)

LinePath args MUST be Coordinate objects.

*sort=True* will sort the Coordinate objects into anticlockwise order around the polygon's centroid therefore allowing 
correct rendering by Google Earth.  This is experimental and is highly unlikely to work with concave polygons.

*height=float or int* will override all height values in the Coordinate arguments.  

```
from kmlplus import paths
my_line_path = paths.Linepath(coordinate_1, coordinate_2, *arcpath_1)
```

Sides of polygons are generated using the LinePath.create_sides(*another_linepath*).  See the example code supplied.

ArcPath objects must be passed as iterable arguments by using the * operator.

#### ArcPath

ArcPath(*origin, start_bearing, end_bearing, radius, height=self.origin.height, direction='Clockwise', points=50*)

ArcPath objects are used to create a series of Coordinate objects to simulate a circle or arc which starts and ends on a
specified bearing from a specified origin at a given radius.  They can be 'Clockwise' or 'Anticlockwise' and return as
many or as few 'points' as desired.
 

#### Acknowledgements

- [Simplekml](https://pypi.org/project/simplekml/) - for creating an awesome library which has helped me create many
things and also inspiring me to write this library.`


