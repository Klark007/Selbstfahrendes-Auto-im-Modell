"""
    Simulates a bad driving vehicle
"""
import Image_Recognition.Find_Car as find_car
import Image_Recognition.Find_Box as find_box

import Image_Recognition.Find_Rotation as find_rot

import Simplification.Image_Greyscaling as img_greyscale

import U_Generate_Image as generate_image

import time
from random import randint
from os import remove, listdir


def randomize(rest):
    # randomize the rest value (simulate errors of the motors)
    rest[0][0][0] += randint(-5, 5)
    rest[0][0][1] += randint(-5, 5)
    rest[1] += randint(-20, 20)
    return rest


def simulate(name):
    # delete images
    file_list = listdir("Images/Animation/")
    for file in file_list:
        remove("Images/Animation/" + str(file))

    number = 1

    # pos, rotation, rectangles (image coordinates), cell size
    o_values = run_on(name)

    # make an error
    rest = randomize(run_on(name))

    # error for cell size movement and 90 degree turn
    error = [o_values[0][0][0] - rest[0][0][0], o_values[0][0][1] - rest[0][0][1], o_values[1] - rest[1]]

    print("X-Error:", error[0])
    print("Y-Error:", error[1])
    print("Rot-Error:", error[2])

    generate_image.run(None, rest)

    # to a certain number or error margin
    while number < 4:
        # analyse error image
        values = run_on("Images/Animation/" + str(number) + ".png")
        # correct the cars position
        values[0][0][0] += min(error[0] / 2, o_values[3])
        values[0][0][1] += min(error[1] / 2, o_values[3])

        values[1] += min(error[2], 90)

        if abs(error[2]) > 90:
            raise ValueError

        if abs(error[2]) < abs(o_values[1] - values[1]) - 10:
            raise ValueError(abs(error[2]), abs(o_values[1] - values[1]))

        # look new difference to the destination
        error = [o_values[0][0][0] - values[0][0][0], o_values[0][0][1] - values[0][0][1], o_values[1] - values[1]]

        print("X-Error:", error[0])
        print("Y-Error:", error[1])
        print("Rot-Error:", error[2])

        # the overlapping car may destroy some rectangles, keep the original (o_values) cell size
        values[2] = o_values[2]
        values[3] = o_values[3]

        generate_image.run(None, values)
        number += 1
    pass


def run_on(name):
    start_time = time.time()
    debugging = 1

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

    return [car_box, rot, rectangles, cell_size]


if __name__ == "__main__":
    for x in range(1, 10):
        simulate("Images/Artificial/2.png")

    exit()
