import re
# from fractions import Fraction
from collections import defaultdict

# Define ANSI color codes for console output
COLORS = {
    'GREEN': '\033[1;32;40m',
    'RED': '\033[1;31;40m',
    'YELLOW': '\033[1;33;40m',
    'BLUE': '\033[1;34;40m',
    'ORANGE': '\033[1;35;40m',
    'RESET': '\033[0;37;40m'
}

def print_error(msg):
    print(COLORS['RED'], msg, COLORS['RESET'])
    exit()

def Handle_errors(equation):
    if not re.match(r'^[X0-9\^\+\-\=\*\.\s]*$', equation):
        print(f"{COLORS.red}Error: Invalid characters in the equation{COLORS.reset}")
        exit(0)
    if equation.find('=') == -1:
        print(f"{COLORS.red}Error: this is not an equation{COLORS.reset}")
        exit(0)
    if equation.split('=')[1].strip() == "":
        print(f"{COLORS.red}Error: Left-hand side of the equation is empty{COLORS.reset}")
        exit(0)
    if equation.split('=')[1].strip().find("X") == -1 and equation.split('=')[0].strip().find("x") == -1:
        print(f"{COLORS.red}Error: Equation must contain an X variable{COLORS.reset}")
        exit(0)

class Polynomial:

    def __init__(self, equation) -> None:
        self.equation = equation

        self.lhs = ""
        self.rhs = ""
        self.terms = defaultdict(tuple)
        self.degree = 0
        self.reduced_form = ""
        self.solutions = []

        self.rhs_dict = {}
        self.lhs_dict = {}
        
        self.complex = False
        
        self.parse_equation()

    def parse_equation(self):
        print(f"Equation: {self.equation}")
        
        if '=' not in self.equation: 
            raise ValueError("Equation must contain an equal sign")
        
        parts = self.equation.split('=')
        if len(parts) != 2:
            raise ValueError("Equation must contain exactly one equal sign")
        
        self.lhs, self.rhs = map(str.strip, parts)

        # Negate the right-hand side by using a regex for term parsing
        self.rhs = self.rhs.replace('-', '+-')

        # Split by '+' to separate terms
        rhs_terms = [term.strip() for term in self.rhs.split('+') if term.strip()]

        # Negate each term of the RHS
        negated_rhs_terms = []
        for term in rhs_terms:
            if term:
                if term.startswith('-'):
                    negated_rhs_terms.append(term[1:].strip())  # Remove leading minus
                else:
                    negated_rhs_terms.append('-' + term)  # Add leading minus

        # Reconstruct the RHS
        self.rhs = ' + '.join(negated_rhs_terms)
        
        # Extract terms and compute polynomial degree if necessary
        self.extract_terms()
    
    def extract_terms(self):
        self.equation = self.lhs + " + " + self.rhs
        print(f"Equation: {self.equation} = 0")

        for term in re.findall(r'([+-]?\s*\d*\.?\d*)\s*\*\s*X\^([+-]?\d+)', self.equation):
            coef, power = term
            coef = coef.replace(' ', '')
            coef = float(coef) if coef and coef not in ['+', '-'] else 1.0
            if coef == '-':
                coef = -1.0
            power = int(power)
            self.terms[power] = self.terms.get(power, 0) + coef

        # Compute the polynomial degree
        self.degree = max(self.terms.keys())
        # # Reduce the equation
        self.reduce_equation()

    def reduce_equation(self):
        self.reduced_form = ' + '.join(f"{coef} * X^{power}" for power, coef in sorted(self.terms.items(), reverse=True))
        self.reduced_form = self.reduced_form.replace(' + -', ' - ')
        self.reduced_form = self.reduced_form.replace(' 1 * ', ' ')
        self.reduced_form = self.reduced_form.replace(' * X^0', ' ')
        self.reduced_form = self.reduced_form.replace(' * X^1', ' X')
        self.reduced_form = self.reduced_form.replace(' * X^', ' X ^ ')
        self.reduced_form = self.reduced_form.replace('  ', ' ')
        self.reduced_form = self.reduced_form.strip()
        self.degree = max(self.terms.keys())

    def solve(self):
        if self.degree == 0:
            if self.terms[0] == 0:
                self.solutions = ["All real numbers are solutions."]
            else:
                self.solutions = ["No solution."]
        elif self.degree == 1:
            a = self.terms.get(1, 0)
            b = self.terms.get(0, 0)
            if a == 0:
                self.solutions = ["No solution."]
            else:
                self.solutions = [-b / a]
        elif self.degree == 2:
            a = self.terms.get(2, 0)
            b = self.terms.get(1, 0)
            c = self.terms.get(0, 0)
            discriminant = b**2 - 4*a*c
            if discriminant > 0:
                root1 = (-b + discriminant**0.5) / (2*a)
                root2 = (-b - discriminant**0.5) / (2*a)
                self.solutions = [root1, root2]
            elif discriminant == 0:
                if a == 0:
                    self.solutions = ["No solution."]
                    return
                root = -b / (2*a)
                self.solutions = [root]
            else:
                real_part = -b / (2*a)
                imaginary_part = (-discriminant)**0.5 / (2*a)
                root1 = complex(real_part, imaginary_part)
                root2 = complex(real_part, -imaginary_part)
                self.solutions = [root1, root2]
                self.complex = True
        else:
            self.solutions = ["The polynomial degree is strictly greater than 2, I can't solve."]
    
    def print_solution(self):
        if len(self.solutions) == 1 and self.solutions[0] == "No solution.":
            print("No solution.")
        elif self.degree == 0:
            print("All real numbers are solutions.")
        elif self.degree == 1:
            print(f"The solution is: {self.solutions[0]}")
        elif self.degree == 2 and len(self.solutions) == 2:
            print(f"Discriminant is strictly positive, the two solutions are: {self.solutions}")
        elif self.degree == 2 and len(self.solutions) == 1:
            print(f"Discriminant is equal to zero, the solution is: {self.solutions[0]}")
        elif self.degree == 2 and self.complex:
            print(f"Discriminant is strictly negative, the two complex solutions are: {self.solutions}")
        else:
            print("The polynomial degree is strictly greater than 2, I can't solve.")

    def print_degree(self):
        print("Polynomial degree: ", self.degree)
    

    def print_reduced_form(self):
        print("Reduced form: ", self.degree)

