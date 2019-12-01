"""
    Shows the bounding boxes of the recognized objects
"""
import matplotlib.pyplot as plt


def get_extremes(rect, img):
    _min = (rect[0][0], rect[0][1])
    # calculates the maximal position using the formula from creates_bounding_car
    _max = (rect[1][0] + _min[0] - 1, rect[1][1] + _min[1] - 1)

    # draws two vertical lines
    for x in range(_min[0], _max[0]):
        img[_min[1]][x] = 255
        img[_max[1]][x] = 255

    # draws two horizontal lines
    for y in range(_min[1], _max[1]):
        img[y][_min[0]] = 255
        img[y][_max[0]] = 255

    return img


def show(car, boxes, img):
    img = get_extremes(car, img)
    
    for box in boxes:
        img = get_extremes(box, img)

    plt.imshow(img, cmap="gray")
    plt.show()

    # plt.imsave("Images/Old_G4.png", img, cmap="gray")
