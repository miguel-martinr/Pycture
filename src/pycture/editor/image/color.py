from enum import Enum


class RGBColor(Enum):
    Red = 0
    Green = 1
    Blue = 2


class Color(Enum):
    Red = 0
    Green = 1
    Blue = 2
    Gray = 3


# LUT stands for LookUpTable
# These gray scale transformation values correspond to the NTSC method
GrayScaleLUT = [list(map(lambda r: 0.299 * r, list(range(256)))),
                list(map(lambda g: 0.587 * g, list(range(256)))),
                list(map(lambda b: 0.114 * b, list(range(256))))]
