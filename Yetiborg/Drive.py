"""
    Gets orders and has its own direction reactive to the image (later calibrated)
    The car gets the concrete motor orders from here

    for documentation on the functions of the zeroborg:
    https://www.piborg.org/blog/zeroborg-examples
"""
import Yetiborg.ZeroBorg3 as Zeroborg

from time import sleep

# map vectors to their corresponding degree
options = {
    (0, 1): 270,  # 90
    (0, -1): 90,  # 270
    (1, 0): 0,
    (-1, 0): 180
}

time_for_1m = {
    "forward": 6.5,
    "backward": 9.6,
    "left": 5.2,
    "right": 5.2
}


class Yetiborg():
    def __init__(self, start_dir, socket):
        self.direction = start_dir
        self.socket = socket

        """
        # Initiate Yetiborg
        self.ZB = Zeroborg.ZeroBorg()
        self.ZB.Init()

        # if CommsFailssafe == true then the motors would be stopped
        # unless they are commanded every 1/4 second
        self.ZB.SetCommsFailsafe(False)
        # allows movement again after the EPO has been tripped
        self.ZB.ResetEpo()

        self.maxPower = 6.0 / 8.4
        """
        pass

    def calculate_movement(self, vec):
        # first checks how much the car has to rotate
        degree = options[vec] - options[self.direction]
        # degree can be a negative number because it could calculate 180-270

        print(degree)

        # self.degree_to_spin(degree)

        self.direction = vec

        counter = 0
        while counter < 4:
            # send correction cmd
            self.socket.send(bytes("ct", "utf-8"))

            # wait for correction
            cmd = None
            while cmd != "rt":
                # header_size = 2
                header = self.socket.recv(2).decode("utf-8")
                print("New message length:", header[:2])
                cmd_len = int(header[:2])

                # name of cmd
                txt = self.socket.recv(cmd_len).decode("utf-8")
                cmd = txt[:2]  # cmd name
                rot = txt[2:]  # real rotation

                """
                    the complete turn can be used because we know that the car normally doensn't drive to far
                    it drives to little because the car has less charge than it had when the values were calculated
                """

                # shouldn't have to correct more than 90 degree, emergency prevention of bad rotation calculations
                turn = options[self.direction] - float(rot)
                if turn > 0:
                    turn = min(turn, 90)

                    # self.spin_left(360/turn)
                elif turn < 0:
                    turn = max(turn, -90)

                    # self.spin_right(360/-turn)
                elif turn == 0:
                    # doesn't need to be corrected
                    break

                print(float(rot), "-", options[self.direction], "=",  float(rot) - options[self.direction])

            counter += 1
        # send stop cmd
        self.socket.send(bytes("st", "utf-8"))

        # self.move_forward()

        # send correction
        counter = 0
        while counter < 4:
            # send correction cmd
            self.socket.send(bytes("ct", "utf-8"))

            # wait for correction
            cmd = None
            while cmd != "cr":
                # header_size = 2
                header = self.socket.recv(2).decode("utf-8")
                # print("New message length:", header[:2])
                cmd_len = int(header[:2])

                # name of cmd
                txt = self.socket.recv(cmd_len).decode("utf-8")
                cmd = txt[:2]  # cmd name
                mov = float(txt[2:])  # real movement

                # self.move_forward(4/mov)
            counter += 1
        # send stop cmd
        self.socket.send(bytes("st", "utf-8"))
        pass

    def degree_to_spin(self, degree):
        """
        :param degree: degree which is translated to left/right turns
        """
        if degree == -90 or degree == 270:
            self.spin_right()
        elif degree == 90 or degree == -270:
            self.spin_left()
        if degree == 180 or degree == -180:
            self.spin_left()
            self.spin_left()
        pass

    def move(self, left, right):
        print("movement:" + str(left) + "/" + str(right))
        self.ZB.SetMotor1(-right * self.maxPower)
        self.ZB.SetMotor2(-right * self.maxPower)
        self.ZB.SetMotor3(-left * self.maxPower)
        self.ZB.SetMotor4(-left * self.maxPower)
        pass

    def move_forward(self, factor=4):
        self.move(+1.0, +1.0)
        self.sleep_stop("forward", factor)
        pass

    def move_backward(self, factor=4):
        self.move(-1.0, -1.0)
        self.sleep_stop("backward", factor)
        pass

    def spin_left(self, factor=4):
        self.move(-1.0, +1.0)
        self.sleep_stop("left", factor)
        self.stop()
        pass

    def spin_right(self, factor=4):
        self.move(+1.0, -1.0)
        self.sleep_stop("right", factor)
        pass

    def sleep_stop(self, _type, factor):
        sleep(time_for_1m[_type] / factor)
        self.stop()
        pass

    def stop(self):
        self.ZB.MotorsOff()
        pass
