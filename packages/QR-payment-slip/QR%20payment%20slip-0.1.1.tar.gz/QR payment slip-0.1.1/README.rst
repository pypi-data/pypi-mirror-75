=========================
QR payment slip generator
=========================

Purpose
=======
This library generates QR payment slips for Switzerland and Liechtenstein, which follow the `Swiss Payment Standards 2019 (Version 2.1) <https://www.paymentstandards.ch/>`_.

The library currently outputs the payment slips as SVG graphics.

Samples
-------

* `Minimal`_
* `Minimal with amount`_
* `Minimal with amount and debtor`_
* `Minimal with amount, debtor and reference number`_
* `Minimal with amount, debtor, reference number and unstructured message`_

.. _Minimal: ./sample/01_bill_minimal.svg
.. _Minimal with amount: ./sample/02_bill_amount.svg
.. _Minimal with amount and debtor: ./sample/03_bill_amount_debtor.svg
.. _Minimal with amount, debtor and reference number: ./sample/04_bill_amount_debtor_ref.svg
.. _Minimal with amount, debtor, reference number and unstructured message: ./sample/05_bill_amount_debtor_ref_msg.svg

Installation
============

    $ pip install qr-payment-slip

Usage example
=============

.. code-block:: python

    from qr_payment_slip.bill import QRPaymentSlip, Address

    payment_slip = QRPaymentSlip()

    # Set IBAN number (mandatory)
    payment_slip.account = "CH9889144356966475815"

    # Set address of creditor (mandatory)
    payment_slip.creditor = Address(name="Hans Muster", address_line_1="Musterstrasse", address_line_2="1", pcode=1000, town="Musterhausen")

    # Set amount (optional)
    payment_slip.amount = 100

    # Set address of debtor (optional)
    payment_slip.debtor = Address(name="Marie de Brisay", address_line_1="Dreibündenstrasse 34", pcode=7260,
                                  town="Davos Dorf")

    # Generate and save qr payment slip
    payment_slip.save_as("my_bill.svg")

Running tests
=============

You can run tests either by executing::

    $ python setup.py test

