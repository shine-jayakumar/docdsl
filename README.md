# DocDSL

![Version](https://img.shields.io/static/v1?label=version&message=v.0.0.3&color=blue)
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
from docdsl import DSLTranslator

translator = DSLTranslator()

dsl = """
FIND "Patient:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];
"""

pattern = translator.translate(dsl)
print(pattern)

with open("doc.txt", "r") as fh:
    text = fh.read()
    matches = pattern.finditer(text)
    for matched in matches:
        print(f"{matched=}")
        matched_groups = matched.groupdict()
        name = matched_groups.get("NAME", None)
        print(f"Name: {name}")

```

The `NAME` entity is part of DocDSL's built-in entity library and is available
automatically. Custom entities can still be supplied when additional matching
behaviour is required.

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

Complete language documentation is available in the
[DocDSL Documentation](https://github.com/shine-jayakumar/docdsl/blob/master/Documentation.md).

The reference includes:

- Complete command reference
- DSL syntax
- Built-in helper tokens
- Conditional statements
- Examples
- Best practices

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
