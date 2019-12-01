import Image_Recognition.Find_Car as find_car
import Image_Recognition.Find_Box as find_box

import Image_Recognition.Find_Rotation as find_rot

import Image_Recognition.Show_Scan as show

import Simplification.Image_Greyscaling as img_greyscale
import Simplification.Grid_Creation as create_grid

import Pathfinding.Find_Exit as find_exit

import numpy
import time
from sys import exit

"""
    Notes:
        end function with either pass or return
        
        :param var_name: to say what the purpose of a certain var is
        
        for x in range(len(a)):
            e = a[x]
        ->
        for e in a:
        
        y,x in arrays
        x, y in bounding boxes
"""

"""
    Image 1: 1 meter high
    Image 2: 1.5 meter high
    Image 3: 1.5 meter high with book
    Image 4: 1.5 meter high with 2 books
    Image 5&6: 2 objects too bright (switch lighting/room)
"""

"""
    debugging:
        0: normal image, normal procedure
        0.5: normal image, grid creation
        1: special image, normal procedure
"""


def advanced_scanning_car(name, img, brightness, start_time, debugging):
    # 2 possible problems: no car or recursion error
    try:
        car_scanner = find_car.ImageScanner(img, 87, 30)
        car_box = car_scanner.run()

        print("Car:", car_box)

        return car_box
    except RecursionError:
        # Brightness change should be calculated
        run_on(name, brightness + 1, start_time, debugging)
        # so it doesn't execute the run_on with the old settings
        exit()
    except IndexError:
        # No car found (empty array = car_scanner.boxes)
        run_on(name, brightness - 1 / 10)
        exit()
    pass


def run_on(name, brightness=1, start_time=time.time(), debugging=0):
    # debugging = 0.5 will just be used when it is run as main
    if __name__ != "__main__" and debugging == 0.5:
        debugging = 0

    print("Brightness:", brightness)

    img = img_greyscale.prepare_image(name, 100, brightness)

    print("Time after image preparation:", time.time() - start_time)

    car_box = advanced_scanning_car(name, img, brightness, start_time, debugging)

    # size_range has to be tested out on different images
    box_scanner = find_box.ImageScanner(img, 25, 25, 50, debugging)
    rectangles, cell_size = box_scanner.run()

    print("Time after image recognition:", time.time() - start_time)

    grid_creator = create_grid.GridThresholding(img.shape, car_box, rectangles, cell_size, debugging)
    grid = grid_creator.prepare_grid()

    print(grid)

    # searches for possible exits and if they are reachable. Returns the closest
    directions = find_exit.scan(numpy.copy(grid))

    print_grid = numpy.copy(grid)

    # searches for car (2) position in the grid
    y, x = numpy.where(grid == 2)
    # numpy.where returns a list not a int
    y = int(y)
    x = int(x)

    # Not to be confused mit built in dir
    for _dir in directions:
        x += _dir[0]
        y += _dir[1]
        print_grid[y][x] = 5

    print(print_grid)

    print("Time after A*:", time.time() - start_time)

    if __name__ == '__main__':
        # showing image afterwards because it somehow messes
        # with the values of the picture.

        show.show(car_box, rectangles, img)

    return directions, brightness, car_box, cell_size


def get_corrections(name, brightness=1):
    img = img_greyscale.prepare_image(name, 100, brightness)

    car_scanner = find_car.ImageScanner(img, 87, 30)  # 60, 25
    car_box = car_scanner.run()

    # creates a cutout version of the car bounding box
    car_part = img[car_box[0][1]:car_box[0][1] + car_box[1][1], car_box[0][0]:car_box[0][0] + car_box[1][0]]
    # get rotation of the car using the white point on the robot
    car_rot = find_rot.RotationScanner(car_part, 195, 65).rotation

    return car_box, car_rot


if __name__ == "__main__":
    run_on("Images/From Camera/6.png")
