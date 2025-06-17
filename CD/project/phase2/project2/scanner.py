import re
from scanner_rules import *

"""This function generates tokens from the input code"""
def getNextToken(code):
    pos = 0
    line_number = 1

    # Return the next character from the code and increment the position
    def getchar(): 
        nonlocal pos
        if pos == len(code):
            return None
        c = code[pos]
        pos += 1
        return c

    t = "" # processing token
    while True:
        if SYMBOL.match(t):
            if t in ("!", "="): #lookahead for != and ==
                lookahead = getchar()
                if lookahead == "=":
                    yield  "SYMBOL", t + lookahead, line_number
                    t = ""
                else:
                    pos -= 1
                    yield "SYMBOL", t, line_number
                    t = ""
            else :
                yield "SYMBOL", t, line_number
                t = ""
        elif KEYWORD.match(t):
            lookahead = getchar()
            pos -= 1
            if not re.match(r'[a-zA-Z0-9]',lookahead): 
                yield "KEYWORD", t, line_number
                t = ""
        elif ID.match(t):
            lookahead = getchar()
            pos -= 1
            if not re.match(r'[A-Za-z0-9]',lookahead):
                yield "ID", t, line_number
                t = ""
        elif NUM.match(t):
            lookahead = getchar()
            pos -= 1
            if not re.match(r'[0-9]',lookahead):
                yield "NUM", t, line_number
                t = ""
        next_char = getchar()
        if not next_char:
            yield "FIN", line_number
            return
        elif next_char == "\n":
            line_number += 1
        elif next_char == " " and len(t) == 0: # ignore leading spaces 
            pass
        else:
            t += next_char # Add new character to the token


