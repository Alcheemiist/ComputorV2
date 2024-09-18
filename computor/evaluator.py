from math import pow
from lexer import lexer
from parser import parser
from computorv1 import computorv1

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

    def validate_function(node, DEBUG=False):
        if DEBUG:
            print(" | Context : ", context)
            print(f" | Solve function : {node.function}({node.variable}) = {node.func_exp} = {node.value}")
            print(" | Function expression : ", node.func_exp)
            print(" | Function variable : ", node.variable)
            print(" | Function value : ", node.value)

        rhs = node.func_exp.split()
        lhs = node.value.strip().split()

        rexp = ""
        for token in rhs:
            if token in ['+', '-', '*', '/', '%', '^']:
                rexp += token + " "
                continue
            elif node.variable == token:
                if len(rhs) - 1 <= rhs.index(token) + 1 or rhs[ rhs.index(token) + 1 ] != '^':
                    rexp += "1 * X^1 "
                continue
            else:
                for n in token:
                    if  n not in [node.variable,'0', '1', '2', '3', '4', '5', '6', '7','8','9']:
                        raise ValueError(f"Function {node.func_exp} has multiple variables {n} != {node.variable}")

                rexp += token + " * X^0 "          
        # ------------------- #
        
        lexp = ""
        for token in lhs:
            print(token)
            token = token
            if token in ['+', '-', '*', '/', '%', '^']:
                lexp += token + " "
                continue
            if node.variable == token:
                if len(lhs) - 1 <= lhs.index(token) + 1 or lhs[ lhs.index(token) + 1 ] != '^':
                    lexp += "1 * X^1 "
                continue
            for n in token:
                if  n not in [node.variable,'0', '1', '2', '3', '4', '5', '6', '7','8','9']:
                    raise ValueError(f"Function {node.func_exp} has multiple variables {n} != {node.variable}")

            lexp += token + " * X^0 "   

        DEBUG and print(" | Function rexp : ", rexp)
        DEBUG and print(" | Function lexp : ", lexp)
        return f"{rexp} = {lexp}"

    def solve_equation(node, DEBUG=False):
        if context[node.function]:
            node.variable = node.func_exp.strip()
            node.func_exp = context[node.function]
        else:
            raise ValueError(f"Function {node.function} not defined") 
        equation = validate_function(node)
        DEBUG and print(" | SOLVE : ", equation)
        return computorv1(equation)

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
            DEBUG and print(" | DEBUUG : ", node)
            if node.function in context  and not isnumber(node.func_exp) and check_function(node.function, context[node.function], node.value) and is_resignement(node, context[node.function], DEBUG):
                return solve_equation(node)
            context[node.function] = node.value
            return  node.value
        elif node.type == 'FUNCTION_OPERATION':

            if node.function not in context:
                raise ValueError(f"Undefined function: {node.function}")

            node.func_exp = context[node.function]
            for x in node.func_exp:
                if x not in ['+', '-', '*', '/', '%', '^', '(', ')', ' ', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    node.variable = x
                    break
            node.func_exp = node.func_exp.replace(node.variable, str(node.value.value))
            tokens  = lexer(node.func_exp, DEBUG)
            ast     = parser(tokens)
            context_, result = evaluator(ast, context, DEBUG)
            return result
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def main_evaluator():
        DEBUG and print(" | Evaluator input : ", ast)
        result = evaluate_node(ast)
        return context, result
        
    return main_evaluator()

def isnumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def get_variable_name(func_exp):
    variable = ""
    expression = func_exp.split()

    for x in expression:
        if x not in ['+', '-', '*', '/', '%', '^', '(', ')', ' ', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and not isnumber(x):
            variable = x
            break
    
    if not variable:
        raise ValueError(f"Function {func_exp} does not have a variable")

    for x in expression:
        if x not in ['+', '-', '*', '/', '%', '^', '(', ')', ' ', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and not isnumber(x):
            if variable != x:
                raise ValueError(f"Function {func_exp} has multiple variables : {variable} != {x}   ")
            
    return variable

def check_function(func, func_exp, value):
    variable_name = get_variable_name(func_exp)
    
    if variable_name is None:
        raise ValueError(f"Function {func} does not have a variable")
    return variable_name

def is_resignement(node, func_exp, DEBUG=False):
    expression = func_exp.split()
    for x in expression:
        if x not in ['+', '-', '*', '/', '%', '^', '(', ')', ' '] and not isnumber(x):
            if node.variable == x:
                return True
    return False
    DEBUG and print(" | node : ", node)
    DEBUG and print(" | func_exp : ", func_exp)