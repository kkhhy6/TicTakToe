import pygame
import sys
import numpy as np

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1300
HEIGHT = 1300

BG_COLOUR = (28, 170, 156)
LINE_COLOUR = (23, 145, 135)
ACTIVE_LINE_COLOUR = (0, 145, 152)
CIRCLE_COLOUR = (239, 231, 200)
CROSS_COLOUR = (66, 66, 66)

small_l_stage = 0
big_l_stage = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('TIC TAC TOE')

WIDTH, HEIGHT = pygame.display.get_surface().get_size()
TILE_SIZE = HEIGHT / 13
SPACE = TILE_SIZE / 4

board = np.zeros((14, 14))
borders = [4, 8]
active_boards = np.ones((3, 3))

player = 1
play = True


def draw_board(tile, stage, start_x, start_y, width, colour):

    if stage < 3 * tile:
        stage += tile / 20
    else:
        stage = 3 * tile

    pygame.draw.line(screen, colour, (start_x, start_y + tile), (start_x + stage, start_y + tile), width)
    pygame.draw.line(screen, colour, (start_x, start_y + tile * 2), (start_x + stage, start_y + tile * 2), width)

    pygame.draw.line(screen, colour, (start_x + tile, start_y), (start_x + tile, start_y + stage), width)
    pygame.draw.line(screen, colour, (start_x + tile * 2, start_y), (start_x + tile * 2, start_y + stage), width)

    return stage


def draw_big_board(tile, off_x, off_y, small_stage, big_stage, width):

    for row in range(3):
        for col in range(3):
            if active_boards[row][col] == 1:
                small_stage = draw_board(tile, small_stage, tile + tile * 4 * row + OFF_X, tile + tile * 4 * col + OFF_Y, width, ACTIVE_LINE_COLOUR)
            else:
                small_stage = draw_board(tile, small_stage, tile + tile * 4 * row + off_x, tile + tile * 4 * col + off_y, width, LINE_COLOUR)

    if big_stage < 12 * tile:
        big_stage += 12 * tile / 20
    else:
        big_stage = 12 * tile

    draw_board(tile * 4, big_stage, tile / 2 + off_x, tile / 2 + off_y, 2 * width, LINE_COLOUR)

    return small_stage, big_stage


def find_active(pos):
    pos_0 = [1, 5, 9]
    pos_1 = [2, 6, 10]

    if pos in pos_0:
        return 0
    elif pos in pos_1:
        return 1
    return 2


def check_active_board(pos):
    pos_0 = [1, 2, 3]
    pos_1 = [5, 6, 7]
    pos_2 = [9, 10, 11]

    if pos in pos_0:
        return 0
    elif pos in pos_1:
        return 1
    elif pos in pos_2:
        return 2


def mark_active_board(col, row):
    if active_boards[find_active(col)][find_active(row)] == 0 or active_boards[find_active(col)][find_active(row)] == 1:
        for pos_x in range(3):
            for pos_y in range(3):
                if active_boards[pos_x][pos_y] == 1:
                    active_boards[pos_x][pos_y] = 0
        active_boards[find_active(col)][find_active(row)] = 1
    else:
        for pos_x in range(3):
            for pos_y in range(3):
                if active_boards[pos_x][pos_y] == 0:
                    active_boards[pos_x][pos_y] = 1


def figure_pos(line):
    return int(line * TILE_SIZE + TILE_SIZE / 2)


def draw_circle(col, row, size, off_x, off_y):
    pygame.draw.circle(screen, CIRCLE_COLOUR,
                       (col * size + size / 2 + off_x, row * size + size / 2 + off_y), size * 1 / 3, LINE_WIDTH)


def draw_x(col, row, size, off_x, off_y):
    pygame.draw.line(screen, CROSS_COLOUR,
                     (col * size + SPACE + off_x, row * size + size - SPACE + off_y),
                     (col * size + size - SPACE + off_x, row * size + SPACE + off_y), int(LINE_WIDTH * 1.5))
    pygame.draw.line(screen, CROSS_COLOUR,
                     (col * size + SPACE + off_x, row * size + SPACE + off_y),
                     (col * size + size - SPACE + off_x, row * size + size - SPACE + off_y), int(LINE_WIDTH * 1.5))


def draw_figures():
    for row in range(13):
        for col in range(13):
            if board[row][col] == 1:
                draw_circle(col, row, TILE_SIZE, OFF_X, OFF_Y)
            if board[row][col] == 2:
                draw_x(col, row, TILE_SIZE, OFF_X, OFF_Y)


def mark_square(row, col, turn):
    board[row][col] = int(turn)


def available_square(row, col):
    if not row in borders and not col in borders:
        if col > 0 and col < 12 and row > 0 and row < 12:
            if active_boards[check_active_board(col)][check_active_board(row)] == 1:
                return board[row][col] == 0
    return False


def check_win(player):
    draw_vertical_winning_line(player)
    draw_horizontal_winning_line(player)
    draw_desc_diagonal_winning_line(player)
    draw_asc_diagonal_winning_line(player)
    check_draw(player)


