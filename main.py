from parser import lexer
from parser import parser
from evaluator import evaluator
from utils.helpers import get_user_input, print_color, COLORS


def test_color():
    print_color("OKGREEN", "Hello, World!")
    print_color("WARNING", "Hello, World!")
    print_color("FAIL", "Hello, World!")
    print_color("HEADER", "Hello, World!")
    print_color("OKBLUE", "Hello, World!")
    print_color("OKCYAN", "Hello, World!")
    print_color("BOLD", "Hello, World!")
    print_color("UNDERLINE", "Hello, World!")
    print_color("ENDC", "Hello, World!")

def main():
    context = {}  # Store variables and functions
    DEBUG = True
    test_color()
    
    while True:
        user_input = get_user_input()
        if user_input == "exit":
            break
        try:
            DEBUG and print("Input:", user_input)

            tokens = lexer(user_input)
            ast = parser(tokens)
            result = evaluator(ast, context)
            # print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()