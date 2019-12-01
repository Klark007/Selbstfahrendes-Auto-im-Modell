"""
    converts the data gathered by the image recognition to a 2d numpy array
    representing the image. The array contains integers:
    0: free space
    1: block
    2: car
"""
import numpy as np
import U_Generate_Image as generate_image


class GridThresholding:
    def __init__(self, img_shape, car, rectangles, cell_size, debugging):
        """
        :param img: Dimensions of the image
        :param car: bounding box of car
        :param rectangles: bounding box of rectangle
        :param cell_size: default size of rectangles or the size of the car
            if there are no rectangles
        """
        self.img_shape = img_shape

        self.car = car
        self.rectangles = rectangles

        self.cell_size = cell_size

        self.debugging = debugging
        pass

    def get_dimensions(self):
        # returns the dimensions of the grid
        y, x = self.img_shape
        width = round(x / self.cell_size)
        height = round(y / self.cell_size)

        return height, width

    @staticmethod
    def test_round_to(x, base):
        return round(x/base)

    def get_pos(self, rectangle_shape):
        # returns middle of rectangle as a position in the threshold image
        x = (rectangle_shape[0][0] + rectangle_shape[1][0] / 2) / self.cell_size
        y = (rectangle_shape[0][1] + rectangle_shape[1][1] / 2) / self.cell_size

        x_round = round(x)
        y_round = round(y)

        # if rounded up -> -1
        if x_round > x:
            x_round -= 1
        if y_round > y:
            y_round -= 1

        # y, x used so it is placed correctly in the grid
        return [y_round, x_round]

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
        print("Gridsize:", dim[1], "|", dim[0], ", Cellsize:", self.cell_size)

        # Numpy uses y, x coordinates, be careful!
        grid = np.full(dim, 0)
        car_element = [self.get_pos(self.car), 2]

        grid[car_element[0][0], car_element[0][1]] = car_element[1]

        for rectangle in self.rectangles:
            rectangle_element = (self.get_pos(rectangle), 1)

            if grid[rectangle_element[0][0], rectangle_element[0][1]] == 0:
                grid[rectangle_element[0][0], rectangle_element[0][1]] = rectangle_element[1]
            else:
                print("Can't place " + str(rectangle_element[1]) + " here because its already occupied")
                print("Position is: " + str((rectangle_element[0][0], rectangle_element[0][1])))
        if self.debugging == 0.5:
            generate_image.run(grid)
        return grid
