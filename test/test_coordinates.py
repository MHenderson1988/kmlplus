from unittest import TestCase

from kmlplus.coordinates import Coordinate


class TestCoordinates(TestCase):
    def test_coordinate(self):
        latitude_list = ["55.11", "55.11111234", "55.1232", "55.37823782"]
        c1 = Coordinate("55.21434", "-4.38487", 0, coordinate_type="dms")
        for latitude in latitude_list:
            c1.latitude = latitude
            self.assertEqual(c1.latitude, latitude)

        longitude_list = ["-4.37363", "-3.0", "-5.43", "5.34873478"]
        for longitude in longitude_list:
            c1.longitude = longitude
            self.assertEqual(c1.longitude, longitude)

        print(c1.to_string())
