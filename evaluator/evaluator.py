from math import pow

def evaluator(ast, context, DEBUG=False):
    DEBUG and print(" | Evaluator input : ", ast)
    
    def evaluate_node(node):
        if node.type == 'NUMBER':
            return node.value
        elif node.type == 'VARIABLE':
            if node.value not in context:
                raise ValueError(f"Undefined variable: {node.value}")
            return context[node.value]
        elif node.type == 'OPERATOR':
            left = evaluate_node(node.left)
            right = evaluate_node(node.right)

            if node.value == '+':
                return left + right
            elif node.value == '-':
                return left - right
            elif node.value == '-' and node.left is None:
                return -right
            elif node.value == '*':
                return left * right
            elif node.value == '/':
                if right == 0:
                    raise ValueError("Division by zero")
                return left / right
            elif node.value == '^':
                return pow(left, right)
            else:
                raise ValueError(f"Unknown operator: {node.value}")
        elif node.type == 'ASSIGNMENT':
            value = evaluate_node(node.right)
            # if left value is a number raise an error
            if node.left.type == 'NUMBER':
                raise ValueError(f"Cannot assign value to a number")
            # if left value is an operator raise an error
            if node.left.type == 'OPERATOR':
                raise ValueError(f"Cannot assign value to an operator")
            context[node.left.value] = value
            return value
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    result = evaluate_node(ast)
    return context, result

# from math import pow

# def evaluator(ast, context, DEBUG=False):
#     DEBUG and print("Evaluator called : ", ast)
    
#     def evaluate_node(node):
#         if node.type == 'NUMBER':
#             return node.value
#         elif node.type == 'VARIABLE':
#             if node.value not in context:
#                 raise ValueError(f"Undefined variable: {node.value}")
#             return context[node.value]
#         elif node.type == 'OPERATOR':
#             left = evaluate_node(node.left)
#             right = evaluate_node(node.right)
#             if node.value == '+':
#                 return left + right
#             elif node.value == '-':
#                 return left - right
#             elif node.value == '*':
#                 return left * right
#             elif node.value == '/':
#                 if right == 0:
#                     raise ValueError("Division by zero")
#                 return left / right
#             elif node.value == '^':
#                 return pow(left, right)
#             else:
#                 raise ValueError(f"Unknown operator: {node.value}")
#         elif node.type == 'ASSIGNMENT':
#             value = evaluate_node(node.right)
#             context[node.left.value] = value
#             return value
#         else:
#             raise ValueError(f"Unknown node type: {node.type}")

#     result = evaluate_node(ast)
#     return context, result
