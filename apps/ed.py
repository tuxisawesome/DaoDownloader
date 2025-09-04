#1.1
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Python implementation of the ed (line editor) command-line utility.
This script provides a line-oriented text editor, similar to the classic
Unix ed, with all logic contained within a single function.
"""

import re

def init(drivers,drivernames,configmgr,drivermgr,kernel):
    sys = drivers[drivernames.index("sys")]
    display = drivers[drivernames.index("display")]
    inp = drivers[drivernames.index("input")]
    argv = configmgr.getvalue(configmgr.readconfig("env.cfg"), "argv")
    """
    Runs the entire ed editor logic within a single function scope.
    Encapsulates state and functionality using nested functions.
    """
    # --- Editor State ---
    buffer = []
    current_line_idx = -1  # 0-based index for the buffer
    dirty = False
    quit_flag = False
    current_filename = argv if argv != "null" else None

    # --- Nested Helper Functions (formerly class methods) ---

    def load_file(filename):
        """Load a file into the buffer."""
        nonlocal buffer, current_filename, current_line_idx
        try:
            with open(filename, 'r') as f:
                buffer = [line.rstrip('\n') for line in f.readlines()]
            current_filename = filename
            current_line_idx = len(buffer) - 1 if buffer else -1
            display.printline(sum(len(line) + 1 for line in buffer)) # display.printline byte count
        except FileNotFoundError:
            display.printline(f"? [new file]")
        except Exception as e:
            display.printline("?")
            sys.stderr.write(str(e) + '\n')

    def parse_address(addr_str):
        """Parse a single address string into a 0-based index."""
        if not addr_str:
            return None
        
        addr_str = addr_str.strip()
        
        if addr_str == '.':
            return current_line_idx
        if addr_str == '$':
            return len(buffer) - 1
        if addr_str.isdigit():
            line_num = int(addr_str)
            if 1 <= line_num <= len(buffer):
                return line_num - 1
            else:
                raise IndexError("invalid address")
        
        # Handle relative addresses like .+2, $-1
        match = re.match(r'([.$]?)(\s*[+-]\s*\d+)?', addr_str)
        if match:
            base_str, offset_str = match.groups()
            base = current_line_idx
            if base_str == '$':
                base = len(buffer) -1
            
            if offset_str:
                offset = int(offset_str.replace(" ", ""))
                base += offset

            if 0 <= base < len(buffer):
                return base
            else:
                # Allow address to be len(self.buffer) for append
                if base == len(buffer):
                    return base
                raise IndexError("invalid address")

        raise ValueError("invalid address")

    def parse_range(range_str, default_start=None, default_end=None):
        """Parse a range string like '1,5' into start and end indices."""
        range_str = range_str.strip()
        
        # No address given
        if not range_str:
            start = default_start if default_start is not None else current_line_idx
            end = default_end if default_end is not None else start
            return start, end

        # Single address given
        if ',' not in range_str:
            addr = parse_address(range_str)
            return addr, addr

        # Range of addresses given
        start_str, end_str = range_str.split(',', 1)
        start = parse_address(start_str) if start_str else default_start
        end = parse_address(end_str) if end_str else default_end
        
        if start is None: start = current_line_idx
        if end is None: end = current_line_idx

        if start > end:
            raise ValueError("invalid range")
            
        return start, end

    def get_input_lines():
        """Get multiple lines of input from the user until a '.' is entered."""
        lines = []
        while True:
            try:
                line = inp.getinput("")
                if line == '.':
                    break
                lines.append(line)
            except EOFError:
                break
        return lines

    def dispatch(addr_str, cmd, params):
        """Dispatch a command to its handler logic."""
        nonlocal buffer, current_line_idx, dirty, quit_flag, current_filename
        
        if cmd == 'a':
            start, _ = parse_range(addr_str, default_start=current_line_idx)
            lines = get_input_lines()
            # Special case: appending to empty buffer
            insert_at = start + 1 if buffer else 0
            buffer[insert_at:insert_at] = lines
            current_line_idx = insert_at + len(lines) - 1
            dirty = True

        elif cmd == 'i':
            start, _ = parse_range(addr_str, default_start=current_line_idx)
            lines = get_input_lines()
            insert_at = start if start != -1 else 0
            buffer[insert_at:insert_at] = lines
            current_line_idx = insert_at + len(lines) - 1
            dirty = True
        
        elif cmd in ('d', 'c'):
            if not buffer:
                raise IndexError("invalid address")
            start, end = parse_range(addr_str, default_start=current_line_idx)
            del buffer[start : end + 1]
            dirty = True
            current_line_idx = min(start, len(buffer) - 1)
            if cmd == 'c':
                lines = get_input_lines()
                insert_at = start
                buffer[insert_at:insert_at] = lines
                current_line_idx = insert_at + len(lines) - 1

        elif cmd in ('p', 'n'):
            if not buffer:
                raise IndexError("invalid address")
            start, end = parse_range(addr_str, default_start=current_line_idx)
            for i in range(start, end + 1):
                if cmd == 'n':
                    display.printline(f"{i+1}\t{buffer[i]}")
                else:
                    display.printline(buffer[i])
            current_line_idx = end

        elif cmd == 'w':
            filename = params if params else current_filename
            if not filename:
                raise ValueError("no current filename")
            
            start, end = parse_range(addr_str, default_start=0, default_end=len(buffer)-1)
            
            with open(filename, 'w') as f:
                content = '\n'.join(buffer[start : end + 1]) + '\n'
                f.write(content)
            
            current_filename = filename
            dirty = False
            display.printline(len(content))

        elif cmd == 'f':
            if params:
                current_filename = params
            if current_filename:
                display.printline(current_filename)
            else:
                display.printline("?")

        elif cmd == '=':
            _, end = parse_range(addr_str, default_start=len(buffer)-1, default_end=len(buffer)-1)
            display.printline(end + 1)

        elif cmd == 'q':
            if dirty:
                display.printline("?")
                dirty = False # Second 'q' will quit
            else:
                quit_flag = True
        
        else:
            display.printline("?")

    # --- Main Execution Logic ---
    if current_filename:
        load_file(current_filename)

    while not quit_flag:
        try:
            cmd_line = inp.getinput("")
        except EOFError:
            break

        # Regex to separate address, command, and parameters
        match = re.match(r'([.,$0-9\s+-]*)([a-z=])(.*)', cmd_line)
        if not match:
            if cmd_line.strip():
                display.printline("?")
            continue

        addr_str, cmd, params = match.groups()
        params = params.strip()

        try:
            dispatch(addr_str, cmd, params)
        except (ValueError, IndexError):
            display.printline("?")
        except Exception as e:
            display.printline("?")
            sys.stderr.write(f"An unexpected error occurred: {e}\n")