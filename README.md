# DocDSL

![Version](https://img.shields.io/static/v1?label=version&message=v.0.0.2&color=blue)
![License](https://img.shields.io/static/v1?label=license&message=MIT&color=green)
![Status](https://img.shields.io/badge/status-alpha-yellow.svg)
![Open Source](https://img.shields.io/static/v1?label=OpenSource&message=Yes&color=brightgreen)
![GitHub issues](https://img.shields.io/github/issues/shine-jayakumar/docdsl)
![Last Commit](https://img.shields.io/github/last-commit/shine-jayakumar/docdsl)


A declarative DSL for extracting structured information from OCR output, PDFs, reports, and other semi-structured documents.

Instead of writing large, difficult-to-maintain regular expressions, **DocDSL** lets you describe **what** to extract using a simple, readable language while keeping extraction rules separate from your application code.

---

# Installation

```bash
pip install docdsl
```

---
# Quick Start

```python
from docdsl import DSLTranslator, Entity

# Define reusable entities
NAME = Entity(
    name="NAME",
    pattern=r"[A-Za-z ,.'-]+"
)

POSTCODE = Entity(
    name="POSTCODE",
    pattern=r"[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}"
)

# Create the translator
translator = DSLTranslator(
    entities=[
        NAME,
        POSTCODE,
    ]
)

# Describe what to extract
dsl = """
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];
"""

# Generate the regular expression
pattern = translator.translate(dsl)

print(pattern)
```
---

# Features

- Declarative, English-like extraction language
- Reusable named entities
- Readable extraction rules
- Conditional extraction using `IF`
- Multi-line capture
- Capture between delimiters
- Built-in helper tokens
- Friendly syntax and validation errors
- Exact error locations with line and column information

---

# Documentation

For the complete language reference, see **DSL_REFERENCE.md**.

The reference includes:

- Complete command reference
- DSL syntax
- Built-in helper tokens
- Conditional statements
- Examples
- Best practices
- Exception reference

---

# Requirements

- Python 3.11+

---

# Contributing

Contributions, bug reports and feature requests are welcome.

If you discover a bug or have an idea for improving **DocDSL**, please open an issue or submit a pull request.

---

# License

Released under the MIT License.
