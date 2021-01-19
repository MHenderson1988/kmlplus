from unittest import TestCase

from kmlplus import coordinates


class TestCoordinates(TestCase):

    def test_latitude_and_longitude(self):
        c1 = coordinates.Coordinate("55.11213, -4.24453")
        c2 = coordinates.Coordinate("55.33, -4.33, 483")
        c3 = coordinates.Coordinate(33.232, -4.232)

        # Make sure initial values have initialised correctly
        self.assertEqual(c1._latitude, 55.11213)
        self.assertEqual(c1._longitude, -4.24453)
        # Switch them up
        c1._latitude = 34.32433
        c1._longitude = -4.3823
        # Check the new values have updated correctly
        self.assertEqual(c1._latitude, 34.32433)
        self.assertEqual(c1._longitude, -4.3823)

        # Check c2 initialises correctly
        self.assertEqual(c2._latitude, 55.33)
        self.assertEqual(c2._longitude, -4.33)
        self.assertEqual(c2._height, 483)

        # Check c3 initialises correctly
        self.assertEqual(c3._latitude, 33.232)
        self.assertEqual(c3._longitude, -4.232)
        self.assertEqual(c3._height, 0)