markable_squares = [1, 2, 3, 5, 6, 7, 9, 10, 11]


def draw_vertical_winning_line(player):
    for pos_x in markable_squares:
        for pos_y in markable_squares:
            if board[pos_x][pos_y] != 0 and board[pos_x][pos_y] == board[pos_x + 1][pos_y] and board[pos_x][pos_y] == board[pos_x + 2][pos_y]:
                active_boards[check_active_board(pos_y)][check_active_board(pos_x)] = board[pos_x][pos_y] + 1

                posX = pos_y * TILE_SIZE + TILE_SIZE / 2
                posY = pos_x * TILE_SIZE

                if board[pos_x][pos_y] == 1:
                    colour = CIRCLE_COLOUR
                else:
                    colour = CROSS_COLOUR

                pygame.draw.line(screen, colour, (posX + OFF_X, posY + LINE_WIDTH + OFF_Y), (posX + OFF_X, posY + 3 * TILE_SIZE - LINE_WIDTH + OFF_Y), int(LINE_WIDTH * 1.5))


def draw_horizontal_winning_line(player):
    for pos_x in markable_squares:
        for pos_y in markable_squares:
            if board[pos_x][pos_y] != 0 and board[pos_x][pos_y] == board[pos_x][pos_y + 1] and board[pos_x][pos_y] == board[pos_x][pos_y + 2]:
                active_boards[check_active_board(pos_y)][check_active_board(pos_x)] = board[pos_x][pos_y] + 1

                posX = pos_y * TILE_SIZE
                posY = pos_x * TILE_SIZE + TILE_SIZE / 2

                if board[pos_x][pos_y] == 1:
                    colour = CIRCLE_COLOUR
                else:
                    colour = CROSS_COLOUR

                pygame.draw.line(screen, colour, (posX + LINE_WIDTH + OFF_X, posY + OFF_Y), (posX + 3 * TILE_SIZE - LINE_WIDTH + OFF_X, posY + OFF_Y),int(LINE_WIDTH * 1.5))


def draw_desc_diagonal_winning_line(player):
    for pos_x in markable_squares:
        for pos_y in markable_squares:
            if board[pos_x][pos_y] != 0 and board[pos_x][pos_y] == board[pos_x + 1][pos_y + 1] and board[pos_x][pos_y] == board[pos_x + 2][pos_y + 2]:
                active_boards[check_active_board(pos_y)][check_active_board(pos_x)] = board[pos_x][pos_y] + 1

                posX = pos_y * TILE_SIZE
                posY = pos_x * TILE_SIZE

                if board[pos_x][pos_y] == 1:
                    colour = CIRCLE_COLOUR
                else:
                    colour = CROSS_COLOUR

                pygame.draw.line(screen, colour, (posX + LINE_WIDTH + OFF_X, posY + LINE_WIDTH + OFF_Y), (posX + 3 * TILE_SIZE - LINE_WIDTH + OFF_X, posY + 3 * TILE_SIZE - LINE_WIDTH + OFF_Y), int(LINE_WIDTH * 2))


def draw_asc_diagonal_winning_line(player):
    for pos_x in markable_squares:
        for pos_y in markable_squares:
            if board[pos_x + 2][pos_y] != 0 and board[pos_x + 2][pos_y] == board[pos_x + 1][pos_y + 1] and board[pos_x + 2][pos_y] == board[pos_x][pos_y + 2]:
                active_boards[check_active_board(pos_y)][check_active_board(pos_x)] = board[pos_x + 2][pos_y] + 1

                posX = pos_y * TILE_SIZE
                posY = pos_x * TILE_SIZE

                if board[pos_x][pos_y] == 1:
                    colour = CIRCLE_COLOUR
                else:
                    colour = CROSS_COLOUR

                pygame.draw.line(screen, colour, (posX + 3 * TILE_SIZE - LINE_WIDTH + OFF_X, posY + LINE_WIDTH + OFF_Y), (posX + LINE_WIDTH + OFF_X, posY + 3 * TILE_SIZE - LINE_WIDTH + OFF_Y), int(LINE_WIDTH * 2))


def check_draw(player):
    for pos_x in [1, 5, 9]:
        for pos_y in [1, 5, 9]:
            if board[pos_x][pos_y] != 0 and board[pos_x][pos_y + 1] != 0 and board[pos_x][pos_y + 2] != 0 and board[pos_x + 1][pos_y] != 0 and board[pos_x + 1][pos_y + 1] != 0 and board[pos_x + 1][pos_y + 2] != 0 and board[pos_x + 2][pos_y] != 0 and board[pos_x + 2][pos_y + 1] != 0 and board[pos_x + 2][pos_y + 2] != 0:
                    active_boards[check_active_board(pos_y)][check_active_board(pos_x)] = 4



def check_big_win(player):
    if draw_big_vertical_winning_line(player) or draw_big_horizontal_winning_line(player) or draw_big_desc_diagonal_winning_line(player) or draw_big_asc_diagonal_winning_line(player):
        global active_boards
        active_boards = np.zeros((3, 3))
        return False
    return True


