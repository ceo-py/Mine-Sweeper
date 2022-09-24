import pygame
from pygame.locals import *
from minesweeper import *

FPS = 60
pygame.init()
WIDTH = 400
HEIGHT = 400
pygame.display.set_caption("Minesweeper beta v0.000000000000001")
window = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
SIZE = WIDTH / ROW


def re_scale_all_pictures():
    for key, link in PICTURES.items():
        PICTURES[key] = pygame.transform.scale(pygame.image.load(link), (SIZE, SIZE))


def game_over_result():
    for row in range(START_ROW, ROW):
        for col in range(COL):
            mine_field[row][col].show_square()


def draw_pawns():
    for row in range(START_ROW, ROW):
        for col in range(COL):
            window.blit(PICTURES[mine_field[row][col].picture], (col * SIZE, row * SIZE))


re_scale_all_pictures()


while running:
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click, middle_click, right_click = pygame.mouse.get_pressed()
            col, row = [int(x // SIZE) for x in pygame.mouse.get_pos()]
            symbol = mine_field[row][col]

            if right_click:
                if not symbol.open_field:
                    symbol.change_flag()

            elif left_click:
                if symbol.got_flag or symbol.open_field:
                    continue
                if symbol.name == "unclicked_bomb":
                    symbol.name = "clicked_bomb"
                    game_over_result()
                elif symbol.name == 0:
                    open_zero_field(row, col)

                symbol.show_square()
                symbol.open_field = True


    draw_pawns()
    pygame.display.update()
pygame.quit()
