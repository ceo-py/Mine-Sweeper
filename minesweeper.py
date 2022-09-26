import random
import os

ROW = 11
COL = 9
START_ROW = 2
BOMB_NUMBER = 10
field_to_explore = []
CURRENT_PATH = os.getcwd()
PICTURES = {}
directions = {
    "up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0),
    "top left diagonal": (-1, -1), "bottom left diagonal": (-1, 1),
    "top right diagonal": (1, -1), "bottom right diagonal": (1, 1)}


def create_empty_matrix():
    return [[int(0) for x in range(COL)] for _ in range(ROW)]


def load_pictures():
    for file_name in os.listdir("pictures"):
        if not file_name.endswith(".png"):
            continue
        digit = file_name[-5]
        if digit.isdigit():
            PICTURES[int(digit)] = f"{os.getcwd()}\pictures\{file_name}"
        else:
            PICTURES[file_name[:-4]] = f"{os.getcwd()}\pictures\{file_name}"


def check_valid_index(row, col):
    return 0 <= row < ROW and 0 <= col < COL


def generate_bombs(mine_field):
    bombs_pos = []
    while len(bombs_pos) != BOMB_NUMBER:
        bomb_pos = [random.randrange(START_ROW, ROW), random.randrange(0, COL)]
        if bomb_pos not in bombs_pos:
            bombs_pos.append(bomb_pos)

    for row, col in bombs_pos:
        mine_field[row][col] = "*"
    return mine_field


def check_for_bombs_in_range(mine_field):
    for row in range(ROW):
        for col in range(COL):
            if row < START_ROW:
                continue
            if mine_field[row][col] != "*":
                current_sum = 0
                for moving_col, moving_row in directions.values():
                    check_row, check_col = row + moving_row, col + moving_col
                    if check_valid_index(check_row, check_col) and mine_field[check_row][check_col] == "*":
                        current_sum += 1
                mine_field[row][col] = current_sum
    return mine_field


def open_zero_field(row, col):
    if check_valid_index(row, col) and mine_field[row][col].name == 0 and mine_field[row][col].visited == "No":
        for d_row, d_col in directions.values():
            c_row, c_cow = row + d_row, col + d_col
            if check_valid_index(c_row, c_cow) and isinstance(mine_field[c_row][c_cow].name, int) \
                    and mine_field[c_row][c_cow].name > 0:
                mine_field[c_row][c_cow].picture = mine_field[c_row][c_cow].name
                mine_field[row][col].visited = "Yes"
                mine_field[c_row][c_cow].open_field = True

        mine_field[row][col].picture = mine_field[row][col].name
        mine_field[row][col].visited = "Yes"
        mine_field[row][col].open_field = True
        [open_zero_field(row, col) for row, col in
         ((row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col))]


def start_game():
    global mine_field
    mine_field = create_empty_matrix()
    load_pictures()
    mine_field = generate_bombs(mine_field)
    mine_field = check_for_bombs_in_range(mine_field)
    mine_field = create_table(mine_field)
    return mine_field


class Figure:
    flag_counter = BOMB_NUMBER
    alive = True

    def __init__(self, name):
        self.name = name
        self.visited = "No"
        self.open_field = False
        self.got_flag = False
        self.picture = "square"

    def change_flag(self):
        if self.open_field:
            return
        if self.got_flag:
            Figure.flag_counter += 1
            self.got_flag = False
            self.picture = "square"
        else:
            Figure.flag_counter -= 1
            self.got_flag = True
            self.picture = "flag"

    def show_square(self):
        self.picture = self.name


def create_table(mine_field):
    for row in range(ROW):
        for col in range(COL):
            if row in (0, 1) and col == 4:
                mine_field[row][col] = Figure("Menu")
                mine_field[row][col].picture = "square_restart"

            elif row < START_ROW:
                mine_field[row][col] = Figure("Blank")
                mine_field[row][col].picture = "square_b"

            elif mine_field[row][col] != "*":
                symbol = mine_field[row][col]
                mine_field[row][col] = Figure(symbol)
            else:
                mine_field[row][col] = Figure("unclicked_bomb")
    return mine_field
