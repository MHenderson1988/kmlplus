from abc import abstractmethod, ABC
from collections import deque
from kmlplus.geo import PointFactory


class Polygon:
    @classmethod
    def new_layer(cls, coordinate_list, **kwargs) -> list:
        z_override = kwargs.pop('z', None)
        generated_points = PointFactory(coordinate_list, z=z_override).process_coordinates()
        return generated_points
