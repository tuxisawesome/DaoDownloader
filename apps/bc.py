#1.0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Python implementation of the bc (basic calculator) command-line utility.
This script provides an interactive command-line interface for performing
arbitrary-precision arithmetic calculations. It supports basic arithmetic
operations, variable assignments, and a range of mathematical functions.
"""


from decimal import Decimal, getcontext

# --- Globals ---
# Set the precision for decimal calculations.
getcontext().prec = 28

# Symbol table to store variables and functions.
SYMBOL_TABLE = {}

# --- Helper Functions ---
def is_number(s):
    """
    Check if a string can be converted to a number.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

# --- Core Evaluation Logic ---
def evaluate(expression):
    """
    Evaluate a mathematical expression provided as a string.
    This function uses a custom parsing mechanism to handle arithmetic
    operations in the correct order of precedence.
    """
    # Tokenize the expression.
    tokens = tokenize(expression)

    # Convert infix to postfix notation (Reverse Polish Notation).
    postfix_tokens = infix_to_postfix(tokens)

    # Evaluate the postfix expression.
    return evaluate_postfix(postfix_tokens)

def tokenize(expression):
    """
    Break down the expression into a list of tokens.
    """
    # Add spaces around operators to facilitate splitting.
    expression = expression.replace('(', ' ( ').replace(')', ' ) ')
    for op in ['+', '-', '*', '/', '%', '^']:
        expression = expression.replace(op, f' {op} ')

    # Split the expression into tokens.
    tokens = expression.split()
    return tokens

def infix_to_postfix(tokens):
    """
    Convert an infix expression to postfix (RPN) using the Shunting-yard algorithm.
    """
    # Operator precedence.
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
    
    # Output queue and operator stack.
    output = []
    operators = []

    for token in tokens:
        if is_number(token):
            output.append(token)
        elif token in SYMBOL_TABLE and is_number(str(SYMBOL_TABLE[token])):
            output.append(str(SYMBOL_TABLE[token]))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Pop the '('.
        else: # An operator.
            while (operators and operators[-1] != '(' and
                   precedence.get(operators[-1], 0) >= precedence.get(token, 0)):
                output.append(operators.pop())
            operators.append(token)

    while operators:
        output.append(operators.pop())

    return output

def evaluate_postfix(tokens):
    """
    Evaluate a postfix expression.
    """
    stack = []
    for token in tokens:
        if is_number(token):
            stack.append(Decimal(token))
        else:
            # Pop the required number of operands from the stack.
            val2 = stack.pop()
            val1 = stack.pop()
            
            # Perform the operation.
            if token == '+':
                stack.append(val1 + val2)
            elif token == '-':
                stack.append(val1 - val2)
            elif token == '*':
                stack.append(val1 * val2)
            elif token == '/':
                stack.append(val1 / val2)
            elif token == '%':
                stack.append(val1 % val2)
            elif token == '^':
                stack.append(val1 ** val2)
    
    return stack[0]

# --- Main Program Loop ---
def init(drivers, drivernames, configmgr, drivermgr,kernel):
    """
    Main function to run the bc calculator.
    """
    display = drivers[drivernames.index("display")]
    inp = drivers[drivernames.index("input")]
    display.printline("bc (basic calculator)")
    display.printline("Walter Brobson, 2025")
    display.printline("Enter 'quit' to exit.")

    while True:
        try:
            # Read user input.
            line = inp.getinput("> ").strip()

            if not line:
                continue
            if line == 'quit':
                break

            # Handle variable assignment.
            if '=' in line:
                var, expr = line.split('=', 1)
                var = var.strip()
                expr = expr.strip()
                SYMBOL_TABLE[var] = evaluate(expr)
                display.printline(f"{var} = {SYMBOL_TABLE[var]}")
            else:
                # Evaluate the expression and print the result.
                result = evaluate(line)
                display.printline(result)

        except Exception as e:
            display.printline(f"Error: {e}")

