from lexer import lexer
from parser import parser
from evaluator import evaluator
from helpers import print_color

# ---------------- # 

def test_case_main():
    global context

    input = "AA(y) = 10 * 21 + y"

    print_color( "WARNING", f"Input: {input}")
    tokens  = lexer(input, DEBUG=True)
    ast     = parser(tokens)
    print_color("HEADER", f"AST: {ast} | value {ast.value}")
    print_color("HEADER", f"Context: {context}")
    context, result = evaluator(ast, context, DEBUG=True)
    print_color("HEADER", f"Result: {result}")

    print_color("OKBLUE", "----------------------------------")
    
    input1 = "AA(y) = 9 + y"

    print_color( "WARNING", f"Input: {input1}")
    tokens  = lexer(input1, DEBUG=True)
    ast     = parser(tokens)
    print_color("HEADER", f"AST: {ast} | value {ast.value}")
    print_color("HEADER", f"Context: {context}")
    context, result = evaluator(ast, context, DEBUG=True)
    print_color("HEADER", f"Result: {result}")

def test_case_complex():
    global context

    inputs = ["1i", "2j", "4 + 2i", "3 - 2j","10 + 10j + 5 - 5j", "a = 10 + 10j + 5 - 5j", "a + 10j "]
    # inputs = ["1i", "2j", "2 + 3i", "3 - 2j","10 + 10j"]

    for input in inputs:
        print_color( "WARNING", f"Input: {input}")
        tokens  = lexer(input, DEBUG=True)
        ast     = parser(tokens)
        # print_color("HEADER", f"AST: {ast} | value {ast.value}")
        # print_color("HEADER", f"Context: {context}")
        context, result = evaluator(ast, context, DEBUG=True)
        print_color("HEADER", f"Result: {result}")
        print_color("OKBLUE", "----------------------------------")

def test_function_and_matrix_errors():
    global context

    # inputs = ["AA(y = 10 + x", "[1, 2, 3]", "[[1, 2, 3], [4, 5, 6]]", "[[1, 2, 3], [[4, 5, 6]]", ]
    inputs = ["[1, 2, 3]", "[[1, 2, 3], [4, 5, 6]]", "[[1, 2, 3], [[4, 5, 6]]", ]
    inputs = ["[[1, 2, 3][1,2,2]]", ]

    for input in inputs:
        res = computorv2(input, DEBUG=True, Raise_flag=False)  
        print_color("HEADER", f"Result: {res}")
        print_color("OKBLUE", "----------------------------------")

def test_case():
    global context

    input = "f(x) = 10 * 21 + x"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

    input = "T  = f(x)"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

    input = "T = f(10)"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

def test_question_mark():
    global context

    input = "X = 69"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

    input = "X = ?"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

    input = "F = ?"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

def test_function():
    global context2

    input = "funB(y) = 40 +  y"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

    input = "funA(x) = x - 45"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

    input = "funB(4) + funA(2)"
    res = computorv2(input, DEBUG=True, Raise_flag=False)  
    print_color("HEADER", f"Result: {res}")
    print_color("OKBLUE", "----------------------------------")

# ---------------- # 

