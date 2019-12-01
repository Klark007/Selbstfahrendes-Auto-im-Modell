"""
    converts the data gathered by the image recognition to a 2d numpy array
    representing the image. The array contains integers:

    0: free space
    1: block
    2: car

    rectangle element structured
    0: real position
    1: grid position "not the right one in some circumstances
    2: type (0-2)
"""
import numpy as np
from math import pow, sqrt, atan, pi

# used to decide in which way a cell should be moved
options = {
    (True, False, False, False, False): (0, 1),
    (False, True, False, False, False): (1, 0),
    (False, False, True, False, False): (0, -1),
    (False, False, False, True, False): (-1, 0),
    (False, False, False, False, True): (0, 1)
}
degree_delta = 20

class GridThresholding:
    def __init__(self, img_shape, car, rectangles, cell_size):
        """
        :param img: Dimensions of the image
        :param car: bounding box of car
        :param rectangles: bounding box of rectangle
        :param cell_size: default size of rectangles or the size of the car
            if there are no rectangles
        """
        self.img_shape = img_shape

        self.car = car
        self.rectangles = rectangles.copy() # new list so the other list stays intact
        self.start_len = len(self.rectangles)

        self.cell_size = cell_size
        
        self.current_element = None

        self.opened = []
        self.closed = []
        pass

    def get_dimensions(self):
        # returns the dimensions of the grid
        y, x = self.img_shape
        width = round(x / self.cell_size)
        height = round(y / self.cell_size)

        return height, width

    def get_grid_pos(self, rectangle_shape):
        # returns middle of rectangle as a position in the threshold image
        x = (rectangle_shape[0][0] + rectangle_shape[1][0] / 2) / round(self.cell_size)
        y = (rectangle_shape[0][1] + rectangle_shape[1][1] / 2) / round(self.cell_size)

        x_round = round(x)
        y_round = round(y)

        dim = self.get_dimensions()

        x_round -= 1
        y_round -= 1

        return [y_round, x_round]

    @staticmethod # doesn't use self
    def get_pos(rectangle_shape):
        return [rectangle_shape[0][0] + rectangle_shape[1][0] / 2, rectangle_shape[0][1] + rectangle_shape[1][1] / 2]

    @staticmethod
    def get_degree(posA, posB):
        delta_x = posB[0] - posA[0]
        delta_y = posB[1] - posA[1]

        if delta_x != 0:
            return atan(delta_y/delta_x)
        else:
            if delta_y > 0:
                return pi/2
            else:
                return 3*pi/2

    @staticmethod
    def distance_to(posA, posB):
        delta_x = posB[0] - posA[0]
        delta_y = posB[1] - posA[1]

        return sqrt(pow(delta_x, 2) + pow(delta_y, 2))

    def prepare_grid(self):
        """
            adds all elements with a pos (middle) and their type (int) to a list
            scans trough list and creates a 2d numpy array out of it
        """
        # If cell_size = 0 (no rectangles found) then the cell-size will be set
        # to the length of biggest side of the car
        if self.cell_size == 0:
            self.cell_size = self.car[1][0] if self.car[1][0] > self.car[1][1] else self.car[1][1]

        dim = self.get_dimensions()
        print("Gridsize:", dim[1], "|", dim[0])

        # Numpy uses y, x coordinates, be careful!
        grid = np.full(dim, 0)

        self.current_element = [self.get_pos(self.car), self.get_grid_pos(self.car), 2]
        grid[self.current_element[1][0], self.current_element[1][1]] = self.current_element[2]

        while len(self.closed) < self.start_len:
            self.closed.append(self.current_element)

            # look for nearest cell
            r = []
            nearest_object = []
            # shortest distance at the moment the longest distance possible
            shortest_distance = self.distance_to([0,0], [dim[1]*self.cell_size, dim[0]*self.cell_size])

            open_rectangle_list = [rectangle for rectangle in self.rectangles if rectangle not in self.closed]
            for rectangle in open_rectangle_list:
                distance = self.distance_to(self.get_pos(rectangle), self.current_element[0])
                if distance < shortest_distance:
                    r = rectangle
                    nearest_object = [self.get_pos(rectangle), self.get_grid_pos(rectangle), 1]
                    shortest_distance = distance

            self.rectangles.remove(r)

            # calculate the degree between the positions and try to group them into 4 categories
            degree = self.get_degree(nearest_object[0], self.current_element[0]) * 180 / pi
            if degree < 0:
                degree + 360

            # 360 and 0 are two parts of the same group
            _360_range = 360 >= degree >= 360-degree_delta
            _270_range = 270+degree_delta >= degree >= 270-degree_delta
            _180_range = 180+degree_delta >= degree >= 180-degree_delta
            _90_range = 90+degree_delta >= degree >= 90-degree_delta
            _0_range = degree_delta >= degree >= 0

            degree_test = (_0_range, _90_range, _180_range, _270_range, _360_range)

            if shortest_distance < self.cell_size * 1.5 and (_360_range or _270_range or _180_range or _90_range or _0_range):
                # an neighbouring cell found, move it 1 tile in the right direction
                grid[self.current_element[1][0]+ options[degree_test][0], self.current_element[1][1]+ options[degree_test][1]] = nearest_object[2]
            else:
                # otherwise place it with absolute position
                if grid[nearest_object[1][0], nearest_object[1][1]] == 0:
                    grid[nearest_object[1][0], nearest_object[1][1]] = nearest_object[2]
                else:
                    print("Can't place " + str(nearest_object[1]) + " here because its already occupied")
                    print("Position is: " + str((nearest_object[0][0], nearest_object[0][1])))

            self.current_element = nearest_object
        return grid
