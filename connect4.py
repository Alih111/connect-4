import numpy as np
import random
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))




def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True




def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def isFull(board): 
    if 0 not in board[ROW_COUNT-1]:
        return True
    return False

def CalculateUtilityPiece(board,piece):
    score = 0
    row_indices = []
    col_indices = []
    pos_diagonal_indices = []
    neg_diagonal_indices = []

    for connectNum in range(7,3,-1):
         # Check horizontal locations for win
        
        print(f'connnectNum = {connectNum}')
        
        for c in range(COLUMN_COUNT - connectNum + 1):
            for r in range(ROW_COUNT):
                if r in row_indices:
                    continue
                temp = 0
                connect = True
                while(temp < connectNum):
                    if board[r][c + temp] == piece:
                        connect = connect and True
                    else:
                        connect = False
                        break
                    temp += 1

                #print(connect)
                if connect:
                    score += connectNum - 3
                    row_indices.append(r)
                #print(f'score = {score}')
            # Check vertical locations for win
        if connectNum < 7:
            for c in range(COLUMN_COUNT):
                if  connectNum == 7:
                    break
                if c in col_indices:
                        continue
                for r in range(ROW_COUNT  - connectNum + 1):
                    temp = 0
                    connect = True
                    while(temp < connectNum):
                        if board[r + temp][c] == piece:
                            connect = connect and True
                        else:
                            connect = False
                            break
                        temp += 1

                    #print(connect)
                    if connect:
                        score += connectNum - 3
                        col_indices.append(c)

            # Check positively sloped diaganols
            for c in range(COLUMN_COUNT - connectNum + 1):
                for r in range(ROW_COUNT - connectNum + 1):
                    if r + c in pos_diagonal_indices:
                        continue
                    else:
                        temp = 0
                        connect = True
                        while(temp < connectNum):
                            if board[r + temp][c + temp] == piece:
                                connect = connect and True
                            else:
                                connect = False
                                break
                            temp += 1

                        if connect:
                            score += connectNum - 3
                            pos_diagonal_indices.append(r+c)
                        # if connectNum == 6:
                        #     score -= 7 # 2*2 + 1*3
                        # elif connectNum == 5:
                        #     score -= 2 # 2*1
            print(pos_diagonal_indices)
            # Check negatively sloped diaganols
            for c in range(COLUMN_COUNT - connectNum + 1):
                for r in range(ROW_COUNT - connectNum, ROW_COUNT):    
                    if r + c in neg_diagonal_indices:
                        continue           
                    else:
                        temp = 0
                        connect = True
                        while(temp < connectNum):
                            if board[r - temp][c + temp] == piece:
                                connect = connect and True
                            else:
                                connect = False
                                break
                            temp += 1

                        if connect:
                            score += connectNum - 3
                            neg_diagonal_indices.append(r+c)
                            # if connectNum == 6:
                            #     score -= 7
                            # elif connectNum == 5:
                            #     score -= 2
                            
                            

            # for c in range(COLUMN_COUNT - 3):
            #     for r in range(3, ROW_COUNT):
            #         if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
            #             c + 3] == piece:
            #             return score

    return score

def minimax(board):
    #check if terminal node
    board = [[1,1,1,1,1,1,1],
             [1,2,2,2,1,1,2],
             [1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1],
             [1,1,1,2,2,2,2],
             [1,1,1,1,1,1,1]]
    
    if isFull(board):
        #print_board(board)
        print(board)
        PLAYER_Score = CalculateUtilityPiece(board,PLAYER_PIECE)
        AIScore = CalculateUtilityPiece(board,AI_PIECE)
        score = PLAYER_Score - AIScore   
        print(f'player score = {PLAYER_Score}')
        print(f'AI score = {AIScore}')
        print(f'Total score = {score}')


board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)
#minimax(board)
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS) 
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True     

            # # Ask for Player 2 Input
            if turn == AI and not game_over:

                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col): 
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        label = myfont.render("AI wins!!", 2, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            turn += 1
            turn = turn % 2

            
            if isFull(board) == True:
                label = myfont.render("Tie!!", 2, BLUE)
                screen.blit(label, (40, 10))
                game_over = True
            
            print_board(board)
            draw_board(board)
    if game_over:
        pygame.time.wait(3000)