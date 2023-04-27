import math
import random
# import keyboard   requires root access, not pog
from sshkeyboard import listen_keyboard, stop_listening
import time
import rich
from rich.console import Console
from rich import print as rprint

from rich.table import Table
from rich.text import Text
from rich import box

from pyfiglet import Figlet


last_key: str
console: Console
color_lookup: dict[int, str] = {
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
    global symbol_lookup
    f = Figlet(font='slant')
    for i in range(1, 12):
        symbol_lookup[int(math.pow(2, i))] = f.renderText(str(int(math.pow(2, i))))

    for key, value in symbol_lookup.items():
        # print(key, "\n", value)
        print(value)

    # initialize the board
    board: list[list[int]] = list()
    for i in range(4):
        board.append(list())
        for j in range(4):
            board[i].append(0)
    print(board)

    # randomly assign two spots on the board with the starting values
    cords1: tuple[int, int] = (random.randint(0, 3), random.randint(0, 3))
    cords2: tuple[int, int] = cords1
    while cords2 == cords1:
        cords2 = (random.randint(0, 3), random.randint(0, 3))
    print(cords1)
    print(cords2)

    global last_key
    last_key = "default"

    listen_keyboard(on_press=press, sequential=True)
    print(last_key)

    board[0][0] = 128
    board[0][1] = 64
    board[0][2] = 32
    board[0][3] = 16
    board[1][3] = 8
    board[1][2] = 4
    board[1][1] = 2
    board[1][0] = 2

    print_board(board, console, 1234)

    end_time = time.time()
    print(f'total time is: {end_time - start_time} seconds')


def press(key: str):
    if key in ['w', 'a', 's', 'd']:
        print(f'{key} was pressed')
        rprint('[bold magenta]' + key + '[/bold magenta] was pressed')
        global last_key
        last_key = key
        stop_listening()

# board is passed by variable, means that since board is a mutable object I can change its contents
# and the changes will be preserved in main
# def shift_up(board: list[list[int]]):
#     # for each column
#     for j in range(4):
#         index = 0
#         while index < 3:
#             if board[index][j] == board[index + 1][j]:
#                 # merge the two similar cells in the column and then
#
# def merge_up(board: list[list[int]]):
    


def print_board(board: list[list[int]], input_console: Console, score: int):
    # input_console.clear()
    # input_console.rule('[bright_white]Play 2048', align='center', style='green_yellow')
    # input_console.print()
    # input_console.print('----------------------------', style='bright_white', justify='center')
    # input_console.print('|')
    start_time = time.time()

    global color_lookup

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

    for i in range(4):
        cells = []
        for j in range(4):
            cell_text = None
            if board[i][j] != 0:
                cell_text = Text(str(board[i][j]), justify="center")
                cell_text.stylize(color_lookup[board[i][j]])
            else:
                cell_text = Text("")
            cells.append(cell_text)
        table.add_row(*cells)

    input_console.clear()
    input_console.print(table)

    end_time = time.time()
    print(f"\n\ntime to print board: {end_time - start_time}")


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
