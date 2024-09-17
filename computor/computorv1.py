import re
from fractions import Fraction

# play with console colors
green = "\033[1;32;40m"
red = "\033[1;31;40m"
yellow = "\033[1;33;40m"
bleu = "\033[1;34;40m"
orange = "\033[1;35;40m" 
reset = "\033[0;37;40m"


class Polynomial:

    def __init__(self) -> None:
        self.lhs = ""
        self.rhs = ""

        self.rhs_dict = {}
        self.lhs_dict = {}
        self.terms = {}
        self.degree = 0
        self.reduced_form = ""
        self.solutions = []

    def get_degree(self):
        self.degree = max([int(power) for power in self.reduced_form.keys()])
        return self.degree

    def get_solutions(self):
        return self.solutions
    
    def print_reduced_form(self):
        print(f"{yellow}> Reduced form : {green} [ ", end=f"")
        for power, coef , i in zip(self.reduced_form.keys(), self.reduced_form.values(), range(len(self.reduced_form))):
            print(f"{coef} * X^{power}", end="")
            if i < len(self.reduced_form) - 1:
                print(" + ", end="")
        print(f" = 0 ] {reset}")

    def extract_rhs_terms(self, rhs_parsed, DEBUG=False):
        DEBUG and  print("\n > Parsing right-hand side terms..", self.rhs, "---------------->")
        # multiply coef by -1 to get the reduced form
        for i in range(len(rhs_parsed)):
            # print("   *> Adding term:", rhs_parsed[i])
            rhs_term = rhs_parsed[i].split('*')
            if len(rhs_term) == 2:
                coef = float(rhs_term[0])
                if len(rhs_term[1].split('^')) == 2:
                    power = rhs_term[1].split('^')[1]
                else:
                    print_error("Error Format : a * X^2 not followed in rhs -> "+ rhs_parsed[i])
            else:
                coef = float(rhs_term[1]) * -1
                power = rhs_term[2].split('^')[1]
            
            self.rhs_dict[i] = (coef, power)
        DEBUG and print(f"  -> rhs_dict[{len(self.rhs_dict)}]:", self.rhs_dict)

    def extract_lhs_terms(self, DEBUG=False):
        DEBUG and print("\n > Parsing left-hand side terms..", self.lhs, "------------->")
        lhs_parsed = self.lhs.split('+')
        lhs_parsed = [term.strip() for term in lhs_parsed if term.strip()]  # Remove empty spaces
        terms = []
        print

        for i in range(len(lhs_parsed)):
            lhs_term = lhs_parsed[i].split('-')
            # print("   -> Adding term:", lhs_term)
            for k in range(len(lhs_term)):
                coef, power = 0, 0
                # print("     -> lhs_term[", i + k, "]:", lhs_term[k])
                lhs_parse_term = lhs_term[k].split('*')
                lhs_parse_term = [term.strip() for term in lhs_parse_term if term.strip()]  # Remove empty spaces
                # print("    -> lhs_parse", lhs_parse_term)
                if len(lhs_parse_term) == 2 and lhs_parse_term[1].startswith('X') and k == 0:
                    coef = float(lhs_parse_term[0])
                    if len(lhs_parse_term[1].split('^')) == 2:
                        power = lhs_parse_term[1].split('^')[1]
                    else:
                        print_error("Error Format : a * X^2 not followed in rhs -> "+ lhs_term[k])
                elif len(lhs_parse_term) == 2 and i > 0:
                    coef = float(lhs_parse_term[0]) * -1
                    power = lhs_parse_term[1].split('^')[1]
                else:
                    print_error(" Term is not in the form a * X^b -> " + lhs_parse_term[k])
                # print("     -> Coefficient:", coef, "Power:", power)
                terms.append((coef, power))
        # print(f"  -> lhs_dict[{len(terms)}]:", terms)
        self.lhs_dict = terms

    def parse_equation(self, equation, DEBUG=False):
        print(f"{yellow}> Parsing equation : ", equation, f"{reset}")
        try:
            self.lhs, self.rhs = equation.split('=')
        except ValueError:
            raise ValueError("Error: Equation must contain an equal sign")

        DEBUG and print(f"\n  -> Left-hand side:{yellow}", self.lhs, f"{reset}")
        DEBUG and print(f"  -> Right-hand side:{yellow}", self.rhs, f"{reset}\n")

        self.rhs = self.rhs.replace('-', '+ -')  # Handle minus signs on the right side
        rhs_terms = self.rhs.split('+')
        rhs_terms = [term.strip() for term in rhs_terms if term.strip()]  # Remove empty spaces
        
        # print("  -> rhs_terms:", rhs_terms)
        rhs_parsed = ['-1 * ' + term if not term.startswith('-') else term.replace('-', '') for term in rhs_terms]
        DEBUG and print("  -> rhs extracted :", rhs_parsed)

        # Convert terms from the rhs and lhs sides into dict {power: coefficient} 
        self.extract_rhs_terms(rhs_parsed)
        self.extract_lhs_terms()

    def transform_terms(self):
        all_terms = self.lhs_dict + list(self.rhs_dict.values())
        print("> Function terms:", all_terms)

        self.reduced_form = {}
        for term in all_terms:
            coef, power = term
            if power in self.reduced_form :
                self.reduced_form [power] += coef
            else:
                self.reduced_form [power] = coef
        print(f"> Transformed Function terms:{yellow}", self.reduced_form , f"{reset}")

    def solve(self):
        print(f"{yellow}> Solving the equation : ", end="")
        print(f"  -> Degree:{orange}", self.degree, f"{reset}", end="")
        print(f" {yellow} -> Terms:{orange}", self.reduced_form, f"{reset}")
        
        print(f"{orange}> The solution is : ", end="")

        if int(self.degree) == 0:

            if self.reduced_form['0'] == 0:
                self.solutions = "True"
                print(f"{green}All real numbers are solutions")
            else:
                self.solutions = 'False'
                print(f"{red}No solution for this equation")

        if int(self.degree) == 1:
            
            if self.reduced_form['1'] == 0:
                self.solutions = "No solution"
                print(f"{red}No solution")
            else:
                x = (-1 * float(self.reduced_form['0']) / float(self.reduced_form['1']))
                self.solutions = x
                # -> -1 * a0 / a1 
                print(f" X = {green}",Fraction(self.solutions).limit_denominator() , " = ", x, f"{reset}")
                return x

        if int(self.degree) == 2:
            # Calculate the discriminant : delta = b^2 - 4ac
            delta = self.reduced_form["1"] ** 2 - 4 * self.reduced_form["2"] * self.reduced_form["0"]
            print("\n> Delta:", delta, end=" -> ")

            if delta > 0:
                print("> Discriminant is strictly positive, the two solutions are: x1 = (-b + sqrt(delta) / 2a) and x2 = (-b - sqrt(delta) / 2a)")

                # Convert solutions to irreducible fractions
                self.solutions = [0, 0]
                self.solutions[0] = (-self.reduced_form["1"] - delta ** 0.5) / (2 *  self.reduced_form["2"])
                self.solutions[1] = (-self.reduced_form["1"] + delta ** 0.5) / (2 *  self.reduced_form["2"])

                frac_x1 = Fraction(self.solutions[0]).limit_denominator()
                frac_x2 = Fraction(self.solutions[1]).limit_denominator()
                
                print(f"{reset}x1 = {orange}",frac_x1 ,  " =  ", self.solutions[0], f"{reset}")
                print(f"x2 = {orange}",frac_x2 , " =  ",self.solutions[1] ,f"{reset}")
                return frac_x1, frac_x2
            elif delta == 0:
                print(f"{green}Discriminant is zero, the solution is: x = -b / 2a")
                if self.reduced_form["2"] == 0:
                    print(f"{green}Division by zero, there are no real solutions{reset}")
                    return None
                print(-self.reduced_form["1"] / (2 *  self.reduced_form["2"]))
                self.solution[0] = -self.reduced_form["1"] / (2 *  self.reduced_form["2"])
                return -self.reduced_form["1"] / (2 *  self.reduced_form["2"]), None    
            elif delta < 0:
                print(f"{orange}Discriminant is strictly negative, let's solve it with complex numbers")
                real_part = -self.reduced_form["1"] / (2 * self.reduced_form["2"])
                imaginary_part = (abs(delta) ** 0.5) / (2 * self.reduced_form["2"])
                print(f"Complex solutions are:{green} x1 = {real_part} + {imaginary_part}i, x2 = {real_part} - {imaginary_part}i{reset}")
                return (real_part, imaginary_part), (real_part, -imaginary_part)

    def Handle_equation(self):
        degree = self.get_degree()
        if int(degree) > 2:
            print(f"{red}> The polynomial degree is stricly greater than 2nd degree, I can't solve{reset}")
            return None, None
        else:
            print(f"{green}> The polynomial degree is less than 2nd degree, I can solve{reset}")
            self.solve()
            return self.get_solutions()



