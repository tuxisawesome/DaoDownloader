#1.0
def interp(code, display, imp,portable=False):
    """
    Interprets Brainfuck code.
    Returns 0 on success, 1 on syntax error (mismatched brackets).
    """
    # Initialize the memory tape (30,000 cells is standard)
    tape = [0] * 30000
    cell_ptr = 0
    code_ptr = 0
    
    # Pre-process brackets to handle loops efficiently
    # This prevents O(n^2) scanning during execution
    jump_map = {}
    stack = []
    
    try:
        for i, char in enumerate(code):
            if char == '[':
                stack.append(i)
            elif char == ']':
                start = stack.pop()
                jump_map[start] = i
                jump_map[i] = start
        if stack: raise IndexError # Mismatched open bracket
    except IndexError:
        return 1 # Return 1 for syntax/bracket errors

    # Execution Loop
    code_len = len(code)
    while code_ptr < code_len:
        command = code[code_ptr]

        if command == '>':
            cell_ptr = (cell_ptr + 1) % 30000
        elif command == '<':
            cell_ptr = (cell_ptr - 1) % 30000
        elif command == '+':
            tape[cell_ptr] = (tape[cell_ptr] + 1) % 256
        elif command == '-':
            tape[cell_ptr] = (tape[cell_ptr] - 1) % 256
        elif command == '.':
            if portable: print(chr(tape[cell_ptr]), end='', flush=True)
            else: display.printline(chr(tape[cell_ptr]),'')
        elif command == ',':
            # Basic input handling: defaults to 0 if no input provided
            if portable: import sys;char = sys.stdin.read(1)
            else: char = imp.stdin().read(1)
            tape[cell_ptr] = ord(char) if char else 0
        elif command == '[':
            if tape[cell_ptr] == 0:
                code_ptr = jump_map[code_ptr]
        elif command == ']':
            if tape[cell_ptr] != 0:
                code_ptr = jump_map[code_ptr]
        
        code_ptr += 1

    return 0 # Success




# Brainfuck interpreter
def init(drivers,drivernames,configmgr,drivermgr,kernel):
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")
    display = drivers[drivernames.index("display")]
    imp = drivers[drivernames.index("input")]
    if argv == "-i":
        instream = imp.getinput("[Please enter your code here]: ")
        interp(instream,display,imp)
        pass
    elif argv == "null" or argv == "-h":
        # Help
        display.printline("Brainfuck interpreter")
        display.printline("Dao Extras")
        display.printline("Usage: ")
        display.printline("-i   Interactive mode")
        display.printline("-h   Help")
        display.printline("Any other character will be considered as code.")
    else:
        # Interpret argv
        interp(argv,display,imp)

if __name__ == "__main__":
    interp(input("[Please enter your code here]: "),None,None,True)
