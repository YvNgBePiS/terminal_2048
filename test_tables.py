from rich.table import Table, Column
from rich import box
from rich.console import Console

def main():
    # Create a 4x4 table with minimum cell width of 14 characters

    console = Console()
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
        row = table.add_row("", "", "", "")
        for cell in row.cells:
            cell.min_height = 5
    # Print the table
    console.print(table)


if __name__ == "__main__":
    main()