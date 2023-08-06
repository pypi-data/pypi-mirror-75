import abc
import gettext
import re
from typing import Tuple, Union, TYPE_CHECKING

import svgwrite
from svgwrite import container, shapes, text, path, pattern
from svgwrite import mm, pt, percent

if TYPE_CHECKING:
    from qr_payment_slip.bill import QRPaymentSlip

from qr_payment_slip.enum import PaperSize, PaymentSlipPosition
from qr_payment_slip.errors import ValidationError, ConversionError

_ = gettext.gettext


class Printer(abc.ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def save_as(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def draw(self, *args, **kwargs):
        pass


class SVGPrinter(Printer):
    """Create a svg image of a payment slip based on the information stored in a QrPaymentSlip

    NOTE: All position and size variables have units in mm
    """

    def __init__(self, bill: "QRPaymentSlip" = None,
                 fonts=None,
                 bill_height=105, receipt_width=62, payment_width=148, margin=5,
                 y_amount_section=66, y_acceptance_section=82,
                 as_sample=False):
        """
        :param bill:
        :type bill: qrbill.bill.QRPaymentSlip
        :param fonts: fonts used for the title, header, text
        :type fonts: dict
        :param bill_height: total height of the bill
        :param receipt_width: width of the receipt part
        :param payment_width: width of the payment part
        :param margin: margin within all parts
        :param y_amount_section: absolute y coordinate of the amount section (receipt and payment part)
        :param y_acceptance_section: absolute y coordinate of the acceptance point (receipt part only)
        :param as_sample: indicator if bill is a sample
        """
        super(SVGPrinter, self).__init__()

        self.bill = bill

        self.bill_height = bill_height
        self.receipt_width = receipt_width
        self.payment_width = payment_width
        self.margin = margin

        # Font size of header and associated values must be between 6 pt and 10 pt. Header must always be printed in the
        # same size. Headings should be printed in bold and 2 pt smaller than the font size of the associated values.
        # Recommended font size:
        # - header  8 pt
        # - text   10 pt, bold
        # - title  11 pt, bold
        # - Alternative procedures 7 pt,
        if fonts:
            self.fonts = fonts

        self.fonts = {
            "title": {"font_size": 11, "font_family": "Helvetica", "font_weight": "bold"},
            "payment": {
                "header": {"font_size": 8, "font_family": "Helvetica", "font_weight": "bold"},
                "text": {"font_size": 10, "font_family": "Helvetica"},
            },
            "receipt": {
                "header": {"font_size": 6, "font_family": "Helvetica", "font_weight": "bold"},
                "text": {"font_size": 9, "font_family": "Helvetica"},
            }
        }

        self.y_amount_section = y_amount_section * mm
        self.y_acceptance_point = y_acceptance_section * mm
        self.as_sample = as_sample

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    @property
    def bill(self):
        return self._bill

    @bill.setter
    def bill(self, bill: "QRPaymentSlip"):
        self._bill = bill

    @property
    def total_width(self):
        """Total width of the payment slip"""
        return self.receipt_width + self.payment_width

    def save_as(self, file_name, *args, **kwargs):
        """Save SVG image after drawing it directly to file

        :param file_name: File name under which the invoice should be saved
        """
        drawing = self.draw(*args, **kwargs)
        drawing.saveas(filename=file_name)

    def draw(self,
             bill: "QRPaymentSlip" = None,
             paper_size: Union[Tuple[float, float], PaperSize] = PaperSize.A4,
             payment_slip_position: Union[Tuple[float, float], PaymentSlipPosition] = PaymentSlipPosition.BOTTOM):
        """Draw svg image

        :param bill: Bill which should be printed
        :param paper_size: Size of the paper on which the payment slip is printed. Either a tuple with width and height
        in mm or as an enum of PaperSize
        :param payment_slip_position: Position where to payment slip should be position on the paper. Either a tuple
        with the x and y position in mm or as an enum of PaymentSlipPosition

        :return: SVG image
        """

        if bill:
            self.bill = bill

        if self.bill is None:
            raise ValidationError("No bill provided!")

        if isinstance(paper_size, PaperSize):
            if paper_size is PaperSize.A4:
                size = (210 * mm, 297 * mm)
            elif paper_size is PaperSize.PAYMENT_SLIP:
                size = (self.receipt_width + self.payment_width, self.bill_height)
        else:
            size = (SVGPrinter.convert_to_pixel(v) for v in paper_size)

        if isinstance(payment_slip_position, PaymentSlipPosition):
            if payment_slip_position is PaymentSlipPosition.BOTTOM:
                insert = (0, 192 * mm)
            elif payment_slip_position is PaymentSlipPosition.TOP:
                insert = (0, 0)
        else:
            insert = (SVGPrinter.convert_to_pixel(v) for v in payment_slip_position)

        dwg = svgwrite.Drawing(size=size)
        dwg.add(shapes.Rect(size=(100 * percent, 100 * percent), fill="white"))

        drawing = self._draw(payment_slip_insert=insert)
        dwg.add(drawing)

        return dwg

    def _draw(self, payment_slip_insert=None):
        """ Internal draw method

        The drawing of the bill is split into the receipt and payment part. The two parts are separated by a dotted
        line.

        NOTE: Bill can be provided with the creation of the printer, by setting the attribute manually or when calling
        this function.

        :param payment_slip_insert: Insert position of the payment slip
        :return: None
        """

        payment_slip_container = container.SVG(
            id="qr_payment_slip",
            insert=payment_slip_insert,
            size=(self.total_width * mm, self.bill_height * mm)
        )

        # dwg.add(dwg.rect(id="background", insert=(0, 0), size=(100 * percent, 100 * percent), fill="yellow"))

        if self.as_sample:
            defs = container.Defs()
            p = pattern.Pattern(id="sample", patternUnits="userSpaceOnUse",
                                width="200", height="100", patternTransform="rotate(-30)")

            p.add(text.Text("Sample", font_size=40, text_anchor="middle", fill="#FFD3D3"))
            defs.add(p)
            payment_slip_container.add(defs)

            payment_slip_container.add(
                shapes.Rect(insert=(0, 0), size=(100 * percent, 100 * percent), fill="url(#sample)"))

        # Receipt part
        payment_slip_container.add(self._draw_recipient_part(
            insert=(self.margin * mm, self.margin * mm),
            size=((self.receipt_width - 2 * self.margin) * mm, (self.bill_height - 2 * self.margin) * mm))
        )

        # Horizontal separation line above payment slip
        payment_slip_container.add(shapes.Line(start=(0, 0), end=(self.total_width * mm, 0),
                                               stroke="black", stroke_dasharray="3 3"))

        # Vertical separation line between receipt and payment parts
        payment_slip_container.add(shapes.Line(id="separation_line", start=(self.receipt_width * mm, 0),
                                               end=(self.receipt_width * mm, self.bill_height * mm),
                                               stroke="black", stroke_dasharray="3 3"))

        # Payment part
        payment_slip_container.add(self._draw_payment_part(
            insert=((self.receipt_width + self.margin) * mm, self.margin * mm),
            size=((self.payment_width - 2 * self.margin) * mm, (self.bill_height - 2 * self.margin) * mm))
        )

        return payment_slip_container

    def _draw_recipient_part(self, insert, size):
        """ Draw receipt part

        The receipt part consists of four sections. The title and information and acceptance point section are always
        printed. If there is no amount, a blank field is printed instead.

        :param insert: absolute coordinate
        :param size: size of this part
        :return payment part
        :rtype svgwrite.container.SVG
        """

        fonts = self.fonts["receipt"]

        receipt_part = container.SVG(insert=insert, size=size, id="receipt_part")

        # title section
        title = self._draw_title(_("Receipt"), **self.fonts["title"])
        receipt_part.add(title)

        # Information section
        y = self.calculate_y(0, title)
        header = _("Account / Payable to")
        recipient = self.bill.recipient()
        creditor = self._draw_paragraph(y, header, recipient, fonts)
        receipt_part.add(creditor)

        y = self.calculate_y(y, creditor)
        header = _("Reference")
        lines = [self.bill.ref_number]
        reference = self._draw_paragraph(y, header, lines, fonts)
        receipt_part.add(reference)

        y = self.calculate_y(y, reference)
        lines = self.bill.sender()
        if not lines:
            header = _("Payable by (name/address)")
        else:
            header = _("Payable by")
        debtor = self._draw_paragraph(y, header, lines, fonts, blank_field_if_empty=True, field_width=52 * mm,
                                      field_height=20 * mm)
        receipt_part.add(debtor)

        # Amount section
        y = self.y_amount_section
        headers = [_("Currency"), _("Amount")]
        lines = [self.bill.currency, self.bill.amount]
        amount_section = self._draw_amount(y, headers, lines, fonts, field_width=30 * mm, field_height=10 * mm)
        receipt_part.add(amount_section)

        # Acceptance point section
        receipt_part.add(
            text.Text(_("Acceptance point"),
                      insert=((self.receipt_width - 2 * self.margin) * mm, self.y_acceptance_point),
                      text_anchor="end", **self.fonts["receipt"]["header"]))

        return receipt_part

    def _draw_payment_part(self, insert, size):
        """ Draw payment part

         Payment part consists is divided into two columns and consists of five sections. The left column contains the
         title, QR code and amount section. The right column contains the information section. The further information
         section is currently not implemented.

         The amount and information section have optional fields. If the amount or the debtor are unknown, the title and
         a blank field are printed. If other fields are empty, the corresponding title and the content are not printed
         at all (SVG container is stilled added).

         TODO: Move blank field below title instead of to the right
         TODO: Implement further information section

         :param insert: absolute coordinate
         :param size: size of this part
         :return payment part
         :rtype svgwrite.container.SVG
         """
        fonts = self.fonts["payment"]

        payment_part = container.SVG(id="payment_part", insert=insert, size=size)
        # payment_part.add(shapes.Rect(insert=(0, 0), size=("100%", "100%"), fill="blue"))

        # Left column
        left_part = container.SVG(id="left_column", insert=(0, 0), size=(56 * mm, 100 * percent))

        # title section
        title = self._draw_title(_("Payment part"), **self.fonts["title"])
        left_part.add(title)

        # qr code section
        y = self.calculate_y(0, title)
        qr_code = self.bill.qr_code(version=25, border=12, box_size=15).make_image().make_path().attrib["d"]
        qr_code_section = self._draw_qr_code(y, qr_code=qr_code)
        left_part.add(qr_code_section)

        # amount section
        y = self.y_amount_section
        headers = [_("Currency"), _("Amount")]
        lines = [self.bill.currency, self.bill.amount]
        amount_section = self._draw_amount(y, headers, lines, fonts, field_width=40 * mm, field_height=15 * mm)
        payment_part.add(amount_section)

        payment_part.add(left_part)

        # Right column
        right_part = container.SVG(insert=(56 * mm, 0), size=(82 * mm, 100 * percent))
        # right_part.add(shapes.Rect(size=(100*percent, 100*percent), fill="green"))

        y = 0
        header = _("Account / Payable to")
        recipient = self.bill.recipient()
        creditor = self._draw_paragraph(y, header, recipient, fonts)
        right_part.add(creditor)

        y = self.calculate_y(y, creditor)
        header = _("Reference")
        lines = [self.bill.ref_number]
        reference = self._draw_paragraph(y, header, lines, fonts)
        right_part.add(reference)

        y = self.calculate_y(y, reference)
        header = _("Additional information")
        additional_info = self.bill.additional_info()
        info = self._draw_paragraph(y, header, additional_info, fonts)
        right_part.add(info)

        y = self.calculate_y(y, info)
        lines = self.bill.sender()
        if not lines:
            header = _("Payable by (name/address)")
        else:
            header = _("Payable by")
        debtor = self._draw_paragraph(y, header, lines, fonts, blank_field_if_empty=True, field_width=65 * mm,
                                      field_height=25 * mm)
        right_part.add(debtor)

        payment_part.add(right_part)

        return payment_part

    @staticmethod
    def _draw_title(title, font_size=11, line_space=1.5, **extras):
        """ Draw title

        Returned SVG container has a height of font_size*line_space. The space is added below the text.

        :param title: text
        :param font_size: font size of the title
        :param line_space:
        :param extras: passed to text
        :return:
        """
        content = container.SVG(insert=(0, 0), size=(100 * percent, font_size * line_space))
        content.add(text.Text(title, dx=[0], dy=[font_size+1], **extras))

        return content

    @staticmethod
    def _draw_paragraph(y, head, lines, fonts, line_space=1.2, bottom_padding=3, blank_field_if_empty=False,
                        field_height=0, **kwargs):
        """ Write header with provided lines

        The paragraph is only drawn if :lines: contains at least one item.

        :param y: absolute coordinate of the paragraph
        :param head: header of the paragraph
        :param lines: List of text to be inserted
        :param fonts: Fonts for header and text as dict
        :param line_space: Multiplier of the font size for whitespace between lines:default 1.2
        :param bottom_padding: Padding at the end of the paragraph
        :return:
        """

        header_height = fonts["header"]["font_size"]
        text_start = header_height * line_space + fonts["text"]["font_size"]
        text_line_height = fonts["text"]["font_size"] * line_space

        lines_of_text = sum(1 for _ in filter(None.__ne__, lines))
        empty_paragraph = False

        if lines_of_text > 0:
            paragraph_height = header_height + text_start + lines_of_text * text_line_height + bottom_padding
        elif blank_field_if_empty:
            paragraph_height = field_height  # draw blank field
        else:
            paragraph_height = 0  # do not draw at all
            empty_paragraph = True

        content = container.SVG(insert=(0, y), size=("100%", paragraph_height))

        if empty_paragraph:
            return content  # return empty paragraph

        head = text.Text(text=head, dx=[0], dy=[header_height], **fonts["header"])
        content.add(head)

        if lines_of_text > 0:
            line_id = (i for i in range(len(lines)) if lines[i] is not None)

            for i in line_id:
                content.add(text.Text(text=lines[i], x=[0], dy=[text_line_height * i + text_start], **fonts["text"]))
        else:
            blank_field = SVGPrinter._draw_blank_field(x=0, y=text_start, field_height=field_height, **kwargs)
            content.add(blank_field)

        return content

    @staticmethod
    def _draw_line(text, dy, **extras):
        return text.Text(text=text, x=[0], dy=dy, **extras)

    @staticmethod
    def _draw_amount(y, headers, lines, fonts, intent=14 * mm, line_space=1.2, bottom_padding=3, **kwargs):

        header_height = fonts["header"]["font_size"]
        text_start = header_height + fonts["text"]["font_size"]
        text_line_height = fonts["text"]["font_size"] * line_space

        paragraph_height = header_height + (len(headers) - 1) * text_line_height + bottom_padding

        content = container.SVG(insert=(0, y), size=("100%", paragraph_height))

        for i, head in enumerate(headers):
            x = i * SVGPrinter.convert_to_pixel(intent)
            content.add(text.Text(text=head, insert=(x, header_height), **fonts["header"]))

            if i > 0 and (len(lines) < 2 or not lines[1]):
                content.add(SVGPrinter._draw_blank_field(x + text_start * 1.8, 0, **kwargs))
            else:
                content.add(text.Text(text=lines[i], insert=(x, text_start), **fonts["text"]))

        return content

    @staticmethod
    def _draw_qr_code(y, qr_code, bottom_padding=0):
        """Draw qr code with white cross in the center

        :param y: y coordinate where to draw the qr code
        :param qr_code: path instance containing the QR code
        :return:
        """
        content = container.SVG(insert=(0, y), size=("100%", 56 * mm))

        content.add(
            path.Path(id="qr_code", d=qr_code, style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none"))
        content.add(SVGPrinter._draw_white_cross(insert=(24.5 * mm, 24.5 * mm)))

        return content

    @staticmethod
    def _draw_white_cross(insert=(19.5 * mm, 19.5 * mm), size=(7 * mm, 7 * mm)):
        """Draw a white cross on a black square

        According to the 2017 flag law (SR 232.21) the cross is fixed at 5:8 of the height of the flag and the arms of
        the cross are one-sixth longer than they are wide.

        :param size: Size of the flag
        :param insert: Position of the flag
        :return:
        """
        content = container.SVG(insert=insert, size=size)

        content.add(shapes.Rect(size=(100*percent, 100*percent), fill="black"))

        # a = 0.18750 * SVGPrinter.convert_to_pixel(size[0])  # 6/32
        # b = 0.40625 * SVGPrinter.convert_to_pixel(size[0])  # 13/32
        # c = 0.62500 * SVGPrinter.convert_to_pixel(size[0])  # 20/32

        a = 18.750 * percent  # 6/32
        b = 40.625 * percent  # 13/32
        c = 62.500 * percent  # 20/32

        # Build cross from two rectangles
        content.add(shapes.Rect(insert=(a, b), size=(c, a), fill="white"))
        content.add(shapes.Rect(insert=(b, a), size=(a, c), fill="white"))

        return content

    @staticmethod
    def _draw_blank_field(x, y, field_width, field_height, line_width=None, line_height=None):
        stroke_info = {"stroke": "black", "stroke_width": 0.75 * pt, "stroke_linecap": "square", "fill": "none"}

        x = SVGPrinter.convert_to_pixel(x)
        y = SVGPrinter.convert_to_pixel(y)
        field_width = SVGPrinter.convert_to_pixel(field_width)
        field_height = SVGPrinter.convert_to_pixel(field_height)

        blank_field = container.Group()

        line_width = line_width or SVGPrinter.convert_to_pixel(3 * mm)
        line_height = line_height or SVGPrinter.convert_to_pixel(2 * mm)

        upper_left = [(x, y + line_height), (x, y), (x + line_width, y)]
        upper_right = [(x + field_width - line_width, y), (x + field_width, y), (x + field_width, y + line_height)]
        bottom_left = [(x, y + field_height - line_height), (x, y + field_height), (x + line_width, y + field_height)]
        bottom_right = [(x + field_width - line_width, y + field_height), (x + field_width, y + field_height),
                        (x + field_width, y + field_height - line_height)]

        blank_field.add(shapes.Polyline(upper_left, **stroke_info))
        blank_field.add(shapes.Polyline(upper_right, **stroke_info))
        blank_field.add(shapes.Polyline(bottom_left, **stroke_info))
        blank_field.add(shapes.Polyline(bottom_right, **stroke_info))

        return blank_field

    @staticmethod
    def calculate_y(current_y, previous_element):
        """Calculate the y coordinate based on the current_y coordinate and the height of the previous element"""
        if not previous_element:
            return current_y

        return current_y + SVGPrinter.convert_to_pixel(previous_element.attribs["height"])

    @staticmethod
    def convert_to_pixel(value):
        """Convert length in millimeter into pixels"""
        if isinstance(value, (int, float)):
            return value

        match = re.match(r"(\d+\.?\d{0,2})(?=mm)", value)
        if match:
            return float(match.group(1)) * 3.543307

        raise ConversionError(f"Could not convert '{value}' into pixel")


# class PDFPrinter(Printer):
#
#     def __init__(self, *args, **kwargs):
#         self.help_printer = SVGPrinter(*args, **kwargs)
#
#     def save_as(self, file_name, *args, **kwargs):
#         drawing = self.help_printer.draw(*args, **kwargs)
#         cairosvg.svg2pdf(drawing.tostring().encode(), write_to=file_name)
#
#     def draw(self, *args, **kwargs):
#         raise NotImplementedError
