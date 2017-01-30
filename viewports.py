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

    def __mul__(self, other):
        return type(self)(self.left * other,
                          self.top * other,
                          self.right * other,
                          self.bottom * other)



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
    def dpu(self):
        # for the moment assume square pixels
        return self.screen.width / self.physical.width


class Layout:
    DPU_MAX = -1
    DPU_REFERENCE = -2

    def __init__(self, viewports):
        self.viewports = viewports
        self.reference = None

    def add_viewport(self, viewport: Viewport):
        self.viewports.append(viewport)

    def set_reference(self, viewport: Viewport):
        if viewport in self.viewports:
            self.reference = viewport
        else:
            raise ViewportsError("The reference needs to be part"
                                 " of the layout")

    def does_overlap(self, screen):
        return any([screen & v.screen for v in self.viewports])

    def _find_overlaps(self):
        overlaps = []
        for v1, v2 in itertools.combinations(self.viewports, 2):
            overlap = v1 & v2
            if overlap:
                overlaps.append((v1, v2, overlap))
        return overlaps

    @property
    def hasOverlaps(self):
        return bool(self._find_overlaps())

    def _calc_size(self, which):
        viewports = iter(self.viewports)
        rect = getattr(next(viewports), which)
        for viewport in viewports:
            rect |= getattr(viewport, which)
        return rect.size

    @property
    def screenSize(self):
        return self._calc_size('screen')

    @property
    def physicalSize(self):
        return self._calc_size('physical')

    def max_dpu(self, width, height):
        physWidth, physHeight = self.physicalSize
        if width / height >= physWidth / physHeight:
            return height / physHeight
        else:
            return width / physWidth

    def cut_image(self, image: Image.Image, dpu, common_point=(0, 0, 0, 0)):
        if dpu == Layout.DPU_REFERENCE:
            # TODO: Handling of insufficiently large source image
            dpu = self.reference.dpu
        elif dpu == Layout.DPU_MAX:
            dpu = self.max_dpu(*image.size)
        elif dpu <= 0:
            raise ValueError("dpu needs to be positive or"
                             "equal to any Layout.DPU_* constants")
        for viewport in self.viewports:
            # TODO: actual work
            print(f"{viewport.name}: {round(viewport.physical * dpu)}")


class ViewportsError(Exception):
    pass


if __name__ == "__main__":
    pass
