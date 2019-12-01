import socket
from ast import literal_eval
import Yetiborg.Drive as Yetiborg

HEADERSIZE = 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("localhost", 12345))  # 192.168.0.11 / localhost / 192.168.0.108

# car always looks up at the beginning
car = Yetiborg.Yetiborg((0, 1))

"""
    fs: finished
"""


def move(vec):
    print(vec)
    # movement command at motors
    car.calculate_movement(vec)
    pass


def stop():
    print("Stop")
    exit()


def command_decoder(str):
    # decodes the send command into an action
    cmd = str[:2]

    if cmd == "mv":
        # gets the direction (tuple) from the command
        move(literal_eval(str[2:]))
    elif cmd == "en":
        stop()
    pass


while True:
    full_cmd = ""

    header = s.recv(HEADERSIZE).decode("utf-8")
    print("New message length:", header[:HEADERSIZE])
    cmd_len = int(header[:HEADERSIZE])

    full_cmd = s.recv(cmd_len).decode("utf-8")

    command_decoder(full_cmd)

    # send finished execution signal
    s.send(bytes("fs", "utf-8"))

