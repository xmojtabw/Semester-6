"""Utility functions for the compiler."""
from typing import List, Optional
from pathlib import Path


def getfile(filename) -> str:
    """Reads the content of a file and returns it as a string."""
    with open(filename) as f:
        code = f.read()
    return code

class Node:
    """Represents a node in the parse tree."""

    def __init__(self, symbol: str, tok_type: Optional[str] = None, lexeme: Optional[str] = None):
        # The grammar symbol (terminal or non-terminal)
        self.symbol = symbol
        # Token type for terminals (e.g., ID, NUM, KEYWORD)
        self.tok_type = tok_type
        self.lexeme = lexeme      # The actual value of the token
        self.children: List[Node] = []  # Child nodes in the parse tree

    def add(self, child: 'Node'):
        """Adds a child node to this node."""
        self.children.append(child)


def draw_tree(node: Node, prefix: str, is_last: bool, out: List[str]):
    """Recursively dumps the parse tree to a list of strings with proper formatting.

    Args:
        node: The current node to process
        prefix: The prefix string for proper indentation
        is_last: Whether this node is the last child of its parent
        out: The list to store the output strings
    """
    if prefix == "":
        out.append(node.symbol)
    else:
        branch = "└── " if is_last else "├── "
        if node.tok_type is None:
            out.append(f"{prefix}{branch}{node.symbol}")
        else:
            out.append(f"{prefix}{branch}({node.tok_type}, {node.lexeme})")
    new_pref = prefix + ("    " if is_last else "│   ")
    for i, ch in enumerate(node.children):
        draw_tree(ch, new_pref, i == len(node.children) - 1, out)


def write_output_files(tree: Node, syntax_errors: List[str]):
    """Writes the parse tree and syntax errors to their respective output files.

    Args:
        tree: The root node of the parse tree
        syntax_errors: List of syntax error messages
    """
    # Write parse tree
    lines: List[str] = []
    draw_tree(tree, "", True, lines)
    Path("parse_tree.txt").write_text("\n".join(lines), encoding="utf-8")

    # Write syntax errors
    if syntax_errors:
        Path("syntax_errors.txt").write_text(
            "\n".join(syntax_errors), encoding="utf-8")
    else:
        Path("syntax_errors.txt").write_text(
            "There is no syntax error.", encoding="utf-8")
