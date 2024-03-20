import time

import numpy as np
import random
import pygame
import sys
import math
import copy
import networkx as nx
import matplotlib.pyplot as plt
import graphviz

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
DEPTH = 6
PLAYER = 0
AI = 1
tree=[[]for i in range(DEPTH+1)]
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


def stringTo2d(string):
    array_2d = [[] for i in range(ROW_COUNT)]
    j = 0
    for i in range(COLUMN_COUNT * ROW_COUNT):
        if (i % 7 == 0 and i != 0):
            j += 1
        array_2d[j].append(int(string[i]))

    return array_2d


zeros_string = "0" * 42


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
    if 0 not in board[ROW_COUNT - 1]:
        return True
    return False


def CalculateUtilityPiece(board, piece):
    score = 0
    # Check horizontal locations for win
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 6):
            length = 0
            while (c + length < 7 and board[r][c + length] == piece):
                length += 1
            c += length
            if length > 3:
                score += length - 3

    # Check vertical locations for win
    for r in range(ROW_COUNT - 5):
        for c in range(COLUMN_COUNT):
            length = 0
            while (r + length < 6 and board[r + length][c] == piece):
                length += 1
            r += length
            if length > 3:
                score += length - 3

    # Check positively sloped diaganols
    pos_indcies = []
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if r - c in pos_indcies:
                continue
            else:
                for length in range(6, 3, -1):

                    if all(r - c not in pos_indcies and r + i < 6 and c + i < 7 and board[r + i][c + i] == piece for i
                           in range(length)):
                        print(f'length = {length},r = {r} and c = {c}')
                        print(f'before = {score}')
                        score += length - 3
                        length = 3
                        pos_indcies.append(r - c)
    # check negatively sloped diagonals
    neg_indices = []
    print('negative slope:')
    for r in range(ROW_COUNT - 1, 2, -1):
        for c in range(COLUMN_COUNT - 3):
            if r + c in neg_indices:
                continue
            else:

                if c == 3:
                    print('hi')
                for length in range(6, 3, -1):
                    if all(r + c not in neg_indices and r - i < 6 and c + i < 7 and board[r - i][c + i] == piece for i
                           in range(length)):
                        print(f'length = {length},r = {r} and c = {c}')
                        score += length - 3
                        length = 3
                        neg_indices.append(r + c)
    return score
def detectVertical(board,piece):
    counts = []
    score = 0
    for i in range(COLUMN_COUNT):
        c=0
        for j in range(ROW_COUNT):
            a=board[j][i]
            if a==piece:
                c+=1
            elif a==0:
                break
            else:
                if c > 3:
                    break
                else:
                    c=0
                    if ROW_COUNT-j<4:
                        break
        counts.append(c)
    for c in counts:
        if c == 2:
            score += 1 * 2
        elif c == 3:
            score += 1 * 4
        elif c == 4:
            score += 1 * 8
        elif c == 5:
            score += 1 * 16
        elif c == 6:
            score += 1 * 24
    return score
def detectHorizontal(board,piece):
    counts=[]
    score=0
    for i in range(ROW_COUNT):
        c=0
        zerosbet=0
        for j in range (COLUMN_COUNT):
            if board[i][j]==0:
                zerosbet+=1
                continue
            elif board[i][j]==piece:
                if(j%3==0):
                    score+=1
                c+=1
            else:
                if c<4:
                    c=0
                counts.append(c)
                if COLUMN_COUNT-j<4:
                    break
                c=0
        counts.append(c)
    i=0
    for c in counts:
        if c==2:
            score+=1*2

        elif c==3:
            score+=1*4

        elif c==4:
            score+=1*10
        elif c==5:
            score+=1*20
        elif c==6:
            score+=1*30
        elif c==7:
            score+=1*40
        i+=1
    return score
def evaluation(board):
    a=detectHorizontal(board,AI_PIECE)+detectVertical(board,AI_PIECE)
    b = detectHorizontal(board, PLAYER_PIECE)+detectVertical(board, PLAYER_PIECE)
    return a-b



def generateChildren(board, piece):
    children = []
    for col in range(COLUMN_COUNT):
        tempBoard = copy.deepcopy(board)
        if is_valid_location(tempBoard, col):
            row = get_next_open_row(tempBoard, col)
            children.append(drop_piece(tempBoard, row, col, piece))
    return children
def generateChildrenWithCol(board, piece):
    children = []
    cols=[]
    for col in range(COLUMN_COUNT):
        tempBoard = copy.deepcopy(board)
        if is_valid_location(tempBoard, col):
            row = get_next_open_row(tempBoard, col)
            children.append(drop_piece(tempBoard, row, col, piece))
            cols.append(col)
    return children,cols