def validate_equation(equation):
    if not re.match(r'^[X0-9\^\+\-\=\*\.\s]*$', equation):
        print_error("Invalid characters in the equation")
    if equation.find('=') == -1:
        print_error("This is not an equation")
    if equation.split('=')[1].strip() == "":
        print_error("Left-hand side of the equation is empty")
    if equation.split('=')[1].strip().find("X") == -1 and equation.split('=')[0].strip().find("x") == -1:
        print_error("Equation must contain an X variable")

def computorv1(equation, DEBUG=False):
    validate_equation(equation)
    p = Polynomial(equation)
    p.solve()
    p.print_degree()
    p.print_reduced_form()
    p.print_solution()
    return p.solutions

# if __name__ == "__main__":

#     # Test cases
#     # case 0 : second degree
#     computorv1("3 * X^2 - 5 * X^1 = 2 * X^0 - 3 * X^2 + 2 * X^1 - 5 * X^0 - 5 * X^2", DEBUG=False)
#     print("Case 0: ", 0.5, -1.0)

#     computorv1("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0", DEBUG=False)
#     print("Case 1: ", 0.905239, -0.475131)

#     computorv1("5 * X^0 + 4 * X^1 = 4 * X^0", DEBUG=False)
#     print("Case 2: ", -0.25)

#     computorv1("8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0", DEBUG=False)
#     print("Case 3: ", "The polynomial degree is strictly greater than 2, I can't solve.")

#     computorv1("5 * X^0 = 154 * X^0", DEBUG=False)
#     print("Case 4: ", "All real numbers are solutions.")

#     computorv1("1 * X^2 + X^1 = 1 * X^2", DEBUG=False)
#     print("Case 5: ", "No solution.")

#     computorv1("1 * X^2 + 5 * X^1 = 1", DEBUG=False)
#     print("Equation must contain an X variable ")