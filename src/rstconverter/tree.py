#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

"""
This module contains code to convert discourse graphs into rooted, ordered
trees.
"""

from collections import defaultdict, deque
import io
import textwrap

from nltk.tree import Tree, ParentedTree


class DGParentedTree(ParentedTree):
    """An nltk.tree.ParentedTree with an additional root_id parameter."""
    def __init__(self, node, children=None, root_id=None):
        # super calls __init__() of base class nltk.tree.ParentedTree
        super(DGParentedTree, self).__init__(node, children)
        self.root_id = root_id

    def get_position(self, rst_tree, node_id=None):
        """Get the linear position of an element of this DGParentedTree in an RSTTree.

        If ``node_id`` is given, this will return the position of the subtree
        with that node ID. Otherwise, the position of the root of this
        DGParentedTree in the given RSTTree is returned.
        """
        if node_id is None:
            node_id = self.root_id

        if node_id in rst_tree.edu_set:
            return rst_tree.edus.index(node_id)

        return min(self.get_position(rst_tree, child_node_id)
                   for child_node_id in rst_tree.child_dict[node_id])

    def node_height(self, rst_tree, node_id=None):
        if node_id is None:
            node_id = self.root_id
        return rst_tree.node_height(node_id)


def debug_root_label(root_label, debug=False, root_id=None):
    if debug is True and root_id is not None:
        return root_label + " ({})".format(root_id)
    else:
        return root_label


def t(root, children=None, debug=False, root_id=None):
    "Create (DGParented)Tree from a root (str) and a list of (str, list) tuples."
    if isinstance(root, Tree):
        if children is None:
            return root
        return root.__class__(root, children, root_id)

    elif isinstance(root, str):
        root = debug_root_label(root, debug, root_id)

        # Beware: (DGParented)Tree is a subclass of list!
        if isinstance(children, Tree):
            child_trees = [children]

        elif isinstance(children, list):
            child_trees = []
            for child in children:
                if isinstance(child, Tree):
                    child_trees.append(child)
                elif isinstance(child, list):
                    child_trees.extend(child)
                elif isinstance(child, tuple):
                    child_trees.append(t(*child))
                elif isinstance(child, str):
                    child_trees.append(child)
                else:
                    raise NotImplementedError

        elif isinstance(children, str):
            # this tree does only have one child, a leaf node
            # TODO: this is a workaround for the following problem:
            # Tree('foo', [Tree('bar', [])]) != Tree('foo', ['bar'])
            child_trees = [Tree(children, [])]

        else:
            # this tree only consists of one leaf node
            assert children is None
            child_trees = []

        return DGParentedTree(root, child_trees, root_id)

    else:
        raise NotImplementedError


def p(tree):
    """pretty-print a tree"""
    return tree.pretty_print()


def word_wrap_tree(parented_tree, width=0):
    """line-wrap an NLTK ParentedTree for pretty-printing"""
    if width != 0:
        for i, leaf_text in enumerate(parented_tree.leaves()):
            dedented_text = textwrap.dedent(leaf_text).strip()
            parented_tree[parented_tree.leaf_treeposition(i)] = textwrap.fill(dedented_text, width=width)
    return parented_tree


def is_leaf(elem):
    """Returns True, iff the given tree node is a leaf node."""
    return isinstance(elem, str)


def write_svgtree(tree, output_file=None):
    """convert an nltk.tree into an SVG file using svgling."""
    # We're not importing svgling globally because it monkey-patches
    # nltk's tree drawing mechanism, i.e. all trees in Jupyter will
    # look different when importing svgling.
    import svgling
    svgling.disable_nltk_png()

    tree_layout = svgling.draw_tree(tree)
    drawing = tree_layout.get_svg()
    
    if output_file is None:  # return string representation of SVG image
        f = io.StringIO()
        drawing.write(f)
        return f.getvalue()
    else:
        drawing.saveas(output_file)

