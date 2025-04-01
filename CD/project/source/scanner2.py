import re 
from math import log10

def getfile()->str:
    with open('input.txt') as f:
        code = f.read()
    return code

def writefile(name:str,lines,empty_message):
    empty = True
    c = int(log10(len(lines)))
    with open(name,'w') as f:
        for i,line in enumerate(lines,start=1):
            if line:
                prefix = str(i)+'.'+' '*(c-int(log10(i)))
                f.write(f'{prefix} {line} \n')
                empty = False
        if empty:
            f.write(empty_message)

INVALID_INPUT = re.compile(r"(a-z|A-Z|!|=|&|\||\*|\-|\+|<|>|/|\(|\)|{|}|\[|\]|;|,)*[~^`'\"\.@#\$%\\]|[a-zA-Z0-9]+!(?!=)|!(?!\s*[a-zA-Z0-9(=-])|! (?!\s*[a-zA-Z0-9(-])|/(?!\s*[a-zA-Z0-9\(-])") 
ID = re.compile(r"[A-Za-z][A-Za-z0-9]*(?![a-zA-Z0-9])]")
NUM = re.compile(r"[0-9]+(?![a-zA-Z0-9])]")
INVALID_NUM = re.compile(r"[0-9]+[A-Za-z@#\$%\\]")
KEYWORD = re.compile(r"(int|void|if|else|while|return|repeat|until|break|bool|true|false|void)(?=[ \(\),])") 
SYMBOL = re.compile(r"(!|!=|==|=|&&|\|\||\*|\-|\+|<=|>=|<|>|/|\(|\)|{|}|\[|\]|;|,)")
UNCLOSED_COMMENT = re.compile(r"/\*")
UNOPENED_COMMENT = re.compile(r"\*/")
STUPID_INVALID_INPUT = re.compile(r"")
KEYWORDS = 'int bool void true false if else while until repeat break return'.split(' ') 
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

def preprocess(code:str) -> list:

    def replace_with_spaces(match): # Ensure that \n will not replace
        comment = match.group(0)
        return "".join("\n" if c == "\n" else " " for c in comment)
    
    # Replace the comments with spaces
    COMMENT = r"/\*[\s\S]*?\*/"
    code = re.sub(COMMENT, replace_with_spaces, code)

    # Replace other whitespace with space 
    OTHER_WHITESPACE = r"[\r\t\v\f]"
    code = re.sub(OTHER_WHITESPACE, " ", code)

    return code



def process_invalid(code:str):
    lines = code.split("\n")

    def process_invalid_tokens(line,tokens):
        output = []
        for token in tokens:
            t = token.group(0)
            s,e = token.start(), token.end()
            m = 7 
            if UNCLOSED_COMMENT.match(t):
                e = len(line) # remove whatever comes after \* 
                output.append((f"({line[s:s+m]}, Unclosed comment)",s))
            elif UNOPENED_COMMENT.match(t):
                output.append((f"({line[max(s-m,0):s+2]}, Unopened comment)",s))
            elif INVALID_INPUT.match(t):
                output.append((f"({t}, Invalid input)",s) )
            elif INVALID_NUM.match(t):
                output.append((f"({t}, Invalid number)",s))
            line = line[:s] + " " * (e-s) + line[e:]
        return output

    def find_invalid(line):
        output = []
        unclosed_comments = list(UNCLOSED_COMMENT.finditer(line))
        output += process_invalid_tokens(line,unclosed_comments)
        unopened_comments =list(UNOPENED_COMMENT.finditer(line))
        output += process_invalid_tokens(line,unopened_comments)
        invalid_inputs = list(INVALID_INPUT.finditer(line))
        output += process_invalid_tokens(line,invalid_inputs)
        invalid_nums = list(INVALID_NUM.finditer(line)) 
        output += process_invalid_tokens(line,invalid_nums)
        output.sort(key = lambda x : x[1])
        return output
    
    errors = []
    for line in lines:
        errors.append(' '.join([x[0] for x in find_invalid(line)]))
    return errors


def getNextToken(code):
    pos = 0
    line_number = 1
    def getchar():
        nonlocal pos
        if pos == len(code):
            return None
        c = code[pos]
        pos += 1
        return  c 
        
    t=""
    while True:
        if SYMBOL.match(t):
            if t in ('!','='):
                n = getchar()
                if n == '=':
                    yield f"(SYMBOL, {t+n})" , line_number
                    t=""
                else :
                    pos -= 1 
            yield f"(SYMBOL, {t})"
        elif KEYWORD.match(t):
            yield f"(KEYWORD, {t})" , line_number
            t=""
        elif ID.match(t):
            yield f"(ID, {t})" ,line_number
            t=""
        elif NUM.match(t):
            yield f"(NUM, {t})" , line_number
            t=""
        c = getchar()
        if not c :
            yield 'FIN' , line_number
            return
        elif c=='\n':
            t+= ' '
            line_number +=1 
        else :
            t+= c



if __name__ == '__main__' :
    code = getfile()
    code = preprocess(code)

    errors = process_invalid(code)
    tokens = []
    symbols = KEYWORDS
    line_number = 0
    getToken = getNextToken(code)
    while True :
        token , ln= next(getToken) 
        if token == 'FIN':
            break
        if line_number != ln :
            tokens.append(token+' ')
            line_number +=1 
        else :
            tokens[line_number]+=tokens+' '
    
    writefile('lexical_errors.txt',errors,'There is no lexical error.')
    writefile('tokens.txt',tokens,'There is no token')






