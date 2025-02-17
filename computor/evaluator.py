from lexer import lexer
from parser import parser
from computorv1 import computorv1
import math

# --------- helper ------------- #  

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
        if x not in ['+', '-', '*', '/', '%', '^', '(', ')', ' ', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'i'] and not isnumber(x):
            variable = x
            break
    
    if not variable:
        raise ValueError(f"Function {func_exp} does not have a variable")

    for x in expression:
        if x not in ['+', '-', '*', '/', '%', '^', '(', ')', ' ', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "i"] and not isnumber(x):
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

def is_complex(value):
    if 'i' in value or 'j' in value:
        return True
    return False

def power_complex(a, b, n):
    # Convert to polar form
    r = math.sqrt(a**2 + b**2)  # Magnitude
    theta = math.atan2(b, a)     # Angle

    # Apply De Moivre's Theorem
    r_n = r ** n  # Magnitude raised to the power n
    theta_n = theta * n  # Angle multiplied by n

    # Convert back to rectangular form
    real_part = r_n * math.cos(theta_n)
    imaginary_part = r_n * math.sin(theta_n)

    return real_part, imaginary_part


# # Function to raise a complex number to a power
# def power_complesx(z, n):
#     r, theta = cmath.polar(z)  # Get the magnitude and angle
#     r_n = r ** n  # Magnitude raised to the power n
#     theta_n = theta * n  # Angle multiplied by n
#     result = cmath.rect(r_n, theta_n)
#     return result

def replace_variables(func_exp, context):

    print("replace : ", func_exp)
    expression = func_exp.split()

    for x in expression:
        print("x : ", x)
        if context[str(x)]:
            print("found : ", x)
        else:
            print("not found : ", x)
            # func_exp = func_exp.replace(x, str(context[x]))
        
    
    print("replace : ", func_exp)
    exit()




# --------- evaluator ------------- #

def evaluator(ast, context, DEBUG=False):
  
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

    def handle_equation(node):
        # print("expression : ", context[node.function])
        # print("variable : ", get_variable_name(context[node.function]))
        # print(node.func_exp)
        variable = get_variable_name(context[node.function])
        expression =  context[node.function].replace(variable, node.func_exp.strip())

        # print(" calculate : ",expression)
        tokens  = lexer(expression, DEBUG)
        ast     = parser(tokens, context)
        context_, result = evaluator(ast, context, DEBUG)
        return result 
    
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
                    if  n not in [node.variable,'0', '1', '2', '3', '4', '5', '6', '7','8','9', 'i']:
                        raise ValueError(f"Function {node.func_exp} has multiple variables {n} != {node.variable}")

                rexp += token + " * X^0 "          
        # ------------------- #
        lexp = ""
        for token in lhs:
            token = token
            if token in ['+', '-', '*', '/', '%', '^']:
                lexp += token + " "
                continue
            if node.variable == token:
                if len(lhs) - 1 <= lhs.index(token) + 1 or lhs[ lhs.index(token) + 1 ] != '^':
                    lexp += "1 * X^1 "
                continue
            for n in token:
                if  n not in [node.variable,'0', '1', '2', '3', '4', '5', '6', '7','8','9', 'i']:
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
            if not is_complex(node.value):
                raise ValueError(f"Invalid complex number: {node.value} without i or j")
            value = node.value.replace('i', '')
            value = value.replace('j', '')
            return complex(0, int(value))
        elif node.type == 'VARIABLE':
            if node.value not in context:
                raise ValueError(f"Undefined variable: {node.value}")
            return context[node.value]
        elif node.type == 'OPERATOR':
            left = evaluate_node(node.left)
            right = evaluate_node(node.right)
            if isinstance(left, list) or isinstance(right, list):
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
                    if right == 2:
                        result = "-2j"
                    else:     
                        result = power_complex(left.real, left.imag, right)
                    return result
                return pow(left, right)
            else:
                raise ValueError(f"Unknown operator: {node.value}")
        elif node.type == 'ASSIGNMENT':
            value = evaluate_node(node.right)
            if value == 'QUESTION':
                if node.left.value not in context:
                    raise ValueError(" Variable undefined !")
                return context[node.left.value]
            if node.left.type == 'NUMBER':
                raise ValueError("Cannot assign value to a number")
            if node.left.type == 'OPERATOR':
                raise ValueError("Cannot assign value to an operator")
            context[node.left.value] = value
            return value
        elif node.type == 'MATRIX':
            if not node.value:
                return []
            return [[evaluate_node(cell) for cell in row] for row in node.value]
        elif node.type == 'FUNCTION':
            DEBUG and print(" | DEBUG : ", node)
            if node.function in context  and  isnumber(node.value) and check_function(node.function, context[node.function], node.value) :
                return solve_equation(node)
            if node.value == "?":
                if isnumber(node.func_exp):
                    return handle_equation(node)
                return context[node.function]
            
            expression_replace = node.value.split()
            for x in expression_replace:
                if x in context:
                    node.value = node.value.replace(x, str(context[x]))
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
            ast     = parser(tokens, context)
            context_, result = evaluator(ast, context, DEBUG)
            return result
        elif node.type == 'QUESTION':
            return "QUESTION"
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def main_evaluator():
        DEBUG and print(" | Evaluator input : ", ast)
        result = evaluate_node(ast)
        return context, result
        
    return main_evaluator()

# --------- evaluator ------------- #
