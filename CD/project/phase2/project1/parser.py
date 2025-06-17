#!/usr/bin/env python3
"""Ciut LL(1) predictive parser – class-based implementation."""
from __future__ import annotations
import sys
from collections import deque
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from nodes import Node
from scanner import Scanner
from utils import read_input_file, compute_first_sets, compute_follow_sets, build_parse_table
import json
import hashlib

class Parser:
    def __init__(self):
        self.grammar: Dict[str, List[List[str]]] = {
        'Program': [['Declaration-list']],
        'Declaration-list': [['Declaration', 'Declaration-list'], ['EPSILON']],
        'Declaration': [['Declaration-initial', 'Declaration-prime']],
        'Declaration-initial': [['Type-specifier', 'ID']],
        'Declaration-prime': [['Fun-declaration-prime'], ['Var-declaration-prime']],
        'Var-declaration-prime': [[';'], ['[', 'NUM', ']', ';']],
        'Fun-declaration-prime': [['(', 'Params', ')', 'Compound-stmt']],
        'Type-specifier': [['int'], ['void']],
        'Params': [['int', 'ID', 'Param-prime', 'Param-list'], ['void']],
        'Param-list': [[',', 'Param', 'Param-list'], ['EPSILON']],
        'Param': [['Declaration-initial', 'Param-prime']],
        'Param-prime': [['[', ']'], ['EPSILON']],
        'Compound-stmt': [['{', 'Declaration-list', 'Statement-list', '}']],
        'Statement-list': [['Statement', 'Statement-list'], ['EPSILON']],
        'Statement': [
            ['Expression-stmt'],
            ['Compound-stmt'],
            ['Selection-stmt'], 
            ['Iteration-stmt'],
            ['Return-stmt']
        ],
        'Expression-stmt': [['Expression', ';'], ['break', ';'], [';']],
        'Selection-stmt': [['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement']],
        'Iteration-stmt': [['repeat', 'Statement', 'until', '(', 'Expression', ')']],
        'Return-stmt': [['return', 'Return-stmt-prime']],
        'Return-stmt-prime': [[';'], ['Expression', ';']],
        'Expression': [['Simple-expression-zegond'], ['ID', 'B']],
        'B': [['=', 'Expression'], ['[', 'Expression', ']', 'H'], ['Simple-expression-prime']],
        'H': [['=', 'Expression'], ['G', 'D', 'C']],
        'Simple-expression-zegond': [['Additive-expression-zegond', 'C']],
        'Simple-expression-prime': [['Additive-expression-prime', 'C']],
        'C': [['Relop', 'Additive-expression'], ['EPSILON']],
        'Relop': [['<'], ['==']],
        'Additive-expression': [['Term', 'D']],
        'Additive-expression-prime': [['Term-prime', 'D']],
        'Additive-expression-zegond': [['Term-zegond', 'D']],
        'D': [['Addop', 'Term', 'D'], ['EPSILON']],
        'Addop': [['+'], ['-']],
        'Term': [['Factor', 'G']],
        'Term-prime': [['Factor-prime', 'G']],
        'Term-zegond': [['Factor-zegond', 'G']],
        'G': [['*', 'Factor', 'G'], ['EPSILON']],
        'Factor': [['(', 'Expression', ')'], ['ID', 'Var-call-prime'], ['NUM']],
        'Var-call-prime': [['(', 'Args', ')'], ['Var-prime']],
        'Var-prime': [['[', 'Expression', ']'], ['EPSILON']], 
        'Factor-prime': [['(', 'Args', ')'], ['EPSILON']],
        'Factor-zegond': [['(', 'Expression', ')'], ['NUM']],
        'Args': [['Arg-list'], ['EPSILON']],
        'Arg-list': [['Expression', 'Arg-list-prime']],
        'Arg-list-prime': [[',', 'Expression', 'Arg-list-prime'], ['EPSILON']]
    }
        self.terminals = {
            ';', '(', ')', '{', '}', '[', ']', ',', 
            '=', '<', '==', '+', '-', '*',
            'if', 'else', 'repeat', 'until', 'return', 'break',
            'int', 'void',
            'ID', 'NUM','$'
        }
        
        # Compute FIRST and FOLLOW sets
        self.first = compute_first_sets()
        self.follow = compute_follow_sets()
        
        # Build parse table
        self.table = build_parse_table(self.grammar, self.terminals)     



    
        self.scanner = Scanner()
        # Parser state
        self.lookahead: Optional[str] = None
        self.tok_type: Optional[str] = None
        self.lexeme: Optional[str] = None
        self.current_line: int = 1
        self.syntax_errors: List[str] = []
    
    def load_input(self, input_file: str = "input.txt"):
        """Load input file and initialize scanner."""
        try:
            input_text = read_input_file(input_file)
            self.scanner.set_input(input_text)
        except FileNotFoundError as e:
            sys.exit(str(e))
    
    def advance(self) -> None:
        """Get next token from scanner."""
        tok = self.scanner.get_next_token()
        if tok is None:  # EOF
            self.lookahead = "$"
            self.tok_type = self.lexeme = None
            return
        self.tok_type, self.lexeme, self.current_line = tok
        self.lookahead = self.tok_type if self.tok_type in {"ID", "NUM"} else self.lexeme
    
    def record_error(self, msg: str) -> None:
        """Record syntax error."""
        self.syntax_errors.append(f"#{self.current_line} : {msg}")
    
    def parse(self) -> Node:
        """Parse input and return parse tree."""
        self.advance()
        root = Node("Program")
        sym_stack: deque[str] = deque(["$", "Program"])
        node_stack: deque[Node] = deque([Node("$"), root])
        while sym_stack:
            X = sym_stack.pop()
            cur_node = node_stack.pop()
            if X == "EPSILON":
                cur_node.add(Node("epsilon"))
                continue
            
            # Terminal case
            if X in self.terminals:
                if self.lookahead == X:
                    if X != "$":
                        cur_node.tok_type, cur_node.lexeme = self.tok_type, self.lexeme
                    self.advance()
                else:
                    self.record_error(f"syntax error, missing {X}")
                continue
            
            # Non-terminal case
            prod = self.table.get((X, self.lookahead))
            if prod is None:
                if self.lookahead in self.follow[X] or self.lookahead == "$":
                    self.record_error(f"syntax error, missing {X}")
                    cur_node.add(Node("epsilon"))
                    continue
                
                while (self.lookahead not in self.first[X] and 
                       self.lookahead not in self.follow[X] and 
                       self.lookahead != "$"):
                    self.record_error(f"syntax error, illegal {self.lookahead}")
                    self.advance()
                
                if self.lookahead in self.first[X]:
                    sym_stack.append(X)
                    node_stack.append(cur_node)
                else:
                    self.record_error(f"syntax error, missing {X}")
                    cur_node.add(Node("epsilon"))
                continue
            
            # Expand production
            if prod == ["EPSILON"]:
                cur_node.add(Node("epsilon"))
            else:
                children = [Node(sym) for sym in prod]
                for ch in children:
                    cur_node.add(ch)
                for sym, ch in reversed(list(zip(prod, children))):
                    sym_stack.append(sym)
                    node_stack.append(ch)
        
        root.add(Node("$"))
        return root
    
    def dump_tree(self, node: Node, prefix: str, is_last: bool, out: List[str]):
        """Recursively dump parse tree to lines."""
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
            self.dump_tree(ch, new_pref, i == len(node.children) - 1, out)
    
    def write_output_files(self, tree: Node):
        """Write parse tree and syntax errors to files."""
        # Write parse tree
        lines: List[str] = []
        self.dump_tree(tree, "", True, lines)
        Path("parse_tree.txt").write_text("\n".join(lines), encoding="utf-8")
        
        # Write syntax errors
        if self.syntax_errors:
            Path("syntax_errors.txt").write_text("\n".join(self.syntax_errors), encoding="utf-8")
        else:
            Path("syntax_errors.txt").write_text("There is no syntax error.", encoding="utf-8")

def main():
    parser = Parser()
    try:
        parser.load_input("input.txt")
        tree = parser.parse()
        parser.write_output_files(tree)
        print("Parsing complete - examine parse_tree.txt and syntax_errors.txt")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()