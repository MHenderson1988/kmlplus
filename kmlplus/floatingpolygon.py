from kmlplus import coordinates, paths


class FloatingPolygon:
    def __init__(self, path_1, path_2):
        self.lower_face = path_1
        self.upper_face = path_2
        self.kml_list = self.create_polygon_sides()

    def __str__(self):
        return "{}".format(self.kml_list)

    def __getitem__(self, item):
        return self.kml_list[item]

    def test_same_length(self):
        if len(self.lower_face) != len(self.upper_face):
            return False
        else:
            return True

    def create_polygon_sides(self):
        i = 0
        list_to_return = []
        if i < len(self.lower_face.kml_coordinate_list) - 1:
            coordinate_1 = coordinates.Coordinate(self.lower_face[i][1], self.lower_face[i][0],
                                                  height=self.lower_face[i][2])
            coordinate_2 = coordinates.Coordinate(self.lower_face[i + 1][1], self.lower_face[i][0],
                                                  height=self.lower_face[i][2])
            coordinate_3 = coordinates.Coordinate(self.upper_face[i + 1][1], self.upper_face[i][0],
                                                  height=self.upper_face[i][2])
            coordinate_4 = coordinates.Coordinate(self.upper_face[i][1], self.upper_face[i][0],
                                                  height=self.upper_face[i][2])
            line_path = paths.LinePath(coordinate_1, coordinate_2, coordinate_3, coordinate_4)
            list_to_return.append(line_path)
            i += 1
        return list_to_return
