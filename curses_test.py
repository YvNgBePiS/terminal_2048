import curses


def main():

    # initialize curses
    screen = curses.initscr()
    curses.noecho() # turn off key echoing
    curses.cbreak() # respond to keys immediately (don't wait for Enter)
    screen.keypad(True) # enable arrow keys

    # set up initial position of character
    row, col = 10, 10

    while True:
        # draw the character at its current position
        screen.addch(row, col, '@')

        # get user input
        key = screen.getch()

        # move the character based on input
        if key == curses.KEY_UP:
            row -= 1
        elif key == curses.KEY_DOWN:
            row += 1
        elif key == curses.KEY_LEFT:
            col -= 1
        elif key == curses.KEY_RIGHT:
            col += 1
        elif key == ord('q'):
            break

        # clear the screen and move the cursor back to the top left
        screen.clear()
        screen.move(0, 0)

    # clean up curses before exiting
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    main()