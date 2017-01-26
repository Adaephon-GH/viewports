#!/usr/bin/env python
import re
from PIL import Image


class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        # Do not allow "negative" rectangles, assume size 0x0 instead
        self.right = right if right > left else left
        self.bottom = bottom if bottom > top else top

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def size(self):
        return self.width, self.height

    @property
    def position(self):
        return self.left, self.top

    @property
    def box(self):
        return self.left, self.top, self.right, self.bottom

    @classmethod
    def from_size(cls, width, height):
        return cls(0, 0, width, height)

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
        left = max(self.left, other.left)
        top = max(self.top, other.top)
        right = min(self.right, other.right)
        bottom = min(self.bottom, other.bottom)
        return type(self)(left, top, right, bottom)

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
        left = min(self.left, other.left)
        top = min(self.top, other.top)
        right = max(self.right, other.right)
        bottom = max(self.bottom, other.bottom)
        return type(self)(left, top, right, bottom)

    def __bool__(self):
        return bool(self.width and self.height)

    def __repr__(self):
        return (f"{type(self).__name__}("
                f"left={self.left}, top={self.top}, "
                f"right={self.right}, bottom={self.bottom})")

    def __round__(self, n=None):
        return type(self)(*[round(v, n) for v in self.box])


class PhysicalRectangle(Rectangle):
    pass


class ScreenRectangle(Rectangle):
    @classmethod
    def from_geometry_string(cls, string):
        geometry = re.match(
            '(?P<width>\d+)x(?P<height>\d+)\+(?P<left>\d+)\+(?P<top>\d+)',
            string)
        left = int(geometry.group('left'))
        top = int(geometry.group('top'))
        right = left + int(geometry.group('width'))
        bottom = top + int(geometry.group('height'))
        return cls(left, top, right, bottom)

    def __str__(self):
        return f"{self.width}x{self.height}+{self.left}+{self.top}"


class Viewport:
    def __init__(self, physical, screen, scale=1.0):
        self.physical = physical
        self.screen = screen
        self.scale = scale

    @property
    def dpi(self):
        # for the moment assume square pixels and measurements in mm
        return self.screen.width / self.physical.width * 25.4

    def scale_to(self, viewport):
        self.scale = self.dpi / viewport.dpi


# class VPImage(Image):
#     def __init__(self, rectangle=None, **kwargs):
#         if rectangle is not None:
#             if any(kwargs.get(key, None) is not None
#                    for key in ["width", "height"]):
#                 raise TypeError(
#                     "rectangle is mutually exclusive to width or height")
#             super().__init__(width=rectangle.width, height=rectangle.height,
#                              **kwargs)
#         else:
#             super().__init__(**kwargs)
#
#     def rcomposite(self, image, rectangle):
#         self.composite(image, rectangle.x, rectangle.y)


def dummy_tester():
    with Image.open('sample.png') as orig:
        with Image.new('RGB', (640, 360), color='gray') as img:
            with orig.crop((100, 100, 150, 150)) as a:
                img.paste(a, (30, 70))
            with orig.crop((100, 100, 200, 200)) as b:
                b.resize((50, 50))
                img.paste(b, (300, 70))
            with orig.crop((10, 30, 210, 230)) as c:
                img.paste(c, (round(200 * .75), round(200 * .75)))
            img.show()


def overlap_tester():
    import itertools
    bigrect = ScreenRectangle(1000, 1000)
    redrect = ScreenRectangle(400, 400, 300, 300)
    for w, h in itertools.combinations_with_replacement([50, 250, 500], 2):
        for x, y in itertools.combinations_with_replacement([50, 400, 700], 2):
            greenrect = ScreenRectangle(w, h, x, y)
            outerrect = redrect | greenrect
            innerrect = redrect & greenrect
            with VPImage(rectangle=bigrect, background=Color("gray")) as img:
                if outerrect:
                    with VPImage(rectangle=outerrect,
                                 background=Color("#7f7f00")) as n:
                        img.rcomposite(n, outerrect)
                if innerrect:
                    with VPImage(rectangle=innerrect,
                                 background=Color("#0000ff")) as n:
                        img.rcomposite(n, innerrect)
                display(img)
                with VPImage(rectangle=redrect,
                             background=Color("#ff00007f")) as m:
                    img.rcomposite(m, redrect)
                with VPImage(rectangle=greenrect,
                             background=Color("#00ff007f")) as n:
                    img.rcomposite(n, greenrect)
                display(img)


#
#
# sampleLayout = {
#     "Left":
#         Viewport(PhysicalRectangle(518, 324, 0, 86.4),
#                  ScreenRectangle.from_geometry_string('1920x1200+0+320')),
#     "Middle":
#         Viewport(PhysicalRectangle(518, 324, 538, 0),
#                  ScreenRectangle.from_geometry_string('1920x1200+1920+0')),
#     "Right":
#         Viewport(PhysicalRectangle(475, 267, 1096, 28.5),
#                  ScreenRectangle.from_geometry_string('1920x1080+3840+60')),
#     "Laptop":
#         Viewport(PhysicalRectangle(346, 194, 624, 384),
#                  ScreenRectangle.from_geometry_string('1920x1080+1920+1200')),
# }
#
#
# def show_layout(layout):
#     from functools import reduce
#     import operator
#
#     scrv = reduce(operator.or_, [layout[k].screen for k in layout])
#     phyv = reduce(operator.or_, [layout[k].physical for k in layout])
#
#     with VPImage(rectangle=scrv, background=Color("gray")) as img:
#         for p in [round(layout[k].screen) for k in layout]:
#             with VPImage(rectangle=p, background=Color("red")) as s:
#                 img.rcomposite(s, p)
#         img.transform(resize="500")
#         display(img)
#
#     with VPImage(rectangle=phyv, background=Color("gray")) as img:
#         for p in [round(layout[k].physical) for k in layout]:
#             with VPImage(rectangle=p, background=Color("red")) as s:
#                 img.rcomposite(s, p)
#         img.transform(resize="500")
#         display(img)


if __name__ == "__main__":
    dummy_tester()
