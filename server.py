"""
    Send different commands to the client
    mv: move this tuple
    en: stop moving and disconnect

    rt: corrects rotation
    cr: corrects movement

    https://www.youtube.com/watch?v=8A4dqoGL62E&t=335s
"""

import socket
from math import sqrt
import main
from time import time
# import Camera.Pi_Camera as cam

HEADERSIZE = 2

# AF_INET->ipv4, SOCK_STREAM->TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allows to reuse address (so no OSErrors: Address already in use)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Own IP and Port
s.bind(("0.0.0.0", 12345))  # 0.0.0.0 / 192.168.0.108 / 192.168.0.11


# Queue length
s.listen(2)


def get_digits(number):
    """
    :return: quantity of digits from the number
    """
    count = 0
    while number > 0:
        number = number // 10
        count += 1

    return count


def add_header(cmd):
    """
    :param cmd: the command with its values
    :return: adds a header and returns it, ready to be send
    """
    # get the length of the length of the cmd (for how many spaces needed)
    header = str(len(cmd))

    for i in range(get_digits(len(cmd)), HEADERSIZE):
        header = header + " "
        
    return header + cmd


def distance_to(_1, _2):
    # returns distance from _1 to _2
    delta = (_2[0] - _1[0], _2[1] - _1[1])
    return sqrt(pow(delta[0], 2) + pow(delta[1], 2))


def get_center(rectangle_shape):
    # return the center position of the rectangle shape
    x = rectangle_shape[0][0] + rectangle_shape[1][0] / 2
    y = rectangle_shape[0][1] + rectangle_shape[1][1] / 2
    return [x, y]


while True:
    client_socket, address = s.accept()

    # calibrate robot

    # take picture

    # run program on picture
    # testing purposes:
    # directions = [(0, 1), (1, 0)]

    # directions = main.run_on("Images/4.png")
    """
    camera = cam.init_picamera()
    
    cam.take_picture(camera, "Camera/Current.png")
    directions, brightness, car_box, cell_size = main.run_on("Camera/Current.png")
    """

    directions, brightness, car_box, cell_size = main.run_on("Images/Artificial/2.png", 1, time(), 1)

    for _dir in directions:
        cmd = "mv" + str(_dir)

        client_socket.send(bytes(add_header(cmd), "utf-8"))

        # two corrections (rotation, position)

        # receive correction (rot) order until quit order
        rot = None
        while True:
            # st: stop, ct: continue
            rot = client_socket.recv(2).decode("utf-8")
            if rot == 'st':
                break
            elif rot == "ct":
                """
                cam.take_picture(camera, "Camera/Current2.png")
                _, rot = main.get_corrections("Camera/Current2.png", brightness)
                """
                _, _rot = main.get_corrections("Images/Artificial/2.png", brightness)
                # to have an error to correct
                _rot = 275

                cmd = "rt" + str(_rot)
                client_socket.send(bytes(add_header(cmd), "utf-8"))

        # receive correction (mov) order until quit order
        mov = None
        while True:
            # st: stop, ct: continue
            mov = client_socket.recv(2).decode("utf-8")
            if mov == 'st':
                break
            elif mov == "ct":
                """
                cam.take_picture(camera, "Camera/Current3.png")
                _mov, _ = main.get_corrections("Camera/Current3.png", brightness)
                """
                _mov, _ = main.get_corrections("Images/Artificial/2.png", brightness)

                _mov[0][0] += 5
                _mov[0][1] -= 4

                # calculate distance of the error in cells (/ cell_size)
                _mov = distance_to(get_center(_mov), get_center(car_box)) / cell_size

                cmd = "cr" + str(_mov)
                client_socket.send(bytes(add_header(cmd), "utf-8"))

        txt = None
        while txt != "fs":
            print("Waiting")
            txt = client_socket.recv(2).decode("utf-8")

    client_socket.send((bytes(add_header("en"), "utf-8")))
    client_socket.close()