def draw_big_vertical_winning_line(player):
    for pos_x in range(3):
        if active_boards[pos_x][0] != 0 and active_boards[pos_x][0] != 1 and active_boards[pos_x][0] == active_boards[pos_x][1] and active_boards[pos_x][0] == active_boards[pos_x][2]:
            posX = pos_x * 4 * TILE_SIZE + 2.5 * TILE_SIZE + OFF_X
            posY = TILE_SIZE + OFF_Y

            if active_boards[pos_x][0] == 2:
                colour = CIRCLE_COLOUR
            else:
                colour = CROSS_COLOUR
            print(player, active_boards[pos_x][0])
            print(active_boards)

            pygame.draw.line(screen, colour, (posX, posY - TILE_SIZE / 2), (posX, posY + TILE_SIZE * 11.5), int(LINE_WIDTH * 3))
            return True
    return False


def draw_big_horizontal_winning_line(player):
    for pos_y in range(3):
        if active_boards[0][pos_y] != 0 and active_boards[0][pos_y] != 1 and active_boards[0][pos_y] == active_boards[1][pos_y] and active_boards[0][pos_y] == active_boards[2][pos_y]:
            posX = TILE_SIZE + OFF_X
            posY = pos_y * 4 * TILE_SIZE + 2.5 * TILE_SIZE + OFF_Y

            if player == 2:
                colour = CIRCLE_COLOUR
            else:
                colour = CROSS_COLOUR

            pygame.draw.line(screen, colour, (posX - TILE_SIZE / 2, posY), (posX + TILE_SIZE * 11.5, posY),int(LINE_WIDTH * 3))
            return True
    return False


def draw_big_desc_diagonal_winning_line(player):
    if active_boards[0][0] != 0 and active_boards[0][0] != 1 and active_boards[0][0] == active_boards[1][1] and active_boards[0][0] == active_boards[2][2]:
        posX = TILE_SIZE + OFF_X
        posY = TILE_SIZE + OFF_Y

        if player == 2:
            colour = CIRCLE_COLOUR
        else:
            colour = CROSS_COLOUR

        pygame.draw.line(screen, colour, (posX - TILE_SIZE / 2, posY - TILE_SIZE / 2), (posX + TILE_SIZE * 12 - TILE_SIZE / 2, posY + TILE_SIZE * 12 - TILE_SIZE / 2), int(LINE_WIDTH * 4.5))
        return True
    return False


def draw_big_asc_diagonal_winning_line(player):
    if active_boards[0][2] != 0 and active_boards[0][2] != 1 and active_boards[0][2] == active_boards[1][1] and active_boards[0][2] == active_boards[2][0]:
        posX = TILE_SIZE + OFF_X
        posY = TILE_SIZE + OFF_Y

        if player == 2:
            colour = CIRCLE_COLOUR
        else:
            colour = CROSS_COLOUR

        pygame.draw.line(screen, colour, (posX - TILE_SIZE / 2, posY + TILE_SIZE * 12 - TILE_SIZE / 2), (posX + TILE_SIZE * 12 - TILE_SIZE / 2, posY - TILE_SIZE / 2), int(LINE_WIDTH * 4.5))
        return True
    return False


def restart():
    global active_boards, player, board, active_boards
    active_boards = np.zeros((3, 3))
    player = 1
    board = np.zeros((14, 14))
    active_boards = np.ones((3, 3))


while True:

    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    SPACE = int(TILE_SIZE / 4)
    LINE_WIDTH = int(TILE_SIZE / 10)

    screen.fill(BG_COLOUR)

    past_player = 1

    if WIDTH > HEIGHT:
        OFF_X = (WIDTH - HEIGHT) / 2
        OFF_Y = 0
        TILE_SIZE = int(HEIGHT / 13)
    else:
        OFF_Y = (HEIGHT - WIDTH) / 2
        OFF_X = 0
        TILE_SIZE = int(WIDTH / 13)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        if play:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0] - OFF_X
                mouseY = event.pos[1] - OFF_Y

                clicked_row = int(mouseY // TILE_SIZE)
                clicked_col = int(mouseX // TILE_SIZE)

                if available_square(clicked_row, clicked_col):
                    if player == 1:
                        mark_square(clicked_row, clicked_col, 1)
                        check_win(player)
                        mark_active_board(clicked_col, clicked_row)

                        player = 2
                        past_player = 1

                    else:
                        mark_square(clicked_row, clicked_col, 2)
                        check_win(player)
                        mark_active_board(clicked_col, clicked_row)

                        player = 1
                        past_player = 2
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()

    current_time = pygame.time.get_ticks()

    if current_time > 400:
        small_l_stage, big_l_stage = draw_big_board(TILE_SIZE, OFF_X, OFF_Y, small_l_stage, big_l_stage, LINE_WIDTH)

    draw_figures()

    check_win(past_player)
    play = check_big_win(player)

    pygame.display.update()
    clock.tick(60)
