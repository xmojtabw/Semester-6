import re

# Predefined keywords for Ciut language in the required order
KEYWORDS = ["break", "else", "if", "int", "repeat", "return", "until", "void"]

# Symbol table to store keywords and identifiers
symbol_table = {}
symbol_index = 1  # Global variable for symbol table indexing

# Global variables for scanning
current_line = 1
char_pos = 0
input_content = ""

# Regular expressions for token patterns
ID_PATTERN = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
NUM_PATTERN = re.compile(r'[0-9]+')
SYMBOL_PATTERN = re.compile(r'[+\-*/=<>!;(){}]|==|<=|>=|!=')
WHITESPACE_PATTERN = re.compile(r'\s+')
COMMENT_START = re.compile(r'/\*')
COMMENT_END = re.compile(r'\*/')
SINGLE_COMMENT = re.compile(r'//')

def add_to_symbol_table(lexeme):
    global symbol_index
    if lexeme not in symbol_table and lexeme not in KEYWORDS:
        symbol_table[lexeme] = symbol_index
        symbol_index += 1

def get_next_token():
    global current_line, char_pos
    token_type = None
    lexeme = ""
    errors = []

    while char_pos < len(input_content):
        remaining_input = input_content[char_pos:]

        # Handle whitespace
        whitespace_match = WHITESPACE_PATTERN.match(remaining_input)
        if whitespace_match:
            whitespace = whitespace_match.group(0)
            char_pos += len(whitespace)
            current_line += whitespace.count('\n')
            continue

        # Handle single-line comments
        if SINGLE_COMMENT.match(remaining_input):
            char_pos += 2  # Skip '//'
            line_end = remaining_input.find('\n')
            if line_end == -1:
                char_pos = len(input_content)
            else:
                char_pos += line_end + 1
                current_line += 1
            continue

        # Handle multi-line comments
        if COMMENT_START.match(remaining_input):
            char_pos += 2  # Skip '/*'
            comment_start_line = current_line
            comment_start = char_pos - 2
            end_match = COMMENT_END.search(input_content[char_pos:])
            if end_match:
                char_pos += end_match.end()
                current_line += input_content[comment_start:char_pos].count('\n')
                continue
            else:
                # Unclosed comment
                discarded = input_content[comment_start:comment_start + 7] + "..." if len(input_content) - comment_start > 7 else input_content[comment_start:]
                errors.append((discarded, "Unclosed comment", comment_start_line))
                char_pos = len(input_content)
                return None, None, errors

        # Handle unmatched '*/'
        if COMMENT_END.match(remaining_input):
            char_pos += 2  # Skip '*/'
            errors.append(("*/", "Unmatched comment", current_line))
            return None, None, errors

        # Handle identifiers and keywords
        id_match = ID_PATTERN.match(remaining_input)
        if id_match:
            lexeme = id_match.group(0)
            char_pos += len(lexeme)
            # Check if followed by '!' (e.g., 'cd!e')
            if char_pos < len(input_content) and input_content[char_pos] == '!':
                invalid_lexeme = lexeme + '!'
                char_pos += 1  # Skip '!'
                errors.append((invalid_lexeme, "Invalid input", current_line))
                return None, None, errors
            if lexeme in KEYWORDS:
                token_type = "KEYWORD"
            else:
                token_type = "ID"
                add_to_symbol_table(lexeme)
            return token_type, lexeme, errors

        # Handle numbers
        num_match = NUM_PATTERN.match(remaining_input)
        if num_match:
            lexeme = num_match.group(0)
            char_pos += len(lexeme)
            # Check if followed by invalid characters (e.g., '3d')
            next_pos = char_pos
            if next_pos < len(input_content) and input_content[next_pos].isalpha():
                invalid_lexeme = lexeme
                while next_pos < len(input_content) and (input_content[next_pos].isalnum() or input_content[next_pos] == '_'):
                    invalid_lexeme += input_content[next_pos]
                    next_pos += 1
                char_pos = next_pos
                errors.append((invalid_lexeme, "Invalid number", current_line))
                return None, None, errors
            token_type = "NUM"
            return token_type, lexeme, errors

        # Handle symbols
        symbol_match = SYMBOL_PATTERN.match(remaining_input)
        if symbol_match:
            lexeme = symbol_match.group(0)
            char_pos += len(lexeme)
            token_type = "SYMBOL"
            return token_type, lexeme, errors

        # Handle invalid input (e.g., '@')
        invalid_char = remaining_input[0]
        char_pos += 1
        if invalid_char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
            errors.append((invalid_char, "Invalid input", current_line))
            return None, None, errors
        # If it's a letter or digit not matched earlier, skip it (Panic Mode)
        continue

    return None, None, errors




def main():
    global input_content, char_pos, current_line, symbol_index
    # Read input file
    with open("input.txt", "r", encoding="utf-8") as f:
        input_content = f.read()

    # Replace comments with space
    COMMENT = r"/\*[\s\S]*?\*/"
    input_content = re.sub(COMMENT, " ", input_content)
    print(input_content)
    
    
    # Initialize symbol table with keywords in specified order
    for keyword in KEYWORDS:
        symbol_table[keyword] = symbol_index
        symbol_index += 1

    # Process tokens
    tokens_by_line = {}
    lexical_errors = []
    char_pos = 0
    current_line = 1

    while char_pos < len(input_content):
        token_type, lexeme, errors = get_next_token()
        if errors:
            lexical_errors.extend(errors)
            continue
        if token_type:
            if current_line not in tokens_by_line:
                tokens_by_line[current_line] = []
            tokens_by_line[current_line].append((token_type, lexeme))

    # Write tokens to file
    with open("tokens.txt", "w", encoding="utf-8") as f:
        for line_num in sorted(tokens_by_line.keys()):
            tokens = " ".join(f"({t[0]}, {t[1]})" for t in tokens_by_line[line_num])
            f.write(f"{line_num}.\t{tokens}\n")

    # Write symbol table to file
    with open("symbol_table.txt", "w", encoding="utf-8") as f:
        for lexeme, index in sorted(symbol_table.items(), key=lambda x: x[1]):
            f.write(f"{index}.\t{lexeme}\n")

    # Write lexical errors to file
    with open("lexical_errors.txt", "w", encoding="utf-8") as f:
        if not lexical_errors:
            f.write("No lexical errors.\n")
        else:
            for discarded, msg, line in sorted(lexical_errors, key=lambda x: x[2]):
                f.write(f"{line}.\t({discarded}, {msg})\n")

if __name__ == "__main__":
    main()