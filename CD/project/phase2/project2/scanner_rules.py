import re

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