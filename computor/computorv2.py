import sys
sys.path.append('..')
from lexer import lexer
from parser import parser
from evaluator import evaluator
from helpers import print_color, COLORS
from test_case import test_function

context = {}

def computorv2(user_input="", DEBUG=False, Raise_flag=False):
    global context
    
    # TO ADD : History of the commands and the results

    if user_input == "!all":
        if context:
            print_color("HEADER", "\n | <---  Variables and functions stored  --->") 
            for key, value in context.items():
                print_color("OKCYAN", f"\n |> {key} = {value}")
            print_color("HEADER", "\n | <---------------------------------------->")
        else:
            print_color("HEADER", "\n |> No variables or functions stored yet.")
        return "all variables and functions"

    try:
        tokens  = lexer(user_input, DEBUG)
        if not tokens:
            print_color("FAIL", "FAIL: Invalid input")
            if Raise_flag:
                raise ValueError("Invalid input")
        ast     = parser(tokens, context)
        if not ast:
            print_color("FAIL", "FAIL: Invalid AST")
            if Raise_flag:
                raise ValueError("Invalid AST")

        context, result = evaluator(ast, context, DEBUG)
        DEBUG and print_color("HEADER", f" | AST: {ast}")
        DEBUG and print_color("HEADER",f" | Context : {context}")
        return result
    except Exception as e:
        print_color("FAIL", f"Error sys: {e}")
        if Raise_flag:
            raise ValueError("Error sys: {e}")
        return None

def main():
    DEBUG = sys.argv[1] if len(sys.argv) > 1 else False
    DEBUG = DEBUG == "--debug"
    Raise_flag = False
    # history = []
    
    print_color("WARNING", "Basic Calculator (Type 'exit' , 'q' to quit)")
    print_color("WARNING", "Type '!all' to display all stored variables and functions.\n")

    count = 0
    while True:
        user_input = input(COLORS["BOLD"] + f"clc({count})> " + COLORS["RESET"])
        
        if user_input == "":
            continue 
        elif user_input.lower() == 'exit' or user_input.lower() == 'q':
            break
        elif user_input == "!all":
            computorv2(user_input, DEBUG, Raise_flag)
        else:
            DEBUG and print_color("OKBLUE" , "-------------------")
            DEBUG and print_color("HEADER", f" |  User input: '{user_input}'")
            DEBUG and print_color("OKBLUE" , "------------------")
            result = computorv2(user_input, DEBUG, Raise_flag)
            if result is not None:
                print_color("UNDERLINE", f" | = {result}")
            DEBUG and print_color("OKBLUE" , "-------------------")
        count += 1



if __name__ == "__main__":
    # main()
    test_function()
    # test_question_mark()
    # test_case()
    # test_case_function()
    # test_case_complex()
    # test_function_and_matrix_errors()