#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

"""
This module contains code that is used by more than one RST-related modules.
"""
import ast

from nltk.tree import Tree


class RSTBaseTree(object):
    """Base class for converter's from from RST file formats into
    DGParentedTree-based trees.
    """
    def _repr_svg_(self):
        """This SVG representation will be automagically used inside
        IPython notebooks.
        """
        return self.tree._repr_svg_()

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


def _error_context(parse_tree_str, pos):
    start = max(0, pos - 20)
    return ("malformed parse tree input at position {}: {!r}"
            .format(pos, parse_tree_str[start:pos + 20]))


def _read_string_literal(parse_tree_str, pos):
    """Read the single-/double-quoted Python string literal that starts at
    position ``pos`` of ``parse_tree_str``.

    Returns a ``(value, next_pos)`` tuple. Escaped characters (e.g. \\" or
    \\\\ inside the literal) are handled exactly as in Python source code.
    """
    quote = parse_tree_str[pos]
    if quote not in '"\'':
        raise ValueError(_error_context(parse_tree_str, pos))

    end = pos + 1
    while end < len(parse_tree_str):
        char = parse_tree_str[end]
        if char == '\\':
            end += 2
        elif char == quote:
            literal = parse_tree_str[pos:end + 1]
            return ast.literal_eval(literal), end + 1
        else:
            end += 1
    raise ValueError("unterminated string literal at position {}".format(pos))


def _expect(parse_tree_str, pos, expected):
    """Skip whitespace and require the character ``expected`` at ``pos``.

    Returns the position after the expected character.
    """
    while pos < len(parse_tree_str) and parse_tree_str[pos].isspace():
        pos += 1
    if pos >= len(parse_tree_str) or parse_tree_str[pos] != expected:
        raise ValueError(_error_context(parse_tree_str, pos))
    return pos + 1


def parse_bracketed_tree(parse_tree_str, constructor_name='ParseTree'):
    """Parse a bracketed parse tree expression into an nltk.tree.Tree.

    Parses expressions of the form ``Name('label', [child, ...])``, where
    each child is either a quoted string (a leaf, e.g. an EDU) or a nested
    ``Name('label', [...])`` expression. This is the output format of RST
    parsers such as HILDA (``ParseTree``) and DPLP (``ParentedTree``).

    The input is parsed iteratively using an explicit stack, as these trees
    can be nested arbitrarily deeply for long documents: eval()-based
    parsing breaks on nesting depths of ~200 and more (with a MemoryError
    or SyntaxError, cf. https://github.com/rst-workbench/rst-converter-service/issues/3).

    Parameters:
    parse_tree_str : str
        bracketed parse tree expression
    constructor_name : str
        name of the tree constructor used in the expression,
        e.g. 'ParseTree' (HILDA) or 'ParentedTree' (DPLP)

    Returns:
    tree : nltk.tree.Tree
        parse tree object of the given parse tree string

    Raises:
    ValueError
        if the input is not a well-formed parse tree expression
    """
    prefix = constructor_name + '('
    stack = []
    root = None
    pos = 0

    while pos < len(parse_tree_str):
        char = parse_tree_str[pos]
        if char.isspace():
            pos += 1
        elif parse_tree_str.startswith(prefix, pos):
            pos = _expect(parse_tree_str, pos + len(prefix) - 1, '(')
            label, pos = _read_string_literal(parse_tree_str, pos)
            pos = _expect(parse_tree_str, pos, ',')
            pos = _expect(parse_tree_str, pos, '[')
            node = Tree(label, [])
            if stack:
                stack[-1].append(node)
            elif root is None:
                root = node
            else:
                raise ValueError(_error_context(parse_tree_str, pos))
            stack.append(node)
        elif char == ']':
            if not stack:
                raise ValueError(_error_context(parse_tree_str, pos))
            pos = _expect(parse_tree_str, pos + 1, ')')
            stack.pop()
        elif char in '"\'':
            if not stack:
                raise ValueError(_error_context(parse_tree_str, pos))
            leaf, pos = _read_string_literal(parse_tree_str, pos)
            stack[-1].append(leaf)
        elif char == ',':
            pos += 1
        else:
            raise ValueError(_error_context(parse_tree_str, pos))

    if stack or root is None:
        raise ValueError("unbalanced parse tree expression")
    return root
