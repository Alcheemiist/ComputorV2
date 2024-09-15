from math import pow

def evaluator(ast, context, DEBUG=False):
    
    def handle_complex(node):
        # Find node in ast to check for neighbour real number 
        print(" | Node : ", node)
        # process operation on imaginary number with i, and real number separately
        #  ((NUMBER(10) * (NUMBER(13.0) - COMPLEX(6i) + NUMBER(2.0)) - COMPLEX(4i)) 
   
    def matrix_multiply(A, B):
        rows_A = len(A)
        cols_A = len(A[0])
        rows_B = len(B)
        cols_B = len(B[0])
        
        if cols_A != rows_B:
            raise ValueError("Cannot multiply: number of columns in A must equal number of rows in B.")

        C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):  # or rows_B since cols_A == rows_B
                    C[i][j] += A[i][k] * B[k][j]
        
        return C

    def process_matrix(left, right, operator):
        # Check if the left and right operands are numbers
        if isinstance(right, int) and isinstance(left,list):
            if operator == '+':
                for i in range(len(left)):
                    for j in range(len(left[i])):
                        left[i][j] = left[i][j] + right
                return left
            elif operator == '-':
                for i in range(len(left)):
                    for j in range(len(left[i])):
                        left[i][j] = left[i][j] - right
                return left
            elif operator == '*':
                for i in range(len(left)):
                    for j in range(len(left[i])):
                        left[i][j] = left[i][j] * right
                return left
            elif operator == '/':
                for i in range(len(left)):
                    for j in range(len(left[i])):
                        left[i][j] = left[i][j] / right
                return left
            elif operator == '%':
                for i in range(len(left)):
                    for j in range(len(left[i])):
                        left[i][j] = left[i][j] % right
                return left
                    
        elif isinstance(left, int) and isinstance(right,list):
            if operator == '+':
                for i in range(len(right)):
                    for j in range(len(right[i])):
                        right[i][j] = right[i][j] + left
                return right
            elif operator == '-':
                for i in range(len(right)):
                    for j in range(len(right[i])):
                        right[i][j] = right[i][j] - left
                return right
            elif operator == '*':
                for i in range(len(right)):
                    for j in range(len(right[i])):
                        right[i][j] = right[i][j] * left
                return right
            elif operator == '/':
                for i in range(len(right)):
                    for j in range(len(right[i])):
                        right[i][j] = right[i][j] / left
                return right
            elif operator == '%':
                for i in range(len(right)):
                    for j in range(len(right[i])):
                        right[i][j] = right[i][j] % left
                return right
            
        elif isinstance(left, list) and isinstance(right, list):

            if operator == '+':
                return [[left[i][j] + right[i][j] for j in range(len(left[i]))] for i in range(len(left))]
            elif operator == '-':
                return [[left[i][j] - right[i][j] for j in range(len(left[i]))] for i in range(len(left))]
            elif operator == '*':
                return matrix_multiply(left, right)
            elif operator == '/':
                return [[left[i][j] / right[i][j] for j in range(len(left[i]))] for i in range(len(left))]
            elif operator == '%':
                return [[left[i][j] % right[i][j] for j in range(len(left[i]))] for i in range(len(left))]
         
            else:
                raise ValueError(f"Unknown matrix operator: {operator}")


        else:
            raise ValueError(f"Unknown matrix operator: {operator}")

    def process_function(left, right, operator):
        if operator == '+':
            return left.value + right.value
        elif operator == '-':
            return left.value - right.value
        elif operator == '*':
            return left.value * right.value
        elif operator == '/':
            return left.value / right.value
        elif operator == '%':
            return left.value % right.value
        else:
            raise ValueError(f"Unknown function operator: { operator }")


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
            elif isinstance(left, list) or isinstance(right, list):
                return process_matrix(left, right, node.value)               
            elif left.type == 'FUNCTION' or right.type == 'FUNCTION':
                if left.type == 'FUNCTION':
                    return process_function(left, right, node.value)
                
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
        elif node.type == 'MATRIX':
            if not node.value:
                return []
            return [[evaluate_node(cell) for cell in row] for row in node.value]
        elif node.type == 'FUNCTION':
            context[node.function] = node.value
            return  node.value
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    
    
    
    DEBUG and print(" | Evaluator input : ", ast)
    result = evaluate_node(ast)
    return context, result
