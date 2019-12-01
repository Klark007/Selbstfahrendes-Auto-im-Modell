import Camera.Pi_Camera as cam
import Thresholding.Image_Tresholding as img_treshold
from PIL import Image

# take a picture and treshhold it

cam.take_picture("Camera/Current.png")
arr = img_treshold.prepare_image("Camera/Current.png", 100, 1)

# convert the numpy array to a Pillow Image
img = Image.fromarray(arr)
img.save('Camera/G_Current.png')
