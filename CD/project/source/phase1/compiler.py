import re

# name: Mojtaba Mollaei
# stdnum: 40131383
# resources: Chatgpt, Copilot, Slides and Compilers, principles, techniques and tools by Aho, Sethi and Ullman

"""Reads the content of a file and returns it as a string."""
def getfile(filename) -> str:
    with open(filename) as f:
        code = f.read()
    return code


"""Writes the given lines to a file. If the lines are empty, writes the empty_message instead."""
def writefile(name: str, lines, empty_message):
    empty = True
    with open(name, "w") as f:
        for i, line in enumerate(lines, start=1):
            if line:
                prefix = str(i) + "." +"\t"
                f.write(f"{prefix}{line}\n")
                empty = False
        if empty:
            f.write(empty_message)


"""Regex patterns for identifying invalid inputs, identifiers, numbers and comments
Invalid input:
    This regex pattern is used to match invalid inputs, including:
        - '//'
        - Invalid characters (e.g., special characters, symbols) like ~ and ^  matches-> '^' 'abc^'
        - Things like cd!e matches-> 'cdie' 'cd!' 'cd!e' not matches-> 'cd!= 1' 'cd!= 1.0' 
        - Things like 'return;;!' if ! is not followed by some \\s*[a-zA-Z0-9(=-]) matches-> '!' '!)' '!!' not matches-> '!=' '! =' '! abc'  
        - For '! ='. matches-> '! =' not matches-> '! abc' 
        - For handeling '/'. matches-> '/ +' '/ /' not matches-> '/ abc' '/ !1' '/ 1.0' 
Invalid num:
    this regex pattern is used to match invalid numbers, including:
        - '123abc' '123@' '123#' '123$' '123%' '123\''
Uncosed comment:
    this regex pattern is used to match unclosed comments, including:
        - '/* comment' 
Unopened comment:
    this regex pattern is used to match unopened comments, including:
        - 'comment */'
"""
INVALID_INPUT = re.compile(
    r"//|(a-z|A-Z|!|=|&|\||\*|\-|\+|<|>|/|\(|\)|{|}|\[|\]|;|,)*[~^`'\"\.@#\$%\\]|[a-zA-Z0-9]+!(?!=)|!(?!\s*[a-zA-Z0-9!(=-])|! (?!\s*[a-zA-Z0-9!(-])|/(?!\s*[a-zA-Z0-9!\(-])"
)
INVALID_NUM = re.compile(r"[0-9]+[A-Za-z@#\$%\\]")
UNCLOSED_COMMENT = re.compile(r"/\*")
UNOPENED_COMMENT = re.compile(r"\*/")

"""Regex patterns for identifying valid inputs, identifiers, numbers, symbols and keywords"""
ID = re.compile(r"[A-Za-z][A-Za-z0-9]*")
NUM = re.compile(r"[0-9]+")
KEYWORD = re.compile(
    r"(int|void|if|else|while|return|repeat|until|break|bool|true|false|void)"
)
SYMBOL = re.compile(r"(!|!=|==|=|&&|\|\||\*|\-|\+|<=|>=|<|>|/|\(|\)|{|}|\[|\]|;|,)")

"""list of keywords"""
KEYWORDS = "int bool void true false if else while until repeat break return".split(" ")



"""Preprocesses the input code by removing comments and replacing other whitespace characters with spaces."""
def preprocess(code: str) -> list:
    def replace_with_spaces(match):  # Ensure that \n will not replace
        comment = match.group(0)
        return "".join("\n" if c == "\n" else " " for c in comment)

    # Replace the comments with spaces
    COMMENT = r"/\*[\s\S]*?\*/" # It will match everything between /* and */ but non-greedy
    code = re.sub(COMMENT, replace_with_spaces, code)

    # Replace other whitespace with space
    OTHER_WHITESPACE = r"[\r\t\v\f]"
    code = re.sub(OTHER_WHITESPACE, " ", code)

    return code

