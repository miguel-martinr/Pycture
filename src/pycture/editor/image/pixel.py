from .color import RGBColor

class Pixel():
    def __init__(self, value: int):
        self.value = value

    def get_color(self, color: RGBColor) -> int:
        if color == RGBColor.Red:
            return (self.value & 0x00ff0000) >> 16
        elif color == RGBColor.Green:
            return (self.value & 0x0000ff00) >> 8
        else:
            return self.value & 0x000000ff

    def get_rgb(self) -> (int, int, int):
        return tuple(map(lambda color: self.get_color(color), RGBColor))

    def set_color(self, value: int, color: RGBColor) -> "Pixel":
        if color == RGBColor.Red:
            return self.set_red(value)
        elif color == RGBColor.Green:
            return self.set_green(value)
        else:
            return self.set_blue(value)

    def set_red(self, red_value: int) -> "Pixel":
        red_value = (red_value & 0x000000ff) << 16
        return Pixel(red_value | (self.value & 0xff00ffff))

    def set_green(self, green_value: int) -> "Pixel":
        green_value = (green_value & 0x000000ff) << 8
        return Pixel(green_value | (self.value & 0xffff00ff))

    def set_blue(self, blue_value: int) -> "Pixel":
        blue_value &= 0x000000ff
        return Pixel(blue_value | (self.value & 0xffffff00))

    def set_rgb(self, value: int) -> "Pixel":
        value &= 0x000000ff
        for _ in range(2):
            value = value | (value << 8)
        return Pixel(value | (self.value & 0xff000000))