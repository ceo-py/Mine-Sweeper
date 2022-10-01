import pygame
from pygame.locals import *
from minesweeper import *
import time


pygame.init()
FPS = 60
WIDTH = 400
HEIGHT = 400
MAIN_FONT = pygame.font.SysFont("comicsans", 50)
SIZE_R = HEIGHT // ROW
SIZE_C = WIDTH // COL
pygame.display.set_caption("Minesweeper beta v0.000000000000001")
window = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
winner = False
mine_field = start_game()
starting_time = time.time()


def re_scale_all_pictures():
    for key, link in PICTURES.items():
        PICTURES[key] = pygame.transform.scale(pygame.image.load(link), (SIZE_C, SIZE_R))


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
            if not mine_field[row][col].open_field:
                if show:
                    mine_field[row][col].show_square()
                mine_field[row][col].open_field = True


def draw_bombs_counter():
    score_text = MAIN_FONT.render(str(Figure.flag_counter), 1, ("red"))
    window.blit(score_text, (20, 0))


def draw_time_counter(show=True):
    if show:
        game_timer = MAIN_FONT.render(str(timer), 1, ("red"))
        window.blit(game_timer, (300, 0))


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
    timer = int(time.time() - starting_time)
    wrong_flag = None
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click, middle_click, right_click = pygame.mouse.get_pressed()
            col, row = [x // size for x, size in zip(pygame.mouse.get_pos(), [SIZE_C, SIZE_R])]
            symbol = mine_field[row][col]
            if symbol.name == "Blank":
                continue
            if right_click:
                if not symbol.open_field:
                    symbol.change_flag()

            elif left_click:
                if symbol.got_flag:
                    continue

                elif symbol.open_field and not winner:
                    wrong_flag, row, col = open_available_square(row, col, *show_available_moves(row, col))
                    symbol = mine_field[row][col]

                if symbol.name == "unclicked_bomb" and not winner or wrong_flag == "Bomb":
                    symbol.name = "clicked_bomb"
                    change_reset_button("square_death")
                    game_over_result()

                elif symbol.name == 0:
                    open_zero_field(row, col)

                elif symbol.name == "Menu":
                    Figure.flag_counter = BOMB_NUMBER
                    mine_field = start_game()
                    re_scale_all_pictures()
                    starting_time = time.time()
                    winner = False

                if not winner:
                    symbol.show_square()
                    symbol.open_field = True

    if check_for_game_winner() == BOMB_NUMBER:
        change_reset_button("square_winner")
        winner = True
        game_over_result(False)

    draw_square()
    pygame.display.update()
pygame.quit()
