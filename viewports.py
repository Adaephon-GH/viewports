#!/usr/bin/env python
import re

import itertools
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
            '^(?P<width>\d+)x(?P<height>\d+)\+(?P<left>\d+)\+(?P<top>\d+)$',
            string)
        try:
            left = int(geometry.group('left'))
            top = int(geometry.group('top'))
            right = left + int(geometry.group('width'))
            bottom = top + int(geometry.group('height'))
            return cls(left, top, right, bottom)
        except AttributeError:
            raise ViewportsError(f"Geometry '{string}' does not match format "
                                 f"<width>x<height>+<x>+<y>, where all values "
                                 f"must be non-negative integers only.")

    def __str__(self):
        return f"{self.width}x{self.height}+{self.left}+{self.top}"


class Viewport:
    def __init__(self, physical: PhysicalRectangle, screen: ScreenRectangle,
                 name=None):
        self.physical = physical
        self.screen = screen
        self.name = name or str(self.screen)

    @property
    def dpi(self):
        # for the moment assume square pixels and measurements in mm
        return self.screen.width / self.physical.width * 25.4


class Layout:
    def __init__(self):
        self.viewports = []
        self.reference = None

    def add_viewport(self, viewport: Viewport):
        self.viewports.append(viewport)

    def does_overlap(self, screen):
        return any([screen & v.screen for v in self.viewports])

    @property
    def is_non_overlapping(self ):
        for v1, v2 in itertools.combinations(self.viewports, 2):
            pass


class ViewportsError(Exception):
    pass


if __name__ == "__main__":
    pass
