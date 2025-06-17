# utils.py
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional

def read_input_file(file_path: str) -> str:
    """Read input file and return its content."""
    inp = Path(file_path)
    if not inp.exists():
        raise FileNotFoundError(f"{file_path} not found.")
    return inp.read_text(encoding="utf-8")

def compute_first_sets():
        return {
            'Program': {'int', 'void'},
            'Declaration-list': {'int', 'void', 'ε'},
            'Declaration': {'int', 'void'},
            'Declaration-initial': {'int', 'void'},
            'Declaration-prime': {';', '[', '('},
            'Var-declaration-prime': {';', '['},
            'Fun-declaration-prime': {'('},
            'Type-specifier': {'int', 'void'},
            'Params': {'int', 'void'},
            'Param-list': {',', 'ε'},
            'Param': {'int', 'void'},
            'Param-prime': {'[', 'ε'},
            'Compound-stmt': {'{'},
            'Statement-list': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{', 'ε'},
            'Statement': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{'},
            'Expression-stmt': {'(', ';', 'ID', 'NUM', 'break'},
            'Selection-stmt': {'if'},
            'Iteration-stmt': {'repeat'},
            'Return-stmt': {'return'},
            'Return-stmt-prime': {'(', ';', 'ID', 'NUM'},
            'Expression': {'(', 'ID', 'NUM'},
            'B': {'=', '[', '(', '*', '+', '-', '<', '=='},
            'H': {'=', '*', '+', '-', '<', '=='},
            'Simple-expression-zegond': {'(', 'NUM'},
            'Simple-expression-prime': {'(', '*', '+', '-', '<', '=='},
            'C': {'<', '==', 'ε'},
            'Relop': {'<', '=='},
            'Additive-expression': {'(', 'ID', 'NUM'},
            'Additive-expression-prime': {'(', '*', '+', '-'},
            'Additive-expression-zegond': {'(', 'NUM'},
            'D': {'+', '-', 'ε'},
            'Addop': {'+', '-'},
            'Term': {'(', 'ID', 'NUM'},
            'Term-prime': {'(', '*'},
            'Term-zegond': {'(', 'NUM'},
            'G': {'*', 'ε'},
            'Factor': {'(', 'ID', 'NUM'},
            'Var-call-prime': {'(', '['},
            'Var-prime': {'[', 'ε'},
            'Factor-prime': {'(', 'ε'},
            'Factor-zegond': {'(', 'NUM'},
            'Args': {'(', 'ID', 'NUM', 'ε'},
            'Arg-list': {'(', 'ID', 'NUM'},
            'Arg-list-prime': {',', 'ε'}
        }
        
        
def compute_follow_sets():
        return {
            'Program': {'$'},
            'Declaration-list': {'$', '(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{', '}'},
            'Declaration': {'int', 'void', '(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{', '}', '$'},
            'Declaration-initial': {'(', ')', ',', ';', '['},
            'Declaration-prime': {'int', 'void', '(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{', '}', '$'},
            'Type-specifier': {'ID'},
            'Fun-declaration-prime': {'int', 'void', '(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{', '}', '$'},
            'Var-declaration-prime': {'int', 'void', '(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{', '}', '$'},
            'Params': {')'},
            'Param-list': {')'},
            'Param': {')', ','},
            'Param-prime': {')', ','},
            'Compound-stmt': {'int', 'void', '(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', 'until', '{', '}', 'else', '$'},
            'Statement-list': {'}'},
            'Statement': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', 'until', '{', '}', 'else'},
            'Expression-stmt': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', 'until', '{', '}', 'else'},
            'Selection-stmt': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', 'until', '{', '}', 'else'},
            'Iteration-stmt': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', 'until', '{', '}', 'else'},
            'Return-stmt': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', 'until', '{', '}', 'else'},
            'Return-stmt-prime': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', 'until', '{', '}', 'else'},
            'Expression': {')', ',', ';', ']'},
            'B': {')', ',', ';', ']'},
            'H': {')', ',', ';', ']'},
            'Simple-expression-zegond': {')', ',', ';', ']'},
            'Simple-expression-prime': {')', ',', ';', ']'},
            'C': {')', ',', ';', ']'},
            'Relop': {'(', 'ID', 'NUM'},
            'Additive-expression': {')', ',', ';', ']'},
            'Additive-expression-prime': {')', ',', ';', '<', '==', ']'},
            'Additive-expression-zegond': {')', ',', ';', '<', '==', ']'},
            'D': {')', ',', ';', '<', '==', ']'},
            'Addop': {'(', 'ID', 'NUM'},
            'Term': {')', '+', ',', '-', ';', '<', '==', ']'},
            'Term-prime': {')', '+', ',', '-', ';', '<', '==', ']'},
            'Term-zegond': {')', '+', ',', '-', ';', '<', '==', ']'},
            'G': {')', '+', ',', '-', ';', '<', '==', ']'},
            'Factor': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
            'Var-call-prime': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
            'Var-prime': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
            'Factor-prime': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
            'Factor-zegond': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
            'Args': {')'},
            'Arg-list': {')'},
            'Arg-list-prime': {')'}
        }


def build_parse_table(grammar: Dict[str, List[List[str]]], terminals: Set[str]) -> Dict[Tuple[str, str], Optional[List[str]]]:
    """Build LL(1) parse table using precomputed FIRST and FOLLOW sets."""
    # Precomputed FIRST sets
    FIRST = {
        'Program': {'EPSILON', 'int', 'void'},
        'Declaration-list': {'EPSILON', 'int', 'void'},
        'Declaration': {'int', 'void'},
        'Declaration-initial': {'int', 'void'},
        'Declaration-prime': {'(', ';', '['},
        'Var-declaration-prime': {';', '['},
        'Fun-declaration-prime': {'('},
        'Type-specifier': {'int', 'void'},
        'Params': {'int', 'void'},
        'Param-list': {',', 'EPSILON'},
        'Param': {'int', 'void'},
        'Param-prime': {'EPSILON', '['},
        'Compound-stmt': {'{'},
        'Statement-list': {'(', ';', 'EPSILON', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{'},
        'Statement': {'(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{'},
        'Expression-stmt': {'(', ';', 'ID', 'NUM', 'break'},
        'Selection-stmt': {'if'},
        'Iteration-stmt': {'repeat'},
        'Return-stmt': {'return'},
        'Return-stmt-prime': {'(', ';', 'ID', 'NUM'},
        'Expression': {'(', 'ID', 'NUM'},
        'B': {'(', '*', '+', '-', '<', '=', '==', 'EPSILON', '['},
        'H': {'*', '+', '-', '<', '=', '==', 'EPSILON'},
        'Simple-expression-zegond': {'(', 'NUM'},
        'Simple-expression-prime': {'(', '*', '+', '-', '<', '==', 'EPSILON'},
        'C': {'EPSILON', '<', '=='},
        'Relop': {'<', '=='},
        'Additive-expression': {'(', 'ID', 'NUM'},
        'Additive-expression-prime': {'(', '*', '+', '-', 'EPSILON'},
        'Additive-expression-zegond': {'(', 'NUM'},
        'D': {'+', '-', 'EPSILON'},
        'Addop': {'+', '-'},
        'Term': {'(', 'ID', 'NUM'},
        'Term-prime': {'(', '*', 'EPSILON'},
        'Term-zegond': {'(', 'NUM'},
        'G': {'*', 'EPSILON'},
        'Factor': {'(', 'ID', 'NUM'},
        'Var-call-prime': {'(', 'EPSILON', '['},
        'Var-prime': {'EPSILON', '['},
        'Factor-prime': {'(', 'EPSILON'},
        'Factor-zegond': {'(', 'NUM'},
        'Args': {'(', 'EPSILON', 'ID', 'NUM'},
        'Arg-list': {'(', 'ID', 'NUM'},
        'Arg-list-prime': {',', 'EPSILON'},
    }

    # Precomputed FOLLOW sets
    FOLLOW = {
        'Program': {'$'},
        'Declaration-list': {'$', '(', ';', 'ID', 'NUM', 'break', 'if', 'repeat', 'return', '{', '}'},
        'Declaration': {'$', '(', ';', 'ID', 'NUM', 'break', 'if', 'int', 'repeat', 'return', 'void', '{', '}'},
        'Declaration-initial': {'(', ')', ',', ';', '['},
        'Declaration-prime': {'$', '(', ';', 'ID', 'NUM', 'break', 'if', 'int', 'repeat', 'return', 'void', '{', '}'},
        'Var-declaration-prime': {'$', '(', ';', 'ID', 'NUM', 'break', 'if', 'int', 'repeat', 'return', 'void', '{', '}'},
        'Fun-declaration-prime': {'$', '(', ';', 'ID', 'NUM', 'break', 'if', 'int', 'repeat', 'return', 'void', '{', '}'},
        'Type-specifier': {'ID'},
        'Params': {')'},
        'Param-list': {')'},
        'Param': {')', ','},
        'Param-prime': {')', ','},
        'Compound-stmt': {'$', '(', ';', 'ID', 'NUM', 'break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void', '{', '}'},
        'Statement-list': {'}'},
        'Statement': {'(', ';', 'ID', 'NUM', 'break', 'else', 'if', 'repeat', 'return', 'until', '{', '}'},
        'Expression-stmt': {'(', ';', 'ID', 'NUM', 'break', 'else', 'if', 'repeat', 'return', 'until', '{', '}'},
        'Selection-stmt': {'(', ';', 'ID', 'NUM', 'break', 'else', 'if', 'repeat', 'return', 'until', '{', '}'},
        'Iteration-stmt': {'(', ';', 'ID', 'NUM', 'break', 'else', 'if', 'repeat', 'return', 'until', '{', '}'},
        'Return-stmt': {'(', ';', 'ID', 'NUM', 'break', 'else', 'if', 'repeat', 'return', 'until', '{', '}'},
        'Return-stmt-prime': {'(', ';', 'ID', 'NUM', 'break', 'else', 'if', 'repeat', 'return', 'until', '{', '}'},
        'Expression': {';', ',', ')', ']'},
        'B': {';', ',', ')', ']'},
        'H': {';', ',', ')', ']'},
        'Simple-expression-zegond': {';', ',', ')', ']'},
        'Simple-expression-prime': {';', ',', ')', ']'},
        'C': {';', ',', ')', ']'},
        'Relop': {'(', 'ID', 'NUM'},
        'Additive-expression': {';', ',', ')', ']'},
        'Additive-expression-prime': {';', '<', '==', ',', ')', ']'},
        'Additive-expression-zegond': {';', '<', '==', ',', ')', ']'},
        'D': {';', '<', '==', ',', ')', ']'},
        'Addop': {'(', 'ID', 'NUM'},
        'Term': {')', '+', ',', '-', ';', '<', '==', ']'},
        'Term-prime': {')', '+', ',', '-', ';', '<', '==', ']'},
        'Term-zegond': {')', '+', ',', '-', ';', '<', '==', ']'},
        'G': {')', '+', ',', '-', ';', '<', '==', ']'},
        'Factor': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
        'Var-call-prime': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
        'Var-prime': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
        'Factor-prime': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
        'Factor-zegond': {')', '*', '+', ',', '-', ';', '<', '==', ']'},
        'Args': {')'},
        'Arg-list': {')'},
        'Arg-list-prime': {')'},
    }

    # Build the parse table
    table = {(nt, t): None for nt in grammar for t in terminals}
    
    for A, prods in grammar.items():
        for prod in prods:
            prod_first: Set[str] = set()
            nullable = True
            for sym in prod:
                sym_first = FIRST.get(sym, {sym})  # Use terminal if not in FIRST
                prod_first |= (sym_first - {"EPSILON"})
                if "EPSILON" not in sym_first:
                    nullable = False
                    break
            
            targets = prod_first | (FOLLOW[A] if nullable else set())
            for a in targets:
                if a in terminals:  # Only add entries for valid terminals
                    table[(A, a)] = prod
                    
    return table