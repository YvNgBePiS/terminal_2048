import curses
import io
import time

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

def main():

    # initialize curses
    screen = curses.initscr()
    curses.noecho() # turn off key echoing
    curses.cbreak() # respond to keys immediately (don't wait for Enter)
    # screen.keypad(True) # enable arrow keys

    # # set up initial position of character
    # row, col = 10, 10
    #
    # while True:
    #     # draw the character at its current position
    #     screen.addch(row, col, '@')
    #
    #     # get user input
    #     key = screen.getch()
    #
    #     # move the character based on input
    #     if key == curses.KEY_UP:
    #         row -= 1
    #     elif key == curses.KEY_DOWN:
    #         row += 1
    #     elif key == curses.KEY_LEFT:
    #         col -= 1
    #     elif key == curses.KEY_RIGHT:
    #         col += 1
    #     elif key == ord('q'):
    #         break
    #
    #     # clear the screen and move the cursor back to the top left
    #     screen.clear()
    #     screen.move(0, 0)


    console = Console(file=io.StringIO())
    table = Table(
        title="My 4x4 Table",
        style="bright_white",
        caption_style="bright_white",
        box=box.ROUNDED,
        padding=0,
        show_header=False,
        show_footer=False,
        show_lines=True
    )

    # Add four columns with a minimum width of 14 characters
    for i in range(4):
        table.add_column(justify="center", min_width=14)

    # Add four rows to the table
    for i in range(4):
        row = table.add_row("'   _____ __ __\n  / ___// // /\n / __ \\/ // /_\n/ /_/ /__  __/\n\\____/  /_/   \n              \n'", "", "", "")
        # for cell in row.cells:
        #     cell.min_height = 5
    # Print the table
    console.print(table)
    output = console.file.getvalue()
    screen.addstr(f"size of output: {len(output)}")
    screen.addstr(output)
    screen.refresh()
    time.sleep(5)



    # console.print(table)
    #
    # # print("\n\n======\n")
    # screen.addstr("\n\n======\n")
    # with console.capture() as capture:
    #     console.print(table)
    # capture_str = capture.get()
    # # print("capture string length: ", len(capture_str))
    # screen.addstr("capture string length: ", len(capture_str))
    # # for i in range(10):
    # #     print("a")
    # # print("capture string type: ", type(capture_str))
    # # print("num returns: ", len(capture_str.split("\n")))
    # # print("printing line by line seprarated by ==========")
    # for line in capture_str.split("\n"):
    #     # print(line)
    #     screen.addstr(line)
    #     # print("==========")


    # # clean up curses before exiting
    curses.nocbreak()
    # screen.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    main()