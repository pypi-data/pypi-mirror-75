import pathlib
import tempfile
import unittest

import svgwrite
from svgwrite import mm, percent, shapes

from qr_payment_slip import SVGPrinter
from qr_payment_slip.errors import ConversionError


class SVGPrinterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_init(self):
        printer = SVGPrinter()

        self.assertEqual(repr(printer), f"<{printer.__class__.__name__}>")

    def test_white_cross(self):
        height = SVGPrinter.convert_to_pixel(32 * mm)

        file_path = pathlib.Path(self.temp_dir.name) / "cross.svg"

        dwg = svgwrite.Drawing(size=(height, height), filename=file_path)
        cross = SVGPrinter._draw_white_cross()

        self.assertEqual(len(cross.elements), 4)

        self.assertEqual(cross.elements[1].tostring(),
                         '<rect fill="black" height="100%" width="100%" x="0" y="0" />')

        self.assertEqual(cross.elements[2].tostring(),
                         '<rect fill="white" height="18.75%" width="62.5%" x="18.75%" y="40.625%" />')

        self.assertEqual(cross.elements[3].tostring(),
                         '<rect fill="white" height="62.5%" width="18.75%" x="40.625%" y="18.75%" />')

    def test_convert_to_pixel(self):
        MM_CONST = 3.543307

        value = SVGPrinter.convert_to_pixel(1)  # pixel value (unitless)
        self.assertEqual(value, 1)

        value = SVGPrinter.convert_to_pixel(1 * mm)  # millimeter value
        self.assertEqual(value, MM_CONST)

        value = SVGPrinter.convert_to_pixel(1.05 * mm)  # millimeter value with decimal point
        self.assertEqual(value, 1.05 * MM_CONST)

        with self.assertRaises(ConversionError):
            SVGPrinter.convert_to_pixel(1 * percent)  # percentage (cannot convert)
