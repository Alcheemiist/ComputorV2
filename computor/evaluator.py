from math import pow

def evaluator(ast, context, DEBUG=False):
    DEBUG and print(" | Evaluator input : ", ast)
    
    def handle_complex(node):
        # Find node in ast to check for neighbour real number 
        print(" | Node : ", node)
        # process operation on imaginary number with i, and real number separately
        #  ((NUMBER(10) * (NUMBER(13.0) - COMPLEX(6i) + NUMBER(2.0)) - COMPLEX(4i)) 
        

                
       
    def evaluate_node(node):
        if node.type == 'NUMBER':
            return node.value
        elif node.type == 'COMPLEX':  # Handling complex numbers
            value = node.value[0].split('j')[0]

            return complex(0, int(value))
        elif node.type == 'VARIABLE':
            if node.value not in context:
                raise ValueError(f"Undefined variable: {node.value}")
            return context[node.value]
        elif node.type == 'OPERATOR':
            left = evaluate_node(node.left)
            right = evaluate_node(node.right)
            
            # Handle complex numbers
            if isinstance(left, str) or isinstance(right, str):
                return handle_complex(node)
            elif node.value == '+':
                return left + right
            elif node.value == '-':
                return left - right
            elif node.value == '*' or node.value == 'MUL':
                return left * right
            elif node.value == '/' or node.value == 'DIV':
                if right == 0:
                    raise ValueError("Division by zero")
                return left / right
            elif node.value == '%':
                if isinstance(left, complex) or isinstance(right, complex):
                    raise ValueError("Modulo operation not supported for complex numbers")
                return left % right
            elif node.value == '^' or node.value == 'POW':
                if isinstance(left, complex) or isinstance(right, complex):
                    return left ** right  # Handle complex exponentiation with **
                return pow(left, right)
            else:
                raise ValueError(f"Unknown operator: {node.value}")
        elif node.type == 'ASSIGNMENT':
            value = evaluate_node(node.right)
            # if left value is a number or operator raise an error
            if node.left.type == 'NUMBER':
                raise ValueError(f"Cannot assign value to a number")
            if node.left.type == 'OPERATOR':
                raise ValueError(f"Cannot assign value to an operator")
            context[node.left.value] = value
            return value
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    result = evaluate_node(ast)
    return context, result
