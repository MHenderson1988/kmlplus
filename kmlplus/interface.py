from abc import ABC, abstractmethod


class ILocation(ABC):
    @property
    @abstractmethod
    def x(self):
        pass

    @property
    @abstractmethod
    def y(self):
        pass

    @property
    @abstractmethod
    def z(self):
        pass

    @classmethod
    @abstractmethod
    def from_decimal_degrees(cls):
        pass

    @classmethod
    @abstractmethod
    def from_dms(cls):
        pass

    @abstractmethod
    def get_bearing(self):
        pass

    @abstractmethod
    def get_distance(self):
        pass


class ILocationFactory(ABC):
    @abstractmethod
    def process_coordinates(self):
        pass


class ICurvedSegmentFactory(ABC):
    @abstractmethod
    def generate_segment(self):
        pass


class ICurvedSegment(ABC):
    @abstractmethod
    def get_points(self) -> list:
        pass

    @abstractmethod
    def get_bearing_increment(self):
        pass

    @abstractmethod
    def get_height_increment(self):
        pass

    @abstractmethod
    def find_midpoint(self):
        pass

    @abstractmethod
    def find_start_bearing(self):
        pass

    @abstractmethod
    def find_end_bearing(self):
        pass


class ICircle(ABC):
    @property
    @abstractmethod
    def radius(self):
        pass

    @property
    @abstractmethod
    def centre(self):
        pass

    @property
    @abstractmethod
    def sample(self):
        pass

    @abstractmethod
    def create(self):
        pass


class IPolygon(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    @abstractmethod
    def __setitem__(self, index, point):
        pass

    @abstractmethod
    def __ne__(self, another_polygon):
        pass
