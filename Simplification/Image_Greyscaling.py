import numpy as np
from PIL import Image, ImageEnhance


def prepare_image(path, width, brightness):
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