"""processes the invalid tokens in the code and returns a list of errors and the cleaned code."""
def process_invalid(code: str):
    lines = code.split("\n")
    cleaned_lines = []
    all_errors = []

    """For each invalid token, we add the in output and replace the error part with spaces"""
    def process_invalid_tokens(line, tokens, error_type):
        output = [] # each error consist of a tuple (error_msg, position)
        modified_line = line
        for token in tokens: 
            t = token.group(0) 
            s, e = token.start(), token.end()
            context_len = 7 # for showing in errors

            if error_type == "Unclosed comment":
                e = len(line)
                snippet = line[s : s + context_len] # error message
                output.append((f"({snippet}, {error_type})", s))
                # Critical error, stop everything
                return output,  modified_line[:s] + " " * (e - s) + modified_line[e:], True
            elif error_type == "Unopened comment":
                snippet = line[max(s - context_len, 0) : s + 2]
                output.append((f"({snippet}, {error_type})", s))
            else: # Invalid number or input
                output.append((f"({t}, {error_type})", s))

            modified_line = modified_line[:s] + " " * (e - s) + modified_line[e:]
        return output, modified_line, False
    
    """Finds invalid tokens in a line and process them."""
    def process_line(line):
        errors = []
        updated_line = line
        should_abort = False

        patterns = [
            (UNCLOSED_COMMENT, "Unclosed comment"),
            (UNOPENED_COMMENT, "Unopened comment"),
            (INVALID_INPUT, "Invalid input"),
            (INVALID_NUM, "Invalid number")
        ]
        for pattern, error_type in patterns:
            matches = list(pattern.finditer(updated_line)) # Find invalid tokens matching the pattern 
            if matches:
                found_errors, updated_line, abort = process_invalid_tokens(updated_line, matches, error_type)
                errors.extend(found_errors)
                # if there are any unclosed comment, don't look for other errors. 
                if abort:
                    should_abort = True
                    break

        errors.sort(key=lambda x: x[1]) # Sort errors by their position in the line
        return errors, updated_line, should_abort

    for line in lines:
        errors, cleaned_line, abort = process_line(line)
        all_errors.append(" ".join([error_msg for error_msg, _ in errors]))
        cleaned_lines.append(cleaned_line)
        if abort: # if there is an unclosed comment, stop processing the rest of the code
            break

    cleaned_code = '\n'.join(cleaned_lines) + ' \n'
    return all_errors, cleaned_code


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
                    yield f"(SYMBOL, {t + lookahead})", line_number
                    t = ""
                else:
                    pos -= 1
                    yield f"(SYMBOL, {t})", line_number
                    t = ""
            else :
                yield f"(SYMBOL, {t})", line_number
                t = ""
        elif KEYWORD.match(t):
            lookahead = getchar()
            pos -= 1
            if not re.match(r'[a-zA-Z0-9]',lookahead): 
                yield f"(KEYWORD, {t})", line_number
                t = ""
        elif ID.match(t):
            lookahead = getchar()
            pos -= 1
            if not re.match(r'[A-Za-z0-9]',lookahead):
                yield f"(ID, {t})", line_number
                t = ""
        elif NUM.match(t):
            lookahead = getchar()
            pos -= 1
            if not re.match(r'[0-9]',lookahead):
                yield f"(NUM, {t})", line_number
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


if __name__ == "__main__":
    code = getfile("input.txt")
    code = preprocess(code)

    errors, correct_code = process_invalid(code)
    tokens = [""]
    symbols = set(KEYWORDS) # Initialize the symbol table with keywords
    line_number = 1
    getToken = getNextToken(correct_code)
    while True:
        token ,token_line_number = next(getToken) # Get the next token and line number
        if token == "FIN":
            break
        if line_number != token_line_number:
            while line_number != token_line_number-1: # Add empty lines for the missing lines
                tokens.append('')
                line_number+=1
            tokens.append(token + " ")
            line_number += 1
        else:
            tokens[line_number - 1] += token + " "
        if token.startswith("(ID, "): # Add identifiers to the symbol table
            symbols.add(token[5:-1])


    writefile("lexical_errors.txt", errors, "There is no lexical error.")
    writefile("tokens.txt", tokens, "There is no token")
    writefile("symbol_table.txt",symbols,"There is no symbol")
