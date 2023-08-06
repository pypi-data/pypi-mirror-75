from enum import Enum


class PaperSize(Enum):
    A4 = 0
    PAYMENT_SLIP = 1


class PaymentSlipPosition(Enum):
    TOP = 0
    BOTTOM = 1
