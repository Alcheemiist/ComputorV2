
class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.type in ('NUMBER', 'VARIABLE'):
            return f"{self.type}({self.value})"
        elif self.type == 'OPERATOR':
            return f"({self.left} {self.value} {self.right})"
        elif self.type == 'ASSIGNMENT':
            return f"ASSIGN({self.left} = {self.right})"
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
    
    def parse_matrix():
        if not tokens:
            raise ValueError("Unexpected end of input")
        rows = []
        print(" | Matrix Tokens : ", tokens)
        while tokens :
            tokens.pop(0)
            row = []
            while tokens and tokens[0][0] != 'SEMICOLON':
                if tokens and tokens[0][0] == 'COMMA':
                    tokens.pop(0)
                row.append(parse_expression())
            if tokens and tokens[0][0] == 'SEMICOLON':
                tokens.pop(0)

            rows.append(row)

            if not tokens or tokens.pop(0)[0] != 'RBRACKET':
                raise ValueError("Missing closing bracket")
                
        print(" | Rows : ", rows)
        return ASTNode('MATRIX', rows)

    def parse_primary():
        if not tokens:
            raise ValueError("Unexpected end of input")
        token = tokens.pop(0)
        if token[0] == 'NUMBER':
            return ASTNode('NUMBER', float(token[1]))
        elif token[0] == 'COMPLEX':
            return ASTNode('COMPLEX', token[1])  # Directly create a complex node
        elif token[0] == 'VARIABLE':
            return ASTNode('VARIABLE', token[1])
        elif token[0] == 'LPAREN':  # Handle parentheses
            expr = parse_expression()  # Parse the inner expression
            if not tokens or tokens.pop(0)[0] != 'RPAREN':  # Expect a closing ')'
                raise ValueError("Missing closing parenthesis")
            return expr
        elif token[0] == 'LBRACKET':
            expr = parse_matrix()
            print(" | Matrix : ", expr)
            print(" | Tokens : ", tokens)

            if not tokens or tokens.pop(0)[0] != 'RBRACKET':
                raise ValueError("Missing closing bracket")
            return expr
        else:
            raise ValueError(f"Unexpected token: {token}")

    ast = parse_expression()
    return ast

