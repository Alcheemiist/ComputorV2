from parser.lexer import lexer
from parser.parser import parser
from evaluator import evaluator
from utils.helpers import get_user_input, print_color, COLORS, test_color
import sys

def main():
    context = {}  # Store variables and functions
    # history = []  # Store history of user input and results

    DEBUG = sys.argv[1] if len(sys.argv) > 1 else False
    DEBUG = DEBUG == "--debug"
    DEBUG and test_color()
    
    while True:
        user_input = get_user_input()
        if user_input == "exit" or user_input == "quit" or user_input == "q!":
            break
        if user_input == "history":
            for i, (input, result) in enumerate(history):
                print(f"{i+1}. {input} = {result}")
            continue
        try:
            DEBUG and print("Input:", user_input)
            tokens = lexer(user_input, DEBUG)

            # continue
            ast = parser(tokens)
            result = evaluator(ast, context)
            # print(result)
            # history.append((user_input, result))


        except Exception as e:
            print(f"Error: {e}")
        

if __name__ == "__main__":
    main()