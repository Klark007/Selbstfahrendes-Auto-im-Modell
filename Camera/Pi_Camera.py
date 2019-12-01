"""
	Simple Camera (used on Raspberry 3b) Example
    https://picamera.readthedocs.io/en/release-1.13/recipes1.html
"""
from time import sleep
from picamera import PiCamera


def take_picture(name):
    camera = PiCamera()

    camera.resolution = (200, 266)

    # setting the camera settings
    camera.saturation = 50
    camera.brightness = 55
    camera.contrast = 10
    camera.sharpness = 50
    camera.saturation = 0

    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(name)
    camera.stop_preview()
