"""
    https://www.pygame.org/docs/tut/PygameIntro.html

    Generate an image for the programm to use
"""

import pygame
from os import walk
from numpy import where
# import main


def int_put(text):
    return int(input(text))


def to_real_pos(x, y, c):
    return x * c, y * c


def run(grid=None, rest=None):
    pygame.init()

    size = width, height = 200, 266
    screen = pygame.display.set_mode(size)

    white = 240, 240, 240

    distance = 3

    print("Start to create matrix")

    car = pygame.image.load("Images/Artificial/Car.png")


    rectangles = []

    if rest:
        # generate image from data
        # * 2 because the cell size printed out in the main programm is from the downscaled image (/2)
        cell_size = rest[2] * 2

        # resize the car to the grid
        car = pygame.transform.scale(car, (cell_size - distance, cell_size - distance))

        # rest[0]: car_grid_position, rest[1] rectangles grid position, rest[2] cell_size
        x, y = to_real_pos(rest[0][0], rest[0][1], cell_size)

        car_position = x + distance, y + distance

        for rect in rest[1]:
            x, y = to_real_pos(rect[0], rect[1], cell_size)
            w, h = cell_size - distance, cell_size - distance

            rectangles.append(pygame.Rect(x + distance, y + distance, w, h))

    elif __name__ == "__main__":
        # * 2 because we work with the simplified version of the grid
        cell_size = int_put("Cell size:") * 2

        # resize the car to the grid
        car = pygame.transform.scale(car, (cell_size - distance, cell_size - distance))

        # Generate image from hand
        x, y = to_real_pos(int_put("Car position x:"), int_put("Car position y:"), cell_size)
        car_position = x+distance, y+distance

        car_rotation = int_put("Car Rotation (°):")
        # rotate car
        car = pygame.transform.rotate(car, car_rotation)

        print("Input rectangles")

        last_input = True
        while last_input:
            x, y = to_real_pos(int_put("Rectangle position x:"), int_put("Rectangle position y:"), cell_size)
            # +/- for gap between cells
            w, h = cell_size-distance, cell_size-distance
            rectangles.append(pygame.Rect(x+distance, y+distance, w, h))
            last_input = bool(int_put("Continue (1:yes, 0:no):"))
    else:
        # * 2 because we work with the simplified version of the grid
        cell_size = int_put("Cell size:") * 2

        # resize the car to the grid
        car = pygame.transform.scale(car, (cell_size - distance, cell_size - distance))

        # Generate image from grid
        x, y = where(grid == 2)
        x, y = x[0], y[0]
        car_rotation = int_put("Car Rotation (°):")
        car_position = x*cell_size + distance, y*cell_size + distance

        # rotate car
        car = pygame.transform.rotate(car, car_rotation)

        print(grid)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 1:
                    w, h = cell_size - distance, cell_size - distance
                    rectangles.append(pygame.Rect(x*cell_size + distance, y*cell_size + distance, w, h))

    print("Finished grid creation")

    # makes the background not completely white
    screen.fill(white)

    for rectangle in rectangles:
        pygame.draw.rect(screen, (0, 0, 0), rectangle)

    screen.blit(car, car_position)

    pygame.display.flip()

    if rest:
        _str = "Images/Animation"
        _, _, files = next(walk("Images/Animation"))
        file_count = len(files) + 1
    else:
        _str = "Images/Artificial"
        _, _, files = next(walk("Images/Artificial"))
        file_count = len(files) - 1

    pygame.image.save(screen, _str + "/" + str(file_count) + ".png")


if __name__ == "__main__":
    run()
