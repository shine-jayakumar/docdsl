# DocDSL Reference

This document describes the complete syntax of the **DocDSL** language.

---

# Table of Contents

- [Introduction](#Introduction)
- [Language Overview](#Language-Overview)
- [Entities](#Entities)
- Translator
- [Commands](#Commands)
    - [FIND](#FIND)
    - [SKIP](#SKIP)
    - [CAPTURE](#CAPTURE)
    - [CAPTURE n LINES](#CAPTURE-n-LINES)
    - [CAPTURE LINES](#CAPTURE-LINES)
    - [CAPTURE BETWEEN](#CAPTURE-BETWEEN)
    - [IF](#IF)
- [Built-in Tokens](#Built-in-Tokens)
- [Error Handling](#Error-Handling)
- [Best Practices](#Best-Practices)
- [Examples](#Examples)
---

# Introduction

DocDSL is a Domain Specific Language (DSL) for describing document extraction rules.

Instead of writing complex regular expressions directly, you write a sequence of simple commands that are translated into a regular expression.

For example,

```text
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];
```

is considerably easier to read than an equivalent regular expression.

---

# Language Overview

A DocDSL program consists of one or more commands.

Example:

```text
FIND "Invoice Number:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@INVOICE_NUMBER];
```

Commands are executed in the order they appear.

Each command must terminate with a semicolon (`;`).

```text
✓ FIND "Name";
✓ SKIP UNTIL NEWLINE;
✓ CAPTURE TARGET [@NAME];
```

Missing semicolons produce a syntax error.

---

# Comments

Comments are not currently supported.

---

# Whitespace

Extra spaces and blank lines are ignored.

The following examples are equivalent.

```text
FIND "Name";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];
```

```text
FIND      "Name";


SKIP      UNTIL     NEWLINE;


CAPTURE TARGET [@NAME];
```

---

# String Literals

Text enclosed in double quotes is treated as a literal string.

Example:

```text
FIND "Name";
```

```text
FIND "Invoice Number";
```

```text
FIND "Address";
```

Strings are case-sensitive unless `IGNORECASE` is specified.

---

# IGNORECASE

Append `IGNORECASE` to a `FIND` command to perform a case-insensitive search.

Example:

```text
FIND IGNORECASE "Name";
```

Matches:

```
Name
name
NAME
NaMe
```

---

# Entities

Entities are reusable regular expressions supplied to the translator.

Example:

```python
from docdsl import Entity

NAME = Entity(
    name="NAME",
    pattern=r"[A-Za-z ,.'-]+"
)
```

Entities are registered when constructing the translator.

```python
translator = DSLTranslator(
    entities=[
        NAME,
    ]
)
```

Within the DSL they are referenced using the `@` symbol.

```text
@NAME
```

---

# Entity Naming Rules

Entity names

- must be unique
- are case-sensitive
- should use uppercase letters
- may contain digits
- may contain underscores

Recommended:

```text
@NAME
@FIRST_NAME
@LAST_NAME
@POSTCODE
```

Avoid:

```text
@name
@firstName
@LastName
```

---

# Undefined Entities

If an entity is referenced but not supplied to the translator, an
`UndefinedEntity` exception is raised.

Example:

```text
CAPTURE TARGET [@FULL_NAME];
```

Output:

```text
Undefined Entity: @FULL_NAME

Ln 1: CAPTURE TARGET [@FULL_NAME];
                      ^^^^^^^^^^
```

---

# Translator

Create a translator by supplying every entity used within the DSL.

```python
from docdsl import DSLTranslator, Entity

NAME = Entity(
    name="NAME",
    pattern=r"[A-Za-z ]+"
)

POSTCODE = Entity(
    name="POSTCODE",
    pattern=r"[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}"
)

translator = DSLTranslator(
    entities=[
        NAME,
        POSTCODE,
    ]
)
```

Translate a DSL.

```python
pattern = translator.translate(dsl)
```

The returned value is a regular expression.

---

# DSL Structure

A typical extraction script follows this pattern.

```text
FIND "...";
SKIP ...;
CAPTURE ...;

FIND "...";
SKIP ...;
CAPTURE ...;
```

This makes extraction rules easy to read and maintain.

---

# Command Overview

The language currently provides the following commands.

| Command | Purpose |
|----------|---------|
| FIND | Locate a string |
| SKIP | Advance through the document |
| CAPTURE | Capture text into an entity |
| IF | Conditional extraction |

The following sections describe every command in detail.

---
# FIND

Searches for a literal string in the document.

The generated regular expression advances until the specified string is found.

---

## Syntax

```text
FIND (optional IGNORECASE) "<string>";
```

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `IGNORECASE` | Performs a case-insensitive search. |
| `"<string>"` | The literal string to search for. |


---

## Examples

Find a simple string.

```text
FIND "Name:";
```

Case-insensitive search.

```text
FIND IGNORECASE "Name:";
```

---

## Notes

- Searches forward from the current position.
- Matching is case-sensitive unless `IGNORECASE` is specified.
- Multiple `FIND` commands may be used within the same DSL.

---

## Common Mistakes

Missing string.

```text
FIND;
```

Using an entity.

```text
FIND @NAME;
```

Missing quotation marks.

```text
FIND Name;
```

Incorrect keyword placement.

```text
FIND IGNORECASE "Name";
```

Missing semicolon.

```text
FIND "Name:"
```

---

# SKIP

Moves the current position within the document.

SKIP does not capture text. It only advances the parser.

---

## Syntax

Skip until a literal string.

```text
SKIP UNTIL (optional IGNORECASE) "<string>"|Position;
```
Skip a fixed number of lines.

```text
SKIP <int> LINES;
```

Skip lines until a literal string.

```text
SKIP LINES UNTIL "<string>";
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `IGNORECASE` | Performs a case-insensitive search. |
| `"<string>"` | The literal string to search for. |
| `<int>` | A positive integer. |
| `Position` | A builtin line position (ex. END, EOL, NEXTLINE etc.,)  |


---

## Examples

Skip until a marker.

```text
SKIP UNTIL "Address:";
```

Skip until the next line.

```text
SKIP UNTIL NEWLINE;
```

Skip to the end of the current line.

```text
SKIP UNTIL END;
```
Skip one line.

```text
SKIP 1 LINE;
```

Skip three lines.

```text
SKIP 3 LINES;
```

Skip lines until a marker.

```text
SKIP LINES UNTIL "Home Phone";
```


---

## Notes

- `SKIP` never captures text.
- Skipping is always relative to the current position.
- Multiple `SKIP` commands may be chained together.

Example

```text
SKIP UNTIL NEWLINE;
SKIP 2 LINES;
```

---

## Common Mistakes

Missing argument.

```text
SKIP;
```

Missing `UNTIL`.

```text
SKIP NEWLINE;
```

Invalid keyword.

```text
SKIP TO END;
```

Negative values.

```text
SKIP -2 LINES;
```

Missing semicolon.

```text
SKIP UNTIL END
```

---

# CAPTURE

Captures text from the current position.

A capture may consist of built-in tokens, entities or both.

Every `CAPTURE` command stores its result into a target entity.

---

## Syntax

Capture an entity.

```text
CAPTURE @ENTITY1 TARGET [@TARGET_ENTITY];
```

Capture multiple items.

```text
CAPTURE @ENTITY1, OPTIONAL SPACES, @ENTITY2 TARGET [@TARGET_ENTITY];
```

Capture until a delimiter.

```text
CAPTURE @ENTITY1 TARGET [@TARGET_ENTITY] UNTIL "<string>";
```

Capture until a position.

```text
CAPTURE @ENTITY1 TARGET [@TARGET_ENTITY] UNTIL NEWLINE;
```
Capture lines as target entity.

```text
CAPTURE 2 LINES TARGET [@ADDRESS];
```
---

## Parameters

| Parameter | Description |
|-----------|-------------|
| Capture Items | One or more built-ins or entities to capture. |
| `TARGET` | Specifies the destination entity. |
| `UNTIL` | Optional stopping condition. |
| `OPTIONAL` | Marks a capture item as optional. |
| `"<string>"` | The literal string to search for. |
| `@ENTITY1, @TARGET_ENTITY`,... | Registered entities |

---

## OPTIONAL

Marks a capture item as optional.

```text
CAPTURE OPTIONAL @TITLE, @NAME TARGET [@EMPLOYEE_NAME];
```

Optional whitespace.

```text
CAPTURE OPTIONAL SPACES, @NAME TARGET [@NAME];
```

---

## UNTIL

Limits the capture.

Until a literal string.

```text
CAPTURE @ADDRESS TARGET [@ADDRESS]
UNTIL "Postcode:";
```

Until the next line.

```text
CAPTURE @NAME TARGET [@NAME]
UNTIL NEWLINE;
```

Until the end of the current line.

```text
CAPTURE TARGET [@DESCRIPTION] 
UNTIL END;
```

---

## Examples

Simple capture.

```text
CAPTURE @NAME TARGET [@NAME];
```

Capture a title and name.

```text
CAPTURE @TITLE, SPACES, @NAME
TARGET [@EMPLOYEE_NAME];
```

Capture an optional title.

```text
CAPTURE OPTIONAL @TITLE, SPACES, @NAME
TARGET [@EMPLOYEE_NAME];
```

Capture an address.

```text
CAPTURE @ADDRESS
TARGET [@ADDRESS]
UNTIL "Postcode:";
```

Capture until the next line.

```text
CAPTURE @NAME
TARGET [@NAME]
UNTIL NEWLINE;
```

---

## Notes

- Every `CAPTURE` command must specify exactly one `TARGET`.
- `TARGET` is mandatory.
- A target entity is enclosed in [].
- `UNTIL` is optional.
- Capture items are evaluated from left to right.

---

## Common Mistakes

Missing target.

```text
CAPTURE @NAME;
```

Unknown entity.

```text
CAPTURE @FULL_NAME TARGET [@NAME];
```

Missing semicolon.

```text
CAPTURE @NAME TARGET [@NAME]
```

Using more than one target.

```text
CAPTURE @TITLE TARGET [@TITLE], TARGET [@NAME];
```

---
# Capture n LINES

Captures a fixed number of consecutive lines starting from the current position.

This command is useful when the required information always spans a known number of lines.

---

## Syntax

```text
CAPTURE <int> LINE AS [@ENTITY];
```

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<int>` | The number of lines to capture. |
| `LINE` / `LINES` | Specifies that the capture length is measured in lines. Both forms are accepted. |
| `AS` | Assigns the captured text to an entity. |
| `[@ENTITY]` | The destination entity that stores the captured value. |

---

## Examples

Capture a single line.

```text
CAPTURE 1 LINE AS [@NAME];
```

Capture two lines.

```text
CAPTURE 2 LINES AS [@ADDRESS];
```

---

## Notes

- Capturing begins at the current position.
- Exactly the specified number of lines are captured.
- Both `LINE` and `LINES` are valid keywords.
- The captured text is assigned to the specified target entity.

---


# CAPTURE LINES

Captures complete lines starting from the current position until a specified string is encountered.

The terminating string is **not** included in the captured value.

This command is useful when the length of the text is unknown but ends at a well-defined marker.

---

## Syntax

```text
CAPTURE LINES UNTIL (optional IGNORECASE) "<string>" AS [@ENTITY];
```
---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `"<string>"` | The string that marks the end of the capture. |
| `IGNORECASE` | Performs a case-insensitive search for the terminating string. |
| `AS` | Assigns the captured text to an entity. |
| `[@ENTITY]` | The destination entity that stores the captured value. |

---

## Examples

Capture an address until the postcode heading.

```text
CAPTURE LINES UNTIL "Postcode:" AS [@ADDRESS];
```

Perform a case-insensitive search for the terminating string.

```text
CAPTURE LINES UNTIL IGNORECASE "End of Report" AS [@REPORT];
```

---

## Notes

- Capturing begins at the current position.
- The terminating string is **not** included in the captured value.
- `IGNORECASE` applies only to the terminating string.
- The captured text is assigned to the specified target entity.

---


# CAPTURE BETWEEN

Captures the text between two delimiters.

The starting and ending delimiters may be matched either case-sensitively or case-insensitively. By default, the search is performed across multiple lines, or it can be configured to search in the current line.

This command is useful when the required information is enclosed between two known markers.

---

## Syntax

```text
CAPTURE BETWEEN 
(optional IGNORECASE) "<start>"
AND (optional IGNORECASE) "<end>"
AS [@ENTITY];
```

```text
CAPTURE BETWEEN 
(optional IGNORECASE)"<start>"
AND (optional IGNORECASE) "<end>"
ON SAME LINE
AS [@ENTITY];
```

```text
CAPTURE BETWEEN 
(optional IGNORECASE) "<start>"
AND (optional IGNORECASE) "<end>"
ACROSS LINES
AS [@ENTITY];
```

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `"<start>"` | The string that marks the beginning of the capture. |
| `"<end>"` | The string that marks the end of the capture. |
| `IGNORECASE` | Performs a case-insensitive search for the delimiter immediately following it. |
| `ON SAME LINE` | Restricts the search to the current line. |
| `ACROSS LINES` | Allows the search to continue across multiple lines. |
| `AS` | Assigns the captured text to an entity. |
| `[@ENTITY]` | The destination entity that stores the captured value. |

---

## Examples

Capture the text between parentheses.

```text
CAPTURE BETWEEN "(" AND ")" AS [@VALUE];
```

Capture the text between square brackets.

```text
CAPTURE BETWEEN "[" AND "]" AS [@CODE];
```

Capture a section that spans multiple lines.

```text
CAPTURE BETWEEN "Look"
AND "leap"
ACROSS LINES
AS [@ADAGE];
```

Capture text that must remain on the same line.

```text
CAPTURE BETWEEN "("
AND ")"
ON SAME LINE
AS [@VALUE];
```

Perform a case-insensitive search for both delimiters.

```text
CAPTURE BETWEEN IGNORECASE "Name:"
AND IGNORECASE "Address:"
AS [@SECTION];
```

Perform a case-insensitive search for only the ending delimiter.

```text
CAPTURE BETWEEN "Department"
AND IGNORECASE "Home"
AS [@DEPARTMENT];
```

---

## Notes

- Capturing begins immediately after the starting delimiter.
- The starting and ending delimiters are **not** included in the captured value.
- `IGNORECASE` affects only the delimiter immediately following it.
- If neither `ON SAME LINE` nor `ACROSS LINES` is specified, the default capture scope is used.
- The captured text is assigned to the specified target entity.

---

# IF

The `IF` command allows conditional extraction.

The commands inside an `IF` block are executed only when the condition matches.

---

## Syntax

```text
IF "<text>" THEN
    ...
ENDIF;
```

```text
IF "<text>" IGNORECASE THEN
    ...
ENDIF;
```

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `"<text>"` | String to search for. |
| `IGNORECASE` | Performs a case-insensitive search. |
| `THEN` | Begins the conditional block. |
| `ENDIF` | Ends the conditional block. |

---

## Examples

### Simple Condition

```text
IF "Address:" THEN

    SKIP UNTIL "Home Phone";
    SKIP 3 LINES;

ENDIF;
```

The enclosed commands are executed only if `"Address:"` exists.

---

### Case-Insensitive Condition

```text
IF IGNORECASE "Address:" THEN

    FIND "Address:";
    SKIP UNTIL NEWLINE;
    CAPTURE TARGET [@ADDRESS];

ENDIF;
```

Matches any of the following:

```text
Address:
ADDRESS:
address:
```
---

## Notes

- An `IF` block may contain one or more commands.
- Commands execute in the order they appear.
- Every `IF` block must terminate with `ENDIF;`.

---

## Invalid Syntax

### Missing `THEN`

```text
IF "Name:"
```

### Missing `ENDIF`

```text
IF "Name:" THEN

    FIND "Name:";
```

### Missing condition

```text
IF THEN
```

### Incorrect keyword order

```text
IF THEN "Name:"
```

### Missing semicolon

```text
ENDIF
```

# Built-in Tokens

Built-in tokens are predefined keywords that can be used within the DSL. They represent commonly used character classes or matching behaviors and remove the need to write regular expressions directly.

---

## Character Tokens

| Built-in | Description | Example |
|----------|-------------|---------|
| `SPACES` | Matches one or more space characters. | `CAPTURE @NAME, SPACES, @SURNAME AS [@FULL_NAME];` |
| `WHITESPACES` | Matches one or more whitespace characters, including spaces, tabs and newlines. | `CAPTURE WHITESPACES, @TEXT AS [@VALUE];` |
| `DIGITS` | Matches one or more numeric digits (`0-9`). | `CAPTURE DIGITS AS [@NUMBER];` |
| `ALPHANUMS` | Matches one or more alphanumeric characters (`A-Z`, `a-z`, `0-9`). | `CAPTURE ALPHANUMS AS [@CODE];` |

---

## Matching Tokens

### OPTIONAL

Marks the following capture item as optional.

#### Syntax

```text
OPTIONAL <capture-item>
```

#### Examples

```text
CAPTURE OPTIONAL @TITLE, @NAME AS [@FULL_NAME];
```

```text
CAPTURE OPTIONAL SPACES, @NAME AS [@NAME];
```

```text
CAPTURE OPTIONAL DIGITS, @CODE AS [@PRODUCT_CODE];
```

#### Notes

- `OPTIONAL` only affects the capture item immediately following it.
- Multiple optional items may be used within the same `CAPTURE` command.

---

### IGNORECASE

Performs a case-insensitive match.

`IGNORECASE` affects only the token or string immediately following it.

#### Examples

Case-insensitive `FIND`.

```text
FIND IGNORECASE "Name:";
```

Case-insensitive delimiter.

```text
CAPTURE BETWEEN IGNORECASE "("
AND ")"
AS [@VALUE];
```

Case-insensitive terminating string.

```text
CAPTURE LINES UNTIL IGNORECASE "End"
AS [@SECTION];
```

#### Notes

- `IGNORECASE` applies only to the expression immediately following it.
- It does not affect the entire command.

---

## Position Tokens

The following keywords represent commonly used positions within a document.

| Token | Description | Example |
|------|-------------|---------|
| `NEWLINE`, `NEXTLINE` | Represents the beginning of the next line. | `SKIP UNTIL NEWLINE;` |
| `END`, `EOL`, `ENDOFLINE` | Represents the end of the current line. | `SKIP UNTIL END;` |

---

## Line Scope Tokens

The following tokens control whether a capture is restricted to the current line or allowed to span multiple lines.

| Token | Description | Example |
|------|-------------|---------|
| `ON SAME LINE` | Restricts the capture to the current line. | `CAPTURE BETWEEN "(" AND ")" ON SAME LINE AS [@VALUE];` |
| `ACROSS LINES` | Allows the capture to span multiple lines. | `CAPTURE BETWEEN "Start" AND "End" ACROSS LINES AS [@SECTION];` |

---
# Complete Examples

The following examples demonstrate how multiple commands can be combined to create readable extraction rules.

---

## Example 1 — Extract a Name

```text
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];
```

---

## Example 2 — Extract Multiple Fields

```text
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];

FIND "Email:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@EMAIL];
```

---

## Example 3 — Capture an Optional Title

```text
FIND "Name:";
SKIP UNTIL NEWLINE;

CAPTURE
    OPTIONAL @TITLE,
    OPTIONAL SPACES,
    @NAME
TARGET [@FULL_NAME];
```

---

## Example 4 — Capture a Multi-line Section

```text
FIND "Address:";
SKIP UNTIL NEWLINE;

CAPTURE
TARGET [@ADDRESS]
UNTIL "Email:";
```

---

## Example 5 — Conditional Extraction

```text
IF "Shipping Address" THEN

    FIND "Shipping Address";
    SKIP UNTIL NEWLINE;
    CAPTURE TARGET [@SHIPPING_ADDRESS];

ENDIF;
```

---

## Example 6 — Capture an Entire Description

```text
FIND "Description";
SKIP UNTIL NEWLINE;

CAPTURE
TARGET [@DESCRIPTION]
UNTIL "Notes";
```

---

## Example 7 — Capture a Name with an Optional Title

```text
FIND "Name:";
SKIP UNTIL NEWLINE;

CAPTURE
    OPTIONAL @TITLE,
    OPTIONAL SPACES,
    @NAME
TARGET [@FULL_NAME]
UNTIL NEWLINE;
```

---

## Example 8 — Capture Between Two Headings

```text
FIND "Summary";
SKIP UNTIL NEWLINE;

CAPTURE
TARGET [@SUMMARY]
UNTIL "Remarks";
```

---

## Example 9 — Optional Section

```text
IF "Comments" THEN

    FIND "Comments";
    SKIP UNTIL NEWLINE;

    CAPTURE
    TARGET [@COMMENTS]
    UNTIL NEWLINE;

ENDIF;
```

---
# Best Practices

## Keep Commands Small

Prefer several simple commands.

```text
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];
```

instead of trying to perform everything in one large `CAPTURE`.

---

## Use Descriptive Entity Names

Choose entity names that clearly describe the information they represent.

Recommended:

```text
@FULL_NAME
@EMAIL
@PHONE_NUMBER
@POSTCODE
@ACCOUNT_NUMBER
```

Avoid:

```text
@NAME1
@VALUE
@FIELD
@DATA
```

---

## Group Related Commands

Separate unrelated extractions with blank lines.

```text
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];

FIND "Email:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@EMAIL];

FIND "Phone:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@PHONE_NUMBER];
```

This makes the DSL much easier to read.

---

## Prefer Reusable Entities

Define regular expressions once.

```python
NAME = Entity(
    name="NAME",
    pattern=r"[A-Za-z ,.'-]+"
)
```

Then reference them throughout the DSL.

```text
CAPTURE @NAME TARGET [@NAME];
```

instead of repeating the same regular expression in multiple places.

---

## One Responsibility Per Entity

An entity should represent a single logical piece of information.

Good:

```text
@TITLE
@NAME
@EMAIL
@PHONE_NUMBER
```

Avoid creating overly broad entities that attempt to match multiple kinds of information.

---

## Keep the DSL Declarative

The DSL should describe **what** to extract.

Entities should describe **how** to recognize the text.

Keeping these responsibilities separate results in extraction rules that are easier to understand, maintain, and reuse.

---

## Use Blank Lines

Blank lines are ignored by the parser and can be used to improve readability.

Good:

```text
FIND "Name:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@NAME];

FIND "Address:";
SKIP UNTIL NEWLINE;
CAPTURE TARGET [@ADDRESS];
```

This is much easier to read than writing every command without spacing.

---

## Prefer Literal Headings

When possible, locate sections using clear headings.

```text
FIND "Name:";
```

instead of relying solely on positional extraction.

This makes your DSL more resilient to document layout changes.
