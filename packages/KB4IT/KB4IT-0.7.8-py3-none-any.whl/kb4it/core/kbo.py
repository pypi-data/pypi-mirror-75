#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RDF Graph In Memory database module.

# Author: Tomás Vírseda <tomasvirseda@gmail.com>
# License: GPLv3
# Description: In-memory database module
"""


class KBOject:
    def __init__(self, id=None):
        # ~ if id is None or len(id) ==0:
            # ~ raise ValueError("Identifier can't be None")
        self._id = id

    @property
    def id(self):
        print("Getting identifier...")
        return self._id

    @id.setter
    def id(self, id):
        print("Setting value...")
        if id is None or len(id) == 0:
            raise ValueError("Identifier can't be None")
        self._id = id
