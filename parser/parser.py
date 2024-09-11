
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
        while tokens and tokens[0][0] in ('MUL', 'DIV'):
            op = tokens.pop(0)[1]
            right = parse_exponentiation()
            expr = ASTNode('OPERATOR', op, expr, right)
        return expr

    def parse_exponentiation():
        expr = parse_primary()
        if tokens and tokens[0][0] == 'POW':
            tokens.pop(0)  # Consume '^'
            right = parse_exponentiation()
            return ASTNode('OPERATOR', '^', expr, right)
        return expr

    def parse_primary():
        if not tokens:
            raise ValueError("Unexpected end of input")
        
        token = tokens.pop(0)
        if token[0] == 'NUMBER':
            return ASTNode('NUMBER', float(token[1]))
        elif token[0] == 'VARIABLE':
            return ASTNode('VARIABLE', token[1])
        else:
            raise ValueError(f"Unexpected token: {token}")

    ast = parse_expression()
    return ast

# Test the parser
# tokens = [('VARIABLE', 'var2'), ('EQUAL', '='), ('NUMBER', '2'), ('ADD', '+'), ('NUMBER', '1'), ('MUL', '*'), ('NUMBER', '3'), ('SUB', '-'), ('NUMBER', '4'), ('DIV', '/'), ('NUMBER', '2'), ('POW', '^'), ('NUMBER', '2')]
# test_input = "1 + 1 - x * 3 / 2 ^ 2"
# tokens = lexer(test_input)
# ast = parser(tokens)
# print(ast)
