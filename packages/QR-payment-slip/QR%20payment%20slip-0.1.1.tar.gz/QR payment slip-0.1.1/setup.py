#!/usr/bin/env python
import io
import os
import re


from setuptools import setup, find_packages

module_path = os.path.dirname(__file__)

with io.open(os.path.join(module_path, "qr_payment_slip/__init__.py"), "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with io.open(os.path.join(module_path, "./README.rst"), "rt", encoding="utf8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="QR payment slip",
    version=version,
    project_urls={
        "Source Code": "https://github.com/molitoris/qr_payment_slip"
    },
    author="Rafael S. Müller",
    author_email="rafa.molitoris@gmail.com",
    description="QR payment slip generator for Switzerland and Lichtenstein",
    long_description=LONG_DESCRIPTION,
    long_description_context_type="text/x-rst",
    packages=find_packages(),
    install_requires=[
        "svgwrite~=1.4",
        "qrcode~=6.1",
        "python-stdnum~=1.13",
        "iso3166~=1.0.1",
        "setuptools~=49.2.0",
        # "cairosvg~=2.4.2"
    ],
    keywords="QR payment slip bill swiss payment standard",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
    test_suite="tests"

)
