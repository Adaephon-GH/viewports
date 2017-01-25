#!/usr/bin/env python
import re
from wand.image import Image
from wand.display import display
from wand.color import Color


class Rectangle:
    def __init__(self, width, height, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def __and__(self, other):
        """Returns the Rectangle for the area where this and another
        Rectangle overlap.

        :param other: the other Rectangle
        :return: the Rectangle of the overlapping area
        """
        if type(self) != type(other):
            raise TypeError("unsupported operand type(s) for &: "
                            f"'{type(self).__name__}' "
                            f"and '{type(other).__name__}'")
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        width = max(min(self.x + self.width, other.x + other.width) - x, 0)
        height = max(min(self.y + self.height, other.y + other.height) - y, 0)
        return type(self)(width, height, x, y)

    def __or__(self, other):
        """Returns the minimal Rectangle containing both,
        this and another Rectangle

        :param other: the other Rectangle
        :return: the surrounding Rectangle
        """
        if type(self) != type(other):
            raise TypeError("unsupported operand type(s) for |: "
                            f"'{type(self).__name__}' "
                            f"and '{type(other).__name__}'")
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        width = max(self.x + self.width, other.x + other.width) + x
        height = max(self.y + self.height, other.y + other.height) + y
        return type(self)(width, height, x, y)

    def __bool__(self):
        return bool(self.width and self.height)

    def __repr__(self):
        return(f"{type(self).__name__}("
               f"width={self.width}, height={self.height}, "
               f"x={self.x}, y={self.y})")


class PhysicalRectangle(Rectangle):
    pass


class ScreenRectangle(Rectangle):
    @classmethod
    def from_geometry_string(cls, string):
        geometry = re.match('(\d+)x(\d+)\+(\d+)\+(\d+)', string).groups()
        return cls(*geometry)

    def __str__(self):
        return f"{self.width}x{self.height}+{self.x}+{self.y}"


class Viewport:
    def __init__(self, physical_geometry, screen_geometry, scale=1.0):
        self.physicalGeometry = physical_geometry
        self.screenGeometry = screen_geometry
        self.scale = scale

    @property
    def dpi(self):
        # for the moment assume square pixels
        return self.screenGeometry.width / self.physicalGeometry.width * 2.54

    def scale_to(self, viewport):
        self.scale = self.dpi / viewport.dpi


class VPImage(Image):
    def __init__(self, rectangle=None, **kwargs):
        if rectangle is not None:
            if any(kwargs.get(key, None) is not None
                   for key in ["width", "height"]):
                raise TypeError(
                    "rectangle is mutually exclusive to width or height")
            super().__init__(width=rectangle.width, height=rectangle.height,
                             **kwargs)
        else:
            super().__init__(**kwargs)

    def rcomposite(self, image, rectangle):
        self.composite(image, rectangle.x, rectangle.y)


def dummy_tester():
    with Image(filename='sample.png') as orig:
        with Image(width=640, height=360, background=Color('gray')) as img:
            with orig.clone() as a:
                a.transform('50x50+100+100', '100')
                img.composite(a, 30,70)
            with orig.clone() as b:
                b.transform('100x100+100+100', '50%')
                img.composite(b, 300,70)
            with orig.clone() as c:
                c.transform('200x50+10+30', '75%')
                img.composite(c, 200,200)
            display(img)


def overlap_tester():
    bigrect = ScreenRectangle(1000, 1000)
    redrect = ScreenRectangle(300, 300, 250, 250)
    greenrect = ScreenRectangle(300, 300, 100, 100)
    outerrect = redrect | greenrect
    innerrect = redrect & greenrect
    with VPImage(rectangle=bigrect, background=Color("gray")) as img:
        with VPImage(rectangle=redrect, background=Color("#ff00007f")) as m:
            img.rcomposite(m, redrect)
        with VPImage(rectangle=greenrect, background=Color("#00ff007f")) as n:
            img.rcomposite(n, greenrect)
        display(img)
        with VPImage(rectangle=outerrect, background=Color("#7f7f003f")) as n:
            img.rcomposite(n, outerrect)
        with VPImage(rectangle=innerrect, background=Color("#0000ff")) as n:
            img.rcomposite(n, innerrect)
        display(img)

if __name__ == "__main__":
    dummy_tester()
