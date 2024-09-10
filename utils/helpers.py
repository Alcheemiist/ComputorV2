
COLORS = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m"
}

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


def get_user_input():
    return input(COLORS["OKCYAN"] + "clc> " + COLORS["RESET"])

def print_color(color, text):
    print(COLORS[color] + text + COLORS["ENDC"])





def is_rational(value):
    # Check if a value is a rational number
    print("Rational number check")

def is_complex(value):
    # Check if a value is a complex number
    print("Complex number check")

def is_matrix(value):
    # Check if a value is a matrix
    print("Matrix check")

def is_function(value):
    # Check if a value is a function
    print("Function check")

def evaluate_function(func, x_value):
    # Evaluate a function for a given x value
    print("Function evaluation")

def solve_equation(equation):
    # Solve equations up to degree 2
    # Handle both real and complex solutions
    print("Equation solving")

def resolve(expression, context):
    # Evaluate the expression and return the result
    print("Expression resolution")