def print_error(msg):
    print(red, msg,reset)
    exit()

def Handle_errors(equation):
    # look for any invalid characters except X, ^, +, -, =, *, ., digits
    if not re.match(r'^[X0-9\^\+\-\=\*\.\s]*$', equation):
        print(f"{red}Error: Invalid characters in the equation{reset}")
        exit(0)
    if equation.find('=') == -1:
        print(f"{red}Error: this is not an equation{reset}")
        exit(0)
    if equation.split('=')[1].strip() == "":
        print(f"{red}Error: Left-hand side of the equation is empty{reset}")
        exit(0)
    if equation.split('=')[1].strip().find("X") == -1 and equation.split('=')[0].strip().find("x") == -1:
        print(f"{red}Error: Equation must contain an X variable{reset}")
        exit(0)

def computorv1(equation, DEBUG=False):
    validate_equation(equation)
    p = Polynomial(equation)
    solutions = p.solve()
    p.print_solution()

    return solutions

def validate_equation(equation):
    if not re.match(r'^[X0-9\^\+\-\=\*\.\s]*$', equation):
        print_error("Invalid characters in the equation")
    if equation.find('=') == -1:
        print_error("This is not an equation")
    if equation.split('=')[1].strip() == "":
        print_error("Left-hand side of the equation is empty")
    if equation.split('=')[1].strip().find("X") == -1 and equation.split('=')[0].strip().find("x") == -1:
        print_error("Equation must contain an X variable")

