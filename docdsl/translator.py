"""
File: dsl_translator.py
Project: Docdsl
File Created: Wed 15 Jul 2026 08:12:11 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Wed 15 Jul 2026 08:12:11 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""


import re
from dataclasses import dataclass
from textx.exceptions import TextXSyntaxError
from .parser import DSLMetaModel
from .exceptions import DSLSyntaxError, UndefinedEntity


@dataclass
class Entity:
    name: str
    pattern: str



class DSLTranslator:

    def __init__(self, entities: list[Entity]) -> None:
        self._entity_map: dict[str, Entity] = {
            f"__{entity.name}__": entity for entity in entities
        }
        self._dsl: str = ""
        self._dsl_entities: list[str] = []
        self._template: str = ""
        self._pattern: re.Pattern = None

    def translate(self, dsl: str) -> re.Pattern:
        """Translates DSL to regex"""
        self._dsl = dsl
        self._template = ""
        self._pattern = None
        try:
            model = DSLMetaModel.model_from_str(dsl)
        except TextXSyntaxError as ex:
             raise DSLSyntaxError(dsl, ex)
        for cmd in model.command:
            self._template += cmd.to_regex()

        self._pattern = self._inject_entities(self._template)
        self._pattern = re.compile(self._pattern, re.MULTILINE)
        return self._pattern

    def get_dsl_entities(self) -> list[str]:
        """Get entities present in dsl"""
        return [entity[2:-2] for entity in self._dsl_entities]

    def _extract_entities(self, template: str) -> list[str]:
        """Extracts entities from dsl"""
        entity_pattern = r"__[A-Z\d_]+__"
        entities = re.findall(entity_pattern, template)
        return entities

    def _verify_entities(self, entities: list[str]) -> None:
        """Verifies if entities in the dsl is defined"""
        undefined_entities = [
            entity for entity in entities 
            if entity not in self._entity_map
        ]
        if undefined_entities:
            undefined_entities = [entity[2:-2] for entity in undefined_entities]
            raise UndefinedEntity(self._dsl, undefined_entities)

    def _inject_entities(self, template: str) -> str:
        """Injects entity pattern into template"""
        self._dsl_entities = self._extract_entities(template)
        self._verify_entities(self._dsl_entities)
        pattern = template
        for dslentity, entity in self._entity_map.items():
            pattern = pattern.replace(dslentity, entity.pattern)
        return pattern


if __name__ == "__main__":
    pass



        
