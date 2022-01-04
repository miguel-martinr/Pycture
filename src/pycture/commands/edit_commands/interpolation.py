
from PyQt5.QtGui import QImage
from math import floor, sqrt

def nearest_neighbor_interpolation(image: QImage, point: (float, float)):
    _x, _y = point

    X = floor(_x)
    X_one = min(X + 1, image.width() - 1)

    Y = floor(_y)
    Y_one = min(Y + 1, image.height() - 1)

    #           top left     top right       bottom left     bottom right
    corners = ((X, Y_one),   (X_one, Y_one),  (X, Y),         (X_one, Y))

    distances = [sqrt((x - _x)**2 + (y - _y)**2)
                 for x, y in corners]
    nearest_neighbor = corners[distances.index(min(distances))]
    return image.pixel(nearest_neighbor[0], nearest_neighbor[1])
    
    
