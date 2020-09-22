BOARD = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def print_board(board: list):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - - -')
        for j, column in enumerate(row):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(str(column))
            else:
                print(str(column) + " ", end="")


def find_empty(board: list) -> (int, int):
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == 0:
                return i, j
    return None


def isValid(board: list, number: int, pos: tuple):
    for i, column in enumerate(board[0]):
        if board[pos[0]][i] == number and pos[1] != i:
            return False
    for i, row in enumerate(board):
        if row[pos[1]] == number and pos[0] != i:
            return False
    eval_x = pos[1] // 3
    eval_y = pos[0] // 3
    for i in range(eval_y * 3, eval_y*3 + 3):
        for j in range(eval_x * 3, eval_x*3 + 3):
            if board[i][j] == number and (i, j) != pos:
                return False
    return True


def solveBoard(board: list):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if isValid(board, i, (row, col)):
            board[row][col] = i
            if solveBoard(board):
                return True
            board[row][col] = 0

    return False


solveBoard(BOARD)
print_board(BOARD)
