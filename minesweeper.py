import random
import os

ROW = 9
COL = 9
START_ROW = 0
bombs_number = 10
field_to_explore = []
CURRENT_PATH = os.getcwd()
PICTURES = {}
bombs_pos = []
directions = {
    "up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0),
    "top left diagonal": (-1, -1), "bottom left diagonal": (-1, 1),
    "top right diagonal": (1, -1), "bottom right diagonal": (1, 1)}
mine_field = [[int(x) for x in "0" * COL] for _ in range(ROW)]


def load_pictures():
    for file_name in os.listdir("Pictures"):
        if not file_name.endswith(".png"):
            continue
        digit = file_name[-5]
        if digit.isdigit():
            PICTURES[int(digit)] = f"{os.getcwd()}\pictures\{file_name}"
        else:
            PICTURES[file_name[:-4]] = f"{os.getcwd()}\pictures\{file_name}"


def check_valid_index(row, col):
    return 0 <= row < ROW and 0 <= col < COL


def generate_bombs():
    while len(bombs_pos) != bombs_number:
        bomb_pos = [random.randrange(START_ROW, ROW), random.randrange(0, COL)]
        if bomb_pos not in bombs_pos:
            bombs_pos.append(bomb_pos)

    for row, col in bombs_pos:
        mine_field[row][col] = "*"


load_pictures()
generate_bombs()


def check_for_bombs_in_range(row, col):
    current_sum = 0
    for moving_col, moving_row in directions.values():
        check_row, check_col = row + moving_row, col + moving_col
        if check_valid_index(check_row, check_col) and mine_field[check_row][check_col] == "*":
            current_sum += 1
            mine_field[row][col] = current_sum


for row in range(START_ROW, ROW):
    for col in range(COL):
        if mine_field[row][col] != "*":
            check_for_bombs_in_range(row, col)


def open_zero_field(row, col):
    if check_valid_index(row, col) and mine_field[row][col].name == 0 and mine_field[row][col].visited == "No":
        mine_field[row][col].picture = mine_field[row][col].name
        mine_field[row][col].visited = "Yes"
        mine_field[row][col].open_field = True
        [open_zero_field(row, col) for row, col in ((row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col))]


class Figure:
    def __init__(self, name, position):
        self.name = name
        self.visited = "No"
        self.open_field = False
        self.got_flag = False
        self.picture = "square"

    def change_flag(self):
        if self.got_flag:
            self.got_flag = False
            self.picture = "square"
        else:
            self.got_flag = True
            self.picture = "flag"

    def show_square(self):
        self.picture = self.name

    def clicked_field(self):
        self.open_field = True


for row in range(START_ROW, ROW):
    for col in range(COL):
        if mine_field[row][col] != "*":
            symbol = mine_field[row][col]
            mine_field[row][col] = Figure(symbol, (row, col), )
        else:
            mine_field[row][col] = Figure("unclicked_bomb", (row, col), )

# [print(*mine_field[row]) for row in range(ROW)]
