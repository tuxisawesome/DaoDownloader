#1.0
def init(drivers,drivernames,configmgr,drivermgr,kernel):
    display = drivers[drivernames.index("display")]
    inp = drivers[drivernames.index("input")]
    """
    A simple, self-contained Read-Eval-Print Loop (REPL) for Python.

    This function simulates the Python interactive interpreter. It reads a line
    of input, evaluates it, prints the result, and loops. It uses only
    built-in functions and maintains its own scope for variables.
    """
    # The 'scope' dictionary will hold all the variables, functions, and
    # modules defined by the user during the REPL session.
    # It acts as the global namespace for the executed code.
    scope = {}

    display.printline("Welcome to the simple Python REPL!")
    display.printline("Type 'exit()' or 'quit()' to exit.")

    while True:
        try:
            # 1. READ: Get a line of code from the user.
            source = inp.getinput(">>> ")

            # Check for commands to exit the REPL.
            if source.strip().lower() in ["exit()", "quit()"]:
                display.printline("Exiting REPL.")
                break

            # 2. EVALUATE: Try to evaluate the input as an expression first.
            # An expression is something that returns a value (e.g., "2 + 2", "len('hello')").
            try:
                # The compile() function checks if the source is a valid expression.
                # If it's not, it will raise a SyntaxError, and we'll catch it.
                code = compile(source, '<string>', 'eval')
                result = eval(code, scope)

                # 3. PRINT: If the expression returns a result, print it.
                # We check `is not None` so we don't print anything for expressions
                # that evaluate to None (like a function call that doesn't return).
                if result is not None:
                    display.printline(repr(result))

            except SyntaxError:
                # If compile() fails with a SyntaxError, it's not a valid expression.
                # It's likely a statement (e.g., variable assignment `x = 10`,
                # a for loop, or a function definition).
                # We then execute it as a statement using exec().
                exec(source, scope)

        except Exception as e:
            # If any other error occurs during evaluation or execution
            # (e.g., NameError, TypeError), print the error message
            # to the user without crashing the REPL.
            display.printline(f"Error: {e}")
