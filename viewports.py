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


