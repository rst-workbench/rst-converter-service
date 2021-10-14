#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

"""
This module contains code that is used by more than one RST-related modules.
"""

class RSTBaseTree(object):
    """Base class for converter's from from RST file formats into
    DGParentedTree-based trees.
    """
    def _repr_png_(self):
        """This PNG representation will be automagically used inside
        IPython notebooks.
        """
        return self.tree._repr_png_()

    def __str__(self):
        return self.tree.__str__()

    def label(self):
        """Return the label of the tree's root element."""
        return self.tree.label()

    def pretty_print(self):
        """Return a pretty-printed representation of the RSTTree."""
        return self.tree.pretty_print()

    def __getitem__(self, key):
        return self.tree.__getitem__(key)
