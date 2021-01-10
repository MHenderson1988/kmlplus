from kmlplus import coordinates, paths


class FloatingPolygon:
    def __init__(self, path_1, path_2):
        self.lower_face = path_1
        self.upper_face = path_2
        self.sides = paths.LinePath(*self.create_polygon_sides())

    def __str__(self):
        return "Lower face coordinates = {}, Upper face coordinates = {}, side coordinates = {}".format(self.lower_face,
                                                                                                        self.upper_face,
                                                                                                        self.sides)

    def test_same_length(self):
        if len(self.lower_face) != len(self.upper_face):
            return False
        else:
            return True

    def create_polygon_sides(self):
        i = 0
        coordinate_list = []
        while i < self.lower_face.__len__() - 1:
            coordinate_list.append(coordinates.Coordinate(self.lower_face[i][1], self.lower_face[i][0],
                                                          height=self.lower_face[i][2])),
            coordinate_list.append(coordinates.Coordinate(self.lower_face[i + 1][1], self.lower_face[i + 1][0],
                                                          height=self.lower_face[i + 1][2])),
            coordinate_list.append(coordinates.Coordinate(self.upper_face[i + 1][1], self.upper_face[i + 1][0],
                                                          height=self.upper_face[i + 1][2])),
            coordinate_list.append(coordinates.Coordinate(self.upper_face[i][1], self.upper_face[i][0],
                                                          height=self.upper_face[i][2]))
            i += 1
        return coordinate_list
