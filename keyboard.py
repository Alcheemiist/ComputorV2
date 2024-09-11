import curses

# Store history of commands
history = []
history_index = -1
current_input = ""

def display_calculator(stdscr, result=""):
    # stdscr.clear()
    stdscr.addstr("Basic Calculator (Press 'q' to exit)\n")
    stdscr.addstr("Use arrow keys (Left/Right) to browse command history.\n")
    stdscr.addstr("Enter expression: " + current_input)
    # stdscr.refresh()

def evaluate_expression(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def calculator(stdscr):
    global history_index, current_input

    curses.curs_set(1)  # Show the cursor
    stdscr.nodelay(0)   # Block while waiting for user input

    display_calculator(stdscr)

    while True:
        key = stdscr.getch()

        if key == ord('q'):  # Exit the program
            break
        elif key == curses.KEY_LEFT:  # Left arrow key
            if history_index > 0:
                history_index -= 1
                current_input = history[history_index]
            display_calculator(stdscr)
        elif key == curses.KEY_RIGHT:  # Right arrow key
            if history_index < len(history) - 1:
                history_index += 1
                current_input = history[history_index]
            display_calculator(stdscr)
        elif key == curses.KEY_BACKSPACE:  # Backspace
            current_input = current_input[:-1]
            display_calculator(stdscr)
        elif key == curses.KEY_ENTER or key == 10:  # Enter
            if current_input:
                result = evaluate_expression(current_input)
                stdscr.addstr(f" = {result}\n")
                history.append(current_input)
                history_index = len(history)
                current_input = ""
                display_calculator(stdscr, result)
        else:
            if key != -1 and chr(key).isprintable():
                current_input += chr(key)
                display_calculator(stdscr)

if __name__ == "__main__":
    curses.wrapper(calculator)
