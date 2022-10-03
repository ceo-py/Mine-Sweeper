import pygame
from pygame.locals import *
from minesweeper import *
import time


pygame.init()
FPS = 60
WIDTH = 793
HEIGHT = 793

SIZE_R = HEIGHT // ROW
SIZE_C = WIDTH // COL
MAIN_FONT = pygame.font.SysFont("ds-digital", SIZE_R)
pygame.display.set_caption("Minesweeper beta v0.000000000000002")
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
running = True
game_stop = False
show_empty_fields = False
mine_field = start_game()
starting_time = time.time()


def re_scale_all_pictures():
    for key, link in PICTURES.items():
        PICTURES[key] = pygame.transform.scale(pygame.image.load(link), (SIZE_C, SIZE_R))


def resize_window_parameters(new_width, new_height):
    return new_height // ROW, new_width // COL


def check_min_window_size(c_width, c_height):
    change_size = False
    if c_width < 300:
        c_width = 300
        change_size = True
    if c_height < 300:
        c_height = 300
        change_size = True
    return c_height, c_width, change_size


def clicked_on_bomb(symbol, bomb_pic):
    symbol.name = bomb_pic
    symbol.show_square()
    change_reset_button("square_death")
    game_over_result()
    return True


def check_for_game_winner():
    squares_un_open = 0
    for row in range(START_ROW, ROW):
        for col in range(COL):
            if not mine_field[row][col].open_field:
                squares_un_open += 1
    return squares_un_open


def change_reset_button(status):
    for x in range(2):
        mine_field[x][4].picture = status


def game_over_result(show=True):
    for row in range(START_ROW, ROW):
        for col in range(COL):
            check_square = mine_field[row][col]
            if check_square.open_field:
                continue
            if show:
                if check_square.name != "unclicked_bomb" and check_square.got_flag:
                    print("INside")
                    check_square.name = "flag_wrong"
                check_square.show_square()
            else:
                check_square.picture = "flag"

            check_square.open_field = True


def draw_bombs_counter():
    score_text = MAIN_FONT.render(str(Figure.flag_counter), 1, ("red"))
    window.blit(score_text, (20, 0))


def draw_time_counter():
    game_timer = MAIN_FONT.render(str(timer), 1, ("red"))
    window.blit(game_timer, (WIDTH-80, 0))


def draw_square():
    for row in range(ROW):
        for col in range(COL):
            if row in (0, 1) and col == 4:
                window.blit(PICTURES[mine_field[row][col].picture], (4 * SIZE_C, 0.5 * SIZE_R))
            else:
                window.blit(PICTURES[mine_field[row][col].picture], (col * SIZE_C, row * SIZE_R))
    draw_bombs_counter()
    draw_time_counter()


re_scale_all_pictures()


while running:
    pygame.time.Clock().tick(FPS)
    wrong_flag = None
    c_width, c_height = window.get_size()

    if c_height != HEIGHT or c_width != WIDTH:
        HEIGHT, WIDTH, change_size = check_min_window_size(c_width, c_height)
        if change_size:
            window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        SIZE_R, SIZE_C = resize_window_parameters(WIDTH, HEIGHT)
        MAIN_FONT = pygame.font.SysFont("ds-digital", SIZE_R)
        window.fill("Black")
        load_pictures()
        re_scale_all_pictures()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click, middle_click, right_click = pygame.mouse.get_pressed()
            col, row = [int(x // size) for x, size in zip(pygame.mouse.get_pos(), [SIZE_C, SIZE_R])]
            try:
                symbol = mine_field[row][col]
            except IndexError:
                continue
            if symbol.name == "Blank":
                continue
            if right_click:
                if not symbol.open_field:
                    symbol.change_flag()

            elif left_click:
                if symbol.got_flag:
                    continue

                elif symbol.open_field and not game_stop:
                    show_empty_fields = True
                    wrong_flag, row, col, legal_moves = open_available_square(row, col, *show_available_moves(row, col))
                    symbol = mine_field[row][col]
                    for s_row, s_col in legal_moves:
                        show_element = mine_field[s_row][s_col]
                        show_element.picture = 0

                if symbol.name == "unclicked_bomb" and not game_stop or wrong_flag == "Bomb":
                    game_stop = clicked_on_bomb(symbol, "clicked_bomb")

                elif symbol.name == 0:
                    open_zero_field(row, col)

                elif symbol.name == "Menu":
                    Figure.flag_counter = BOMB_NUMBER
                    mine_field = start_game()
                    re_scale_all_pictures()
                    starting_time = time.time()
                    game_stop = False

                if not game_stop:
                    symbol.show_square()
                    symbol.open_field = True

        if event.type == MOUSEBUTTONUP and show_empty_fields:
            show_empty_fields = False
            for s_row, s_col in legal_moves:
                    show_element = mine_field[s_row][s_col]
                    show_element.picture = "square"

    if not game_stop:
        timer = int(time.time() - starting_time)

    if check_for_game_winner() == BOMB_NUMBER:
        change_reset_button("square_winner")
        game_stop = True
        game_over_result(False)

    draw_square()
    pygame.display.update()
pygame.quit()
