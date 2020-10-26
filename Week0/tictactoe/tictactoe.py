"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0

    for row in board:
        for tile in row:
            if tile == X:
                x += 1
            elif tile == O:
                o += 1
    
    if x > o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for row in range(3):
        for tile in range(3):
            if board[row][tile] is EMPTY:
                actions.add((row, tile))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_state = copy.deepcopy(board)

    new_state[action[0]][action[1]] = player(board)

    return new_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    checks = set(board[0])
    if (len(checks)) == 1:
        return board[0][0]

    checks = set(board[1])
    if (len(checks)) == 1:
        return board[1][0]

    checks = set(board[2])
    if (len(checks)) == 1:
        return board[2][0]

    checks = set([board[0][0], board[1][0], board[2][0]])
    if (len(checks)) == 1:
        return board[0][0]

    checks = set([board[0][1], board[1][1], board[2][1]])
    if (len(checks)) == 1:
        return board[0][1]

    checks = set([board[0][2], board[1][2], board[2][2]])
    if (len(checks)) == 1:
        return board[0][2]

    checks = set([board[0][0], board[1][1], board[2][2]])
    if (len(checks)) == 1:
        return board[0][0]

    checks = set([board[0][2], board[1][1], board[2][0]])
    if (len(checks)) == 1:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    for row in board:
        for tile in row:
            if tile is EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def max_state(board):
    if terminal(board):
        return utility(board), None

    max_score = -10
    act = None

    for action in actions(board):
        score, temp_act = min_state(result(board, action))
        if score > max_score:
            max_score = score
            act = action
            if max_score == 1:
                return max_score, act
    
    return max_score, act

def min_state(board):
    if terminal(board):
        return utility(board), None

    min_score = 10
    act = None

    for action in actions(board):
        score, temp_act = max_state(result(board, action))
        if score < min_score:
            min_score = score
            act = action
            if min_score == -1:
                return min_score, act
    
    return min_score, act


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        _, act = max_state(board)
        return act
    
    _, act = min_state(board)
    return act
