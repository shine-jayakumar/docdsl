"""
File: base.py
Project: DocDSL
File Created: Tue 21 Jul 2026 09:10:19 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Tue 21 Jul 2026 09:10:19 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Entity:
    name: str
    pattern: str
    description: str = ""


if __name__ == "__main__":
    pass


