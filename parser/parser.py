from lexer import print_color, COLORS, lexer

class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.type in ('NUMBER', 'VARIABLE', 'IMAGINARY'):
            return f"{self.type}({self.value})"
        elif self.type == 'OPERATOR':
            return f"({self.left} {self.value} {self.right})"
        elif self.type == 'UNARY':
            return f"({self.value}{self.left})"
        elif self.type == 'ASSIGNMENT':
            return f"ASSIGN({self.left} = {self.right})"
        elif self.type == 'FUNCTION_CALL':
            args = ', '.join(str(arg) for arg in self.left)
            return f"CALL({self.value}({args}))"
        elif self.type == 'MATRIX':
            rows = '; '.join(' '.join(str(elem) for elem in row) for row in self.value)
            return f"MATRIX([{rows}])"
        else:
            return f"{self.type}({self.value})"
    
    def to_dict(self):
        result = {'type': self.type}
        if self.value is not None:
            result['value'] = self.value
        if self.left:
            result['left'] = self.left.to_dict() if isinstance(self.left, ASTNode) else [node.to_dict() for node in self.left]
        if self.right:
            result['right'] = self.right.to_dict() if isinstance(self.right, ASTNode) else [node.to_dict() for node in self.right]
        return result

def parser(tokens):
    print_color("WARNING", "Parser: " + COLORS["ENDC"] + str(tokens))
        
    def parse_expression():
        return parse_assignment()

    def parse_assignment():
        expr = parse_addition()
        if tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] == '=':
            tokens.pop(0)  # Consume '='
            right = parse_expression()
            return ASTNode('ASSIGNMENT', left=expr, right=right)
        return expr

    def parse_addition():
        expr = parse_multiplication()
        while tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] in ('+', '-'):
            op = tokens.pop(0)[1]
            right = parse_multiplication()
            expr = ASTNode('OPERATOR', op, expr, right)
        return expr

    def parse_multiplication():
        expr = parse_exponentiation()
        while tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] in ('*', '/', '%'):
            op = tokens.pop(0)[1]
            right = parse_exponentiation()
            expr = ASTNode('OPERATOR', op, expr, right)
        return expr

    def parse_exponentiation():
        expr = parse_unary()
        if tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] == '^':
            tokens.pop(0)  # Consume '^'
            right = parse_exponentiation()
            return ASTNode('OPERATOR', '^', expr, right)
        return expr

    def parse_unary():
        if tokens and tokens[0][0] == 'OPERATOR' and tokens[0][1] in ('+', '-'):
            op = tokens.pop(0)[1]
            expr = parse_unary()
            return ASTNode('UNARY', op, expr)
        return parse_primary()

    def parse_primary():
        if not tokens:
            raise ValueError("Unexpected end of input")
        
        token = tokens.pop(0)
        if token[0] == 'NUMBER':
            return ASTNode('NUMBER', float(token[1]))
        elif token[0] == 'VARIABLE':
            if tokens and tokens[0][0] == 'LPAREN':
                # Function call
                tokens.pop(0)  # Consume '('
                args = []
                if tokens[0][0] != 'RPAREN':
                    args.append(parse_expression())
                    while tokens[0][0] == 'COMMA':
                        tokens.pop(0)  # Consume ','
                        args.append(parse_expression())
                if tokens.pop(0)[0] != 'RPAREN':
                    raise ValueError("Expected ')'")
                return ASTNode('FUNCTION_CALL', token[1], args)
            return ASTNode('VARIABLE', token[1])
        elif token[0] == 'LPAREN':
            expr = parse_expression()
            if tokens.pop(0)[0] != 'RPAREN':
                raise ValueError("Expected ')'")
            return expr
        elif token[0] == 'LBRACKET':
            # Matrix
            matrix = []
            row = []
            while tokens[0][0] != 'RBRACKET':
                if tokens[0][0] == 'SEMICOLON':
                    matrix.append(row)
                    row = []
                    tokens.pop(0)
                else:
                    row.append(parse_expression())
                    if tokens[0][0] == 'COMMA':
                        tokens.pop(0)
            matrix.append(row)
            tokens.pop(0)  # Consume ']'
            return ASTNode('MATRIX', matrix)
        elif token[0] == 'IMAGINARY':
            return ASTNode('IMAGINARY', 1)
        else:
            raise ValueError(f"Unexpected token: {token}")

        ast = parse_expression()
        if tokens:
            raise ValueError(f"Unexpected tokens: {tokens}")
        
        print_color("SUCCESS", "AST: " + str(ast))
        return ast

    return parse_expression()

# Example usage:
if __name__ == "__main__":
    test_input = "2 + 1 "
    tokens = lexer(test_input)
    ast = parser(tokens)
    print(ast.to_dict())