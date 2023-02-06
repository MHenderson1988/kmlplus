from abc import abstractmethod, ABC


class IPolygon(ABC):
    @abstractmethod
    def new_layer(self):
        pass


class Polygon(IPolygon):
    def __init__(self, coordinates: list, **kwargs):
        self.coordinates = coordinates

    def new_layer(self, **kwargs):
        pass
