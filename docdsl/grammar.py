"""
File: grammar.py
Project: Docdsl
File Created: Wed 15 Jul 2026 08:14:58 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Wed 15 Jul 2026 08:14:58 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""


Grammar = """
Model:
	command*=Command
;

Command:
	  Find 
    | Skip 
    | SkipLines 
    | SkipNLines 
    | CaptureLines 
    | CaptureNLines 
    | CaptureBetween
    | Capture 
    | If
;

Builtin:
    Spaces | WhiteSpaces | Digits | AlphaNums
;

Spaces:
    value=/SPACES/
;

WhiteSpaces:
    value=/WHITESPACES/
;

Digits:
    value=/DIGITS/
;

AlphaNums:
    value=/ALPHANUMS/
;

//Entity will be represented by @ENTITY_NAME
//
//Entity:
//    /(?!SPACES\b
//    |WHITESPACES\b
//    |DIGITS\b
//    |ALPHANUMS\b
//    |FIND\b
//    |SKIP\b
//    |CAPTURE\b
//    |UNTIL\b
//    |OPTIONAL\b
//    |IF\b
//    |END\b
//    |EOL\b
//    |ENDOFLINE\b
//    |NEWLINE\b
//    |NEXTLINE\b
//    |LINE\b
//    |LINES\b
//    |AS\b
//    )[A-Z][A-Z0-9_]*/
//;

Entity:
    name=/@[A-Z][A-Z0-9_]*/
;

Find:
    'FIND'
    items+=FindItem[',']
    ';'
;

FindItem:
    ignorecase?='IGNORECASE'
    text=STRING
;

Skip:
	'SKIP' 
	'UNTIL' 
    ignorecase?='IGNORECASE'
	(position=Position | until=STRING)
    ';'
;

Position:
    End | NewLine
;

End:
    value=/END|EOL|ENDOFLINE/
;

NewLine:
    value=/NEWLINE|NEXTLINE/
;

SkipLines:
    'SKIP'
    'LINES'
    'UNTIL' until=STRING
    ';'
;

SkipNLines:
    'SKIP'
    lines=INT
    ('LINES' | 'LINE')
    ';'
;

Capture:
	'CAPTURE'
	items*=CaptureItem[',']
    'TARGET'
    target=TargetEntity
	('UNTIL' (position=Position | until=STRING))?
    ';'
;

CaptureItem:
	optional?='OPTIONAL' 
    (builtin=Builtin | entity=Entity)
;

TargetEntity:
    '[' entity=Entity ']'
;

CaptureNLines:
    'CAPTURE'
    lines=INT
    ('LINES' | 'LINE')
    'AS'
    target=TargetEntity
    ';'
;

CaptureLines:
    'CAPTURE'
    'LINES'
    'UNTIL' 
    ignorecase?='IGNORECASE'
    until=STRING
    'AS'
    target=TargetEntity
    ';'
;

CaptureBetween:
    'CAPTURE'
    'BETWEEN'
    start=CaptureBetweenItem
    'AND'
    end=CaptureBetweenItem
    scope=CaptureLinesScope?
    'AS'
    target=TargetEntity
    ';'
;

CaptureBetweenItem:
    ignorecase?='IGNORECASE'
    text=STRING
;

CaptureLinesScope:
    AcrossLines | SameLine
;

AcrossLines:
    value=/ACROSS LINES/
;

SameLine:
    value=/ON SAME LINE/
;

If:
	'IF'
    items+=IfItem[',']
    'THEN'
    commands+=Command
    'ENDIF'
;

IfItem:
    ignorecase?='IGNORECASE'
    (entity=Entity | text=STRING)
;

"""
