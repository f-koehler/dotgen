#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="dotgen",
    version="0.1.2",
    description="Dotfiles generator",
    author="Fabian Köhler",
    author_email="fkoehler1024@googlemail.com",
    url="https://github.com/f-koehler/dotgen",
    license="MIT",
    packages=["dotgen"],
    entry_points={
        "console_scripts": [
            "dotgen = dotgen.__main__:main"
        ]
    }
)
