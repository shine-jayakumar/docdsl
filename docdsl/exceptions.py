"""
File: dsl_exceptions.py
Project: Docdsl
File Created: Sun 19 Jul 2026 12:49:39 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Sun 19 Jul 2026 18:59:47 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

import re
from textx.exceptions import TextXSyntaxError


class DocDSLError(Exception):
    pass


class UndefinedEntity(Exception):

    def __init__(self, dsl: str, entities: list[str]):
        """Raise when an undefined entity is found in the dsl"""
        self._dsl: str = dsl
        self._entities: list[str] = entities

    def _underline_entities(
        self, line: str, entspans: list[tuple[int, int]], lineno: str = ""
    ) -> list[str]:
        """Underlines the entities in a line"""
        entspans.sort(key=lambda span: span[0])
        underlined = ""
        marked_until = 0
        for span in entspans:
            st, en = span
            spaces = " " * (len(line[marked_until: st]))
            markers = "^" * (en - st)
            underlined += f"{spaces}{markers}"
            marked_until = en

        if lineno:
            lineno_spaces = " " * len(lineno)
            return f"{lineno}{line}\n{lineno_spaces}{underlined}"
        return f"{line}\n{underlined}"

    def _get_underlined_entities(self) -> str:
        """Get underlined entities"""
        lines = self._dsl.split("\n")
        entity_pattern = r"@([A-Z\d_]+)"
        underlined_lines = []
        for lineno, line in enumerate(lines):
            spans = [
                matched.span() for matched 
                in re.finditer(entity_pattern, line)
                if matched.group(1) in self._entities
            ]
            if not spans:
                continue
            underlined = self._underline_entities(
                line, spans, lineno=f"Ln {lineno}: "
            )
            underlined_lines.append(underlined)
        return underlined_lines

    def __str__(self):
        entities = ", ".join([f"@{entity}" for entity in self._entities])
        underlined = self._get_underlined_entities()
        underlined = "\n".join(underlined)
        return (
            f"\n\nUndefined {'Entity' if len(entities) > 1 else 'Entities'}: "
            f"{entities}\n\n"
            f"{underlined}"
        )


class DSLSyntaxError(DocDSLError):

    def __init__(self, dsl: str, exc: TextXSyntaxError):
        self._dsl: str = dsl
        self._exp: TextXSyntaxError = exc
        self._error: str = str(exc)
        self._errmsg: str = self._extract_errmsg()
        self._errcontext: str = self._extract_errcontext()
        self._org_errpos: tuple[int, int] = tuple()
        self._errpos: tuple[int, int] = self._extract_errpos()

    def _extract_errmsg(self) -> str:
        """Extracts the error message from exception"""
        msg = re.search(r":\s+(.+?)\s+=>", self._error)
        if not msg:
            return ""
        return msg.group(1).strip()

    def _extract_errcontext(self) -> str:
        """Extract the error context from exception"""
        context = self._error.split("=>")[1].strip()
        return context[1:-1]

    def _extract_errpos(self):
        """Extract line and column from the error message"""
        lines = self._dsl.split("\n")
        pos = re.match(r"None:(\d+):(\d+)", self._error)
        if not pos:
            return tuple()
        self._org_errpos = int(pos.group(1)), int(pos.group(2))
        row, col = self._org_errpos
        row, col = row - 1, col - 1
        # error on the same line
        if col != 0:
            if self._is_unterminated():
                # SKIP UNTIL END *SKIP UNTIL NEWLINE;
                # targetting space between END and SKIP
                unterm_part = lines[row][:col]
                last_token = re.search(r"[A-Z\]\[]+\s*$", unterm_part)
                col = last_token.span()[1] - 1
                return row, col

            errline_len = len(lines[row])
            col = errline_len - 1 if col >= errline_len else col
            return row, col

        if self._is_unterminated():
            row -= 1
            col = len(lines[row]) - 1
            return row, col

        return row, col

    def _is_unterminated(self) -> bool:
        """Checks if the line is unterminated"""
        expected_semicolon = re.search(r"Expected(.+?)';'", self._errmsg)
        if not expected_semicolon:
            return False
        return True

        lines = self._dsl.split("\n")
        erow, ecol = self._errpos
        if ecol != 1:
            return lines[erow - 1]
        failed_part = self._errcontext.split("*")[0]
        row = erow - 1
        for i in range(row, -1, -1):
            if not lines[i] or lines[i].isspace():
                continue
            if lines[i].endswith(failed_part):
                return lines[i]
        return lines[erow - 1]

    def _get_underlined(self) -> str:
        """Get underlined failed in error line"""
        row, col = self._errpos
        lines = self._dsl.split("\n")
        errline = lines[row]
        spaces = " " * col
        if col == len(errline) - 1:
            _, orgcol = self._org_errpos
            marker = " ^" if orgcol > len(errline) else "^"
            underlined = f"{spaces}{marker}"
            return f"{errline}\n{underlined}"

        if self._is_unterminated():
            spaces = " " * (col - 1)
            underlined = f"{spaces}^"
            return f"{errline}\n{underlined}"

        failed_token = re.match(r"\S+", errline[col:])
        if not failed_token:
            return errline
        failed_token = failed_token.group()
        underlined = spaces + "^" * len(failed_token)
        return f"{errline}\n{underlined}"

    def _get_display_pos(self) -> tuple[int, int]:
        """Get error position (line, col) for display"""
        row, col = self._errpos
        return row + 1, col + 1

    def _format_err(self) -> str:
        """Get formatted error message"""
        line, col = self._get_display_pos()
        errmsg = self._errmsg.replace("@[A-Z][A-Z0-9_]*", "ENTITY")
        underlined = self._get_underlined()
        return (
            f"\n\nLine {line}, Column {col}\n\n"
            f"{underlined}\n\n"
            f"{errmsg}"
        )

    def __str__(self):
        return self._format_err()


if __name__ == "__main__":
    pass


