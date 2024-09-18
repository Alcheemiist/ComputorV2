
class ASTNode:
    def __init__(self, type, value=None, left=None, right=None, matrix=None, function=None, func_exp=None, variable=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
        self.function = None
        self.func_exp = None
        self.variable = None

        if self.type == 'FUNCTION':
            self.function = function
            self.value = value
            self.func_exp = func_exp
            self.variable = None
            self.type = 'FUNCTION'
        elif self.type == 'FUNCTION_OPERATION':
            self.function = function
            self.value = value
            self.func_exp = func_exp
            self.variable = variable
            self.type = 'FUNCTION_OPERATION'
        elif matrix:
            self.value = matrix
            self.type = 'MATRIX'

    def __str__(self):
        if self.type in ('NUMBER', 'VARIABLE'):
            return f"{self.type}({self.value})"
        elif self.type == 'COMPLEX':
            return f"COMPLEX({self.value})"
        elif self.type == 'OPERATOR':
            return f"({self.left} {self.value} {self.right})"
        elif self.type == 'ASSIGNMENT':
            return f"ASSIGN({self.left} = {self.right})"
        elif self.type == 'MATRIX':
            return f"Matrix({self.value})"
        elif self.type == 'FUNCTION':
            return f"Function({self.function}({self.value})[{self.variable}]->{self.func_exp})"
        elif self.type == 'FUNCTION_OPERATION':
            return f"FUNCTION_OPERATION({self.function}({self.value.value}))"
        else:
            return f"{self.type}({self.value})"

    def __repr__(self):
        return str(self)

def parser(tokens):
    def parse_expression():
        return parse_assignment()

    def parse_assignment():
        left = parse_addition()
        if tokens and tokens[0][0] == 'EQUAL':
            tokens.pop(0)  # Consume '='
            right = parse_expression()
            return ASTNode('ASSIGNMENT', left=left, right=right)
        return left

    def parse_addition():
        expr = parse_multiplication()
        while tokens and tokens[0][0] in ('ADD', 'SUB'):
            op = tokens.pop(0)[1]
            right = parse_multiplication()
            expr = ASTNode('OPERATOR', op, expr, right)
        return expr

    def parse_multiplication():
        expr = parse_exponentiation()
        while tokens and tokens[0][0] in ('MUL', 'DIV', "MOD"):
            op = tokens.pop(0)[1]
            right = parse_exponentiation()
            expr = ASTNode('OPERATOR', op, expr, right)
        return expr

    def parse_exponentiation():
        expr = parse_unary()
        if tokens and tokens[0][0] == 'POW':
            tokens.pop(0)  # Consume '^'
            right = parse_exponentiation()
            return ASTNode('OPERATOR', '^', expr, right)
        return expr
    
    def parse_unary():
        if tokens and tokens[0][0] == 'SUB':
            tokens.pop(0)  # Consume '-'
            right = parse_unary()
            return ASTNode('OPERATOR', '-', ASTNode('NUMBER', 0), right)  # Unary minus as (0 - expr)
        return parse_primary()

    def parse_primary():
        if not tokens:
            raise ValueError("Unexpected end of input")
        token = tokens.pop(0)
        if token[0] == 'NUMBER':

            number = None
            if '.' in token[1]:
                number = float(token[1])
            else:
                number = int(token[1])
            
            return ASTNode('NUMBER', number)
        elif token[0] == 'COMPLEX':
            return ASTNode('COMPLEX', token[1])  # Directly create a complex node
        elif token[0] == 'VARIABLE' and tokens and tokens[0][0] != 'LPAREN':
            return ASTNode('VARIABLE', token[1])
        elif token[0] == 'VARIABLE' and tokens and tokens[0][0] == 'LPAREN':
            expr = parse_function()  # Parse the inner expression
            if "=" not in expr:
                res = handle_function_operation(token[1])
                return ASTNode('FUNCTION_OPERATION', function=token[1], value=res)
            var_expr = expr.split("=")[0].strip().strip("()")
            expr = expr.split("=")[1].strip()
            return ASTNode('FUNCTION', function=token[1], value=expr, func_exp=var_expr)
        elif token[0] == 'LPAREN':
            expr = parse_expression()
            if not tokens or tokens.pop(0)[0] != 'RPAREN':
                raise ValueError("Missing closing parenthesis")
            return expr
        elif token[0] == 'LBRACKET':
            expr = parse_matrix()
            if not tokens or tokens.pop(0)[0] != 'RBRACKET':
                raise ValueError("Missing closing bracket for matrix")
            return expr
        elif token[0] == 'VARIABLE':
            return ASTNode('VARIABLE', token[1])
        elif token[0] == 'FUNCTION':
            return ASTNode('FUNCTION', function=token[1], value=expr, func_exp=parse_expression())
        else:
            raise ValueError(f"Unexpected token: {token}")

    def parse_matrix():
        if not tokens:
            raise ValueError("Unexpected end of input")
        
        rows = []
        size = 0

        while tokens and tokens[0][0] == 'LBRACKET':

            tokens.pop(0)  # Consume '['
            row = []
            while tokens and tokens[0][0] != 'RBRACKET':
                if tokens[0][0] == 'COMMA':
                    tokens.pop(0)  # Consume ','
                row.append(parse_expression())
            
            if tokens[0][0] == 'RBRACKET':
                tokens.pop(0)  # Consume ']'
            if tokens[0][0] == 'SEMICOLON':
                tokens.pop(0)  # Consume ';'
    
            if size == 0:
                size = len(row)
            elif size != len(row):
                raise ValueError("Matrix rows must have the same number of columns")
            rows.append(row)

        
        return ASTNode('MATRIX', matrix=rows)

    def parse_function():
        if not tokens:
            raise ValueError("Unexpected end of input")
        func_str = ""
        for token in tokens:
            func_str += token[1] + " "
        return func_str

    def handle_function_operation(func_name):
        args = []
        if tokens and tokens[0][0] == 'LPAREN':
            tokens.pop(0)  # Consume '('
            while tokens and tokens[0][0] != 'RPAREN':
                if tokens[0][0] == 'COMMA':
                    tokens.pop(0)  # Consume ','
                args.append(parse_expression())
            if not tokens or tokens.pop(0)[0] != 'RPAREN':
                raise ValueError(f"Missing closing parenthesis for function {func_name}")
        return args[0]

    ast = parse_expression()
    return ast

