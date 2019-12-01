"""
    Replacement option for cv2.
    New: script to get values from different pixel
"""

from PIL import Image
import numpy as np

width = 100


def load_PIL(image_path):
    img = Image.open(image_path).convert('L')

    w, h = img.size

    height = int(h * (width / w))
    new_img = img.resize((width, height))

    new_img.show()

    img_arr = np.array(new_img)

    return img_arr


img = load_PIL("Images/Artificial/3.png")

print(img.shape)

while True:
    print("Get value from position")
    x = int(input("X:"))
    y = int(input("Y:"))

    print(img[y][x])
