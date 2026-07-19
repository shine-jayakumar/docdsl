# DocDSL

![License](https://img.shields.io/static/v1?label=license&message=MIT&color=green)
![Open Source](https://img.shields.io/static/v1?label=OpenSource&message=Yes&color=brightgreen)
![Version](https://img.shields.io/static/v1?label=version&message=v.0.0.1&color=blue)
![Status](https://img.shields.io/badge/status-alpha-yellow.svg)


A declarative DSL for extracting structured information from OCR output, PDFs, reports, and other semi-structured documents.

Instead of writing large, difficult-to-maintain regular expressions, **DocDSL** lets you describe **what** to extract using a simple, readable language while keeping extraction rules separate from your application code.

---

# Installation

```bash
pip install docdsl
```

---

# Quick Start

## 1. Define your entities

Entities are reusable regular expressions that can be referenced throughout your DSL.

```python
from docdsl import DSLTranslator, Entity

NAME = Entity(
    name="NAME",
    pattern=r"[A-Za-z ,.'-]+"
)

POSTCODE = Entity(
    name="POSTCODE",
    pattern=r"[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}"
)
```

## 2. Create a translator

```python
translator = DSLTranslator(
    entities=[
        NAME,
        POSTCODE,
    ]
)
```

## 3. Write your extraction rules

```python
dsl = """
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];
"""
```

## 4. Generate the regular expression

```python
pattern = translator.translate(dsl)
```

Your DSL is translated into a regular expression that can be used as part of your document extraction pipeline.

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

# Entities

Entities represent reusable regular expressions.

```python
TITLE = Entity(
    name="TITLE",
    pattern=r"(?:Mr|Mrs|Ms|Miss|Dr)\.?"
)
```

Supply your entities when creating the translator.

```python
translator = DSLTranslator(
    entities=[
        TITLE,
        NAME,
        POSTCODE,
    ]
)
```

Inside the DSL, entities are referenced using the `@` prefix.

```text
@TITLE
@NAME
@POSTCODE
```

If the DSL references an entity that was not supplied to `DSLTranslator`, an `UndefinedEntity` exception is raised.

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
