from unittest import TestCase

from kmlplus import coordinates


class TestCoordinates(TestCase):

    def test_latitude_and_longitude(self):
        c1 = coordinates.Coordinate("55.11213, -4.24453")
        c2 = coordinates.Coordinate("55.33, -4.33, 483")
        c3 = coordinates.Coordinate(33.232, -4.232)
        c4 = coordinates.Coordinate(223212, -32312, 40)

        # Make sure initial values have initialised correctly
        self.assertEqual(c1._latitude, 55.11213)
        self.assertEqual(c1._longitude, -4.24453)
        # Switch them up
        c1.latitude = 34.32433
        c1.longitude = -4.3823
        # Check the new values have updated correctly
        self.assertEqual(c1.latitude, 34.32433)
        self.assertEqual(c1.longitude, -4.3823)

        # Check c2 initialises correctly
        self.assertEqual(c2.latitude, 55.33)
        self.assertEqual(c2.longitude, -4.33)
        self.assertEqual(c2.height, 483)

        # Test updating c2 values
        c2.latitude = "55.1111"
        c2.longitude = "-1200203"
        c2.height = "53.23"
        self.assertEqual(c2.latitude, 55.1111)
        self.assertEqual(c2.longitude, -120.03417)
        self.assertEqual(c2.height, 53.23)

        # Check c3 initialises correctly
        self.assertEqual(c3.latitude, 33.232)
        self.assertEqual(c3.longitude, -4.232)
        self.assertEqual(c3.height, 0)

        # Check c4 initialises correctly
        self.assertEqual(c4.latitude, 22.53667)
        self.assertEqual(c4.longitude, -3.38667)
        self.assertEqual(c4.height, 40)
