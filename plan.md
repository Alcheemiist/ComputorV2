# Core Objectives

## Mathematical Knowledge: The program must enable you to work with:

- [ ] Complex numbers
- [ ] Real numbers
- [ ] Matrices
- [ ] Function theory
- [ ] Polynomial equations (degrees ≤ 2)

## Type Handling and Operations: The interpreter should support:

- [ ] Rational numbers
- [ ] Complex numbers (with rational coefficients)
- [ ] Matrices
- [ ] Polynomial equations (degree ≤ 2)

## Variable Management: It should allow

- [ ] Assignment of expressions to variables with type inference.
- [ ] Reassignment of variables, including changing the type.
- [ ] Assignment of one variable to another.

## Expression Resolution: The interpreter must

- [ ] Solve mathematical expressions with or without predefined variables.
- [ ] Solve polynomial equations (degree ≤ 2).
- [ ] Handle operations like addition, subtraction, multiplication, division, modulos, and matrix multiplication.

## Function Support: It should

- [ ] Define functions with one variable.
- [ ] Support operations on functions, including evaluation.

## User Interface: The program should behave like a shell, retrieving user inputs for

- [ ] Performing computations
- [ ] Handling parentheses and computation priorities
- [ ] Additional Features
- [ ] Managing conventional operations (+, -, *, /) and modulo.
- [ ] Exponentiation (^) for integer and positive powers.
- [ ] Displaying results and computation history.

## Bonus Objectives (if mandatory parts are fully implemented)

- [ ] Displaying function curves.
- [ ] Supporting advanced mathematical functions (e.g., exponentials, trigonometry).
- [ ] Composition of functions.
- [ ] Matrix inversion, vector computation.
- [ ] Tracking command history.

This project will test both the ability to implement complex mathematical operations and the design skills in creating a flexible, extensible interpreter without using external libraries for complex number or matrix management

---------

ertainly, I'll generate test cases based on the correction page you provided. Here are the key test cases in bullet points:

Preliminary Part:

Verify the presence of code for handling:
    Natural integers
    Rational numbers
    Complex numbers (with rational coefficients)
    Matrices
    Polynomial equations of degree 2 or less
    Check if the program compiles and executes properly
    Verify that the program never quits unexpectedly (Segfault, interpretation error, etc.)
    Ensure no libraries are used for parsing or handling complex types

Assignment Part:
    Test elementary errors:
    Invalid syntax (e.g., x == 2, random keyboard input)
    Nonsensical inputs (e.g., x = 23edd23-+-+)
    Test semi-advanced errors:
    Incorrect syntax (e.g., = 2, 3 = 4)
    Undefined variable usage (e.g., x = g when g is not defined)
    Incomplete inputs (e.g., f(x = 2, x = [[4,2])
    Test advanced errors:
    Edge cases (e.g., x = --2)
    Invalid function assignments (e.g., f(x) = x * 2 then t = f(x))
    Restricted variable assignments (e.g., i = 2)
    Test valid elementary assignments:
    Simple variable assignments (e.g., x = 2, y = 4i, z = [[2,3];[3,5]])
    Test valid semi-advanced assignments:
    Function assignments and inter-variable operations
    Reassignment of variables
    Matrix and imaginary number assignments
    Test valid advanced assignments:
    Complex assignments involving multiple elements and types

Calculation Part:
    Test valid elementary calculations:
    Simple arithmetic (e.g., 2 + 2, 3 * 4)
    Variable usage in calculations
    Division by zero handling
    Float handling
    Test valid semi-advanced calculations:
    Complex number operations
    Matrix multiplication
    Function evaluation
    Test valid advanced calculations:
    Complex expressions with multiple operations and parentheses
    Function composition and evaluation
    Mixing complex numbers, functions, and matrices in calculations

Bonus Part:
    Test any additional features implemented by the student (if the mandatory part is perfect)
    Throughout all tests:

    Verify that the program never crashes or exits unexpectedly
    Check for proper error handling and user feedback
    Ensure consistent behavior across different input types and complexities