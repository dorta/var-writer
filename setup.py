# Variscite Writer Tool - Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import os
from setuptools import setup, find_packages

setup(
    name = "varwriter",
    version = "0.0.1",
    author = "Diego Dorta",
    description = "Variscite Writer Tool",
    license = "BSD-3-Clause",
    url = "https://github.com/dorta/var-writer",
    packages=find_packages(),
    entry_points = {
        'console_scripts' : ['varwriter = varwriter.varwriter:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        "License :: OSI Approved :: BSD-3-Clause License",
        'Natural Language :: English',
        'Operating System :: Other OS',
        'Programming Language :: Python :: 3.8'
    ],
)
