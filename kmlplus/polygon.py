from abc import abstractmethod, ABC
from collections import deque
from kmlplus.geo import PointFactory


class IPolygon(ABC):
    @abstractmethod
    def new_layer(self):
        pass


class Polygon(IPolygon):
    def __init__(self, coordinates: list, **kwargs):
        self.coordinates_list = coordinates

    def new_layer(self, **kwargs) -> list:
        generated_points = PointFactory(self.coordinates_list).process_coordinates()
        return generated_points
