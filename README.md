KML+
===

KMLPLUS IS CURRENTLY BEING UPDATED. UNTIL NEW VERSION IS RELEASED PLEASE CONTINUE TO USE V2.1.0 
https://pypi.org/project/KMLPlus

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

KmlPlus(self, save_name='KmlPlus', output_path=None)
```
KmlPlus is the class through which you create your 2D and 3D geometries. 

* save_name accepts a string and is used for naming the resulting .kml file.
* output_path accepts a string representing the directory the resulting .kml shall be saved to.

#### KmlPlus (functions)

v3 update in progress.

linestring(coordinate_list, **kwargs)

The linestring function updates the kml file with a KML linestring feature.  

```
from kmlplus.kml import KmlPlus

"""

        Args:
            coordinate_list (list): A list containing a single coordinate
        Keyword Args:
            fol (str): A string to name the folder in which the point is stored.
            linestring_name (str): String to name the LineString object
            colour_hex (str): String representing a colour hex
            extrude (int): 1 or 0, Whether to extrude the point
            width(int): Line width
            altitude_mode(str): Accepts simplekml Altitude mode options


        Returns:
            None

  """

kml_file = KmlPlus('Point Styling.kml')
kml_file.linestring(coordinates_list)
```

polyhedron(coordinate_list, **kwargs)

Updates the KmlFile with a polyhedron based upon the coordinates and optional upper and lower limits.

```
"""

        Args:
            coordinate_list (list): A list of coordinates
        Keyword Args:
            fol (str): A string to name the folder in which the point is stored.
            lower_layer (float): Height in FT of the lower layer
            upper_layer (float): Height in FT of the upper layer
            lower_polygon_name (str): Lower polygon object name
            upper_polygon_name (str): Upper polygon object name
            colour_hex (str): String representing a colour hex
            fill (str): 1 or 0, whether or not to fill the polygon
            outline (str): 1 or 0, whether to include outline of polygon
            extrude (str): 1 or 0, Whether to extrude the point
            altitude_mode (str): Accepts simplekml Altitude mode options

        Returns:
            None
        """
        
kml_file = KmlPlus('Point Styling.kml')
kml_file.polyhedron(coordinates_list, lower_layer = 2000, upper_layer = 5000)
```

circle(coordinate_list, radius, **kwargs)

Creates a 2D circle. Coordinate list contains a single set of coordinates in x, y, z format. 

```
"""

        Args:
            coordinate_list (list): A list containing a single set of coordinates which is the centre point of the circle
            radius (float): The radius of the circle
        Keyword Args:
            fol (str): Name of the folder in which the KML objects are stored.
            name (str): What to name the Circle object
            uom (str): The unit of measurement of the radius. Accepted arguments are 'FT', 'NM', 'MI', 'KM' and 'M'.
               Defaults to 'NM'
            colour_hex (str): String representing a colour hex
            extrude (int): 1 or 0, Whether to extrude the point
            altitude_mode (str): Accepts simplekml Altitude mode options

        Returns:
            None

        """
        
kml_file = KmlPlus('Point Styling.kml')
kml_file.polyhedron(coordinates_list, 500)
```

cylinder(coordinate_list, radius, **kwargs)

Creates a Cylinder from a single set of coordinates within a list.
## Acknowledgements

- [Simplekml](https://pypi.org/project/simplekml/) - for creating an awesome library which has helped me create many
  things and also inspiring me to write this library.`


