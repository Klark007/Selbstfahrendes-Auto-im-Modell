"""
    Shows the bounding boxes of the recognized objects
"""
import matplotlib.pyplot as plt


def get_extremes(rect, img):
    min = (rect[0][0], rect[0][1])
    # calculates the maximal position using the formula from creates_bounding_car
    max = (rect[1][0] + min[0] - 1, rect[1][1] + min[1] - 1)

    # Sets white border points showing the bounding car
    img[min[1]][min[0]] = 255
    img[max[1]][min[0]] = 255
    img[min[1]][max[0]] = 255
    img[max[1]][max[0]] = 255

    return img


def show(car, boxes, img):
    img = get_extremes(car, img)
    
    for box in boxes:
        img = get_extremes(box, img)

    plt.imshow(img, cmap="gray")
    plt.show()
