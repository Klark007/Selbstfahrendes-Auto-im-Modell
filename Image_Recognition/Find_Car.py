"""
    Scans for the car by searching for the biggest group of bordering pixels
    in the color range.
"""


class ImageScanner:
    def __init__(self, image, color, color_range):
        """
            :param image: np.array (x, y, grey_scale)
            :param color: = base color
            :param color_range: max delta between color in image and self.color to count as this color
        """
        self.image = image
        self.color = color
        self.color_range = color_range

        """
            :param const: are pixels belonging to the image which were already scanned
            :param temp: are pixels  belonging to the image which weren't already scanned
        """
        self.const = []
        self.temp = []

        """
            :param older_box_range: border between pixels (in const) belonging to the old boxes
                              and pixels belonging to the new one
        """
        self.older_box_range = 0
        self.boxes = []

        """
            :param c: a counter for the current box
            :param max pixel: the current highest pixel count
            :param max_pixel_per_box_index: the index of box with the most pixels at the moment
        """
        self.c = 0
        self.max_pixel = 0
        self.max_pixel_per_box_index = 0
        pass

    def scan_for_starting_points(self):
        """
            Scans trough the image for a possible (within colorrange of color) starting point of a polygon
        """
        img = self.image

        for y in range(len(img)):
            for x in range(len(img[y])):

                if self.test_pixel(x, y):
                    self.temp.append((x, y))
                    self.look_for_other_pixels(x, y)

                    # the pixel belonging in this box
                    boxes_const = self.const[self.older_box_range:]
                    self.older_box_range += len(boxes_const)
                    self.creates_bounding_box(boxes_const)
        pass

    def test_pixel(self, x, y):
        # tests if the pixel is with in the color range and looks if it wasn't already scanned
        in_range = self.color - self.color_range < self.image[y][x] < self.color + self.color_range
        not_used = (x, y) not in self.temp and (x, y) not in self.const

        if in_range and not_used:
            return True
        return False

    def look_for_other_pixels(self, x, y):
        """
            Looks for pixels with borders to the polygon and who belong to it (color...)
        """

        img = self.image

        # test if there are any aligning pixels
        if not(y == 0):
            if self.test_pixel(x, y - 1):
                self.temp.append((x, y - 1))

        if not(y == len(img) - 1):
            if self.test_pixel(x, y + 1):
                self.temp.append((x, y + 1))

        if not(x == 0):
            if self.test_pixel(x - 1, y):
                self.temp.append((x - 1, y))

        if not(x == len(img[y]) - 1):
            if self.test_pixel(x + 1, y):
                self.temp.append((x + 1, y))

        # adds the now scanned pixel to the const list
        self.temp.remove((x, y))
        self.const.append((x, y))

        # looks if there are any pixels left to scan
        if len(self.temp) != 0:
            for pos in self.temp:
                self.look_for_other_pixels(pos[0], pos[1])
        else:
            self.c += 1
        pass

    def find_biggest_box(self, number_of_pixel):
        # checks if the number_of_pixel of the current box
        # is bigger than the biggest box at the moment
        if number_of_pixel > self.max_pixel:
            self.max_pixel = number_of_pixel
            self.max_pixel_per_box_index = self.c
        pass

    def creates_bounding_box(self, const_of_box):
        """
            Creates a box out of the furthest pixel
            (may need to add a few coordinates to them to create a bigger box)
        """

        y_min, x_min = self.image.shape
        x_max, y_max = 0, 0

        # loops trough the pixels belonging to the box
        for pixel in const_of_box:
            # checks if they exceed the furthest coordinates at the moment
            x_min = pixel[0] if pixel[0] < x_min else x_min
            y_min = pixel[1] if pixel[1] < y_min else y_min

            x_max = pixel[0] if pixel[0] > x_max else x_max
            y_max = pixel[1] if pixel[1] > y_max else y_max

        box = [(x_min, y_min), (x_max - x_min + 1, y_max - y_min + 1)]

        self.boxes.append(box)

        self.find_biggest_box(len(const_of_box))
        pass

    def run(self):
        # starts the process
        self.scan_for_starting_points()

        return self.boxes[self.max_pixel_per_box_index - 1]
