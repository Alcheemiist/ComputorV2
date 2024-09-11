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

# Define token patterns
token_patterns = [
    ('NUMBER', r'\d+(\.\d*)?'),
    ('VARIABLE', r'[a-zA-Z][a-zA-Z0-9]*=?'),
    # ('OPERATOR', r'[+\-*/^%=]'),
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
    # ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('QUESTION', r'\?'),
    ('IMAGINARY', r'i')
    # ('FUNCTION', r'[a-zA-Z][a-zA-Z0-9]*\('),
    # ('MATRIX', r'\[[^\]]*\]'),
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
    if not input_string:
        print_color("WARNING", "Lexer: Empty input")
    DEBUG and print_color("WARNING", "Lexer input : " + COLORS["ENDC"] + input_string)
    
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
                print_color("FAIL", (("Illegal character: " + input_string[pos])))
                break
        except ValueError as e:
            print_color("FAIL", f"Error: {e}\n")
            not DEBUG and exit(1)
            break
            
        token_type = match.lastgroup
        token_value = match.group()
        
        if token_type != 'WHITESPACE':
            tokens.append((token_type, token_value))
        pos = match.end()
    
    DEBUG and print_color("WARNING", "Tokens: " + COLORS["RESET"] + COLORS["UNDERLINE"]+ str(tokens))
    return tokens

# ----------------- Test main -----------------
if __name__ == "__main__":
    test_input = " a * s*i + 3.5 / 2 * (14- 1) = 0 * [1, 2, 3] + 4i * 13 ?"
    lexer(test_input)