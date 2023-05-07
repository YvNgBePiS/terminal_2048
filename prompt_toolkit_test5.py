import math
import time
import io

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Container, Window, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea

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
color_lookup: dict[int, str] = {
    0: "grey93",
    2: "grey93",
    4: "grey78",
    8: "pale_green3",
    16: "yellow4",
    32: "chartreuse4",
    64: "dark_goldenrod",
    128: "green_yellow",
    256: "medium_spring_green",
    512:"cyan2",
    1024:"cyan1",
    2048:"bright_cyan"
}
symbol_lookup: dict[int, str] = dict()
board: ndarray[int, ...] = np.zeros((4, 4), dtype=int)
score: int

def main():
    global symbol_lookup
    # initialize the symbol lookup
    # f = Figlet(font='slant')
    f = Figlet(font='avatar')
    # f = Figlet(font='starwars')
    symbol_lookup = dict()
    symbol_lookup[0] = empty_cell
    for i in range(1, 12):
        symbol_lookup[int(math.pow(2, i))] = \
            f.renderText(str(int(math.pow(2, i))))

    global board
    board = add_value(board)

    global score
    score = 0

    # control = FormattedTextControl(get_board_str(board, score))
    # control = TextArea(get_board_str(board, score))
    # layout = Window(content=control)
    # control = FormattedTextControl(text=get_board_str(board, score))
    # window = Window(content=control)
    text_area = TextArea(text=get_board_str(board, score), wrap_lines=False)
    root_container = VSplit([text_area])
    layout = Layout(root_container)


    def update_board(key: str):
        key_to_direction_index = {"w": 0, "d": 1, "s": 2, "a": 3}
        key_to_direction_str = {"w": "up", "d":"right", "s":"down", "a":"left"}
        global board
        global score
        if is_valid_move(board, key_to_direction_index[key]):
            board, score = make_move(board, score, key_to_direction_index[key])
            board = add_value(board)
            text_area.text = get_board_str(board, score)
        else:
            text_area.text = get_board_str(board, score, message=f"{key_to_direction_str[key]} is not a valid move")

    bindings = KeyBindings()
    @bindings.add("w")
    @bindings.add("d")
    @bindings.add("s")
    @bindings.add("a")
    def _(event):
        update_board(event.key_sequence[0].key)
        global board
        if not has_valid_move(board):
            event.app.exit()

    @bindings.add("q")
    def exit_(event):
        event.app.exit()

    # Create the application instance with the layout and key bindings.
    app = Application(layout=layout, key_bindings=bindings)

    # Run the application.
    app.run()


def get_board_str(board: ndarray[int, ...], score: int, message = None) -> str:
    global symbol_lookup
    global color_lookup

    caption = f"Your score: {str(score)}"
    if message is not None:
        caption += ", " + message

    table = Table(
        title=f"Play 2048",
        caption=caption,
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

    # buffer = io.StringIO()
    # temp_console = Console(file=buffer)
    # temp_console.print(table)
    # return buffer.getvalue()

    buffer = io.StringIO()
    temp_console = Console(file=buffer)
    with temp_console.capture() as capture:
        temp_console.print(table)
    return capture.get()

if __name__ == "__main__":
    main()