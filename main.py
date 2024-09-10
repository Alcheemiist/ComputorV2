from parser.lexer import lexer
from parser.parser import parser
from evaluator import evaluator
from utils.helpers import get_user_input, print_color, COLORS, test_color
import sys

def main():
    context = {}  # Store variables and functions

    DEBUG = sys.argv[1] if len(sys.argv) > 1 else False
    DEBUG = DEBUG == "--debug"
    DEBUG and test_color()
    
    while True:
        user_input = get_user_input()
        if user_input == "exit" or user_input == "quit" or user_input == "q!":
            break
        try:
            DEBUG and print("Input:", user_input)
            tokens = lexer(user_input, DEBUG)

            continue

            ast = parser(tokens)
            result = evaluator(ast, context)
            # print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()