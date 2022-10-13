import pygame
from pygame.locals import *
from minesweeper import *
import json
import time

pygame.init()
FPS = 60
WIDTH = 793
HEIGHT = 793
BUTTON_STATE = "square_restart"
SIZE_R = HEIGHT // ROW
SIZE_C = WIDTH // COL
MAIN_FONT = pygame.font.SysFont("ds-digital", int(SIZE_R))
pygame.display.set_caption("Minesweeper beta v0.000000000000002")
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
BEGINNER = pygame.transform.scale(pygame.image.load(f"{CURRENT_PATH}\pictures\\beginner.png"), (200, 100))
running = True
game_stop = False
show_empty_fields = False
mine_field = start_game("beginner")
starting_time = time.time()
timer = 0
click_counter = 0
PLAYER_NAME = "anonymous"
menu = True
user_name = MAIN_FONT.render(PLAYER_NAME, 1, ("red"))
high_score_board = {}


def show_high_score():
    a = 0.65
    for game_type in high_score_board:
        for score in high_score_board[game_type]:
            if game_type == "beginner":
                button_show(score, "green", WIDTH * 0.33, HEIGHT * a)
                a += 0.05


def load_high_score(result):
    for game in result:
        for show in sorted(result[game], key=lambda x: (x['time'], x['mouse clicks'], x['player']))[:8]:
            high_score_board[game] = high_score_board.get(game, []) + [f"{show['player']} - {show['time']}"]


def button_show(text, color, pos_row, pos_col):
    mouse_pos = pygame.mouse.get_pos()
    text_font = pygame.font.SysFont("ds-digital", int(SIZE_R))
    user_name = text_font.render(text, 1, (color))
    rect_collide = user_name.get_rect(center=(pos_row, pos_col))
    if rect_collide.collidepoint(mouse_pos):
        user_name = text_font.render(text, 1, ("blue"))


    window.blit(user_name, rect_collide)

    # pygame.draw.rect(window, "BLUE", rect_collide, 4)
    return rect_collide


def game_menu():
    mouse_pos = pygame.mouse.get_pos()
    left_click, *_ = pygame.mouse.get_pressed()
    window.fill("Grey")
    BACKGROUND = pygame.transform.scale(pygame.image.load(f"{CURRENT_PATH}\pictures\\bg.png"), (WIDTH, HEIGHT))

    window.blit(BACKGROUND, (0, 0))

    button_show(PLAYER_NAME, "red", WIDTH / 2, HEIGHT * 0.05)

    beginner_pos = button_show("Beginner", "green", WIDTH * 0.16, HEIGHT * 0.35)
    intermediate = button_show("Intermediate", "yellow", WIDTH * 0.55, HEIGHT * 0.35)
    expert = button_show("Expert", "red", WIDTH * 0.85, HEIGHT * 0.35)

    show_high_score()

    if beginner_pos.collidepoint(mouse_pos) and left_click:
        type_game = "beginner"
        return False, type_game

    elif intermediate.collidepoint(mouse_pos) and left_click:
        type_game = "intermediate"
        return False, type_game

    elif expert.collidepoint(mouse_pos) and left_click:
        type_game = "expert"
        return False, type_game

    return True, None


def typing_name(event, PLAYER_NAME):
    if event.type == pygame.KEYDOWN:
        letters = len(PLAYER_NAME)
        if event.key == pygame.K_BACKSPACE:
            if letters != 0:
                PLAYER_NAME = PLAYER_NAME[:-1]
        else:
            if letters < 9 and event.unicode.isascii() and event.key != pygame.K_RETURN:
                PLAYER_NAME += event.unicode
    return PLAYER_NAME


def high_score(game_type, show_result=False):
    with open("high_score.json", "r+", encoding='utf-8') as json_file:
        result = json.load(json_file)
        if show_result:
            return load_high_score(result)
        result[game_type].append({"player": PLAYER_NAME, "time": timer, "mouse clicks": click_counter})
        [print(f"{show['player']} - {show['time']}") for show in
         sorted(result[game_type], key=lambda x: (x['time'], x['mouse clicks'], x['player']))[:8]]

        json_file.seek(0)
        json.dump(result, json_file, indent=9)


def reset_button_state():
    # size_i = PICTURES[BUTTON_STATE].get_rect(center=(WIDTH / 2, SIZE_R))
    # pygame.draw.rect(window, "BLUE", size_i, 4)
    window.blit(PICTURES[BUTTON_STATE], (WIDTH / 2 - SIZE_C, 0))


