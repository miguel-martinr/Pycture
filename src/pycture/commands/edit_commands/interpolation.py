
from PyQt5.QtGui import QImage
from math import floor, sqrt
import numpy as np

def nearest_neighbor_interpolation(image: QImage, point: (float, float)):
    _x, _y = point

    X = floor(_x)
    X_one = min(X + 1, image.width() - 1)

    Y = floor(_y)
    Y_one = min(Y + 1, image.height() - 1)


    #           top left     top right       bottom left     bottom right
    corners = ((X,  Y),     (X_one, Y),     (X, Y_one),     (X_one, Y_one))

    distances = [sqrt((x - _x)**2 + (y - _y)**2)
                 for x, y in corners]
    nearest_neighbor = corners[distances.index(min(distances))]
    return image.pixel(nearest_neighbor[0], nearest_neighbor[1])
    
    
def bilinear_interpolation(image: QImage, point: (float, float)):
    _x, _y = point

    def get_rgb(pixel):
        return pixel & 0x00ffffff
      
    X = floor(_x)
    X_one = min(X + 1, image.width() - 1)

    Y = floor(_y)
    Y_one = min(Y + 1, image.height() - 1)
    
    A = get_rgb(image.pixel(X,  Y))      # top left
    B = get_rgb(image.pixel(X_one, Y))  # top right
    C = get_rgb(image.pixel(X, Y_one))          # bottom left
    D = get_rgb(image.pixel(X_one, Y_one))      # bottom right
    
    p = _x - X
    q = _y - Y
    
    Q = A + (B - A) * p
    R = C + (D - C) * p
    
    P = round(R + (Q - R) * q)
    
    P_bytes = bytearray(P.to_bytes(4, 'big')) # 0x00aabbcc
    P_bytes[0] = 0xff # 0xffaabbcc
    
    return int.from_bytes(P_bytes, 'big')
    
    