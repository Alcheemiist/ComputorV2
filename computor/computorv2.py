import sys
sys.path.append('..')

from parser.lexer import lexer
from parser.parser import parser
from evaluator.evaluator import evaluator
from utils.helpers import print_color, COLORS

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
        error = f" > Error: {e}"
        print_color("FAIL", f" > Error: {e}")
        raise
        return None

def main():
    DEBUG = sys.argv[1] if len(sys.argv) > 1 else False
    DEBUG = DEBUG == "--debug"

    print_color("WARNING", "Basic Calculator (Type 'exit' , 'q' to quit)")
    print_color("WARNING", "Type '!all' to display all stored variables and functions.\n")

    count = 0
    while True:
        user_input = input(COLORS["BOLD"] + f"clc({count})> " + COLORS["RESET"])
        if user_input.lower() == 'exit' or user_input.lower() == 'q':
            break
        elif user_input == "!all":
            computorv2(user_input, DEBUG)
        else:
            DEBUG and print_color("OKBLUE" , "-------------------")
            DEBUG and print_color("HEADER", f" |  User input: '{user_input}'")
            DEBUG and print_color("OKBLUE" , "------------------")
            result = computorv2(user_input, DEBUG)
            if result is not None:
                print_color("UNDERLINE", f" | = {result}")
            DEBUG and print_color("OKBLUE" , "-------------------")
        count += 1
if __name__ == "__main__":
    main()