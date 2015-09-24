#!/usr/bin/env python

import unittest

__author__ = 'Dmytro Soloviov {dsoloviov@frov.jcu.cz}'

"""
Converting HSL or HSV to RGB.
Source: http://www.rapidtables.com/convert/color/hsl-to-rgb.htm
Source: http://www.rapidtables.com/convert/color/hsv-to-rgb.htm
"""


class HSLtoRGBConverter(object):
    """Perform HSL -> RGB conversion"""

    def convert(self, hsl):
        # Unpack HSL values
        self.H, self.S, self.L = hsl
        # Scale Saturation and Lightness to [0..1]
        self.S /= 100.0
        self.L /= 100.0

        self._H = self.H / 60.0

        # Perform conversion
        self.C = self.calculate_chroma()
        self.X = self.calculate_x()
        self._R, self._G, self._B = self.calculate_rgb()
        m = self.calculate_m()
        return self.round_rgb((self._R + m, self._G + m, self._B + m))

    def calculate_chroma(self):
        return (1 - abs(2 * self.L - 1)) * self.S

    def calculate_x(self):
        return self.C * (1 - abs(self._H % 2 - 1))

    def calculate_rgb(self):
        if 0 <= self._H < 1:
            return self.C, self.X, 0
        elif 1 <= self._H < 2:
            return self.X, self.C, 0
        elif 2 <= self._H < 3:
            return 0, self.C, self.X
        elif 3 <= self._H < 4:
            return 0, self.X, self.C
        elif 4 <= self._H < 5:
            return self.X, 0, self.C
        elif 5 <= self._H < 6:
            return self.C, 0, self.X
        else:
            return 0, 0, 0

    def calculate_m(self):
        return self.L - (self.C / 2.0)

    def round_rgb(self, _R_G_B):
        RGB = []
        for i in _R_G_B:
            RGB.append(int(i * 255))
        return tuple(RGB)


class HSVtoRGBConverter(HSLtoRGBConverter):
    """Perform HSV -> RGB conversion"""

    def calculate_chroma(self):
        return self.L * self.S

    def calculate_m(self):
        return self.L - self.C


# Unit testing: HSL -> RGB
class TestHSLtoRGBConversion(unittest.TestCase):

    def setUp(self):
        self.hsl = HSLtoRGBConverter()

    def test_black(self):
        self.assertEqual(self.hsl.convert((0, 0, 0)), (0, 0, 0))

    def test_white(self):
        self.assertEqual(self.hsl.convert((359, 100, 100)), (255, 255, 255))

    def test_red(self):
        self.assertEqual(self.hsl.convert((0, 100, 50)), (255, 0, 0))

    def test_green(self):
        self.assertEqual(self.hsl.convert((120, 100, 50)), (0, 255, 0))

    def test_blue(self):
        self.assertEqual(self.hsl.convert((240, 100, 50)), (0, 0, 255))

    def test_case_gray(self):
        self.assertEqual(self.hsl.convert((0, 0, 50)), (127, 127, 127))

    def test_case_1(self):
        self.assertEqual(self.hsl.convert((211, 57, 47)), (51, 117, 188))

    def test_case_2(self):
        self.assertEqual(self.hsl.convert((27, 66, 49)), (207, 116, 42))


# Unit testing: HSV -> RGB
class TestHSVtoRGBConversion(unittest.TestCase):

    def setUp(self):
        self.hsv = HSVtoRGBConverter()

    def test_black(self):
        self.assertEqual(self.hsv.convert((0, 0, 0)), (0, 0, 0))

    def test_white(self):
        self.assertEqual(self.hsv.convert((0, 0, 100)), (255, 255, 255))

    def test_red(self):
        self.assertEqual(self.hsv.convert((0, 100, 100)), (255, 0, 0))

    def test_green(self):
        self.assertEqual(self.hsv.convert((120, 100, 100)), (0, 255, 0))

    def test_blue(self):
        self.assertEqual(self.hsv.convert((240, 100, 100)), (0, 0, 255))

    def test_case_gray(self):
        self.assertEqual(self.hsv.convert((0, 0, 50)), (127, 127, 127))

    def test_case_1(self):
        self.assertEqual(self.hsv.convert((211, 57, 47)), (51, 84, 119))

    def test_case_2(self):
        self.assertEqual(self.hsv.convert((27, 66, 49)), (124, 79, 42))


if __name__ == '__main__':
    unittest.main()
