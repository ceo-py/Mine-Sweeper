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
BACKGROUND = pygame.transform.scale(pygame.image.load(f"{CURRENT_PATH}\pictures\\bg.png"), (WIDTH, HEIGHT))
BEGINNER = pygame.transform.scale(pygame.image.load(f"{CURRENT_PATH}\pictures\\beginner.png"), (200, 100))
running = True
game_stop = False
show_empty_fields = False
mine_field = start_game("beginner")
starting_time = time.time()
menu = True


def game_menu():
    mouse_pos = pygame.mouse.get_pos()
    window.fill("Black")
    window.blit(BACKGROUND, (0, 0))
    # window.blit(BEGINNER, (50, 150))
    window.blit(BEGINNER, (315, 150))
    window.blit(BEGINNER, (580, 150))

    beginner_ = MAIN_FONT.render("BEGINNER", 1, ("red"))
    window.blit(beginner_, (50, 150))
    # beginner
    size_ = beginner_.get_rect(center=(50, 150))
    rect_ = beginner_.get_rect(center=(140, 166))

    # intermediate

    size_i = BEGINNER.get_rect(center=(315, 150))
    rect_i = BEGINNER.get_rect(center=(415, 200))

    # expert

    size_e = BEGINNER.get_rect(center=(580, 150))
    rect_e = BEGINNER.get_rect(center=(680, 200))

    pygame.draw.rect(window, "BLUE", rect_, 4)
    pygame.draw.rect(window, "BLUE", rect_i, 4)
    pygame.draw.rect(window, "BLUE", rect_e, 4)

    print(rect_, rect_.collidepoint(mouse_pos))


    if rect_.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        type_game = "beginner"
        return False, type_game

    elif rect_i.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        type_game = "intermediate"
        return False, type_game

    elif rect_e.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        type_game = "expert"
        return False, type_game

    return True, None


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
            check_square.open_field = True
            if show:
                if check_square.name != "unclicked_bomb" and check_square.got_flag:
                    check_square.name = "flag_wrong"
                    check_square.show_square()
                elif check_square.name == "unclicked_bomb":
                    check_square.show_square()
                    continue

            if check_square.name == "unclicked_bomb":
                check_square.name = "flag"
                check_square.show_square()


def draw_bombs_counter():
    score_text = pygame.font.SysFont("ds-digital", SIZE_R*3).render(f"{Figure.flag_counter:03d}", 1, ("red"))
    window.blit(score_text, (0, 0))


def draw_time_counter():
    # get_size = (HEIGHT / COL) * 3
    game_timer = pygame.font.SysFont("ds-digital", SIZE_R*3).render(f"{timer:03d}", 1, ("red"))
    window.blit(game_timer, (WIDTH - SIZE_C*3, 0))


def draw_square():
    window.fill("Black")
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

    if menu:
        menu, type_game = game_menu()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                continue
        if not menu:
            mine_field = start_game(type_game)
            Figure.flag_counter = GAME_DIFFICULTY[type_game]["bombs"]
            ROW, COL = len(mine_field), len(mine_field[0])
            SIZE_R = HEIGHT // ROW
            SIZE_C = WIDTH // COL
            load_pictures()
            re_scale_all_pictures()

    if c_height != HEIGHT or c_width != WIDTH:
        HEIGHT, WIDTH, change_size = check_min_window_size(c_width, c_height)
        if change_size:
            window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        SIZE_R, SIZE_C = resize_window_parameters(WIDTH, HEIGHT)
        MAIN_FONT = pygame.font.SysFont("ds-digital", SIZE_R)
        load_pictures()
        re_scale_all_pictures()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if menu:
            break
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

                elif symbol.name == 0 and not game_stop:
                    open_zero_field(row, col)

                elif symbol.name == "Menu":
                    menu = True
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

    if not menu:
        draw_square()
    pygame.display.update()
pygame.quit()
