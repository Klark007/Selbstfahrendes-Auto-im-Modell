import numpy as np
#import cv2
from PIL import Image, ImageEnhance


def prepare_image(path, width, brightness):
    """
    # This option would be faster, but relies more on the librarys... (used because reasons mentioned above)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    h, w, *_ = img.shape

    height = int(h * (width / w))
    small = cv2.resize(img, (width, height))
    """

    img = Image.open(path).convert('L')

    enhancer = ImageEnhance.Brightness(img)

    img_out = enhancer.enhance(brightness)

    w, h = img_out.size

    height = int(h * (width / w))
    new_img = img_out.resize((width, height))

    small = np.array(new_img)

    # Shows treshold image
    # new_img.show()



    return small
