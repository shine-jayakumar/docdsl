"""
File: generic.py
Project: DocDSL
File Created: Tue 21 Jul 2026 09:10:52 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Tue 21 Jul 2026 09:10:52 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

from .base import Entity


TITLE = Entity(
    name="TITLE",
    description="Matches common personal titles.",
    pattern=(
        r"(?:\b"
        r"(?i:Mr|Mrs|Miss|Ms|Mx|Dr|Prof|Professor|Sir|Madam|Lady|Lord)"
        r"\b\.?)"
    )

)

NAME = Entity(
    name="NAME",
    description="Matches a person's name.",
    pattern=r"[A-Za-z][A-Za-z ,.'-]*",
)

EMAIL = Entity(
    name="EMAIL",
    description="Matches an email address.",
    pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
)

PHONE = Entity(
    name="PHONE",
    description="Matches a telephone number.",
    pattern=(
        r"\+?\d{1,3}"
        r"(?:[-.\s]?\(?\d+\)?)?"
        r"(?:[-.\s]?\d+){2,}"
    ),
)

URL = Entity(
    name="URL",
    description="Matches an HTTP or HTTPS URL.",
    pattern=r"https?://[^\s]+",
)

DATE = Entity(
    name="DATE",
    description="Matches common date formats.",
    pattern=(
        r"\b(?:"
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|"
        r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
        r"|"
        r"\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
        r"[a-z]*\s\d{2,4}"
        r")\b"
    ),
)

TIME = Entity(
    name="TIME",
    description="Matches common time formats.",
    pattern=r"\b\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM)?\b",
)

DATETIME = Entity(
    name="DATETIME",
    description="Matches ISO-style date and time values.",
    pattern=(
        r"\b\d{4}-\d{2}-\d{2}"
        r"[ T]"
        r"\d{2}:\d{2}"
        r"(?::\d{2})?"
        r"\b"
    ),
)

INTEGER = Entity(
    name="INTEGER",
    description="Matches whole numbers.",
    pattern=r"-?\d+",
)

DECIMAL = Entity(
    name="DECIMAL",
    description="Matches decimal numbers.",
    pattern=r"-?\d+\.\d+",
)

NUMBER = Entity(
    name="NUMBER",
    description="Matches integer and decimal numbers.",
    pattern=r"-?\d+(?:\.\d+)?",
)

PERCENTAGE = Entity(
    name="PERCENTAGE",
    description="Matches percentage values.",
    pattern=r"-?\d+(?:\.\d+)?%",
)

MONEY = Entity(
    name="MONEY",
    description="Matches monetary values prefixed with a currency symbol.",
    pattern=r"(?:£|\$|€)\s?\d+(?:,\d{3})*(?:\.\d{2})?",
)

POSTCODE = Entity(
    name="POSTCODE",
    description="Matches UK postcodes.",
    pattern=r"\b(?:GIR\s?0AA|[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b",
)


if __name__ == "__main__":
    pass
