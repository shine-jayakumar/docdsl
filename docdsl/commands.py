"""
File: commands.py
Project: Docdsl
File Created: Wed 15 Jul 2026 08:07:54 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Wed 15 Jul 2026 08:07:54 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

import re
from dataclasses import dataclass, field
from .dsl_builtins import *
from .text_to_regex import TextToRegex


@dataclass
class Entity:
    parent: object
    name: str

    @property
    def group_name(self):
        return f"{self.name[1:]}"

    def to_regex(self):
        return f"__{self.name[1:]}__"


@dataclass
class Command:
    parent: object


@dataclass
class Find(Command):
    items: list = None

    def to_regex(self):
        pat_parts = [item.to_regex() for item in self.items]
        pattern = "|".join(pat_parts)
        pattern = f"(?:{pattern})" if len(self.items) > 1 else pattern
        return pattern


@dataclass
class FindItem(Command):

    text: str = ""
    ignorecase: bool = False

    def to_regex(self):
        pat = TextToRegex().get_regex(self.text)
        pat = f"(?i:{pat})" if self.ignorecase else pat
        return pat


@dataclass
class Skip(Command):

    position: str = ""
    until: str = ""
    ignorecase: bool = False

    def to_regex(self):
        if self.position:
            return self.position.to_regex()

        if self.until:
            until = re.escape(self.until)
            until = f"(?i:{until})" if self.ignorecase else until
            pat = rf".*?{until}"
            return pat


@dataclass
class SkipLines(Command):

    until: str

    def to_regex(self):
        until = re.escape(self.until)
        pat = rf"[\s\S]*?{until}"
        return pat


@dataclass
class SkipNLines(Command):

    lines: int

    def to_regex(self):
        pat = rf"(?:.*[\r\n]){{{self.lines}}}"
        return pat


#@dataclass
#class Capture(Command):
#
#    items: list = None
#    until: str = ""
#    position: Position = None
#
#    def to_regex(self):
#        target_count = sum([bool(item.target) for item in self.items])
#        if not target_count:
#            raise Exception("CAPTURE requires at least one target entity")
#        if target_count > 1:
#            raise Exception("CAPTURE cannot have more than one target entity")
#
#        target = self.items[-1]
#        pat_parts = [item.to_regex() for item in self.items[:-1]]
#        target_pat = target.target.to_regex()
#        group_name = target.target.entity.group_name
#        pat_parts.append(f"(?P<{group_name}>{target_pat})")
#        if self.until:
#            until_pat = TextToRegex().get_regex(self.until)
#            pat_parts.append(until_pat)
#        elif self.position:
#            pos = self.position.to_regex()
#            pat_parts.append(pos)
#        return "".join(pat_parts)

    #def __repr__(self):
    #    return (
    #        "Capture(items=[\n"
    #        f"{self.items}\n]\n,"
    #        f"until={self.until},\n"
    #        f"position={self.position}\n"
    #        ")"
    #    )
@dataclass
class TargetEntity(Command):

    entity: Entity

    def to_regex(self):
        return self.entity.to_regex()



@dataclass
class Capture(Command):

    items: list = None
    target: TargetEntity = None
    until: str = ""
    position: Position = None

    def to_regex(self):
        pat_parts = [item.to_regex() for item in self.items]
        target_pat = self.target.entity.to_regex()
        group_name = self.target.entity.group_name
        pat_parts.append(f"(?P<{group_name}>{target_pat})")
        if self.until:
            until_pat = TextToRegex().get_regex(self.until)
            pat_parts.append(until_pat)
        elif self.position:
            pos = self.position.to_regex()
            pat_parts.append(pos)
        return "".join(pat_parts)



#@dataclass
#class CaptureItem(Command):
#
#    optional: bool = False
#    builtin: Builtin=None
#    entity: str = None
#    target: TargetEntity = None
#
#    def to_regex(self):
#        if self.builtin:
#            pat = self.builtin.to_regex()
#            pat = f"{pat}?" if self.optional else pat
#            return pat
#
#        if self.entity:
#            pat = self.entity.to_regex()
#            pat = f"{pat}?" if self.optional else pat
#            return pat
#
#        if self.target:
#            return self.target.entity.to_regex()

@dataclass
class CaptureItem(Command):

    optional: bool = False
    builtin: Builtin=None
    entity: str = None

    def to_regex(self):
        if self.builtin:
            pat = self.builtin.to_regex()
            pat = f"{pat}?" if self.optional else pat
            return pat

        if self.entity:
            pat = self.entity.to_regex()
            pat = f"{pat}?" if self.optional else pat
            return pat


@dataclass
class CaptureNLines(Command):

    lines: int
    target: TargetEntity

    def to_regex(self):
        group_name = self.target.entity.group_name
        #pat = rf"(?P<{entity}>(?:.*[\r\n]){{{self.lines}}})"
        pat = rf"(?P<{group_name}>(?:.*\r?\n){{{self.lines}}})"
        return pat


@dataclass
class CaptureLines(Command):

    until: str
    target: TargetEntity
    ignorecase: bool = False

    def to_regex(self):
        group_name = self.target.entity.group_name
        between = AcrossLines(None, None).to_regex()
        until = TextToRegex().get_regex(self.until)
        until = f"(?i:{until})" if self.ignorecase else until
        pat = rf"(?P<{group_name}>{between}){until}"
        return pat


@dataclass
class CaptureBetween(Command):

    start: str
    end: str
    target: TargetEntity
    scope: CaptureLinesScope = None

    def to_regex(self):
        group_name = self.target.entity.group_name
        start = self.start.to_regex()
        end = self.end.to_regex()
        between = (
            AcrossLines(None, None).to_regex() if not self.scope
            else self.scope.to_regex()
        )
        pat = rf"{start}(?P<{group_name}>{between}){end}"
        return pat


@dataclass
class CaptureBetweenItem(Command):

    text: str
    ignorecase: bool = False

    def to_regex(self):
        pat = TextToRegex().get_regex(self.text)
        pat = f"(?i:{pat})" if self.ignorecase else pat
        return pat


@dataclass
class If(Command):

    items: list = None
    commands: list[Command] = None

    def _get_item_pattern(self) -> str:
        pat_parts = [item.to_regex() for item in self.items]
        pat = "|".join(pat_parts)
        pat = f"({pat})" if len(pat_parts) > 1 else pat
        return pat

    def _get_command_pattern(self) -> str:
        pat_parts = [cmd.to_regex() for cmd in self.commands]
        pat = "".join(pat_parts)
        return pat
        
    def to_regex(self):
        #pat_parts = [item.to_regex() for item in self.items]
        #pat = "|".join(pat_parts)
        #pat = f"({pat})" if len(pat_parts) > 1 else pat

        #pat += self.action.to_regex()
        pat = self._get_item_pattern()
        pat += self._get_command_pattern()
        pat = f"(?:{pat})?"
        return pat

        #for item in self.items:
        #    pat = self.item.to_regex()
        #pat = ""
        #if self.keyword:
        #    kwd_pattern = TextToRegex().get_regex(self.keyword)
        #    pat += kwd_pattern
        #elif self.entity:
        #    ent = f"__{self.entity}__"
        #    pat += ent
        #action_pattern = self.action.to_regex()
        #pat += action_pattern
        #pat = f"(?:{pat})?"
        #return pat



@dataclass
class IfItem(Command):

    text: str = ""
    entity: Entity = None
    ignorecase: bool = False

    def to_regex(self):
        if self.text:
            pat = TextToRegex().get_regex(self.text)
            pat = f"(?i:{pat})" if self.ignorecase else pat
            return pat

        # for entity
        pat = self.entity.to_regex()
        pat = f"(?i:{pat})" if self.ignorecase else pat
        return pat



if __name__ == "__main__":
    pass
