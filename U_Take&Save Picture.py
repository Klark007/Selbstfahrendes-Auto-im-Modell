import Camera.Pi_Camera as cam
import Simplification.Image_Greyscaling as img_greyscale
from PIL import Image

# take a picture and greyscale it
camera = cam.init_picamera()
cam.take_picture(camera, "Camera/Current.png")
arr = img_greyscale.prepare_image("Camera/Current.png", 100, 1)

# convert the numpy array to a Pillow Image
img = Image.fromarray(arr)
img.save('Camera/G_Current.png')
