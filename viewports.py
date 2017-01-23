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
    def __init__(self, physicalgeom, virtualgeom):
        self.physicalgeom = physicalgeom
        self.virtualgeom = virtualgeom


