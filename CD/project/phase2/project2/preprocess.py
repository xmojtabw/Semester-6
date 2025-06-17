import re 
from scanner_rules import *


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
