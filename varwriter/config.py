#!/usr/bin/env python3
"""
Variscite Writer Tool - Copyright 2022 Variscite LTD

SPDX-License-Identifier: BSD-3-Clause
"""

import itertools
import os


CACHEDIR = os.path.join(os.environ['HOME'], ".cache", "varwriter")
CHUNK = 4 * 1024 * 1024
BUFFER_SIZE = 8192

GENERAL_FOLDER = "General"
VAR_WRITER_FOLDER = "var-writer"

MX8_SOM_DT_8M       = "DART-MX8M"
MX8_SOM_DT_8M_MINI  = "DART-MX8M-MINI"
MX8_SOM_DT_8M_PLUS  = "DART-MX8M-PLUS"

INFO_FILE_MX8_SOM_DT_8M       = "dart-mx8m.yml"
INFO_FILE_MX8_SOM_DT_8M_MINI  = "dart-mx8m-mini.yml"
INFO_FILE_MX8_SOM_DT_8M_PLUS  = "dart-mx8m-plus.yml"

MX8_SOM_DARTS = [MX8_SOM_DT_8M,
                 MX8_SOM_DT_8M_MINI,
                 MX8_SOM_DT_8M_PLUS]

MX8_SOM_VS_8        = "VAR-SOM-MX8"
MX8_SOM_VS_8X       = "VAR-SOM-MX8X"
MX8_SOM_VS_8M_NANO  = "VAR-SOM-MX8M-NANO"

INFO_FILE_MX8_SOM_VS_8        = "var-som-mx8.yml"
INFO_FILE_MX8_SOM_VS_8X       = "var-som-mx8x.yml"
INFO_FILE_MX8_SOM_VS_8M_NANO  = "var-som-mx8m-nano.yml"

MX8_SOM_VARS = [MX8_SOM_VS_8,
                MX8_SOM_VS_8X,
                MX8_SOM_VS_8M_NANO]

MX8_YAML_FILES = {MX8_SOM_DT_8M : INFO_FILE_MX8_SOM_DT_8M,
                  MX8_SOM_DT_8M_MINI : INFO_FILE_MX8_SOM_DT_8M_MINI,
                  MX8_SOM_DT_8M_PLUS : INFO_FILE_MX8_SOM_DT_8M_PLUS,
                  MX8_SOM_VS_8 : INFO_FILE_MX8_SOM_VS_8,
                  MX8_SOM_VS_8X : INFO_FILE_MX8_SOM_VS_8X,
                  MX8_SOM_VS_8M_NANO : INFO_FILE_MX8_SOM_VS_8M_NANO}

VAR_SYSTEM_ON_MODULES = list(itertools.chain(
                                   MX8_SOM_DARTS,
                                   MX8_SOM_VARS))
