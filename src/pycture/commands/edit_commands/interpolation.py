
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
    
    
def bilinear_interpolation(image: QImage, point: (float, float)):
    _x, _y = point

    X = floor(_x)
    X_one = min(X + 1, image.width() - 1)

    Y = floor(_y)
    Y_one = min(Y + 1, image.height() - 1)
    
    A = image.pixel(X, Y_one)      # top left
    B = image.pixel(X_one, Y_one)  # top right
    C = image.pixel(X, Y)          # bottom left
    D = image.pixel(X_one, Y)      # bottom right
    
    p = _x - X
    q = _y - Y
    
    Q = A + (B - A) * p
    R = C + (D - C) * p
    
    P = R + (Q - R) * q
    
    return round(P)
    