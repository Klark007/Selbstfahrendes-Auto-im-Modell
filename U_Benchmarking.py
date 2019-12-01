import U_Generate_Image as generate
import main
from random import randint as rand
from os import remove, listdir, walk, path
from time import time


def rand_xy_coordinates(size):
    return [rand(0, round(200/size/2)-2), rand(0, round(266/size/2)-2)]


def loop_over_values():
    sums = [0, 0, 0, 0, 0]

    if not(path.isfile("Log File.txt")):
        return None

    log_file = open("Log File.txt", "r")

    for line in log_file:
        sums[sums[-1] % len(sums)-1] = float(line[:len(line)-2])
        sums[-1] += 1

    for _sum in sums:
        print(_sum / sums[-1])
    pass


if path.isfile("Log File.txt"):
    remove("Log File.txt")


for i in range(0, 10):
    # delete images
    file_list = listdir("Images/Animation/")
    for file in file_list:
        remove("Images/Animation/" + str(file))

    # generate random image
    cell_size = rand(15, 25)

    car = rand_xy_coordinates(cell_size)

    rectangles = []
    c = rand(7, 11)
    while c > 0:
        pos = rand_xy_coordinates(cell_size)
        if pos != car and not(pos in rectangles):
            rectangles.append(pos)
            c -= 1

    rest = [car, rectangles, cell_size]

    generate.run(None, rest)

    # run main on it
    path, dirs, files = next(walk("Images/Animation"))
    file_count = len(files)

    main.run_on("Images/Animation/" + str(file_count) + ".png", 1, time(), 1)

loop_over_values()
