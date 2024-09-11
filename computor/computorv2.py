import sys
sys.path.append('..')

from parser.lexer import lexer
from parser.parser import parser
from evaluator.evaluator import evaluator
from utils.helpers import get_user_input, print_color, COLORS, test_color

# Global context to store variables or functions, if needed
context = {}

def computorv2(user_input="", DEBUG=False):
    global context

    if user_input == "!all":
        if context:
            print_color("HEADER", f"\n | <---  Variables and functions stored  --->") 
            for key, value in context.items():
                print_color("OKCYAN", f"\n |> {key} = {value}")
            print_color("HEADER", f"\n | <---------------------------------------->")
        else:
            print_color("HEADER", f"\n |> No variables or functions stored yet.")
        return "all variables and functions"

    try:
        tokens  = lexer(user_input, DEBUG)
        ast     = parser(tokens)
        context, result = evaluator(ast, context, DEBUG)
        DEBUG and print_color("HEADER", f" | AST: {ast}")
        DEBUG and print_color("HEADER",f" | Context : {context}")
        return result
    except Exception as e:
        DEBUG and print_color("FAIL", f" > Error: {e}")
        return None

def main():
    DEBUG = sys.argv[1] if len(sys.argv) > 1 else False
    DEBUG = DEBUG == "--debug"

    print_color("WARNING", "Basic Calculator (Type 'exit' , 'q' to quit)")
    print_color("WARNING", "Type '!all' to display all stored variables and functions.\n")

    count = 0
    while True:
        user_input = input(COLORS["BOLD"] + "clc> " + COLORS["RESET"])
        if user_input.lower() == 'exit' or user_input.lower() == 'q':   # Command to exit the program
            break
        elif user_input == "!all":  # Display all variables and functions
            computorv2(user_input, DEBUG)
        else:
            DEBUG and print_color("OKBLUE" , "-------------------")
            DEBUG and print_color("HEADER", f" |  User input: '{user_input}'")
            DEBUG and print_color("OKBLUE" , "------------------")
            # Call computorv2 
            result = computorv2(user_input, DEBUG)
            if result is not None:
                print_color("UNDERLINE", f" | = {result}")
            DEBUG and print_color("OKBLUE" , "-------------------")

if __name__ == "__main__":
    main()