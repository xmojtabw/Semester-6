import re
from math import log10


def getfile() -> str:
    with open("input.txt") as f:
        code = f.read()
    return code


def writefile(name: str, lines, empty_message):
    empty = True
    c = int(log10(len(lines)))
    with open(name, "w") as f:
        for i, line in enumerate(lines, start=1):
            if line:
                prefix = str(i) + "." + " " * (c - int(log10(i)))
                f.write(f"{prefix} {line} \n")
                empty = False
        if empty:
            f.write(empty_message)


INVALID_INPUT = re.compile(
    r"(a-z|A-Z|!|=|&|\||\*|\-|\+|<|>|/|\(|\)|{|}|\[|\]|;|,)*[~^`'\"\.@#\$%\\]|[a-zA-Z0-9]+!(?!=)|!(?!\s*[a-zA-Z0-9(=-])|! (?!\s*[a-zA-Z0-9(-])|/(?!\s*[a-zA-Z0-9\(-])"
)
ID = re.compile(r"[A-Za-z][A-Za-z0-9]*")
NUM = re.compile(r"[0-9]+")
INVALID_NUM = re.compile(r"[0-9]+[A-Za-z@#\$%\\]")
KEYWORD = re.compile(
    r"(int|void|if|else|while|return|repeat|until|break|bool|true|false|void)"
)
SYMBOL = re.compile(r"(!|!=|==|=|&&|\|\||\*|\-|\+|<=|>=|<|>|/|\(|\)|{|}|\[|\]|;|,)")
UNCLOSED_COMMENT = re.compile(r"/\*")
UNOPENED_COMMENT = re.compile(r"\*/")
STUPID_INVALID_INPUT = re.compile(r"")
KEYWORDS = "int bool void true false if else while until repeat break return".split(" ")
# class InputText() :
#     input_pos = 0
#     def __init__(self,file_name:str):
#         with open(file_name,'r') as file:
#             self.input_text = file.read()

#     def getchar(self):
#         try:
#             c = self.input_text[self.input_pos]
#         except IndexError :
#             raise EOFError
#         self.input_pos += 1
#         return  c

#     def retract(self):
#         self.input_pos -= 1


def preprocess(code: str) -> list:
    def replace_with_spaces(match):  # Ensure that \n will not replace
        comment = match.group(0)
        return "".join("\n" if c == "\n" else " " for c in comment)

    # Replace the comments with spaces
    COMMENT = r"/\*[\s\S]*?\*/"
    code = re.sub(COMMENT, replace_with_spaces, code)

    # Replace other whitespace with space
    OTHER_WHITESPACE = r"[\r\t\v\f]"
    code = re.sub(OTHER_WHITESPACE, " ", code)

    return code


def process_invalid(code: str):
    lines = code.split("\n")
    cleaned_lines = []
    all_errors = []

    def process_invalid_tokens(line, tokens, error_type):
        output = []
        modified_line = line
        for token in tokens:
            t = token.group(0)
            s, e = token.start(), token.end()
            context_len = 7

            if error_type == "Unclosed comment":
                e = len(line)
                snippet = line[s : s + context_len]
                output.append((f"({snippet}, {error_type})", s))
                # Critical error, stop everything
                return output,  modified_line[:s] + " " * (e - s) + modified_line[e:], True
            elif error_type == "Unopened comment":
                snippet = line[max(s - context_len, 0) : s + 2]
                output.append((f"({snippet}, {error_type})", s))
            else:
                output.append((f"({t}, {error_type})", s))

            modified_line = modified_line[:s] + " " * (e - s) + modified_line[e:]
        return output, modified_line, False

    def find_invalid(line):
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
            matches = list(pattern.finditer(updated_line))
            if matches:
                found_errors, updated_line, abort = process_invalid_tokens(updated_line, matches, error_type)
                errors.extend(found_errors)
                if abort:
                    should_abort = True
                    break

        errors.sort(key=lambda x: x[1])
        return errors, updated_line, should_abort

    for line in lines:
        errors, cleaned, abort = find_invalid(line)
        all_errors.append(" ".join([msg for msg, _ in errors]))
        cleaned_lines.append(cleaned)
        if abort:
            break

    cleaned_code = '\n'.join(cleaned_lines) + ' \n'
    return all_errors, cleaned_code



def getNextToken(code):
    pos = 0
    line_number = 1

    def getchar():
        nonlocal pos
        if pos == len(code):
            return None
        c = code[pos]
        pos += 1
        return c

    t = ""
    while True:
        if SYMBOL.match(t):
            if t in ("!", "="):
                n = getchar()
                if n == "=":
                    yield f"(SYMBOL, {t + n})", line_number
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
        c = getchar()
        if not c:
            yield "FIN", line_number
            return
        elif c == "\n":
            # t+= ' '
            line_number += 1
        elif c == " " and len(t) == 0:
            pass
        else:
            t += c


if __name__ == "__main__":
    code = getfile()
    code = preprocess(code)

    errors, correct_code = process_invalid(code)
    tokens = [""]
    symbols = KEYWORDS
    line_number = 1
    getToken = getNextToken(correct_code)
    while True:
        token, ln = next(getToken)
        if token == "FIN":
            break
        if line_number != ln:
            while line_number != ln-1:
                tokens.append('')
                line_number+=1
            tokens.append(token + " ")
            line_number += 1
        else:
            tokens[line_number - 1] += token + " "

    writefile("lexical_errors.txt", errors, "There is no lexical error.")
    writefile("tokens.txt", tokens, "There is no token")
