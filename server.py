"""
    Send different commands to the client
    mv: move this tuple
    en: stop moving and disconnect
    fs: finished movement

    https://www.youtube.com/watch?v=8A4dqoGL62E&t=335s
"""

import socket
from time import time
import main
# import Camera.Pi_Camera as cam

HEADERSIZE = 2

# AF_INET->ipv4, SOCK_STREAM->TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allows to reuse address (so no OSErrors: Address already in use)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Own IP and Port
s.bind(("0.0.0.0", 12345))  # 0.0.0.0 / 192.168.0.108 / 192.168.0.11


# Queue length
s.listen(1)


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


while True:
    start_time = time()
    client_socket, address = s.accept()

    # run program on picture
    # testing purposes:
    # directions = [(0, 1), (1, 0)]

    print("Connect:", start_time-time())
    start_time = time()

    directions = main.run_on("Images/4.png", 1, time(), 0)

    print("Evaluate:", time() - start_time)
    start_time = time()

    """
    cam.take_picture("Camera/Current.png")
    directions = main.run_on("Camera/Current.png")
    """

    for _dir in directions:
        cmd = "mv" + str(_dir)

        client_socket.send(bytes(add_header(cmd), "utf-8"))

        # waits from answer from client
        txt = None
        while txt != "fs":
            txt = client_socket.recv(2).decode("utf-8")

    print("Send:", time() - start_time)
    start_time = time()

    client_socket.send((bytes(add_header("en"), "utf-8")))
    client_socket.close()

    print("Recive:", time() - start_time)
    start_time = time()
    # just while working at the server

    # remove image
    # break
