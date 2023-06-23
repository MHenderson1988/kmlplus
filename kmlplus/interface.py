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
    def from_decimal_degrees(cls, y, x, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def from_dms(cls, y, x, **kwargs):
        pass

    @abstractmethod
    def get_bearing(self, another_location):
        pass

    @abstractmethod
    def get_inverse_bearing(self, another_location):
        pass

    @abstractmethod
    def get_distance(self, another_location, **kwargs):
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
    @property
    @abstractmethod
    def start(self):
        pass

    @property
    @abstractmethod
    def end(self):
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
    def get_points(self) -> list:
        pass

    @abstractmethod
    def get_bearing_increment(self):
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


class I2DObject(ABC):
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
    def process_points(self):
        pass


class IPolygon(ABC):
    @property
    @abstractmethod
    def z(self):
        pass

    @property
    @abstractmethod
    def point_list(self):
        pass


class I3DObject(ABC):
    @property
    @abstractmethod
    def lower_layer(self):
        pass

    @property
    @abstractmethod
    def upper_layer(self):
        pass

    @property
    @abstractmethod
    def sides(self):
        pass

    @abstractmethod
    def create_layer(self, coordinate_list, layer_height, layer_uom):
        pass

    @abstractmethod
    def generate_sides(self):
        pass

    @abstractmethod
    def to_kml(self):
        pass


class ICylinder(ABC):
    @property
    @abstractmethod
    def lower_radius(self):
        pass

    @property
    @abstractmethod
    def upper_radius(self):
        pass
