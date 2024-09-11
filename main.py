from parser.lexer import lexer
from parser.parser import parser
from evaluator.evaluator import evaluator
from utils.helpers import get_user_input, print_color, COLORS, test_color
import sys
import curses

# Store history of commands
history = []
history_index = -1
current_input = ""
cursor_position = 0

def display_result(stdscr, result):
    return 
    stdscr.addstr(f" = {result}\n")

def display_calculator(stdscr):
    stdscr.clear()
    stdscr.addstr("Basic Calculator (Press 'q' to exit)\n")
    stdscr.addstr("Use arrow keys (Left/Right) to navigate input.\n")
    stdscr.addstr("Use Up/Down keys to browse command history.\n")
    stdscr.addstr("Enter expression: " + current_input)
    stdscr.move(3, len("Enter expression: ") + cursor_position)  # Move the cursor to the correct position
    stdscr.refresh()

def evaluate_expression(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def computorv2(stdscr, user_input=None):
    context = {}  # Store variables and functions

    if user_input == "all":
        for key, value in context.items():
            print(f"{key} = {value}")
    
    # try:
    #     DEBUG and print("Input:", user_input)
    #     tokens = lexer(user_input, DEBUG)
    #     ast = parser(tokens)
    #     context, result = evaluator(ast, context, DEBUG)

    #     DEBUG and print(COLORS["OKBLUE"] + COLORS["UNDERLINE"],f"> Result : {result}", COLORS["ENDC"])
    #     not DEBUG and print(COLORS["BOLD"] + COLORS["UNDERLINE"], f"> Result : {result}", COLORS["ENDC"])
    #     # history.append((user_input, result))


    # except Exception as e:
    #     print(f"Main Error: {e}")

def main(stdscr):
    global history_index, current_input, cursor_position

    DEBUG = sys.argv[1] if len(sys.argv) > 1 else False
    DEBUG = DEBUG == "--debug"
    DEBUG and test_color()
    
    curses.curs_set(1)  # Show the cursor
    stdscr.nodelay(0)   # Block while waiting for user input

    while True:
        key = stdscr.getch()
        if key == ord('q'):  # Exit the program
            break
        elif key == curses.KEY_UP:  # Up arrow key (history backward)
            if history_index > 0:
                history_index -= 1
                current_input = history[history_index]
                cursor_position = len(current_input)
            display_calculator(stdscr)
        elif key == curses.KEY_DOWN:  # Down arrow key (history forward)
            if history_index < len(history) - 1:
                history_index += 1
                current_input = history[history_index]
                cursor_position = len(current_input)
            else:
                current_input = ""
                cursor_position = 0
            display_calculator(stdscr)
        elif key == curses.KEY_LEFT:  # Left arrow key (move cursor left)
            if cursor_position > 0:
                cursor_position -= 1
            display_calculator(stdscr)
        elif key == curses.KEY_RIGHT:  # Right arrow key (move cursor right)
            if cursor_position < len(current_input):
                cursor_position += 1
            display_calculator(stdscr)
        elif key == curses.KEY_BACKSPACE:  # Backspace (delete character)
            if cursor_position > 0:
                current_input = current_input[:cursor_position - 1] + current_input[cursor_position:]
                cursor_position -= 1
            display_calculator(stdscr)
        elif key == curses.KEY_DC or key == 127:  # Delete key (delete at cursor position)
            if cursor_position < len(current_input):
                current_input = current_input[:cursor_position] + current_input[cursor_position + 1:]
            display_calculator(stdscr)
        elif key == curses.KEY_ENTER or key == 10:  # Enter (evaluate expression)
            if current_input:
                result = evaluate_expression(current_input)
                stdscr.addstr(f"\n | eva = {result}\n")

                result = computorv2(stdscr)
                stdscr.addstr(f" | cv2 = {result}\n")

                history.append(current_input)
                history_index = len(history)
                current_input = ""
                cursor_position = 0
                display_result(stdscr, result)
            else :
                display_calculator(stdscr)    
        else:
            # Handle regular characters and add them at the current cursor position
            if key != -1 and chr(key).isprintable():
                current_input = current_input[:cursor_position] + chr(key) + current_input[cursor_position:]
                cursor_position += 1
                display_calculator(stdscr)  

if __name__ == "__main__":
    curses.wrapper(main)