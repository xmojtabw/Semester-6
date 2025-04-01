import re 

invalid_input = re.compile(r'(?<=[a-zA-Z0-9\)]\s*)/')

invalid_input = re.compile(r'/(?!\s*[a-zA-Z0-9\(-])')