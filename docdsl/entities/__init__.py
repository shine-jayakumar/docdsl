"""
File: __init__.py
Project: DocDSL
File Created: Tue 21 Jul 2026 09:33:45 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Tue 21 Jul 2026 09:33:45 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

from .base import Entity
from .generic import *


# register modules here
MODULES = [
    "generic",
]


def builtin_entities() -> dict:
    """Get inbuilt entities"""
    import sys
    entities_mod = sys.modules[__name__]
    entities: dict[str, Entity] = {}
    for modname in MODULES:
        module = getattr(entities_mod, modname, None)
        if not module:
            continue
        entities.update(
            {
                key: val
                for key, val in vars(module).items()
                if isinstance(val, Entity)
            }
        )
    return entities


if __name__ == "__main__":
    pass




