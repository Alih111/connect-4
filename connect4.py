import numpy as np
import random
import pygame
import sys
import math
import copy

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
    return board


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
    connects = []
    # Check horizontal locations for win
    for r in range(ROW_COUNT):      
        for c in range(COLUMN_COUNT - 6):
            length = 0         
            while(c + length < 7 and board[r][c + length] == piece):
                length += 1
            c += length
            if length > 3:
                    connects.append(length)
    print(connects)

    # Check vertical locations for win
    for r in range(ROW_COUNT - 5):      
        for c in range(COLUMN_COUNT):
            length = 0         
            while(r + length < 6 and board[r + length][c] == piece):
                length += 1
            r += length
            if length > 3:
                    connects.append(length)
    print(connects)

    # Check positively sloped diaganols
    pos_indcies = []
    for r in range(ROW_COUNT - 3):      
        for c in range(COLUMN_COUNT - 3):
            if r-c in pos_indcies:
                continue
            else:
                for length in range(6, 3, -1):
                    
                    if all(r-c not in pos_indcies and r + i < 6 and c + i < 7 and board[r + i][c + i] == piece for i in range(length)):
                        print(f'length = {length},r = {r} and c = {c}')
                        print(f'before = {score}')
                        score += length - 3
                        length = 3
                        pos_indcies.append(r-c)
    #check negatively sloped diagonals
    neg_indices = []
    print('negative slope:')
    for r in range(ROW_COUNT - 1,2,-1):      
        for c in range(COLUMN_COUNT - 3):
            if r+c in neg_indices:
                continue
            else:

                if c == 3:
                    print('hi')
                for length in range(6, 3, -1): 
                    if all(r+c not in neg_indices and r - i < 6 and c + i < 7 and board[r - i][c + i] == piece for i in range(length)):
                        print(f'length = {length},r = {r} and c = {c}')
                        score += length - 3
                        length = 3
                        neg_indices.append(r+c)
            
    print(connects)
                    
    for i in range(0,len(connects)): 
        score += connects[i] - 3
    return score


def generateChildren(board,piece):
    children = []
    for col in range(COLUMN_COUNT):
        tempBoard = copy.deepcopy(board)
        if is_valid_location(tempBoard,col):
            row = get_next_open_row(tempBoard,col)
            children.append(drop_piece(tempBoard,row,col,piece))
    return children

def maximize(board):
    print('In maximize')
    print_board(board)
    if isFull(board):
        PLAYER_Score = CalculateUtilityPiece(board,PLAYER_PIECE)
        AIScore = CalculateUtilityPiece(board,AI_PIECE)
        score = PLAYER_Score - AIScore   
        print(f'player score = {PLAYER_Score}')
        print(f'AI score = {AIScore}')
        print(f'Total score = {score}')
        return None,score
    else:
        maxChild = None
        maxUtility = -float('inf')
        children = generateChildren(board,PLAYER_PIECE)
        for child in children:
            print_board(child)
            redudant_child,utility = minimize(child)
            if utility > maxUtility:
                maxChild = child
                maxUtility = utility
        return maxChild,maxUtility


def minimize(board):
    #check if terminal node
    print('In minimize')
    print_board(board)
    if isFull(board):
        PLAYER_Score = CalculateUtilityPiece(board,PLAYER_PIECE)
        AIScore = CalculateUtilityPiece(board,AI_PIECE)
        score = PLAYER_Score - AIScore   
        print(f'player score = {PLAYER_Score}')
        print(f'AI score = {AIScore}')
        print(f'Total score = {score}')
        return None,score
    else:
        minChild = None
        minUtility = float('inf')
        children = generateChildren(board,AI_PIECE)
        for child in children:
            redudant_child,utility = maximize(child)
            if utility < minUtility:
                minChild = child
                minUtility = utility
        return minChild,minUtility


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
game_over = True
board = [[1,1,1,1,1,1,1],
         [1,1,1,2,1,1,2],
         [1,2,1,1,1,1,2],
         [2,1,1,1,1,1,1],
         [2,1,1,2,1,1,2],
         [1,1,1,1,1,1,1]]

print_board(board)
x = CalculateUtilityPiece(board,AI_PIECE)
print(f'AI score = {x}')
print('-------------------------------->')
print(f'Player score = {CalculateUtilityPiece(board,PLAYER_PIECE)}')
#child,score = minimize(board)
# if child != None:
#     print('best child:')
#     print_board(child)
# print(score)
#print(isFull(board))
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