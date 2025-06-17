# nodes.py
from typing import List, Optional


class Node:
    __slots__ = ("symbol", "tok_type", "lexeme", "children")
    
    def __init__(self, symbol: str, tok_type: Optional[str] = None, lexeme: Optional[str] = None):
        self.symbol = symbol
        self.tok_type = tok_type
        self.lexeme = lexeme
        self.children: List[Node] = []
    
    def add(self, child: "Node") -> None:
        self.children.append(child)
    
    def __repr__(self) -> str:
        if self.tok_type is None:
            return f"Node({self.symbol})"
        return f"Node({self.tok_type}, {self.lexeme})"