def re_scale_all_pictures():
    for key, link in PICTURES.items():
        if key in ("square_restart", "square_death", "square_winner"):
            PICTURES[key] = pygame.transform.scale(pygame.image.load(link), (SIZE_C * 2, SIZE_R * 2))
            continue
        PICTURES[key] = pygame.transform.scale(pygame.image.load(link), (SIZE_C, SIZE_R))


def resize_window_parameters(new_width, new_height):
    return new_height / ROW, new_width / COL


def check_min_window_size(c_width, c_height):
    change_size = False
    if c_width < 400:
        c_width = 400
        change_size = True
    if c_height < 400:
        c_height = 400
        change_size = True
    return c_height, c_width, change_size


def clicked_on_bomb(symbol, bomb_pic):
    symbol.name = bomb_pic
    symbol.show_square()
    game_over_result()
    return True


def check_for_game_winner():
    squares_un_open = 0
    for row in range(START_ROW, ROW):
        for col in range(COL):
            if not mine_field[row][col].open_field:
                squares_un_open += 1
    return squares_un_open


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
    score_text = pygame.font.SysFont("ds-digital", int(SIZE_R * 3)).render(f"{Figure.flag_counter:03d}", 1, ("red"))
    window.blit(score_text, (0, 0))


def draw_time_counter():
    # get_size = (HEIGHT / COL) * 3
    game_timer = pygame.font.SysFont("ds-digital", int(SIZE_R * 3)).render(f"{timer:03d}", 1, ("red"))

    # size_e = game_timer.get_rect(center=(WIDTH - SIZE_R * 3 * 1.2, 0))
    #
    # pygame.draw.rect(window, "BLUE", size_e, 4)
    window.blit(game_timer, (WIDTH - SIZE_R * 3 * 1.2, 0))


def draw_square():
    window.fill("Grey")
    for row in range(2, ROW):
        for col in range(COL):
            window.blit(PICTURES[mine_field[row][col].picture], (col * SIZE_C, row * SIZE_R))

    reset_button_state()
    draw_bombs_counter()
    draw_time_counter()


re_scale_all_pictures()
# high_score("_", True)


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
            PLAYER_NAME = typing_name(event, PLAYER_NAME)

        if not menu:
            mine_field = start_game(type_game)
            Figure.flag_counter = GAME_DIFFICULTY[type_game]["bombs"]
            BOMB_NUMBER = GAME_DIFFICULTY[type_game]["bombs"]
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
        MAIN_FONT = pygame.font.SysFont("ds-digital", int(SIZE_R))
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
                click_counter += 1

                if symbol.got_flag:
                    continue

                if click_counter == 1:
                    starting_time = time.time()

                elif symbol.open_field and not game_stop:
                    show_empty_fields = True
                    wrong_flag, row, col, legal_moves = open_available_square(row, col, *show_available_moves(row, col))
                    symbol = mine_field[row][col]
                    for s_row, s_col in legal_moves:
                        show_element = mine_field[s_row][s_col]
                        show_element.picture = 0

                if symbol.name == "unclicked_bomb" and not game_stop or wrong_flag == "Bomb":
                    BUTTON_STATE = "square_death"
                    game_stop = clicked_on_bomb(symbol, "clicked_bomb")

                elif symbol.name == 0 and not game_stop:
                    open_zero_field(row, col)

                if not game_stop:
                    symbol.show_square()
                    symbol.open_field = True

        if event.type == MOUSEBUTTONUP and show_empty_fields:
            show_empty_fields = False
            for s_row, s_col in legal_moves:
                show_element = mine_field[s_row][s_col]
                show_element.picture = "square"

    if not game_stop and click_counter > 0:
        timer = int(time.time() - starting_time)

    if check_for_game_winner() == BOMB_NUMBER:
        print(type_game)
        BUTTON_STATE = "square_winner"
        print(click_counter, timer)
        game_stop = True
        game_over_result(False)
        Figure.flag_counter = 0
        high_score(type_game)

    if not menu:
        draw_square()

    if PICTURES[BUTTON_STATE].get_rect(center=(WIDTH / 2, SIZE_R)).collidepoint(pygame.mouse.get_pos()) and \
            pygame.mouse.get_pressed()[0]:
        menu = True
        BUTTON_STATE = "square_restart"
        timer, click_counter = 0, 0
        game_stop = False
        SIZE_R, SIZE_C = 72, 72

    pygame.display.update()
pygame.quit()
