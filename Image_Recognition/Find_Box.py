"""
    Scans trough the images and searches for boxes( over
    a certain min size: not sure) and then looks which are
    in the size range of the default size of all the boxes.
    Those will be used as a obstacle further on. The grid size
    is then determined by the default size of the obstacles

    Further ideas:
        look for the most squared solution instead of the biggest
        go across (x&y + 1) the spaces to get squares instead of rectangles
        create a list of pixels that were already in a rectangle (possibility) but weren't used so that those aren't used again
"""
from math import sqrt as sqrt


class ImageScanner:
    def __init__(self, image, color, color_range, size_range, debugging):
        """
            :param image: np.array (x, y, grey_scale)
            :param color: base color
            :param color_range: max delta between color in image and self.color to count as this color
        """
        self.image = image
        self.color = color
        self.color_range = color_range
        self.size_range = size_range

        self.rectangles = []

        self.debugging = debugging
        pass

    def scan_for_starting_points(self):
        """
            Scans for possible (in colorrange of color
            and not in color) pixels in the image
        """
        img = self.image

        for y in range(len(img)):
            for x in range(len(img[y])):

                if self.test_pixel(x, y):
                    rectangle = self.scan_diagonal(x, y)

                    # test if the found rectangle is already in one
                    add_rectangle = True

                    # list of objects that need to be removed. They won't be removed if after the loop
                    # the new rectangle won't be added
                    to_remove = []

                    for r in self.rectangles:
                        # check if outer points of the bounding box (new)
                        # lie within the older bounding box

                        left_side = r[0][0] < rectangle[0][0]
                        right_side = rectangle[0][0] + rectangle[1][0] < r[0][0] + r[1][0]

                        x_in_rectangle = left_side and right_side

                        top_side = r[0][1] < rectangle[0][1]
                        bottom_side = rectangle[0][1] + rectangle[1][1] < r[0][1] + r[1][1]

                        y_in_rectangle = top_side and bottom_side

                        if x_in_rectangle or y_in_rectangle:
                            # If that is the case, remove the smaller one
                            if r[1][0]*r[1][1] < rectangle[1][0]*rectangle[1][1]:
                                to_remove.append(r)
                            else:
                                add_rectangle = False

                    if add_rectangle:
                        self.rectangles.append(rectangle)

                        for r in to_remove:
                            self.rectangles.remove(r)
        pass

    def test_pixel(self, x, y):
        """
            boundary just needed on the bottom and right side because of scan movement
            (left to right and top to bottom)
        """
        y_max, x_max = self.image.shape
        if y >= y_max or x >= x_max:
            return False

        # Test if a pixels fits the color requirements
        if self.debugging == 1:
            in_range = self.color - self.color_range <= self.image[y][x] <= self.color + self.color_range
        else:
            in_range = self.color - self.color_range < self.image[y][x] < self.color + self.color_range

        # Test if pixel is already in a rectangle
        for rectangle in self.rectangles:
            x_in_rectangle = rectangle[0][0] <= x <= rectangle[0][0] + rectangle[1][0]
            y_in_rectangle = rectangle[0][1] <= y <= rectangle[0][1] + rectangle[1][1]

            if (x_in_rectangle and y_in_rectangle) or not in_range:
                return False

        if in_range:
            return True

    def scan_diagonal(self, x, y):
        start = (x, y)
        while self.test_pixel(x + 1, y + 1):
            x += 1
            y += 1
        return (start, (x - start[0] + 1, y - start[1] + 1))

    def get_average_size(self):
        """
            returns the average size of the boxes
        """
        size = 0
        for rectangle in self.rectangles:
            size += rectangle[1][0] * rectangle[1][1]
        if len(self.rectangles):
            return size / len(self.rectangles)
        else:
            return 0
        pass

    def sort_out_boxes(self):
        """
            returns the boxes which are near enough to the average
        """
        # store average default size so removing elements wont change the results
        default_size = self.get_average_size()

        good_rectangles = []

        for rectangle in self.rectangles:
            difference = rectangle[1][0]*rectangle[1][1] - default_size

            if difference > self.size_range or self.debugging == 1:
                print("Rectangle found at:", rectangle[0])
                good_rectangles.append(rectangle)

        return good_rectangles

    def run(self):
        # starts the process
        self.scan_for_starting_points()

        self.rectangles = self.sort_out_boxes()
        cell_size = sqrt(self.get_average_size())

        return self.rectangles, cell_size
