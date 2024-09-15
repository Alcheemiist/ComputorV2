
class ASTNode:
    def __init__(self, type, value=None, left=None, right=None, matrix=None, function=None, func_exp=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

        if function:
            self.function = function
            self.func_exp = func_exp
            self.type = 'FUNCTION'

        if matrix:
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
            return f"Function({self.function}({self.left}))"
        
        else:
            return f"{self.type}({self.value})"

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
            print("-----------EXPR", expr)
            return ASTNode('FUNCTION', function=token[1], func_exp=expr)

        elif token[0] == 'LBRACKET':
            expr = parse_matrix()
            if not tokens or tokens.pop(0)[0] != 'RBRACKET':
                raise ValueError("Missing closing bracket for matrix")
            return expr
        elif token[0] == 'FUNCTION':
            return parse_function()
        else:
            raise ValueError(f"Unexpected token: {token}")

    # advanced parser 

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
        pass



        

    ast = parse_expression()
    return ast

