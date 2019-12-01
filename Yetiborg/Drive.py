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
    (0, 1): 270,
    (0, -1): 90,
    (1, 0): 0,
    (-1, 0): 180
}

time_for_1m = {
    "forward": 7.4,
    "backward": 11.45,
    "left": 6.45,
    "right": 6.6
}


class Yetiborg():
    def __init__(self, start_dir):
        self.direction = start_dir

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
        degree = None

        degree = options[self.direction] - options[vec]

        print(degree)

        # self.degree_to_spin(degree)

        # used to test the socket with waiting time
        """if degree == 180 or degree == -180:
            sleep(time_for_1m["left"] / 2)
        elif degree == -90 or degree == 270:
            sleep(time_for_1m["right"] / 4)
        elif degree == 90 or degree == -270:
            sleep(time_for_1m["left"] / 4)

        sleep(time_for_1m["forward"] / 4)"""
        self.direction = vec
        # self.move_forward()
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

    def move_forward(self):
        self.move(+1.0, +1.0)
        self.sleep_stop("forward")
        pass

    def move_backward(self):
        self.move(-1.0, -1.0)
        self.sleep_stop("backward")
        pass

    def spin_left(self):
        self.move(-1.0, +1.0)
        self.sleep_stop("left")
        self.stop()
        pass

    def spin_right(self):
        self.move(+1.0, -1.0)
        self.sleep_stop("right")
        pass

    def sleep_stop(self, _type):
        sleep(time_for_1m[_type] / 4)
        self.stop()
        pass

    def stop(self):
        self.ZB.MotorsOff()
        pass
