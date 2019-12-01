import Image_Recognition.Find_Car as find_circle

from math import atan, pi, pow, sqrt


class RotationScanner(find_circle.ImageScanner):
    def __init__(self, img, color, color_range):
        self.center_pos = (round(img.shape[1] / 2), round(img.shape[0] / 2))

        super().__init__(img, color, color_range)
        self.max_distance = self.distance_to((0, 0), (img.shape[1], img.shape[0]))
        pass

    def test_pixel(self, x, y):
        # replaces < with <=
        in_range = self.color - self.color_range <= self.image[y][x] <= self.color + self.color_range
        not_used = (x, y) not in self.temp and (x, y) not in self.const

        if in_range and not_used:
            return True
        return False
    
    @staticmethod
    def distance_to(_1, _2):
        delta = (_2[0]-_1[0], _2[1]-_1[1])
        return sqrt(pow(delta[0], 2) + pow(delta[1], 2))
    
    def find_biggest_box(self, number_of_pixel=None):
        # number_of_pixel will not be used

        # newest rectangle
        rect = self.boxes[-1]
        circle_pos = (round(rect[0][0] + rect[1][0] / 2), round(rect[0][1] + rect[1][1] / 2))

        distance = self.distance_to(self.center_pos, circle_pos)

        if distance > self.max_distance:
            self.max_distance = distance
            self.max_pixel_per_box_index = self.c

    @staticmethod
    def line_comparison(_1, _2):
        # used to look at case 1 and 2
        if _2-_1 > 0:
            return 0
        elif _2-_1 < 0:
            return 180
        raise ValueError("Mark on robot is in the center")
    
    @property
    def rotation(self):
        # size of circle and relative position to the position of the car
        circle = self.run()
        circle_pos = [round(circle[0][0]+circle[1][0]/2), round(circle[0][1]+circle[1][1]/2)]

        # inverts the y coordinate so the degrees are in the normal
        circle_pos[1] = self.image.shape[1]-circle_pos[1]

        print("Two positions", circle_pos, self.center_pos)

        # cases x == x or y == y look at delta, else use atan
        if circle_pos[0] == self.center_pos[0]:
            degree = 90 + self.line_comparison(self.center_pos[1], circle_pos[1])
        elif circle_pos[1] == self.center_pos[1]:
            degree = self.line_comparison(self.center_pos[0], circle_pos[0])
        else:
            degree = atan((self.center_pos[1]-circle_pos[1])/(self.center_pos[0]-circle_pos[0])) * 180 / pi

            # adjust the degree values of atan so 0 <= degree <= 360
            if degree < 0:
                if self.center_pos[1]-circle_pos[1] < 0:
                    degree += 180
                else:
                    degree += 360
            if degree > 0:
                if self.center_pos[0]-circle_pos[0] > 0:
                    degree += 180

        # return the rotation between the line defined trough the two points and the x-axis
        return degree