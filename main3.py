import math
import random
# import keyboard   requires root access, not pog
# from sshkeyboard import listen_keyboard, stop_listening
import time
import rich
from rich.console import Console
from rich import print as rprint

from rich.table import Table
from rich.text import Text
from rich import box

from pyfiglet import Figlet

import numpy as np
from numpy import ndarray
import curses

# test = "/ /_/ /__  __/"
# temp = "              "
empty_cell = "              \n              \n              \n              \n              \n"
console: Console
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


def main():
    start_time: float = time.time()
    end_time: float

    global console
    console = Console()
    print(console.encoding)
    print(console.color_system)

    # initialize the symbol lookup
    f = Figlet(font='slant')
    global symbol_lookup
    symbol_lookup = dict()
    # symbol_lookup[0] = f.renderText(str(0))
    symbol_lookup[0] = empty_cell
    for i in range(1, 12):
        symbol_lookup[int(math.pow(2, i))] = f.renderText(str(int(math.pow(2, i))))

    # for key, value in symbol_lookup.items():
    #     print(key, "\n", value, "\n\n")

    moves = {0: "up", 1: "right", 2: "down", 3: "left"}
    board = np.zeros((4, 4), dtype=int)
    score = 0

    screen = curses.initscr()
    curses.noecho()  # turn off key echoing
    curses.cbreak()  # respond to keys immediately (don't wait for Enter)

    board = add_value(board)
    print_board(board, score)
    time.sleep(5)
    while has_valid_move(board):
        move = np.random.choice(4, p=[.4, .4, .1, .1])
        while not is_valid_move(board, move):
            move = np.random.choice(4, p=[.4, .4, .1, .1])

        # console.print("chose move: ", moves[move])
        # board, score = make_move(board, score, move)
        # board = add_value(board)
        # print_board(board, score)
        with console.capture() as capture:
            console.print("chose move: ", moves[move])
            board, score = make_move(board, score, move)
            board = add_value(board)
            print_board(board, score)

        # print(capture.get().strip("\n"))
        for line in capture.get().split("\n"):
            print(line)
        time.sleep(0.5)

    end_time = time.time()
    print(f'total time is: {end_time - start_time} seconds')

    # clean up curses before exiting
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def print_board(board: ndarray[int, ...], score: int):
    # input_console.clear()
    # input_console.rule('[bright_white]Play 2048', align='center', style='green_yellow')
    # input_console.print()
    # input_console.print('----------------------------', style='bright_white', justify='center')
    # input_console.print('|')
    start_time = time.time()

    global symbol_lookup
    global color_lookup
    global console

    table = Table(
        title=f"Play 2048",
        caption=f"Your score: {str(score)}",
        style="bright_white",
        caption_style="bright_white",
        box=box.ROUNDED,
        padding=0,
        show_header=False,
        show_footer=False,
        show_lines=True
    )

    for i in range(board.shape[0]):
        cells = []
        for j in range(board.shape[1]):
            cell_text = None
            # print("this is the symbol: ", board[i, j], " , as a string: ", str(board[i, j]), "\n")
            # print("this is the lookup: \n")
            # print(symbol_lookup[board[i, j]])
            cell_text = Text(symbol_lookup[board[i, j]], justify="center")
            cell_text.stylize(color_lookup[board[i, j]])
            cells.append(cell_text)
        table.add_row(*cells)

    console.clear()
    console.print(table)

    end_time = time.time()
    print(f"\n\ntime to print board: {end_time - start_time}")


def has_open_space(board: ndarray[int, ...]) -> bool:
    return np.any(board == 0)


def is_valid_move(board: ndarray[int, ...], direction: int) -> bool:
    new_matrix, _ = make_move(board, 0, direction)
    return not np.array_equal(new_matrix, board)


def has_valid_move(board: ndarray[int, ...]) -> bool:
    # return is_valid_move(board, 0) or is_valid_move(board, 1) or is_valid_move(board, 2) or is_valid_move(board, 3)
    return any(is_valid_move(board, direction) for direction in range(4))


def add_value(board: ndarray[int, ...]) -> ndarray[int, ...]:
    # make a list of all the empty spaces in the
    empty_spaces = list(zip(np.where(board == 0)[0], np.where(board == 0)[1]))
    # empty_spaces = np.argwhere(board == 0)
    random_index = np.random.choice(len(empty_spaces))
    new_board = board.copy()
    new_board[empty_spaces[random_index]] = np.random.choice([2, 4], p=[2 / 3, 1 / 3])
    return new_board


def make_move(board: ndarray[int, ...], current_score: int, direction: int) -> tuple[ndarray[int, ...], int]:
    # 0: up, 1: right, 2: down, 3: left
    new_board = np.copy(board)
    new_board = np.rot90(new_board, k=direction)
    shifted_board = shift(new_board)
    joined_board, score_change = join(shifted_board)
    return_board = np.rot90(joined_board, k=(4 - direction))
    return return_board, current_score + score_change


def shift(board: ndarray[int, ...]) -> ndarray[int, ...]:
    new_board = np.copy(board)
    for column in range(board.shape[1]):
        top_row = 0  # stores the row of the highest zero element
        for row in range(board.shape[0]):
            if new_board[row, column] != 0:
                new_board[(top_row, row), (column, column)] = new_board[(row, top_row), (column, column)]
                top_row += 1
    return new_board


def join(board: ndarray[int, ...]) -> tuple[ndarray[int, ...], int]:
    new_board = np.copy(board)
    score_change = 0
    for column in range(board.shape[1]):
        for row in range(board.shape[0] - 1):
            if new_board[row, column] == new_board[row + 1, column] and new_board[row, column] != 0:
                new_board[row, column] += new_board[row + 1, column]
                score_change += new_board[row, column]
                new_board[row + 1, column] = 0
                new_board[(row + 1):, column] = np.roll(new_board[(row + 1):, column], -1)
    return new_board, score_change


"""
moves = {0: "up", 1: "right", 2: "down", 3: "left"}


board = np.zeros((4,4), dtype=int)
board = add_value(board)
score = 0
print(board, f"\nscore: {score}\n")
while has_valid_move(board):
    move = np.random.choice(4, p=[.4, .4, .1, .1])
    while not is_valid_move(board, move):
        move = np.random.choice(4, p=[.4, .4, .1, .1])
    print("chose move: ", moves[move])
    board, score = make_move(board, score, move)
    board = add_value(board)
    print(board, f"\nscore: {score}\n")
"""

"""    for i in range(board.shape[0]):
        cells = []
        for j in range(board.shape[1]):
            cell_text = None
            if board[i][j] != 0:
                # cell_text = Text(str(board[i][j]), justify="center")
                cell_text = Text(symbol_lookup[board[i, j]], justify="center")
                cell_text.stylize(color_lookup[board[i][j]])
            else:
                cell_text = Text("")
            cells.append(cell_text)
        table.add_row(*cells)

    console.clear()
    console.print(table)"""

if __name__ == "__main__":
    main();

"""
    color_lookup: dict[int, str] = {
        2: "grey37 on light_cyan3",
        4: "grey37 on light_steel_blue",
        8: "bright_white on pale_green3",
        16: "bright_white on yellow4",
        32: "bright_white on chartreuse4",
        64: "bright_white on dark_goldenrod",
        128: "bright_white on green_yellow"
    }
    
    
    rprint("[bold italic yellow on red blink]This text is impossible to read")
"""
