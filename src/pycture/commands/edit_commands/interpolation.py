
from PyQt5.QtGui import QImage
from math import floor, sqrt
import numpy as np

from pycture.editor.image.pixel import Pixel

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

    X = floor(_x)
    X_one = min(X + 1, image.width() - 1)

    Y = floor(_y)
    Y_one = min(Y + 1, image.height() - 1)
    
    # Get (R, G, B) values from pixels
    A = np.array(tuple(image.pixel(X, Y).to_bytes(4, 'big')[1:]))          # top left
    B = np.array(tuple(image.pixel(X_one, Y).to_bytes(4, 'big')[1:]))      # top right
    C = np.array(tuple(image.pixel(X, Y_one).to_bytes(4, 'big')[1:]))      # bottom left
    D = np.array(tuple(image.pixel(X_one, Y_one).to_bytes(4, 'big')[1:]))  # bottom right
    
    p = _x - X
    q = _y - Y
    
    Q = A + (B - A) * p
    R = C + (D - C) * p
    
    P = [round(val) for val in (Q + (R - Q) * q)]
    P_bytes = bytes([0xff, *P]) # \ff\rr\gg\bb
    return int.from_bytes(P_bytes, 'big')  # 0xffrrggbb
    
    