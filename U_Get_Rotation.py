import main
import Camera.Pi_Camera as cam
import Simplification.Image_Greyscaling as img_greyscale
from PIL import Image


camera = cam.init_picamera()

_input = None
while _input != "q":
    cam.take_picture(camera, "Camera/Current2.png")

    arr = img_greyscale.prepare_image("Camera/Current2.png", 100, 1)
    img = Image.fromarray(arr)
    img.save('Camera/G_Current2.png')

    mov, rot = main.get_corrections("Camera/Current2.png", 1)

    print("Movement:", mov, " Rotation:", rot)
    _input = input("Quit (q)?")