if __name__ == "__main__":

    # Test cases
    # case 0 : second degree
    print(computorv1("3 * X^2 + 5 * X^1 = 2 * X^0", DEBUG=False))
    # Reduced form:  3.0 * X^2 + 5.0 * X^1 - 2.0 * X^0 = 0
    # Polynomial degree: 2
    # Discriminant is strictly positive, the two solutions are:
    # -2, 1/3 

    # print(computorv1("5 * X^0 + 4 * X^1 = 4 * X^0"))
    # print(computorv1("8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"))
    # print(computorv1("5 * X^0 = 154 * X^0"))
    # print(computorv1("1 * X^2 + X^1 = 1 * X^2"))
    # print(computorv1("1 * X^2 + 5 * X^1 = 1 "))
    # print(computorv1("3 * X^2 + 5 * X^1 = 2 * X^0"))

    # Case 1:  second degree
    # equation =  "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
    # Reduced form: 4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0
    # Polynomial degree: 2
    # Discriminant is strictly positive, the two solutions are:
    # 0.905239, -0.475131
    
    # Case 2: one degree
    # equation =  "5 * X^0 + 4 * X^1 = 4 * X^0"
    # Reduced form: 1 * X^0 + 4 * X^1 = 0
    # Polynomial degree: 1
    # The solution is: -0.25

    # Case 3: greater than 2
    # equation = "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
    # Reduced form: 5 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 0
    # Polynomial degree: 3
    # The polynomial degree is strictly greater than 2, I can't solve.

    # Case 4: zero degree
    # equation = "5 * X^0 = 154 * X^0"
    # Reduced form: 0 * X^0 = 0
    # Polynomial degree: 0
    # All real numbers are solutions.

    # case 5 : error equation format : a X^2
    # equation = "1 * X^2 + X^1 = 1 * X^2"

    # case 6 : error equation format :1 
    # equation = "1 * X^2 + 5 * X^1 = 1 "
