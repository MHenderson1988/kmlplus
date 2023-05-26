KML+
===


KML+ (KMLPlus) is library of code for Python which allows the user to easily create standard and 'floating' Polygons,
Circles and Arcs.

---

Table of Contents
-----------------

1. [Who is this for](#who-is-this-for)
2. [Installing](#installing)
3. [Usage](#usage)
    - [Recommendations](#recommendations)
    - [Quick Start](#quick-start)
4. [Classes](#classes)
    - [Coordinate](#coordinate)
        - [Methods](#coordinate-methods)
    - [LinePath](#linepath)
        - [Creating a polygon using the LinePath class](#creating-a-polygon-using-the-linepath-class)
        - [Automatically create LinePath objects without Coordinate objects](#automatically-create-linepath-objects-without-coordinate-objects)
        - [Methods](#linepath-methods)
    - [ArcPath](#arcpath)
        - [Methods](#arcpath-methods)
5. [Acknowledgements](#acknowledgements)

---

Who is this for
---------------

This is for anyone who wishes to easily render polygons, especially 'floating' or curved polygons within Google Earth.

I work in the aviation industry and needed a reliable way to create models of our airspace. It its useful for creating
models of airways and controlled airspace. It can be used for anything that takes your fancy!

![Prestwick airspace example](img/egpk_airspace_sideon.png)

![Floating polygon example](img/floating_polygon_1.jpg)

---

Installing
----------

### Pip

```
pip install kmlplus
```

### Clone

```
git clone https://github.com/MHenderson1988/kmlplus.git

# Or

git clone git@github.com:MHenderson1988/kmlplus.git
```

### Running tests

```
python -m unittest
```

---

Usage
-----

### Recommendations

KML+ easily integrates with the fantastic [Simplekml](https://pypi.org/project/simplekml/) library and I highly
recommend using it in conjunction with KML+ for the best experience.

Take a look at the example .py file provided to see how KML+ integrates with SimpleKML to create airspace
representations from CAA AIP supplied data.

---

### Quick Start

To do

---

### Classes and functions

v3.0 has stripped back to one single class which contains functions to create circles, cylinders, polygons, polyhedrons
and linestrings.

#### KmlPlus (Class)

```
from kmlplus.kml import KmlPlus

KmlPlus(self, save_name, output_path=None)
```

* save_name accepts a string and is used for naming the resulting .kml file.
* output_path accepts a string representing the directory the resulting .kml shall be saved to.

#### KmlPlus (functions)

```
from kmlplus.kml import KmlPlus

kmlplus.point(coordinate, **kwargs)
```

The point function creates a single KML point. The coordinate is passed in a list as a single string with the latitude, longitude and
height (optional) separated by a single space. For example '55.11111 -4.29292' or '55.11111 -4.29292 300'

```
from kmlplus.kml import KmlPlus

KmlPlus.linestring(coordinate, **kwargs)
```

The linestring function creates a KML line string. It accepts a  




## Acknowledgements

- [Simplekml](https://pypi.org/project/simplekml/) - for creating an awesome library which has helped me create many
  things and also inspiring me to write this library.`


