"""LL(1) predictive parser implementation."""
from collections import deque
from pathlib import Path
from typing import List, Dict, Set, Optional
from utils import Node
from scanner import getNextToken
from parser_rules import grammar, first_sets, follow_sets, terminals


class Parser:
    """LL(1) predictive parser for the C- language."""

    def __init__(self, code: str):
        """Initialize the parser with input code and build the parse table.

        Args:
            code: The source code to parse
        """
        self.grammar: Dict[str, List[List[str]]] = grammar
        self.first = first_sets
        self.follow = follow_sets
        self.terminals = terminals
        self.table = self.build_parse_table()
        self.tree = None
        # Initialize scanner and parser state
        self.tokens = getNextToken(code)
        self.a: Optional[str] = None
        self.tok_type: Optional[str] = None
        self.lexeme: Optional[str] = None
        self.current_line: int = 1
        self.syntax_errors: List[str] = []
        
        self.parse()

    def build_parse_table(self) -> Dict[tuple, List[str]]:
        """Builds the LL(1) parse table using FIRST and FOLLOW sets.

        Returns:
            A dictionary mapping (non-terminal, terminal) pairs to their productions
        """
        table = {(nt, t): None for nt in grammar for t in terminals}

        for A, productions in grammar.items():
            for production in productions:
                prod_first: Set[str] = set()
                nullable = True
                for symbol in production:
                    # Use terminal if not in FIRST
                    sym_first = self.first.get(symbol, {symbol})
                    prod_first |= (sym_first - {"EPSILON"})  # Add all but EPSILON
                    if "EPSILON" not in sym_first:
                        nullable = False
                        break

                targets = prod_first | (self.follow[A] if nullable else set())
                for a in targets:
                    if a in terminals:  # Only add entries for valid terminals
                        table[(A, a)] = production

        return table

    def advance(self):
        """Advances to the next token from the scanner."""
        tok = next(self.tokens, None)
        if tok is None or tok[0] == "FIN":
            self.a = "$"
            self.tok_type = self.lexeme = None
            return
        self.tok_type, self.lexeme, self.current_line = tok
        self.a = self.tok_type if self.tok_type in {
            "ID", "NUM"} else self.lexeme

    def log_err(self, msg: str):
        """Records a syntax error with line number."""
        self.syntax_errors.append(f"#{self.current_line} : {msg}")

    def parse(self)->None:
        """Parses the input and builds the parse tree.

        Returns:
            The root node of the parse tree
        """
        self.advance()
        root = Node("Program")
        symbol_stack: deque[str] = deque(["$", "Program"]) # initial stack with $ and Program
        node_stack: deque[Node] = deque([Node("$"), root]) # initial stack with $ and root node

        while symbol_stack: # while the symbol stack is not empty
            X = symbol_stack.pop() # pop the top symbol from the symbol stack
            current_node = node_stack.pop() # pop the top node from the node stack 

            # Handle terminals
            if X in self.terminals:
                if self.a == X: 
                    if X != "$":
                        current_node.tok_type, current_node.lexeme = self.tok_type, self.lexeme
                    self.advance()
                else:
                    self.log_err(f"syntax error, missing {X}")
            # Handle non-terminals
            else:
                production = self.table.get((X, self.a))
                if production is None: # if the production is not in the parse table
                    # if production is in follow set of the non-terminal just discard X, becasue it's after X
                    if self.a in self.follow[X] or self.a == "$": # if the input is in the follow set of the non-terminal
                        self.log_err(f"syntax error, missing {X}")
                        current_node.add(Node("epsilon"))
                        continue
                    
                    # Error recovery: skip tokens until we find a valid one
                    while (self.a not in self.first[X] and # if the input is in first of the non-terminal -> it's fixed
                        self.a not in self.follow[X] and # if the input is in follow of the non-terminal -> it's fixed
                        self.a != "$"): # if the input is $ -> it's finished
                        self.log_err(
                            f"syntax error, illegal {self.a}")
                        self.advance()

                    if self.a in self.first[X]: # if the input is in first of the non-terminal -> it's fixed
                        symbol_stack.append(X) # add the symbol to the symbol stack
                        node_stack.append(current_node) # add the node to the node stack
                    else:
                        self.log_err(f"syntax error, missing {X}")
                        current_node.add(Node("epsilon"))
                    continue

                # Expand production
                if production == ["EPSILON"]: # if the production is epsilon
                    current_node.add(Node("epsilon"))
                else:
                    children = [Node(sym) for sym in production] # create the children nodes
                    for ch in children: # add the children to the current node
                        current_node.add(ch)
                    for sym, ch in reversed(list(zip(production, children))): # add the children to the current node
                        symbol_stack.append(sym) # add the symbol to the symbol stack
                        node_stack.append(ch) # add the node to the node stack

        root.add(Node("$"))
        self.tree = root


