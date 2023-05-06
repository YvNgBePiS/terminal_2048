import math
import time

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
import numpy as np
from pyfiglet import Figlet
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from board_functions import *


empty_cell = "              \n              \n              \n" \
             "              \n              \n"
console = Console()
color_lookup: dict[int, str] = {
    0: "grey93",
    2: "grey93",
    4: "grey78",
    8: "pale_green3",
    16: "yellow4",
    32: "chartreuse4",
    64: "dark_goldenrod",
    128: "green_yellow"
}
symbol_lookup: dict[int, str] = dict()
board: ndarray[int, ...] = np.zeros((4, 4), dtype=int)
score: int

def print_board(board: ndarray[int, ...], score: int, message = None):
    start_time = time.time()

    global symbol_lookup
    global color_lookup
    global console

    caption = f"Your score: {str(score)}"
    if message is not None:
        caption += ", " + message

    table = Table(
        title=f"Play 2048",
        caption=message,
        style="bright_white",
        caption_style="bright_white",
        box=box.ROUNDED,
        padding=0,
        show_header=False,
        show_footer=False,
        show_lines=True,
        width=100
    )

    for i in range(4):
        table.add_column(width=25)

    for i in range(board.shape[0]):
        cells = []
        for j in range(board.shape[1]):
            cell_text = None
            cell_text = Text(symbol_lookup[board[i, j]], justify="center")
            cell_text.stylize(color_lookup[board[i, j]])
            cells.append(cell_text)
        table.add_row(*cells)

    console.clear()
    console.print(table)

    end_time = time.time()
    print(f"\n\ntime to print board: {end_time - start_time}")


def main():
    kb = KeyBindings()

    global symbol_lookup
    # initialize the symbol lookup
    f = Figlet(font='slant')
    symbol_lookup = dict()
    symbol_lookup[0] = empty_cell
    for i in range(1, 12):
        symbol_lookup[int(math.pow(2, i))] = \
            f.renderText(str(int(math.pow(2, i))))

    global board
    board = add_value(board)

    global score
    score = 0

    print_board(board, score)


    @kb.add('q')
    def exit_(event):
        """
        Pressing Ctrl-Q will exit the user interface.

        Setting a return value means: quit the event loop that drives the user
        interface and return this value from the `Application.run()` call.
        """
        event.app.exit()

    @kb.add('w')
    def move_up(event):
        global console
        global board
        global score
        if is_valid_move(board, 0):
            board, score = make_move(board, score, 0)
            board = add_value(board)
            print_board(board, score)
            if not has_valid_move(board):
                event.app.exit()
        else:
            print_board(board, score, "up is not a valid move")


    @kb.add("d")
    def move_right(event):
        global console
        global board
        global score
        if is_valid_move(board, 1):
            board, score = make_move(board, score, 1)
            board = add_value(board)
            print_board(board, score)
            if not has_valid_move(board):
                event.app.exit()
        else:
            print_board(board, score, "right is not a valid move")

    @kb.add("s")
    def move_down(event):
        global console
        global board
        global score
        if is_valid_move(board, 2):
            board, score = make_move(board, score, 2)
            board = add_value(board)
            print_board(board, score)
            if not has_valid_move(board):
                event.app.exit()
        else:
            print_board(board, score, "down is not a valid move")

    @kb.add("a")
    def move_left(event):
        global console
        global board
        global score
        if is_valid_move(board, 3):
            board, score = make_move(board, score, 3)
            board = add_value(board)
            print_board(board, score)
            if not has_valid_move(board):
                event.app.exit()
        else:
            print_board(board, score, "left is not a valid move")

    app = Application(key_bindings=kb, full_screen=True)
    app.run()

if __name__ == "__main__":
    main()
