"""
File: dsl_builtins.py
Project: Docdsl
File Created: Wed 15 Jul 2026 08:08:02 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Wed 15 Jul 2026 08:08:02 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

from abc import ABC, abstractmethod


class Position(ABC):

    def __init__(self, parent, value):
        self.value = value

    @abstractmethod
    def to_regex(self):
        pass

class End(Position):

    def to_regex(self):
        return r"[^\r\n]*"

    def __repr__(self):
        return f"End(value='{self.value}')"

class NewLine(Position):

    def to_regex(self):
        return r"[^\r\n]*\s*"

    def __repr__(self):
        return f"NewLine(value='{self.value}')"


class Builtin(ABC):

    def __init__(self, parent, value):
        self.value = value

    @abstractmethod
    def to_regex(self):
        pass

class Spaces(Builtin):

    def to_regex(self):
        return r"(?:[ \t]+)"

    def __repr__(self):
        return f"Spaces(value='{self.value}')"

class WhiteSpaces(Builtin):

    def to_regex(self):
        return r"(?:\s+)"

    def __repr__(self):
        return f"WhiteSpaces(value='{self.value}')"


class Digits(Builtin):

    def to_regex(self):
        return r"(?:\d+)"

    def __repr__(self):
        return f"Digits(value='{self.value}')"


class AlphaNums(Builtin):

    def to_regex(self):
        return "(?:[A-Za-z\d]+)"

    def __repr__(self):
        return f"AlphaNums(value='{self.value}')"


class CaptureLinesScope(ABC):

    def __init__(self, parent, value):
        self.value = value

    @abstractmethod
    def to_regex(self):
        pass


class SameLine(CaptureLinesScope):

    def to_regex(self):
        return r"(?:.*?)"

    def __repr__(self):
        return f"SameLine(value='{self.value}')"


class AcrossLines(CaptureLinesScope):

    def to_regex(self):
        return r"(?s:.*?)"

    def __repr__(self):
        return f"AcrossLines(value='{self.value}')"


if __name__ == "__main__":
    pass
