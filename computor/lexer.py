import re

COLORS = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m"
}

token_patterns = [
    ('COMPLEX', r'\d+(\.\d*)?[ij]'),
    ('ERROR_DOUBLE_OPERATOR', r'[+\-*/%^]{2,}'),
    ('ERROR_INVALID_NUMBER', r'\d+[a-zA-Z]+\d*'),
    ('ERROR_INVALID_OPERATOR', r'[^+\-*/%^=(),\[\];?\s\d\w]+'),
    ('NUMBER', r'\b\d+(\.\d*)?\b'),
    ('ERROR', r'\d+[a-zA-Z0-9]+'),
    ('VARIABLE', r'[a-zA-Z][a-zA-Z0-9]*=?'),
    ('ADD', r'\+'),
    ('SUB', r'\-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('MOD', r'%'),
    ('POW', r'\^'),
    ('EQUAL', r'='),
    ('WHITESPACE', r'\s+'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('QUESTION', r'\?'),
    ('IMAGINARY', r'\d*i'),
    ('FUNCTION', r'[a-zA-Z][a-zA-Z0-9]*\(\)'),
    ('MATRIX', r'\[\[(\d+(\.\d*)?)(,\s*\d+(\.\d*)?)*\](;\s*\[\d+(\.\d*)?(,\s*\d+(\.\d*)?)*\])*\]')
]

def test_color():
    print_color("OKGREEN", "Hello, World!")
    print_color("WARNING", "Hello, World!")
    print_color("FAIL", "Hello, World!")
    print_color("HEADER", "Hello, World!")
    print_color("OKBLUE", "Hello, World!")
    print_color("OKCYAN", "Hello, World!")
    print_color("BOLD", "Hello, World!")
    print_color("UNDERLINE", "Hello, World!")
    print_color("ENDC", "Hello, World!")

def print_color(color, text):
    print(COLORS[color] + text + COLORS["ENDC"])

# ----------------- Lexer -----------------
def lexer(input_string, DEBUG=False):
    input_string = input_string.strip()

    DEBUG and print_color("WARNING", "\n | Input Lexer: " + input_string)

    if not input_string:
        DEBUG and print_color("WARNING" ," | Lexer: Empty input")

    # Compile regex pattern
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_patterns) 
    token_re = re.compile(token_regex)
    
    # Tokenize the input string
    tokens = []
    pos = 0
            
    while pos < len(input_string):
        try:
            match = token_re.match(input_string, pos)
            if not match:
                print_color("WARNING"," | Lexer: Unexpected character found: " + input_string[pos] + "\n")
                return []
        except ValueError as e:
            print_color("WARNING", f"Error: {e}\n")
            not DEBUG and exit(1)
            return []
            
        token_type = match.lastgroup
        token_value = match.group()
        
        if token_type != 'WHITESPACE':
            tokens.append((token_type, token_value))
        pos = match.end()
    
    # Check for syntax errors
    for i, (token_type, token_value) in enumerate(tokens):
        if token_type == 'NUMBER':
            # Check if the number is followed by an invalid character
            if i + 1 < len(tokens):
                next_token_type, next_token_value = tokens[i + 1]
                if next_token_type == 'VARIABLE' and next_token_value[0].isdigit():
                    raise ValueError(f"Invalid syntax: Number '{token_value}' is followed by an invalid identifier '{next_token_value}'")
        elif token_type == 'VARIABLE':
            # Check if the variable name starts with a digit
            if token_value[0].isdigit():
                raise ValueError(f"Invalid variable name: '{token_value}'. Variable names cannot start with a digit.")
        elif token_type == 'LPAREN':
            print("LPAREN", token_value)
            found_flag = False
            for j in range(i, len(tokens)):
                if tokens[i + j - 1][0] == 'RPAREN':
                    print("RPAREN", tokens[i][1])
                    found_flag = True
                    break
            if not found_flag:
                print_color("WARNING", f"Invalid syntax: Missing closing parenthesis for '{token_value}'")
                return None
            

        elif token_type == 'RPAREN':
            print("RPAREN", token_value)
    
    DEBUG and print_color("WARNING", " | Tokens: " + COLORS["UNDERLINE"]+ str(tokens))
    return tokens
