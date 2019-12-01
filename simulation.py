"""
    Simulates a bad driving vehicle
"""
import Image_Recognition.Find_Car as find_car
import Image_Recognition.Find_Box as find_box

import Image_Recognition.Find_Rotation as find_rot

import Simplification.Image_Greyscaling as img_greyscale

import U_Generate_Image as generate_image

import numpy
import time
import random


def simulate(name):
    # pos, rectangles (image coordinates), cell size
    generate_image.run(None, run_on(name))
    pass


def run_on(name):
    start_time = time.time()
    debugging = 1

    # debugging = 0.5 will just be used when it is run as main
    if __name__ != "__main__" and debugging == 0.5:
        debugging = 0

    img = img_greyscale.prepare_image(name, 100, 1)

    print("Time after image preparation:", time.time() - start_time)

    car_scanner = find_car.ImageScanner(img, 87, 30)
    car_box = car_scanner.run()

    print("Car:", car_box)

    # size_range has to be tested out on different images
    box_scanner = find_box.ImageScanner(img, 25, 25, 50, debugging)
    rectangles, cell_size = box_scanner.run()

    # creates a cutout version of the car bounding box
    car_part = img[car_box[0][1]:car_box[0][1] + car_box[1][1], car_box[0][0]:car_box[0][0] + car_box[1][0]]
    # get rotation of the car using the white point on the robot

    rot = find_rot.RotationScanner(car_part, 250, 5).rotation
    print("White circle:" + str(rot))

    print("Time after image recognition:", time.time() - start_time)

    return (car_box, rot, rectangles, cell_size)


if __name__ == "__main__":
    simulate("Images/Artificial/2.png")
