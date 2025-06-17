# scanner.py
from collections import defaultdict
from typing import Optional, Tuple


class Scanner:
    def __init__(self):
        self.FIXED_KEYWORDS = ["break", "else", "if",
                               "int", "repeat", "return", "until", "void"]
        self.KEYWORDS_SET = set(self.FIXED_KEYWORDS)
        self.MULTI_SYMBOLS = ["==", "<=", ">=", "!=", "&&", "||"]
        self.SINGLE_SYMBOLS = {
            ';', ':', '(', ')', '{', '}', '[', ']', '+', '-', '*', '/', '=', '<', '>', '!', ','}
        self.NOT_VALID_ALONE = {'&', '|'}
        self.INVALID_SET = {'@', '#', '$', '%', '^', '~'}
        self.WHITESPACE = {' ', '\t', '\r', '\v', '\f'}

        self.input_text = ""
        self.current_index = 0
        self.line_number = 1

        self.tokens_by_line = {}
        self.lexical_errors = []
        self.symbol_table_order = []

    def set_input(self, text: str):
        """Set the input text and reset state."""
        self.input_text = text
        self.current_index = 0
        self.line_number = 1
        self.tokens_by_line.clear()
        self.lexical_errors.clear()
        self.symbol_table_order.clear()

    def get_char(self) -> Optional[str]:
        """Get next character and update line number."""
        if self.current_index >= len(self.input_text):
            return None
        ch = self.input_text[self.current_index]
        self.current_index += 1
        if ch == "\n":
            self.line_number += 1
        return ch

    def peek_char(self, offset: int = 0) -> Optional[str]:
        """Peek at character without consuming it."""
        pos = self.current_index + offset
        if pos >= len(self.input_text):
            return None
        return self.input_text[pos]

    def add_token(self, tok_type: str, lexeme: str, tok_line: int):
        """Add token to output structures."""
        if tok_line not in self.tokens_by_line:
            self.tokens_by_line[tok_line] = []
        self.tokens_by_line[tok_line].append((tok_type, lexeme))
        if tok_type == "ID" and lexeme not in self.symbol_table_order:
            self.symbol_table_order.append(lexeme)

    def log_error(self, tok_line: int, error_str: str, message: str):
        """Log a lexical error."""
        self.lexical_errors.append((tok_line, error_str, message))

    def skip_whitespace_and_comments(self):
        """Skip whitespace and comments."""
        while True:
            ch = self.peek_char()
            if ch is None:
                return
            if ch in self.WHITESPACE:
                self.get_char()
                continue
            if ch == "\n":
                self.get_char()
                continue
            if ch == "/" and self.peek_char(1) == "*":
                self.get_char()  # consume '/'
                self.get_char()  # consume '*'
                comment_start_line = self.line_number
                comment_content = ""
                while True:
                    c = self.get_char()
                    if c is None:
                        snippet = comment_content[:7] + \
                            ("..." if len(comment_content) > 7 else "")
                        self.log_error(comment_start_line,
                                       "/* " + snippet, "Unclosed comment")
                        return
                    if c == "*" and self.peek_char() == "/":
                        self.get_char()  # consume '/'
                        break
                    else:
                        comment_content += c
                continue
            if ch == "*" and self.peek_char(1) == "/":
                self.get_char()  # consume '*'
                self.get_char()  # consume '/'
                self.log_error(self.line_number, "*/", "Unmatched comment")
                continue
            break

    def get_invalid_symbol_sequence(self, start_line: int, first_char: str) -> str:
        """Get invalid symbol sequence."""
        seq = first_char
        self.get_char()  # consume first_char
        while True:
            nxt = self.peek_char()
            if nxt is None or nxt.isspace():
                break
            if nxt in self.INVALID_SET or nxt in self.NOT_VALID_ALONE:
                seq += self.get_char()
            else:
                break
        return seq

    def get_next_token(self) -> Optional[Tuple[str, str, int]]:
        """Get the next token from input."""
        self.skip_whitespace_and_comments()
        start_line = self.line_number
        ch = self.peek_char()
        if ch is None:
            return None

        # Handle invalid '//' comments
        if ch == "/" and self.peek_char(1) == "/":
            error_token1 = self.get_char()  # consume first '/'
            self.log_error(start_line, error_token1, "Invalid input")
            error_token2 = self.get_char()  # consume second '/'
            self.log_error(start_line, error_token2, "Invalid input")
            return self.get_next_token()

        # Process numbers
        if ch.isdigit():
            num_str = ""
            while self.peek_char() is not None and self.peek_char().isdigit():
                num_str += self.get_char()
            if self.peek_char() is not None and self.peek_char().isalpha():
                error_token = num_str + self.get_char()
                self.log_error(start_line, error_token, "Invalid number")
                return self.get_next_token()
            return ("NUM", num_str, start_line)

        # Process identifiers
        if ch.isalpha():
            id_str = ""
            while self.peek_char() is not None and self.peek_char().isalnum():
                id_str += self.get_char()
            nxt = self.peek_char()
            if nxt is not None and (not nxt.isspace()):
                allowed_after_id = {
                    '(', ')', '{', '}', '[', ']', ';', ',', ':', '+', '-', '*', '/', '=', '<', '>', '&', '|'}
                if nxt not in allowed_after_id:
                    error_char = self.get_char()
                    self.log_error(start_line, id_str +
                                   error_char, "Invalid input")
                    return self.get_next_token()
            if id_str in self.KEYWORDS_SET:
                return ("KEYWORD", id_str, start_line)
            else:
                return ("ID", id_str, start_line)

        # Process multi-character symbols
        for sym in self.MULTI_SYMBOLS:
            if self.input_text[self.current_index:self.current_index+len(sym)] == sym:
                for _ in range(len(sym)):
                    self.get_char()
                return ("SYMBOL", sym, start_line)

        # Process single-character symbols
        if ch in self.SINGLE_SYMBOLS or ch in self.NOT_VALID_ALONE:
            if ch == "!" and self.peek_char(1) == "=":
                self.get_char()  # Consume '!'
                self.get_char()  # Consume '='
                return ("SYMBOL", "!=", start_line)

            if ch == "!":
                if self.tokens_by_line.get(start_line, []) and self.tokens_by_line[start_line][-1] == ("SYMBOL", ";"):
                    error_token = self.get_char()
                    self.log_error(start_line, error_token, "Invalid input")
                    return self.get_next_token()

            if ch == ";":
                token = self.get_char()
                return ("SYMBOL", token, start_line)

            nxt = self.peek_char(1)
            if nxt is not None and (not nxt.isspace()) and (nxt in self.INVALID_SET or nxt in self.NOT_VALID_ALONE):
                invalid_seq = self.get_invalid_symbol_sequence(start_line, ch)
                self.log_error(start_line, invalid_seq, "Invalid input")
                return self.get_next_token()
            token = self.get_char()
            return ("SYMBOL", token, start_line)

        # Process invalid characters
        if ch in self.INVALID_SET:
            error_token = self.get_char()
            self.log_error(start_line, error_token, "Invalid input")
            return self.get_next_token()

        # Fallback for unrecognized characters
        error_token = self.get_char()
        self.log_error(start_line, error_token, "Invalid input")
        return self.get_next_token()

    def process_input(self):
        """Process all input tokens."""
        token = self.get_next_token()
        while token is not None:
            tok_type, lexeme, tok_line = token
            self.add_token(tok_type, lexeme, tok_line)
            token = self.get_next_token()

    def write_output_files(self):
        """Write all output files."""
        self._write_tokens_file()
        self._write_lexical_errors_file()
        self._write_symbol_table_file()

    def _write_tokens_file(self, filename="tokens.txt"):
        """Write tokens to file."""
        with open(filename, "w") as f:
            for lnum in sorted(self.tokens_by_line.keys()):
                token_line = self.tokens_by_line[lnum]
                token_strs = " ".join(f"({t}, {lex})" for t, lex in token_line)
                f.write(f"{lnum}.\t{token_strs}\n")

    def _write_lexical_errors_file(self, filename="lexical_errors.txt"):
        """Write lexical errors to file."""
        errors_by_line = defaultdict(list)
        for ln, err_token, message in self.lexical_errors:
            errors_by_line[ln].append(f"({err_token}, {message})")
        with open(filename, "w") as f:
            if not errors_by_line:
                f.write("There is no lexical error.\n")
            else:
                for ln in sorted(errors_by_line.keys()):
                    error_line = " ".join(errors_by_line[ln])
                    f.write(f"{ln}.\t{error_line}\n")

    def _write_symbol_table_file(self, filename="symbol_table.txt"):
        """Write symbol table to file."""
        with open(filename, "w") as f:
            index = 1
            for kw in self.FIXED_KEYWORDS:
                f.write(f"{index}.\t{kw}\n")
                index += 1
            for ident in self.symbol_table_order:
                f.write(f"{index}.\t{ident}\n")
                index += 1
