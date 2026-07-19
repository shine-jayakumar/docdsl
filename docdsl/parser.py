"""
File: parser.py
Project: Docdsl
File Created: Wed 15 Jul 2026 08:13:45 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Wed 15 Jul 2026 08:13:45 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

from textx import metamodel_from_str
from .commands import (
    Find,
    FindItem,
    Skip,
    SkipLines,
    SkipNLines,
    Capture,
    CaptureItem,
    TargetEntity,
    CaptureNLines,
    CaptureLines,
    CaptureBetween,
    CaptureBetweenItem,
    SameLine,
    AcrossLines,
    If,
    IfItem,
    End,
    NewLine,
    Spaces,
    WhiteSpaces,
    Digits,
    AlphaNums,
    Entity
)
from .grammar import Grammar


DSLMetaModel = metamodel_from_str(
    Grammar,
    classes=[
        Find,
        FindItem,
        Skip,
        SkipLines,
        SkipNLines,
        Capture,
        CaptureItem,
        TargetEntity,
        CaptureNLines,
        CaptureLines,
        CaptureBetween,
        CaptureBetweenItem,
        SameLine,
        AcrossLines,
        If,
        IfItem,
        End,
        NewLine,
        Spaces,
        WhiteSpaces,
        Digits,
        AlphaNums,
        Entity
    ],
)


if __name__ == "__main__":
    pass
