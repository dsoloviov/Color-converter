#!/usr/bin/env python

import unittest

__author__ = 'Dmytro Soloviov {dsoloviov@frov.jcu.cz}'

"""
Converting RGB value to HSL or HSV.
Source: http://www.rapidtables.com/convert/color/rgb-to-hsl.htm
Source: http://www.rapidtables.com/convert/color/rgb-to-hsv.htm
"""


class RGBtoHSLConverter(object):
    """Perform RGB -> HSL conversion"""

    def convert(self, RGB):
        # Scaling the range from 0..255 to 0..1
        R, G, B = RGB
        self._R = R / 255.0
        self._G = G / 255.0
        self._B = B / 255.0
        self.color = (self._R, self._G, self._B)

        # Find minimum, maximum and difference
        self.Cmax = max(self.color)
        self.Cmin = min(self.color)
        self.d = self.Cmax - self.Cmin

        # Perform conversion
        H = self.hue()
        self._L = self.lightness()
        L = self.percentage(self._L)
        S = self.percentage(self.saturation())
        return H, S, L

    def hue(self):
        """Calculate hue. Return H"""
        if self.d == 0:
            return 0
        if self.Cmax == self._R:
            return int(round(60 * ((self._G - self._B) / self.d % 6)))
        if self.Cmax == self._G:
            return int(round(60 * ((self._B - self._R) / self.d + 2)))
        if self.Cmax == self._B:
            return int(round(60 * ((self._R - self._G) / self.d + 4)))

    def saturation(self):
        """Calculate saturation. Return S"""
        if self.d == 0:
            return 0
        else:
            return self.d / (1 - abs(2 * self._L - 1))

    def lightness(self):
        """Calculates lightness. Return _L"""
        return (self.Cmax + self.Cmin) / 2

    def percentage(self, n):
        return round(n * 100, 1)


class RGBtoHSVConverter(RGBtoHSLConverter):
    """Perform RGB -> HSV conversion"""

    def saturation(self):
        if self.d == 0:
            return 0
        else:
            return self.d / self.Cmax

    # Wrapper for value()
    def lightness(self):
        return self.value()

    def value(self):
        return self.Cmax


# Unit testing: RGB -> HSL
class TestRGBtoHSLConvertion(unittest.TestCase):

    def setUp(self):
        self.hsl = RGBtoHSLConverter()

    def test_black(self):
        self.assertEqual(self.hsl.convert((0, 0, 0)), (0, 0.0, 0.0))

    def test_white(self):
        self.assertEqual(self.hsl.convert((255, 255, 255)), (0, 0.0, 100.0))

    def test_red(self):
        self.assertEqual(self.hsl.convert((255, 0, 0)), (0, 100.0, 50.0))

    def test_green(self):
        self.assertEqual(self.hsl.convert((0, 255, 0)), (120, 100.0, 50.0))

    def test_blue(self):
        self.assertEqual(self.hsl.convert((0, 0, 255)), (240, 100.0, 50.0))

    def test_case_gray(self):
        self.assertEqual(self.hsl.convert((128, 128, 128)), (0, 0.0, 50.2))

    def test_case_1(self):
        self.assertEqual(self.hsl.convert((51, 117, 187)), (211, 57.1, 46.7))

    def test_case_2(self):
        self.assertEqual(self.hsl.convert((210, 117, 42)), (27, 66.7, 49.4))


# Unit testing: RGB -> HSV
class TestRGBtoHSVConvertion(unittest.TestCase):

    def setUp(self):
        self.hsv = RGBtoHSVConverter()

    def test_black(self):
        self.assertEqual(self.hsv.convert((0, 0, 0)), (0, 0.0, 0.0))

    def test_white(self):
        self.assertEqual(self.hsv.convert((255, 255, 255)), (0, 0.0, 100.0))

    def test_red(self):
        self.assertEqual(self.hsv.convert((255, 0, 0)), (0, 100.0, 100.0))

    def test_green(self):
        self.assertEqual(self.hsv.convert((0, 255, 0)), (120, 100.0, 100.0))

    def test_blue(self):
        self.assertEqual(self.hsv.convert((0, 0, 255)), (240, 100.0, 100.0))

    def test_case_gray(self):
        self.assertEqual(self.hsv.convert((128, 128, 128)), (0, 0.0, 50.2))

    def test_case_1(self):
        self.assertEqual(self.hsv.convert((51, 117, 187)), (211, 72.7, 73.3))

    def test_case_2(self):
        self.assertEqual(self.hsv.convert((210, 117, 42)), (27, 80.0, 82.4))


if __name__ == '__main__':
    unittest.main()