def expectiMinMax(alpha, beta, depth, board, player):
    if isFull(board):
        PLAYER_Score = CalculateUtilityPiece(board, PLAYER_PIECE)
        AIScore = CalculateUtilityPiece(board, AI_PIECE)
        score = AIScore - PLAYER_Score
        return score, board  # Return score and board

    if depth == 0:
        return evaluation(board), board
    if player == 1:  # maximizing player

        maxUtility = -float('inf')
        maxChild = None  # Keep track of the best child board
        children,columns = generateChildrenWithCol(board, AI_PIECE)
        i = 0
        maxCol=0
        for child in children:
            utility, _ = minMaxAlphaBeta(alpha, beta, depth - 1, child, PLAYER)
            tree[DEPTH - depth + 1].append((utility, len(tree[DEPTH - depth]) - 1))
            if utility > maxUtility:
                maxUtility = utility
                maxChild = child  # Update the best child board
                maxCol=columns[i]
            if alpha < maxUtility:
                alpha = maxUtility
            if alpha >= beta:
                break
            i+=1
        rightColumnProb=0.2# choose according to probablites not optimal choice like normal minmax
        predictedProb=0.6
        leftColumnProb=0.2
        if maxCol==0:
            leftColumnProb = 0
            rightColumnProb=0.4
        elif maxCol==COLUMN_COUNT-1:
            rightColumnProb=0
            leftColumnProb=0.4
        while (1):
            choices = ['A', 'B', 'C']
            probabilities = [leftColumnProb, predictedProb, rightColumnProb]  # Probabilities must sum up to 1
            chosen = random.choices(choices, weights=probabilities, k=1)[0]
            if (chosen == 'A'):
                if (is_valid_location(board, 0)):
                    r = get_next_open_row(board, 0)
                    maxChild=drop_piece(board, r, 0, AI_PIECE)
                    break
            elif (chosen == 'C'):
                if (is_valid_location(board, COLUMN_COUNT - 1)):
                    r = get_next_open_row(board, COLUMN_COUNT - 1)
                    maxChild=drop_piece(board, r, COLUMN_COUNT - 1, AI_PIECE)
                    break
            else:
                break
        return maxUtility, maxChild  # Return the best utility and its corresponding board

    else:
            minUtility = float('inf')
            minChild = None  # Keep track of the best child board
            children,columns = generateChildren(board, PLAYER_PIECE)
            minCol=0
            i=0
            for child in children:
                utility, _ = minMaxAlphaBeta(alpha, beta, depth - 1, child, AI)
                tree[DEPTH - depth + 1].append((utility, len(tree[DEPTH - depth]) - 1))
                if utility < minUtility:
                    minUtility = utility
                    minCol= columns[i]
                    minChild = child  # Update the best child board
                if minUtility < beta:
                    beta = minUtility
                if alpha >= beta:
                    break
                i+=1
            rightColumnProb = 0.2# choose according to probablites not optimal choice like normal minmax
            predictedProb = 0.6
            leftColumnProb = 0.2
            if minCol == 0:
                leftColumnProb = 0
                rightColumnProb = 0.4
            elif minCol == COLUMN_COUNT - 1:
                rightColumnProb = 0
                leftColumnProb = 0.4
            while (1):
                choices = ['A', 'B', 'C']
                probabilities = [leftColumnProb, predictedProb, rightColumnProb]  # Probabilities must sum up to 1
                chosen = random.choices(choices, weights=probabilities, k=1)[0]
                if (chosen == 'A'):
                    if (is_valid_location(board, 0)):
                        r = get_next_open_row(board, 0)
                        minChild = drop_piece(board, r, 0, PLAYER_PIECE)
                        break
                elif (chosen == 'C'):
                    if (is_valid_location(board, COLUMN_COUNT - 1)):
                        r = get_next_open_row(board, COLUMN_COUNT - 1)
                        minChild = drop_piece(board, r, COLUMN_COUNT - 1, PLAYER_PIECE)
                        break
                else:

                    break

            return minUtility, minChild


def minMax(alpha, beta, depth, board, player):

    if isFull(board):
        PLAYER_Score = CalculateUtilityPiece(board, PLAYER_PIECE)
        AIScore = CalculateUtilityPiece(board, AI_PIECE)
        score = AIScore - PLAYER_Score
        return score, board  # Return score and board

    if depth == 0:
        return evaluation(board), board

    if player == 1:  # maximizing player
        maxUtility = -float('inf')
        maxChild = None  # Keep track of the best child board
        children = generateChildren(board, AI_PIECE)
        for child in children:
            utility, _ = minMaxAlphaBeta(alpha, beta, depth - 1, child, PLAYER)
            tree[DEPTH - depth + 1].append((utility, _))
            if utility > maxUtility:
                maxUtility = utility
                maxChild = child  # Update the best child board
            if alpha < maxUtility:
                alpha = maxUtility
        return maxUtility, maxChild  # Return the best utility and its corresponding board

    else:
        minUtility = float('inf')
        minChild = None  # Keep track of the best child board
        children = generateChildren(board, PLAYER_PIECE)
        for child in children:
            utility, _ = minMaxAlphaBeta(alpha, beta, depth - 1, child, AI)
            tree[DEPTH - depth + 1].append((utility, _))
            if utility < minUtility:
                minUtility = utility
                minChild = child  # Update the best child board
            if minUtility < beta:
                beta = minUtility
        return minUtility, minChild


