#!/usr/bin/env python
import re
from wand.image import Image
from wand.display import display
from wand.color import Color



class Geometry:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y


class PhysicalGeometry(Geometry):
    pass


class ScreenGeometry(Geometry):
    @classmethod
    def from_geometry_string(cls, string):
        geometry = re.match('(\d+)x(\d+)\+(\d+)\+(\d+)', string).groups()
        return cls(*geometry)

    def __repr__(self):
        return f"{self.width}x{self.height}+{self.x}+{self.y}"


class Viewport:
    def __init__(self, physical_geometry, screen_geometry, scale=1.0):
        self.physicalGeometry = physical_geometry
        self.screenGeometry = screen_geometry
        self.scale = scale

    @property
    def dpi(self):
        return self.screenGeometry.width / self.physicalGeometry.width * 2.54

    def scale_to(self, viewport):
        self.scale = self.dpi / viewport.dpi


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


if __name__ == "__main__":
    dummy_tester()