def minMaxAlphaBeta(alpha, beta, depth, board, player):

    if isFull(board):
        PLAYER_Score = CalculateUtilityPiece(board, PLAYER_PIECE)
        AIScore = CalculateUtilityPiece(board, AI_PIECE)
        score = AIScore - PLAYER_Score
        return score, board  # Return score and board

    if depth == 0:
        return evaluation(board), board
    if player == 1:  # maximizing player

        maxUtility = -float('inf')
        maxChild = None  # Keep track of the best child board
        children = generateChildren(board, AI_PIECE)
        i=0
        for child in children:
            utility, _ = minMaxAlphaBeta(alpha, beta, depth - 1, child, PLAYER)
            tree[DEPTH - depth + 1].append((utility,len(tree[DEPTH - depth] )-1 ))
            if utility > maxUtility:
                maxUtility = utility
                maxChild = child  # Update the best child board
            if alpha < maxUtility:
                alpha = maxUtility
            if alpha >= beta:
                break
        return maxUtility, maxChild  # Return the best utility and its corresponding board

    else:
        minUtility = float('inf')
        minChild = None  # Keep track of the best child board
        children = generateChildren(board, PLAYER_PIECE)
        for child in children:
            utility, _ = minMaxAlphaBeta(alpha, beta, depth - 1, child, AI)
            tree[DEPTH - depth + 1].append((utility, len(tree[DEPTH - depth]) - 1))
            if utility < minUtility:
                minUtility = utility
                minChild = child  # Update the best child board
            if minUtility < beta:
                beta = minUtility
            if alpha >= beta:
                break

        return minUtility, minChild

def drawTREE():
    G = nx.DiGraph()
    pos = {}
    j = 0
    wid = 0
    for i in range(DEPTH * 7 + 1):
        wid += 1
        pos[i] = (10 * j, 15 * wid)
        if (i % 7 == 0):
            j += 2
            wid = 0

    color1 = 'red'
    j=0
    i=0
    m=0
    len1=0
    for i in range(len(tree)):
        for j in  range(len(tree[i])):
            a=tree[i][j]
            G.add_node(m,color=color1,label=f"{j}/ {i}/ {a[0]}")
            if(a[1] is not None):
                G.add_edge(len1+a[1],m)
        if color1=='red':
            color1='blue'
        else:
            color1='red'
            m+=1
        len1 += len(tree[i]) - 1


pygame.init()

width = COLUMN_COUNT * 100
height = (ROW_COUNT + 1) * 100

size = (width, height)

RADIUS = int(100 / 2 - 5)
pygame.display.set_caption("welcome")

# Load the background image

screen = pygame.display.set_mode(size)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

button_font = pygame.font.SysFont("Arial", 30)
func = None
while True:
    screen.fill((0, 0, 0))
    flag = False
    # Draw menu buttons
    start_button = pygame.Rect(250, 200, 200, 50)
    options_button = pygame.Rect(250, 280, 200, 50)
    exit_button = pygame.Rect(250, 360, 200, 50)

    pygame.draw.rect(screen, (255, 0, 0), start_button)
    pygame.draw.rect(screen, (0, 255, 0), options_button)
    pygame.draw.rect(screen, (0, 0, 255), exit_button)

    start_text = button_font.render("alpha beta", True, (0, 0, 0))
    options_text = button_font.render("no alpha beta", True, (0, 0, 0))
    exit_text = button_font.render("expectiminimax", True, (0, 0, 0))

    screen.blit(start_text, (270, 210))
    screen.blit(options_text, (260, 290))
    screen.blit(exit_text, (250, 370))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if start_button.collidepoint(mouse_pos):
                flag = True
                func = minMaxAlphaBeta
                break
            elif options_button.collidepoint(mouse_pos):
                flag = True
                func = minMax
                break
            elif exit_button.collidepoint(mouse_pos):
                flag = True
                func = expectiMinMax
                break
    if flag:
        break
    pygame.display.update()

board = create_board()
game_over = False

pygame.init()
pygame.display.set_caption("connect 4")
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
turn = random.randint(PLAYER, AI)
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER and not game_over:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    draw_board(board)
                    turn = AI
            # # Ask for Player 2 Input
        if turn == AI and not game_over:
            time.sleep(1)

            sc, a = func(float('-inf'), float('inf'), DEPTH, board, AI)
            tree[0].append((sc,None))
            #draw tree
            drawTREE()
            print(f"ai score ={CalculateUtilityPiece(board,AI_PIECE)} human score = {CalculateUtilityPiece(board,PLAYER_PIECE)}")
            tree = [[] for i in range(DEPTH + 1)]
            board = a
            draw_board(board)
            turn = PLAYER

        if isFull(board) == True:
            label = myfont.render("Tie!!", 2, BLUE)
            screen.blit(label, (40, 10))
            game_over = True
    if game_over:
        pygame.time.wait(3000)